import os
import copy
import numpy as np
from galvatron.utils import (
    read_allreduce_bandwidth_config, 
    read_json_config, 
    read_p2p_bandwidth_config, 
    form_strategy, 
    print_strategies,
    strategy2config,
    array2str,
    write_json_config
)
from galvatron.core import MemoryCostModel, TimeCostModel, DpOnModel

class GalvatronSearchEngine():
    def __init__(self, args):
        self.args = args
        args.gpu_num = args.num_nodes * args.num_gpus_per_node
        self.layernum_arg_names = None
        self.mem_path = None
        self.time_path = None
        self.model_name = None
        self.time_config = None
        self.memory_config = None
        self.param_sizes = None
        self.act_sizes = None
        self.other_memory_pp_off = None
        self.other_memory_pp_on = None
        self.time_profiled_list = None
        self.use_pipeline_costmodel = args.use_pipeline_costmodel
        self.model_type = 'gpt'
        self.optimal_chunk_func = optimal_chunk_func_default
        self.memory_constraint = args.memory_constraint * 1024
        
    # =============== Setting Galvatron Search Engine Basic Information ===============
    def set_search_engine_info(self, path, model_layer_configs, model_name):
        self.set_model_layer_configs(model_layer_configs)
        self.set_path(path)
        self.set_model_name(model_name)
        self.memory_profiling_path()
        self.time_profiling_path()
    
    def set_path(self, path):
        self.path = path

    def set_model_type(self, model_type):
        self.model_type = model_type

    def set_model_name(self, name):
        self.model_name = name
        
    def memory_profiling_path(self):
        if self.mem_path is not None:
            return self.mem_path
        assert self.model_name is not None, 'Should specify the model name!'
        args = self.args
        memory_config_path = 'configs/memory_profiling_%s_%s.json'%(args.mixed_precision, self.model_name)
        self.mem_path = os.path.join(self.path, memory_config_path)
        return self.mem_path
    
    def time_profiling_path(self):
        if self.time_path is not None:
            return self.time_path
        assert self.model_name is not None, 'Should specify the model name!'
        args = self.args
        time_config_path = "configs/computation_profiling_%s_%s.json"%(args.mixed_precision, self.model_name)
        self.time_path = os.path.join(self.path, time_config_path)
        return self.time_path
    
    def set_microbatch_func(self, microbatch_size, max_chunk):
        self.optimal_chunk_func = lambda local_bsz, strategy: optimal_chunk_func_default(local_bsz, strategy, microbatch_size, max_chunk)
    
    def set_model_layer_configs(self, model_layer_configs):
        if model_layer_configs is None:
            return
        self.hiddensize_list = [config['hidden_size'] for config in model_layer_configs]
        self.layernum_list = [config['layer_num'] for config in model_layer_configs]
        self.seqlen_list = [config['seq_len'] for config in model_layer_configs]
        self.num_layertype = len(self.layernum_list)
    
    # =============== Initializing Galvatron Search Engine ===============
    # Generating Strategies, Loading Profiled Memory & Time Config, Setting Memory & Time Cost Models
    def initialize_search_engine(self):
        self.generate_strategies()
        self.get_profiled_model_configs()
        self.get_profiled_hardware_configs()
        self.set_cost_models()
        self.show_search_info()
        
    def get_profiled_model_configs(self):
        self.time_config = read_json_config(self.time_profiling_path())
        self.memory_config = read_json_config(self.memory_profiling_path())
        self.time_profiled_list = [self.time_config['layertype_%d'%i] for i in range(self.num_layertype)]
        self.param_sizes = [0] * self.num_layertype
        self.act_sizes = [{} for _ in range(self.num_layertype)]
        for i in range(self.num_layertype):
            layer_mem_config = self.memory_config['layertype_%d'%i]
            parameter_size = layer_mem_config['parameter_size']
            tp_activation_per_bsz_dict = layer_mem_config['tp_activation_per_bsz_dict'].copy()
            for key, val in layer_mem_config['tp_activation_per_bsz_dict'].items():
                if len(key) < 5:
                    tp_activation_per_bsz_dict[int(key)] = val
                    del tp_activation_per_bsz_dict[key]
            self.param_sizes[i] = parameter_size
            self.act_sizes[i] = tp_activation_per_bsz_dict
        self.other_memory_pp_off = self.memory_config['other_memory_pp_off']
        self.other_memory_pp_on = {'first_stage':self.memory_config['other_memory_pp_on_first'], 'last_stage':self.memory_config['other_memory_pp_on_last']}
        return self.time_config, self.memory_config
        
    def get_profiled_hardware_configs(self):
        args = self.args
        hardware_configs_dir = '../../profile_hardware/hardware_configs/'
        gpu_num_config = '_%dnodes_%dgpus_per_node.json'%(args.num_nodes, args.num_gpus_per_node)
        allreduce_bandwidth_config_path = hardware_configs_dir + 'allreduce_bandwidth' + gpu_num_config
        self.allreduce_bandwidth, self.allreduce_comm_coe = read_allreduce_bandwidth_config(os.path.join(self.path, allreduce_bandwidth_config_path), gpu_num=args.gpu_num)
        p2p_bandwidth_config_path = hardware_configs_dir + 'p2p_bandwidth' + gpu_num_config
        self.p2p_bandwidth, self.p2p_comm_coe = read_p2p_bandwidth_config(os.path.join(self.path, p2p_bandwidth_config_path))
        overlap_coe_path = hardware_configs_dir + 'overlap_coefficient.json'
        self.overlap_coe = read_json_config(overlap_coe_path)['overlap_coe']

    def set_cost_models(self):
        self.set_time_cost_models()
        self.set_memory_cost_models()
    
    def set_time_cost_models(self):
        self.timecost_model_args_list = []
        for i in range(self.num_layertype):
            self.timecost_model_args_list.append({ 
                    'parameter_size': self.param_sizes[i],
                    'microbatch': False if self.use_pipeline_costmodel else True,
                    'optimal_chunk_func': self.optimal_chunk_func,
                    'sequence_length': self.seqlen_list[i],
                    'hidden_size': self.hiddensize_list[i],
                    'forward_computation_time': self.time_profiled_list[i],
                    'bct_fct_coe': 2,
                    'extra_overhead': 0,
                    'comm_coe_dict': self.allreduce_comm_coe,
                    'dp_overlap_coe': self.overlap_coe,
                    'bct_overlap_coe': self.overlap_coe,
                    'p2p_comm_coe_dict': self.p2p_comm_coe,
                    'layer_num': self.layernum_list[i],
                    'use_zero2_for_dp': 1 if self.args.default_dp_type == 'zero2' else 0,
                    'mixed_precision': False if self.args.mixed_precision == 'fp32' else True,
                    'costmodel_coe': self.args.costmodel_coe,
                    })
    
    def set_memory_cost_models(self):
        self.memcost_model_args_list = []
        for i in range(self.num_layertype):
            self.memcost_model_args_list.append({  
                    'parameter_size': self.param_sizes[i],
                    'tp_activation_per_bsz_dict': self.act_sizes[i],
                    'other_memory_pp_off': self.other_memory_pp_off,
                    'other_memory_pp_on': self.other_memory_pp_on,
                    'microbatch': True,
                    'optimal_chunk_func': self.optimal_chunk_func,
                    'model_type': self.model_type,
                    'checkpoint': 0 if self.args.disable_ckpt else 1,
                    'use_zero2_for_dp':1 if self.args.default_dp_type == 'zero2' else 0,
                    'use_zero3_for_embed':self.args.embed_sdp,
                    'mixed_precision': False if self.args.mixed_precision == 'fp32' else True,
                    'pipeline_type': self.args.pipeline_type
                    })
    
    # =============== For Galvatron Search Engine Parallelism Optimization ===============
    def parallelism_optimization(self):
        print('='*25, 'Galvatron Search Engine Start Searching','='*25)
        self.set_searching_bsz()
        
        print('-----', '[Searching Memory Info]', 'Memory constraint:', self.memory_constraint, 'MB', '-----')
        results = dict()
        self.search_history = dict()
        pp_stage_dict_for_bsz = get_pp_stages_for_all_bsz(self.strategies, self.memcost_model_args_list, self.layernum_list, self.BSZs)
        
        max_throughput, optimal_bsz, max_bsz = -1, -1, -1
        for bsz in self.BSZs:
            pp_stage_dict = pp_stage_dict_for_bsz[bsz]
            results[bsz] = self.dynamic_programming(bsz, pp_stage_dict)
            min_res_list, min_pp_deg, throughput = results[bsz]['min_res_list'], results[bsz]['min_pp_deg'], results[bsz]['throughput']
            if throughput > max_throughput:
                max_throughput = throughput
                optimal_bsz = bsz
            if min_pp_deg == -1 and min_res_list is None:
                break
            max_bsz = bsz

        print('\nFinal results of max memory %d MB:'%self.memory_constraint)
        re = results[optimal_bsz]
        print(f"Optimal bsz = {optimal_bsz} Max throughput={re['throughput']} samples/s")
        print(f"pp_deg={re['min_pp_deg']} Minimized timecost={re['min_cost']} Memory remaining={re['mem_remain']} Memory cost={re['mem_cost']}")
        print_strategies(re['min_res_list'])
        
        self.save_results(re, optimal_bsz, pp_stage_dict_for_bsz[optimal_bsz])
        
        if max_bsz > -1 and max_bsz != optimal_bsz:
            re = results[max_bsz]
            print(f"\nMax bsz = {max_bsz} Max throughput={re['throughput']} samples/s")
            print(f"pp_deg={re['min_pp_deg']} Minimized timecost={re['min_cost']} Memory remaining={re['mem_remain']} Memory cost={re['mem_cost']}")
            print_strategies(re['min_res_list'])
        print("-----------------------------------------")
        print('='*25, 'Galvatron Search Engine End Searching','='*25)

    def set_searching_bsz(self):
        args = self.args
        # Set Searching BSZs
        if args.settle_bsz is not None and args.settle_bsz > 0:
            args.settle_bsz = int(np.ceil(args.settle_bsz / min(args.gpu_num, 8)) * min(args.gpu_num, 8))
            if args.search_space in ['dp', 'tp', 'sdp', 'dp+tp'] and args.settle_bsz < args.gpu_num:
                args.settle_bsz = int(np.ceil(args.settle_bsz // args.gpu_num) * args.gpu_num)
            self.min_bsz = self.max_bsz = args.settle_bsz
            self.bsz_scale = 0
            self.BSZs = [args.settle_bsz]
            print('-----', '[Searching Batch Sizes Info]', 'Settle bsz:', args.settle_bsz, '-----')
            return
        self.bsz_scale = args.bsz_scale if args.bsz_scale >= min(args.gpu_num, 8) else min(args.gpu_num, 8)
        if args.search_space in ['dp', 'tp', 'sdp', 'dp+tp'] and self.bsz_scale < args.gpu_num:
            self.bsz_scale = args.gpu_num
        
        if args.recommend_min_bsz:
            recommend_bsz = self.recommend_min_bsz(self.bsz_scale)
            args.min_bsz = recommend_bsz if recommend_bsz > 0 else self.min_bsz
        
        self.min_bsz = max(args.min_bsz, self.bsz_scale)
        self.min_bsz = self.min_bsz // self.bsz_scale * self.bsz_scale
        self.max_bsz = int(np.ceil(args.max_bsz / self.bsz_scale) * self.bsz_scale) if args.max_bsz % self.bsz_scale else (args.max_bsz+self.bsz_scale)
        self.BSZs = list(range(self.min_bsz, self.max_bsz, self.bsz_scale))
        self.max_bsz = self.BSZs[-1]
        print('-----', '[Searching Batch Sizes Info]', 'Min bsz:', self.min_bsz, 'Max bsz:', self.max_bsz, 'bsz_scale:', self.bsz_scale, '-----')

    def recommend_min_bsz(self, scale):
        prune_percent = 0.65
        args = self.args
        gpu_num = args.gpu_num
        if not args.search_space in ['full', 'dp+pp', 'dp+tp']:
            return -1
        baselines = []
        if not args.disable_dp:
            baselines.append([1,1,gpu_num,{'fsdp':0}])
        if not args.disable_sdp:
            baselines.append([1,1,gpu_num,{'fsdp':1}])
        if not args.disable_tp:
            baselines.append([1,gpu_num,1,{'fsdp':0}])
        max_bsz_baselines = [self.estimate_strategy_max_bsz([s], scale) for s in baselines]
        # print(max_bsz_baselines)
        max_bsz, min_bsz = np.max(max_bsz_baselines), np.min(max_bsz_baselines)
        bsz_start = int((min_bsz*(1-prune_percent)+max_bsz*prune_percent)//scale*scale)
        bsz_start = bsz_start if bsz_start > scale else scale
        return bsz_start

    def estimate_strategy_max_bsz(self, strategies, scale):
        max_bsz = 0
        bsz = scale
        while True:
            pp_stage_dict = get_pp_stage_for_bsz(strategies, self.memcost_model_args_list, self.layernum_list, bsz)
            dp_on_model = DpOnModel(strategies, MemoryCostModel, TimeCostModel, 
                                    self.memcost_model_args_list, self.timecost_model_args_list,
                                    max_mem=self.memory_constraint, layer_num=self.layernum_list, 
                                    multi_layer_type = True, pp_stage_dict = pp_stage_dict,
                                    comm_coe_dict=self.allreduce_comm_coe, gpu_num=self.args.gpu_num)
            min_cost, min_res_list, min_pp_deg, mem_remain, mem_cost = dp_on_model.fit(bsz, False)
            if min_pp_deg == -1:
                max_bsz = bsz - scale
                break
            bsz += scale
        return max_bsz

    def dynamic_programming(self, bsz, pp_stage_dict):
        args = self.args
        print('bsz=%d'%bsz, pp_stage_dict)
        dp_on_model = DpOnModel(self.strategies, 
                                MemoryCostModel, 
                                TimeCostModel, 
                                memcost_model_args=self.memcost_model_args_list,
                                timecost_model_args=self.timecost_model_args_list,
                                max_mem=self.memory_constraint,
                                layer_num=self.layernum_list,
                                multi_layer_type = True,
                                pp_stage_dict = pp_stage_dict,
                                search_history=self.search_history,
                                comm_coe_dict=self.allreduce_comm_coe,
                                gpu_num=args.gpu_num,
                                model_microbatch_after_dp=args.use_pipeline_costmodel,
                                pipeline_type=args.pipeline_type)

        print("****Searching with bsz=", bsz, "****")
        chunk_dict = check_optimal_chunks(args.gpu_num, self.strategies, self.optimal_chunk_func, bsz)
        print('Chunk_dict for bsz %d: '%bsz, chunk_dict)
        
        min_cost, min_res_list, min_pp_deg, mem_remain, mem_cost = dp_on_model.fit(bsz)
        throughput = bsz / min_cost
        print(f"[Optimal pp_deg={min_pp_deg}] Minimized timecost={min_cost} Memory remaining={mem_remain} Memory cost={mem_cost}")
        print(f"Max throughput={throughput} samples/s")
        print_strategies(min_res_list)
        result = {'min_cost': min_cost, 'min_res_list': min_res_list, 'min_pp_deg': min_pp_deg, 
                        'mem_remain': mem_remain, 'mem_cost': mem_cost, 'throughput': throughput}
        return result

    def save_results(self, results, bsz, pp_stage_dict):
        re, optimal_bsz = results, bsz
        args = self.args
        if re['min_pp_deg'] > 0 and re['min_res_list'] is not None:
            result_strategy = []
            if isinstance(re['min_res_list'],list):
                for l in re['min_res_list']:
                    result_strategy += l
            else:
                result_strategy = re['min_res_list']
            config = strategy2config(result_strategy)
            config['checkpoint'] = array2str([1 if 'cpt' in s[-1] and s[-1]['cpt'] else 0 for s in result_strategy])
            config['global_bsz'] = optimal_bsz
            config['chunks'] = max([int(self.optimal_chunk_func(optimal_bsz//s[2],s)) for s in result_strategy]) if config['pp_deg'] > 1 else 1
            config['pp_division'] = array2str(pp_stage_dict[config['pp_deg']])
            config['pipeline_type'] = args.pipeline_type
            config['default_dp_type'] = args.default_dp_type
            if args.embed_sdp:
                config['embed_sdp'] = 1
            
            mixed_precision = '_%s'%args.mixed_precision
            settle_bsz = '_bsz%d'%args.settle_bsz if args.settle_bsz > 0 else ''
            off_options = []
            if args.disable_dp:
                off_options.append('dp')
            if args.disable_tp:
                off_options.append('tp')
            if args.disable_pp:
                off_options.append('pp')
            if args.disable_sdp:
                off_options.append('sdp')
            if args.disable_ckpt:
                off_options.append('ckpt')
            if args.disable_tp_consec:
                off_options.append('tpconsec')
            off_options_str = '_[%s_off]'%('_'.join(off_options))if len(off_options) else ''
            
            config_path = 'configs/galvatron_config_%s_%dnodes_%dgpus_per_node_%dGB'%(self.model_name, args.num_nodes, args.num_gpus_per_node, self.memory_constraint//1024)
            config_path += mixed_precision + settle_bsz + off_options_str
            config_path = os.path.join(self.path, config_path+'.json')
            write_json_config(config, config_path)
            print('Already written optimized parallelism config into galvatron config file %s!'%(config_path))

    # Check cost model, for developers
    def check_cost_model(self, bsz):
        memory = [[] for _ in range(self.num_layertype)]
        memory_total = [[] for _ in range(self.num_layertype)]
        other = []
        for i in range(self.num_layertype):
            memcost_model_args, timecost_model_args, layer_num = self.memcost_model_args_list[i], self.timecost_model_args_list[i], self.layernum_list[i]
            for strategy in self.strategies:
                re = MemoryCostModel(strategy, global_batch_size=bsz, **memcost_model_args).get_memory_cost()
                re_total = re['enc_total']*layer_num/strategy[0]
                print(form_strategy(strategy), re['enc_total'], re['other'], [re_total + re_other for re_other in re['other']])
                memory[i].append(re['enc_total'])
                memory_total[i].append(re['enc_total']*layer_num)
                if i == 0:
                    other.append(re['other'])
            print()
        for i, strategy in enumerate(self.strategies):
            if strategy[0]==1:
                print(form_strategy(strategy), np.sum([memory_total[j][i] for j in range(self.num_layertype)])+other[i][0])
            else:
                layer_memcosts = get_layer_costs(self.layernum_list, [memory[j][i] for j in range(self.num_layertype)])
                pp_division = pp_division_even(self.layernum_list, strategy[0])
                mem_cost_stages = get_cost_all_stages(layer_memcosts, pp_division)
                print(form_strategy(strategy), mem_cost_stages[0]+other[i][0], mem_cost_stages[-1]+other[i][-1])
            
        print()
        timecost = [[] for _ in range(self.num_layertype)]
        timecost_total = [[] for _ in range(self.num_layertype)]
        for i in range(self.num_layertype):
            for strategy in self.strategies:
                re = TimeCostModel(strategy, global_batch_size=bsz, **timecost_model_args).gen_result()
                print(form_strategy(strategy), re*layer_num)
                timecost[i].append(re)
                timecost_total[i].append(re*layer_num)
            print()
        if self.num_layertype > 1:
            for i, strategy in enumerate(self.strategies):
                print(form_strategy(strategy), np.sum([timecost_total[j][i] for j in range(self.num_layertype)]))
        
    # =============== Strategies & Search Space Utils ===============
    def generate_strategies(self):
        args = self.args
        gpu_num = args.gpu_num
        strategies = self.generate_dp_tp_pp_sdp()
        if args.search_space == 'dp+tp':
            args.disable_sdp = 1
            args.disable_pp = 1
        elif args.search_space == 'dp+pp':
            args.disable_sdp = 1
            args.disable_tp = 1
        elif args.search_space == '3d':
            args.disable_sdp = 1
        if args.search_space in ['3d', 'dp', 'tp', 'pp', 'sdp']:
            self.strategies = strategies
            args.disable_ckpt = 1
            return strategies
        strategies_new = []
        assert(not(args.disable_sdp and args.disable_dp))
        for s in strategies:
            if args.disable_dp and s[2] > 1 and 'fsdp' in s[-1] and s[-1]['fsdp'] == 0:
                continue
            if args.disable_sdp and s[2] > 1 and 'fsdp' in s[-1] and s[-1]['fsdp'] == 1:
                continue
            if args.disable_tp and s[1] > 1:
                continue
            if args.disable_pp and s[0] > 1:
                continue
            if args.disable_tp_consec and 'tp' in s[-1] and s[-1]['tp'] == 0:
                continue
            if s[1] > args.max_tp_deg:
                continue
            if s[0] > args.max_pp_deg:
                continue
            strategies_new.append(s)
        strategies = strategies_new

        if not args.disable_ckpt:
            strategies_cpt = []
            for s in strategies:
                s_cpt = copy.deepcopy(s)
                s_cpt[-1]['cpt']=1
                strategies_cpt.append(s_cpt)
            strategies += strategies_cpt
        self.strategies = strategies
        return strategies
    
    def generate_strategies_for_memory_test(self):
        strategies = self.generate_dp_tp_pp_sdp(gpu_num=8, search_space='full')
        return strategies
    
    def generate_dp_tp_pp_sdp(self, gpu_num=None, search_space=None):
        args = self.args
        gpu_num = args.gpu_num if gpu_num is None else gpu_num
        search_space = args.search_space if search_space is None else search_space
        i, total = 1, []
        while i<=gpu_num:
            total.append(i)
            i *= 2
        if args.search_space == 'full':
            strategies = []
            for pp in total:
                for tp in total:
                    if pp*tp<=gpu_num:
                        dp = gpu_num // (pp * tp) 
                        if tp==1 or tp == gpu_num/pp:
                            if dp == 1:
                                strategies.append([pp,tp,dp,{}])
                            else:
                                strategies.append([pp,tp,dp,{'fsdp':0}])
                                strategies.append([pp,tp,dp,{'fsdp':1}])
                        else:
                            strategies.append([pp,tp,dp,{'tp':0,'fsdp':0}])
                            strategies.append([pp,tp,dp,{'tp':0,'fsdp':1}])
                            strategies.append([pp,tp,dp,{'tp':1,'fsdp':0}])
                            strategies.append([pp,tp,dp,{'tp':1,'fsdp':1}])
        elif args.search_space == 'dp+tp':
            strategies = []
            pp = 1
            for tp in total:
                if pp*tp<=gpu_num:
                    dp = gpu_num // (pp * tp) 
                    if tp==1 or tp == gpu_num/pp:
                        if dp == 1:
                            strategies.append([pp,tp,dp,{}])
                        else:
                            strategies.append([pp,tp,dp,{'fsdp':0}])
                    else:
                        strategies.append([pp,tp,dp,{'tp':0,'fsdp':0}])
                        strategies.append([pp,tp,dp,{'tp':1,'fsdp':0}])
        elif args.search_space == 'dp+pp':
            strategies = []
            tp = 1
            for pp in total:
                if pp*tp<=gpu_num:
                    dp = gpu_num // (pp * tp) 
                    if tp==1 or tp == gpu_num/pp:
                        if dp == 1:
                            strategies.append([pp,tp,dp,{}])
                        else:
                            strategies.append([pp,tp,dp,{'fsdp':0}])
                    else:
                        strategies.append([pp,tp,dp,{'tp':0,'fsdp':0}])
                        strategies.append([pp,tp,dp,{'tp':1,'fsdp':0}])
        elif args.search_space == '3d':
            strategies = [[2,2,gpu_num//4,{'tp':1,'fsdp':0}]]
        elif args.search_space == 'dp':
            strategies = [[1,1,gpu_num,{'fsdp':0}]]
        elif args.search_space == 'tp':
            strategies = [[1,args.max_tp_deg,gpu_num//args.max_tp_deg,{'fsdp':0}]]
            if strategies[0][2] > 1:
                strategies[0][-1]['tp'] = 1
        elif args.search_space == 'pp':
            strategies = [[args.max_pp_deg,1,gpu_num//args.max_pp_deg,{'fsdp':0}]]
        return strategies
    
    def show_search_info(self):
        print('================================================================================')
        print('--- Optimization Configs ----')
        print('Memory constraint: %d GB'%self.args.memory_constraint)
        print('Pipeline Type:', self.args.pipeline_type)
        print('Default DP Type:', self.args.default_dp_type)
        print('Mixed Precision:', self.args.mixed_precision)
        if self.args.embed_sdp:
            print('Embedding SDP: ON')
        print('Search Space:')
        print_strategies(self.strategies)
        print('================================================================================')
        print('---- Environment Configs ----')
        print('Allreduce Bandwidth (GB/s):', self.allreduce_bandwidth)
        print('Allreduce Communication Coefficient (ms/MB):', self.allreduce_comm_coe)
        print('P2P Bandwidth (GB/s):', self.p2p_bandwidth)
        print('P2P Communication Coefficient (ms/MB):', self.p2p_comm_coe)
        print('Overlap coefficient:', self.overlap_coe)
        print('================================================================================')
        print('------- Model Configs -------')
        print('Model Name:', self.model_name)
        print('Num layertype:', self.num_layertype)
        print('Layer_num:', self.layernum_list)
        print('Hidden_size:', self.hiddensize_list)
        print('Seq_len:', self.seqlen_list)
        print('================================================================================')
        print('--- Model Computation Configs ---')
        print('Forward computation time:', self.time_profiled_list)
        print('================================================================================')
        print('--- Model Memory Configs ---')
        print('Parameter Memory Cost:', self.param_sizes)
        print('Activation Memory Cost of Different TP degree (per bsz):')
        print(self.act_sizes)
        print('Other Memory Cost (pp = 1):')
        print(self.other_memory_pp_off)
        print('Other Memory Cost (pp > 1):')
        print(self.other_memory_pp_on)
        print('================================================================================')
        print('Time Cost Model Args:')
        print(self.timecost_model_args_list)
        print('================================================================================')
        print('Memory Cost Model Args:')
        print(self.memcost_model_args_list)
        print('================================================================================')


# ========================== Pipeline Division & Pipeline Cost Utils ==========================
def pp_division_memory_balanced(memcost_model_args, layer_num, pp_deg, bsz, strategies):
    assert(len(memcost_model_args)==len(layer_num))
    if pp_deg == 1:
        return [np.sum(layer_num)], None
    layer_type_num = len(layer_num)
    layer_min_memcost = []
    strategies = list(filter(lambda s: s[0] == pp_deg, strategies))
    if len(strategies)==0:
        return None, None
    gpu_num = strategies[0][0] * strategies[0][1] * strategies[0][2]
    for i in range(layer_type_num):
        # memcosts = [MemoryCostModel(strategy, global_batch_size=bsz, **memcost_model_args[i]).get_memory_cost()['enc_total'] for strategy in strategies]
        # layer_min_memcost.append(np.min(memcosts))
        memcost = MemoryCostModel([pp_deg, 1, gpu_num//pp_deg, {}], global_batch_size=bsz, **memcost_model_args[i]).get_memory_cost()['enc_total']
        layer_min_memcost.append(np.min(memcost))
    other_cost = MemoryCostModel(strategies[0], global_batch_size=bsz, **memcost_model_args[0]).get_memory_cost()['other']
    # print(layer_min_memcost, other_cost)
    min_memcost_all_layers = []
    for i in range(layer_type_num):
        min_memcost_all_layers += [layer_min_memcost[i]]*layer_num[i]
    #print(min_memcost_all_layers)
    avg_mem_cost = (np.sum(min_memcost_all_layers)+np.sum(other_cost))/pp_deg
    #print('Avg memcost:', avg_mem_cost)

    pp_divide = [0]*pp_deg
    mem_cost_per_stage = other_cost.copy()
    idx = len(min_memcost_all_layers)-1
    for i in range(pp_deg-1,-1,-1):
        while True:
            if idx < 0:
                break
            if i > 0 and avg_mem_cost - mem_cost_per_stage[i] < 0.5 * min_memcost_all_layers[idx]:
                break
            else:
                mem_cost_per_stage[i]+=min_memcost_all_layers[idx]
                idx-=1
                pp_divide[i]+=1
    # print(pp_divide)

    # Avoid too much memory cost on previous stages
    for i in range(pp_deg-1):
        left, right = int(np.sum(pp_divide[:i])), int(np.sum(pp_divide[:i+1]))
        mem_cost_cur_stage = np.sum(min_memcost_all_layers[left:right]) + other_cost[i]
        while mem_cost_cur_stage > avg_mem_cost * 1.3:
            pp_divide[i] -= 1
            pp_divide[i+1] += 1
            right -= 1
            mem_cost_cur_stage -= min_memcost_all_layers[right]

    # Avoid no layers on previous stages
    for i in range(pp_deg-1):
        while pp_divide[i] <= 0:
            pp_divide[i] += 1
            pp_divide[i+1] -= 1

    # Avoid no layers on last stage
    for i in range(pp_deg-1, 0, -1):
        while pp_divide[i] <= 0:
            pp_divide[i] += 1
            pp_divide[i-1] -= 1
    
    mem_cost_per_stage_adjusted = other_cost.copy()
    # print(pp_divide)
    # print(other_cost, avg_mem_cost)
    for i in range(pp_deg):
        left, right = int(np.sum(pp_divide[:i])), int(np.sum(pp_divide[:i+1]))
        mem_cost_per_stage_adjusted[i] +=  np.sum(min_memcost_all_layers[left:right])
    # print(mem_cost_per_stage,mem_cost_per_stage_adjusted)
    return pp_divide, mem_cost_per_stage_adjusted

def get_pp_stage_for_bsz(strategies, memcost_model_args_list, layer_num_list, bsz, single_layer_even=True):
    pp_stage_dict = dict()
    pp_deg_list = sorted(list(set([s[0] for s in strategies])))
    for pp_deg in pp_deg_list:
        if single_layer_even and len(layer_num_list) == 1:
            pp_divide = pp_division_even(layer_num_list, pp_deg)
        else:
            pp_divide, mem_cost_per_stage = pp_division_memory_balanced(memcost_model_args_list, layer_num_list, pp_deg, bsz, strategies)
            #print(bsz, pp_deg, pp_divide, mem_cost_per_stage)
        pp_stage_dict[pp_deg] = pp_divide
    return pp_stage_dict

def get_pp_stages_for_all_bsz(strategies, memcost_model_args_list, layer_num_list, bszs):
    pp_stage_dict_for_bsz = dict()
    for bsz in bszs:
        pp_stage_dict_for_bsz[bsz] = get_pp_stage_for_bsz(strategies, memcost_model_args_list, layer_num_list, bsz)
    return pp_stage_dict_for_bsz
    
def get_cost_all_stages(layer_memcosts, pp_stage_division):
    pp_stage_division = copy.deepcopy(pp_stage_division)
    # include other memory on first stage
    if np.sum(pp_stage_division) + 1 == len(layer_memcosts):
        pp_stage_division[0] += 1
    elif np.sum(pp_stage_division) + 2 == len(layer_memcosts):
        pp_stage_division[0] += 1
        pp_stage_division[-1] += 1
        dist_costmodel = True
    assert(np.sum(pp_stage_division)==len(layer_memcosts))
    stage_memcosts = []
    for stage_id in range(len(pp_stage_division)):
        layer_start_id, layer_end_id = int(np.sum(pp_stage_division[:stage_id])), int(np.sum(pp_stage_division[:stage_id+1]))
        stage_memcosts.append(np.sum(layer_memcosts[layer_start_id:layer_end_id]))
    return stage_memcosts

def get_layer_costs(layernum_list, layer_costs):
    layer_memcosts = []
    for i in range(len(layernum_list)):
        layer_memcosts += [layer_costs[i]]*layernum_list[i]
    return layer_memcosts
    
def pp_division_even(layernum_list, pp_deg):
    total_layer_num = np.sum(layernum_list)
    avg_layer_num = int(total_layer_num // pp_deg)
    last_layer_num = total_layer_num - avg_layer_num * (pp_deg-1)
    pp_division = [avg_layer_num] * (pp_deg-1) + [last_layer_num]
    return pp_division
    
def optimal_chunk_func_default(local_bsz, strategy, microbatch_size=4, max_chunk=8):
    if strategy[0] == 1:
        return 1
    local_bsz = local_bsz // strategy[1]
    chunk = np.ceil(local_bsz / microbatch_size)
    chunk = 1 if chunk == 0 else chunk
    chunk = int(min(max_chunk,chunk))
    return chunk

def check_optimal_chunks(world_size, strategies, optimal_chunk_func, bsz):
    chunk_dict = {}
    for pp_deg in sorted(set([s[0] for s in strategies])):
        chunk_dict[pp_deg] = optimal_chunk_func(bsz/(world_size//pp_deg), [pp_deg,1,world_size//pp_deg,{'fsdp':0,'cpt':0}])
    return chunk_dict