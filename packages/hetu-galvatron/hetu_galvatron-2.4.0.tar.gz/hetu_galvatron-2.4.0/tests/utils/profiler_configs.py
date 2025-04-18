import json
from pathlib import Path
from typing import Dict

def create_computation_static_config() -> Dict[str, float]:
    """Create computation config for static profiling mode"""
    return {
        "layernum[2]_bsz8_seq4096": 397.8879272460938,
        "layernum[4]_bsz8_seq4096": 577.403973388672,
    }

def create_computation_batch_config() -> Dict[str, float]:
    """Create computation config for batch profiling mode"""
    return {
        "layernum[2]_bsz1_seq4096": 56.78504333496094,
        "layernum[2]_bsz2_seq4096": 105.94930801391602,
        "layernum[2]_bsz3_seq4096": 154.13173370361326,
        "layernum[2]_bsz4_seq4096": 205.84587402343746,
        "layernum[2]_bsz5_seq4096": 254.65832366943357,
        "layernum[2]_bsz6_seq4096": 303.82422180175786,
        "layernum[2]_bsz7_seq4096": 351.6025604248047,
        "layernum[2]_bsz8_seq4096": 397.8879272460938,
        "layernum[2]_bsz9_seq4096": 447.52890319824223,
        "layernum[2]_bsz10_seq4096": 497.7088653564453,
        "layernum[4]_bsz1_seq4096": 81.59648361206054,
        "layernum[4]_bsz2_seq4096": 152.3643768310547,
        "layernum[4]_bsz3_seq4096": 225.4001556396484,
        "layernum[4]_bsz4_seq4096": 295.06984252929686,
        "layernum[4]_bsz5_seq4096": 364.5030181884765,
        "layernum[4]_bsz6_seq4096": 433.8601928710938,
        "layernum[4]_bsz7_seq4096": 508.1806396484374,
        "layernum[4]_bsz8_seq4096": 577.403973388672,
        "layernum[4]_bsz9_seq4096": 649.7438232421875,
        "layernum[4]_bsz10_seq4096": 722.4481384277344,
    }

def create_computation_sequence_config() -> Dict[str, float]:
    """Create computation config for sequence profiling mode"""
    return {
        "layernum[1]_bsz1_seq4096": 44.379323196411136,
        "layernum[1]_bsz1_seq8192": 84.72667922973633,
        "layernum[1]_bsz1_seq12288": 126.05830383300781,
        "layernum[1]_bsz1_seq16384": 173.8589874267578,
        "layernum[1]_bsz1_seq20480": 212.65643768310542,
        "layernum[1]_bsz1_seq24576": 260.3837417602539,
        "layernum[1]_bsz1_seq28672": 303.55413208007815,
        "layernum[1]_bsz1_seq32768": 348.99433898925787,
        "layernum[2]_bsz1_seq4096": 56.78504333496094,
        "layernum[2]_bsz1_seq8192": 113.18091049194334,
        "layernum[2]_bsz1_seq12288": 165.49309692382812,
        "layernum[2]_bsz1_seq16384": 226.46562652587892,
        "layernum[2]_bsz1_seq20480": 283.4093292236329,
        "layernum[2]_bsz1_seq24576": 343.0808563232422,
        "layernum[2]_bsz1_seq28672": 409.6926330566406,
        "layernum[2]_bsz1_seq32768": 472.19422912597656,
    }

def create_memory_static_config() -> Dict:
    """Create memory config for static profiling mode"""
    return {
        "1_1_8": {
            "layernum[1]_bsz8_seq4096_rank0_ms": 902.30615234375,
            "layernum[1]_bsz8_seq4096_rank0_act": 918.607421875,
            "layernum[1]_bsz8_seq4096_rank0_act_peak": 1371.5771484375,
            "layernum[1]_bsz8_seq4096_rank7_ms": 902.30615234375,
            "layernum[1]_bsz8_seq4096_rank7_act": 918.607421875,
            "layernum[1]_bsz8_seq4096_rank7_act_peak": 1371.5771484375,
            "layernum[2]_bsz8_seq4096_rank0_ms": 1288.322265625,
            "layernum[2]_bsz8_seq4096_rank0_act": 1523.1708984375,
            "layernum[2]_bsz8_seq4096_rank0_act_peak": 2015.65234375,
            "layernum[2]_bsz8_seq4096_rank7_ms": 1288.322265625,
            "layernum[2]_bsz8_seq4096_rank7_act": 1523.1708984375,
            "layernum[2]_bsz8_seq4096_rank7_act_peak": 2015.65234375
        },
        "1_2_4": {
            "layernum[1]_bsz8_seq4096_rank0_ms": 902.32177734375,
            "layernum[1]_bsz8_seq4096_rank0_act": 1078.669921875,
            "layernum[1]_bsz8_seq4096_rank0_act_peak": 1389.1572265625,
            "layernum[1]_bsz8_seq4096_rank7_ms": 902.32177734375,
            "layernum[1]_bsz8_seq4096_rank7_act": 1078.669921875,
            "layernum[1]_bsz8_seq4096_rank7_act_peak": 1389.1572265625,
            "layernum[2]_bsz8_seq4096_rank0_ms": 1288.353515625,
            "layernum[2]_bsz8_seq4096_rank0_act": 1843.2958984375,
            "layernum[2]_bsz8_seq4096_rank0_act_peak": 2057.275390625,
            "layernum[2]_bsz8_seq4096_rank7_ms": 1288.353515625,
            "layernum[2]_bsz8_seq4096_rank7_act": 1843.2958984375,
            "layernum[2]_bsz8_seq4096_rank7_act_peak": 2057.275390625
        },
        "1_2_4_vtp": {
            "layernum[1]_bsz8_seq4096_rank0_ms": 902.4228515625,
            "layernum[1]_bsz8_seq4096_rank0_act": 1142.78369140625,
            "layernum[1]_bsz8_seq4096_rank0_act_peak": 1297.52099609375,
            "layernum[1]_bsz8_seq4096_rank7_ms": 902.4228515625,
            "layernum[1]_bsz8_seq4096_rank7_act": 1142.78369140625,
            "layernum[1]_bsz8_seq4096_rank7_act_peak": 1297.52099609375,
            "layernum[2]_bsz8_seq4096_rank0_ms": 1288.45458984375,
            "layernum[2]_bsz8_seq4096_rank0_act": 1908.39404296875,
            "layernum[2]_bsz8_seq4096_rank0_act_peak": 1966.62353515625,
            "layernum[2]_bsz8_seq4096_rank7_ms": 1288.45458984375,
            "layernum[2]_bsz8_seq4096_rank7_act": 1908.39404296875,
            "layernum[2]_bsz8_seq4096_rank7_act_peak": 1966.62353515625
        },
        "1_4_2": {
            "layernum[1]_bsz8_seq4096_rank0_ms": 902.35302734375,
            "layernum[1]_bsz8_seq4096_rank0_act": 1334.794921875,
            "layernum[1]_bsz8_seq4096_rank0_act_peak": 1645.2744140625,
            "layernum[1]_bsz8_seq4096_rank7_ms": 902.35302734375,
            "layernum[1]_bsz8_seq4096_rank7_act": 1334.794921875,
            "layernum[1]_bsz8_seq4096_rank7_act_peak": 1645.2744140625,
            "layernum[2]_bsz8_seq4096_rank0_ms": 1288.416015625,
            "layernum[2]_bsz8_seq4096_rank0_act": 2355.5458984375,
            "layernum[2]_bsz8_seq4096_rank0_act_peak": 2569.509765625,
            "layernum[2]_bsz8_seq4096_rank7_ms": 1288.416015625,
            "layernum[2]_bsz8_seq4096_rank7_act": 2355.5458984375,
            "layernum[2]_bsz8_seq4096_rank7_act_peak": 2569.509765625
        },
        "1_4_2_vtp": {
            "layernum[1]_bsz8_seq4096_rank0_ms": 902.5947265625,
            "layernum[1]_bsz8_seq4096_rank0_act": 1527.06494140625,
            "layernum[1]_bsz8_seq4096_rank0_act_peak": 1618.54052734375,
            "layernum[1]_bsz8_seq4096_rank7_ms": 902.5947265625,
            "layernum[1]_bsz8_seq4096_rank7_act": 1527.06494140625,
            "layernum[1]_bsz8_seq4096_rank7_act_peak": 1618.54052734375,
            "layernum[2]_bsz8_seq4096_rank0_ms": 1288.65771484375,
            "layernum[2]_bsz8_seq4096_rank0_act": 2547.81591796875,
            "layernum[2]_bsz8_seq4096_rank0_act_peak": 2542.77587890625,
            "layernum[2]_bsz8_seq4096_rank7_ms": 1288.65771484375,
            "layernum[2]_bsz8_seq4096_rank7_act": 2547.81591796875,
            "layernum[2]_bsz8_seq4096_rank7_act_peak": 2542.77587890625
        },
        "1_8_1": {
            "layernum[1]_bsz8_seq4096_rank0_ms": 902.85302734375,
            "layernum[1]_bsz8_seq4096_rank0_act": 1847.044921875,
            "layernum[1]_bsz8_seq4096_rank0_act_peak": 2157.5087890625,
            "layernum[1]_bsz8_seq4096_rank7_ms": 902.85302734375,
            "layernum[1]_bsz8_seq4096_rank7_act": 1847.044921875,
            "layernum[1]_bsz8_seq4096_rank7_act_peak": 2157.5087890625,
            "layernum[2]_bsz8_seq4096_rank0_ms": 1288.541015625,
            "layernum[2]_bsz8_seq4096_rank0_act": 3380.0458984375,
            "layernum[2]_bsz8_seq4096_rank0_act_peak": 3593.978515625,
            "layernum[2]_bsz8_seq4096_rank7_ms": 1288.541015625,
            "layernum[2]_bsz8_seq4096_rank7_act": 3380.0458984375,
            "layernum[2]_bsz8_seq4096_rank7_act_peak": 3593.978515625
        },
        "1_8_1_vtp": {
            "layernum[1]_bsz8_seq4096_rank0_ms": 902.9384765625,
            "layernum[1]_bsz8_seq4096_rank0_act": 2295.62744140625,
            "layernum[1]_bsz8_seq4096_rank0_act_peak": 2393.2451171875,
            "layernum[1]_bsz8_seq4096_rank7_ms": 902.9384765625,
            "layernum[1]_bsz8_seq4096_rank7_act": 2295.62744140625,
            "layernum[1]_bsz8_seq4096_rank7_act_peak": 2393.9951171875,
            "layernum[2]_bsz8_seq4096_rank0_ms": 1289.06396484375,
            "layernum[2]_bsz8_seq4096_rank0_act": 3828.62841796875,
            "layernum[2]_bsz8_seq4096_rank0_act_peak": 3829.71484375,
            "layernum[2]_bsz8_seq4096_rank7_ms": 1289.06396484375,
            "layernum[2]_bsz8_seq4096_rank7_act": 3828.62841796875,
            "layernum[2]_bsz8_seq4096_rank7_act_peak": 3830.46484375
        },
        "1_1_8_c": {
            "layernum[1]_bsz8_seq4096_rank0_ms": 902.30615234375,
            "layernum[1]_bsz8_seq4096_rank0_act": 346.0439453125,
            "layernum[1]_bsz8_seq4096_rank0_act_peak": 1403.5771484375,
            "layernum[1]_bsz8_seq4096_rank7_ms": 902.30615234375,
            "layernum[1]_bsz8_seq4096_rank7_act": 346.0439453125,
            "layernum[1]_bsz8_seq4096_rank7_act_peak": 1403.5771484375,
            "layernum[2]_bsz8_seq4096_rank0_ms": 1288.322265625,
            "layernum[2]_bsz8_seq4096_rank0_act": 378.0439453125,
            "layernum[2]_bsz8_seq4096_rank0_act_peak": 1475.0888671875,
            "layernum[2]_bsz8_seq4096_rank7_ms": 1288.322265625,
            "layernum[2]_bsz8_seq4096_rank7_act": 378.0439453125,
            "layernum[2]_bsz8_seq4096_rank7_act_peak": 1475.0888671875
        },
        "2_1_4": {
            "layernum[2]_bsz8_seq4096_rank0_ms": 1292.3916015625,
            "layernum[2]_bsz8_seq4096_rank0_act": 1333.06396484375,
            "layernum[2]_bsz8_seq4096_rank0_act_peak": 2143.14208984375,
            "layernum[2]_bsz8_seq4096_rank7_ms": 1291.4072265625,
            "layernum[2]_bsz8_seq4096_rank7_act": 1897.21337890625,
            "layernum[2]_bsz8_seq4096_rank7_act_peak": 2327.45849609375
        },
        "2_2_2": {
            "layernum[2]_bsz8_seq4096_rank0_ms": 1293.3916015625,
            "layernum[2]_bsz8_seq4096_rank0_act": 1653.18896484375,
            "layernum[2]_bsz8_seq4096_rank0_act_peak": 2293.12646484375,
            "layernum[2]_bsz8_seq4096_rank7_ms": 1291.4228515625,
            "layernum[2]_bsz8_seq4096_rank7_act": 2153.33837890625,
            "layernum[2]_bsz8_seq4096_rank7_act_peak": 2583.58349609375
        },
        "2_2_2_vtp": {
            "layernum[2]_bsz8_seq4096_rank0_ms": 1292.5322265625,
            "layernum[2]_bsz8_seq4096_rank0_act": 1653.26708984375,
            "layernum[2]_bsz8_seq4096_rank0_act_peak": 2168.39208984375,
            "layernum[2]_bsz8_seq4096_rank7_ms": 1291.5634765625,
            "layernum[2]_bsz8_seq4096_rank7_act": 2281.42431640625,
            "layernum[2]_bsz8_seq4096_rank7_act_peak": 2587.91552734375
        },
        "2_4_1": {
            "layernum[2]_bsz8_seq4096_rank0_ms": 1291.4697265625,
            "layernum[2]_bsz8_seq4096_rank0_act": 2293.43896484375,
            "layernum[2]_bsz8_seq4096_rank0_act_peak": 2941.51708984375,
            "layernum[2]_bsz8_seq4096_rank7_ms": 1292.4541015625,
            "layernum[2]_bsz8_seq4096_rank7_act": 2665.58837890625,
            "layernum[2]_bsz8_seq4096_rank7_act_peak": 3095.83349609375
        },
        "2_4_1_vtp": {
            "layernum[2]_bsz8_seq4096_rank0_ms": 1292.8134765625,
            "layernum[2]_bsz8_seq4096_rank0_act": 2293.53271484375,
            "layernum[2]_bsz8_seq4096_rank0_act_peak": 2754.29833984375,
            "layernum[2]_bsz8_seq4096_rank7_ms": 1293.8759765625,
            "layernum[2]_bsz8_seq4096_rank7_act": 3049.84619140625,
            "layernum[2]_bsz8_seq4096_rank7_act_peak": 3293.32958984375
        },
        "4_1_2": {
            "layernum[4]_bsz8_seq4096_rank0_ms": 2560.56494140625,
            "layernum[4]_bsz8_seq4096_rank0_act": 2662.12646484375,
            "layernum[4]_bsz8_seq4096_rank0_act_peak": 3564.25146484375,
            "layernum[4]_bsz8_seq4096_rank7_ms": 2560.59619140625,
            "layernum[4]_bsz8_seq4096_rank7_act": 3790.42431640625,
            "layernum[4]_bsz8_seq4096_rank7_act_peak": 4404.89990234375
        },
        "4_2_1": {
            "layernum[4]_bsz8_seq4096_rank0_ms": 2560.62744140625,
            "layernum[4]_bsz8_seq4096_rank0_act": 3302.37646484375,
            "layernum[4]_bsz8_seq4096_rank0_act_peak": 4097.47021484375,
            "layernum[4]_bsz8_seq4096_rank7_ms": 2560.65869140625,
            "layernum[4]_bsz8_seq4096_rank7_act": 4302.67431640625,
            "layernum[4]_bsz8_seq4096_rank7_act_peak": 4917.13427734375
        },
        "4_2_1_vtp": {
            "layernum[4]_bsz8_seq4096_rank0_ms": 2560.87744140625,
            "layernum[4]_bsz8_seq4096_rank0_act": 3302.53271484375,
            "layernum[4]_bsz8_seq4096_rank0_act_peak": 3973.75146484375,
            "layernum[4]_bsz8_seq4096_rank7_ms": 2560.93994140625,
            "layernum[4]_bsz8_seq4096_rank7_act": 4558.84619140625,
            "layernum[4]_bsz8_seq4096_rank7_act_peak": 5049.79833984375
        }
    }

def create_memory_static_config_sp() -> Dict:
    """Create memory config for static profiling mode with sequence parallelism"""
    return {
        "1_1_8_sp": {
            "layernum[1]_bsz8_seq4096_rank0_ms": 902.30615234375,
            "layernum[1]_bsz8_seq4096_rank0_act": 918.607421875,
            "layernum[1]_bsz8_seq4096_rank0_act_peak": 1371.5771484375,
            "layernum[1]_bsz8_seq4096_rank7_ms": 902.30615234375,
            "layernum[1]_bsz8_seq4096_rank7_act": 918.607421875,
            "layernum[1]_bsz8_seq4096_rank7_act_peak": 1371.5771484375,
            "layernum[2]_bsz8_seq4096_rank0_ms": 1288.322265625,
            "layernum[2]_bsz8_seq4096_rank0_act": 1523.1708984375,
            "layernum[2]_bsz8_seq4096_rank0_act_peak": 2015.65234375,
            "layernum[2]_bsz8_seq4096_rank7_ms": 1288.322265625,
            "layernum[2]_bsz8_seq4096_rank7_act": 1523.1708984375,
            "layernum[2]_bsz8_seq4096_rank7_act_peak": 2015.65234375
        },
        "1_2_4_sp": {
            "layernum[1]_bsz8_seq4096_rank0_ms": 966.33740234375,
            "layernum[1]_bsz8_seq4096_rank0_act": 950.607421875,
            "layernum[1]_bsz8_seq4096_rank0_act_peak": 1261.0947265625,
            "layernum[1]_bsz8_seq4096_rank7_ms": 966.33740234375,
            "layernum[1]_bsz8_seq4096_rank7_act": 950.607421875,
            "layernum[1]_bsz8_seq4096_rank7_act_peak": 1261.0947265625,
            "layernum[2]_bsz8_seq4096_rank0_ms": 1352.369140625,
            "layernum[2]_bsz8_seq4096_rank0_act": 1587.1708984375,
            "layernum[2]_bsz8_seq4096_rank0_act_peak": 1801.150390625,
            "layernum[2]_bsz8_seq4096_rank7_ms": 1352.369140625,
            "layernum[2]_bsz8_seq4096_rank7_act": 1587.1708984375,
            "layernum[2]_bsz8_seq4096_rank7_act_peak": 1801.150390625
        },
        "1_2_4_vtp_sp": {
            "layernum[1]_bsz8_seq4096_rank0_ms": 966.4384765625,
            "layernum[1]_bsz8_seq4096_rank0_act": 950.68994140625,
            "layernum[1]_bsz8_seq4096_rank0_act_peak": 1105.42724609375,
            "layernum[1]_bsz8_seq4096_rank7_ms": 966.4384765625,
            "layernum[1]_bsz8_seq4096_rank7_act": 950.68994140625,
            "layernum[1]_bsz8_seq4096_rank7_act_peak": 1105.42724609375,
            "layernum[2]_bsz8_seq4096_rank0_ms": 1352.47021484375,
            "layernum[2]_bsz8_seq4096_rank0_act": 1587.25341796875,
            "layernum[2]_bsz8_seq4096_rank0_act_peak": 1652.68359375,
            "layernum[2]_bsz8_seq4096_rank7_ms": 1352.47021484375,
            "layernum[2]_bsz8_seq4096_rank7_act": 1587.25341796875,
            "layernum[2]_bsz8_seq4096_rank7_act_peak": 1652.68359375
        },
        "1_4_2_sp": {
            "layernum[1]_bsz8_seq4096_rank0_ms": 1030.36865234375,
            "layernum[1]_bsz8_seq4096_rank0_act": 950.607421875,
            "layernum[1]_bsz8_seq4096_rank0_act_peak": 1261.0869140625,
            "layernum[1]_bsz8_seq4096_rank7_ms": 1030.36865234375,
            "layernum[1]_bsz8_seq4096_rank7_act": 950.607421875,
            "layernum[1]_bsz8_seq4096_rank7_act_peak": 1261.0869140625,
            "layernum[2]_bsz8_seq4096_rank0_ms": 1416.431640625,
            "layernum[2]_bsz8_seq4096_rank0_act": 1587.1708984375,
            "layernum[2]_bsz8_seq4096_rank0_act_peak": 1801.134765625,
            "layernum[2]_bsz8_seq4096_rank7_ms": 1416.431640625,
            "layernum[2]_bsz8_seq4096_rank7_act": 1587.1708984375,
            "layernum[2]_bsz8_seq4096_rank7_act_peak": 1801.134765625
        },
        "1_4_2_vtp_sp": {
            "layernum[1]_bsz8_seq4096_rank0_ms": 1030.6103515625,
            "layernum[1]_bsz8_seq4096_rank0_act": 950.78369140625,
            "layernum[1]_bsz8_seq4096_rank0_act_peak": 1042.25927734375,
            "layernum[1]_bsz8_seq4096_rank7_ms": 1030.6103515625,
            "layernum[1]_bsz8_seq4096_rank7_act": 950.78369140625,
            "layernum[1]_bsz8_seq4096_rank7_act_peak": 1042.25927734375,
            "layernum[2]_bsz8_seq4096_rank0_ms": 1416.67333984375,
            "layernum[2]_bsz8_seq4096_rank0_act": 1587.34716796875,
            "layernum[2]_bsz8_seq4096_rank0_act_peak": 1582.30712890625,
            "layernum[2]_bsz8_seq4096_rank7_ms": 1416.67333984375,
            "layernum[2]_bsz8_seq4096_rank7_act": 1587.34716796875,
            "layernum[2]_bsz8_seq4096_rank7_act_peak": 1582.30712890625
        },
        "1_8_1_sp": {
            "layernum[1]_bsz8_seq4096_rank0_ms": 1158.43115234375,
            "layernum[1]_bsz8_seq4096_rank0_act": 950.607421875,
            "layernum[1]_bsz8_seq4096_rank0_act_peak": 1261.0712890625,
            "layernum[1]_bsz8_seq4096_rank7_ms": 1158.43115234375,
            "layernum[1]_bsz8_seq4096_rank7_act": 950.607421875,
            "layernum[1]_bsz8_seq4096_rank7_act_peak": 1261.0712890625,
            "layernum[2]_bsz8_seq4096_rank0_ms": 1545.525390625,
            "layernum[2]_bsz8_seq4096_rank0_act": 1587.1708984375,
            "layernum[2]_bsz8_seq4096_rank0_act_peak": 1801.103515625,
            "layernum[2]_bsz8_seq4096_rank7_ms": 1545.525390625,
            "layernum[2]_bsz8_seq4096_rank7_act": 1587.1708984375,
            "layernum[2]_bsz8_seq4096_rank7_act_peak": 1801.103515625
        },
        "1_8_1_vtp_sp": {
            "layernum[1]_bsz8_seq4096_rank0_ms": 1158.9541015625,
            "layernum[1]_bsz8_seq4096_rank0_act": 950.97119140625,
            "layernum[1]_bsz8_seq4096_rank0_act_peak": 1079.8388671875,
            "layernum[1]_bsz8_seq4096_rank7_ms": 1158.9541015625,
            "layernum[1]_bsz8_seq4096_rank7_act": 950.97119140625,
            "layernum[1]_bsz8_seq4096_rank7_act_peak": 1080.5888671875,
            "layernum[2]_bsz8_seq4096_rank0_ms": 1545.07958984375,
            "layernum[2]_bsz8_seq4096_rank0_act": 1587.53466796875,
            "layernum[2]_bsz8_seq4096_rank0_act_peak": 1620.62109375,
            "layernum[2]_bsz8_seq4096_rank7_ms": 1545.07958984375,
            "layernum[2]_bsz8_seq4096_rank7_act": 1587.53466796875,
            "layernum[2]_bsz8_seq4096_rank7_act_peak": 1620.62109375
        },
        "1_1_8_c_sp": {
            "layernum[1]_bsz8_seq4096_rank0_ms": 902.30615234375,
            "layernum[1]_bsz8_seq4096_rank0_act": 346.0439453125,
            "layernum[1]_bsz8_seq4096_rank0_act_peak": 1403.5771484375,
            "layernum[1]_bsz8_seq4096_rank7_ms": 902.30615234375,
            "layernum[1]_bsz8_seq4096_rank7_act": 346.0439453125,
            "layernum[1]_bsz8_seq4096_rank7_act_peak": 1403.5771484375,
            "layernum[2]_bsz8_seq4096_rank0_ms": 1288.322265625,
            "layernum[2]_bsz8_seq4096_rank0_act": 378.0439453125,
            "layernum[2]_bsz8_seq4096_rank0_act_peak": 1475.0888671875,
            "layernum[2]_bsz8_seq4096_rank7_ms": 1288.322265625,
            "layernum[2]_bsz8_seq4096_rank7_act": 378.0439453125,
            "layernum[2]_bsz8_seq4096_rank7_act_peak": 1475.0888671875
        },
        "2_1_4_sp": {
            "layernum[2]_bsz8_seq4096_rank0_ms": 1292.3916015625,
            "layernum[2]_bsz8_seq4096_rank0_act": 1333.06396484375,
            "layernum[2]_bsz8_seq4096_rank0_act_peak": 2143.14208984375,
            "layernum[2]_bsz8_seq4096_rank7_ms": 1291.4072265625,
            "layernum[2]_bsz8_seq4096_rank7_act": 1897.21337890625,
            "layernum[2]_bsz8_seq4096_rank7_act_peak": 2327.45849609375
        },
        "2_2_2_sp": {
            "layernum[2]_bsz8_seq4096_rank0_ms": 1421.4072265625,
            "layernum[2]_bsz8_seq4096_rank0_act": 1333.06396484375,
            "layernum[2]_bsz8_seq4096_rank0_act_peak": 1909.12646484375,
            "layernum[2]_bsz8_seq4096_rank7_ms": 1419.4384765625,
            "layernum[2]_bsz8_seq4096_rank7_act": 1897.21337890625,
            "layernum[2]_bsz8_seq4096_rank7_act_peak": 2327.45849609375
        },
        "2_2_2_vtp_sp": {
            "layernum[2]_bsz8_seq4096_rank0_ms": 1421.5322265625,
            "layernum[2]_bsz8_seq4096_rank0_act": 1333.14208984375,
            "layernum[2]_bsz8_seq4096_rank0_act_peak": 1785.26708984375,
            "layernum[2]_bsz8_seq4096_rank7_ms": 1419.5791015625,
            "layernum[2]_bsz8_seq4096_rank7_act": 1897.23681640625,
            "layernum[2]_bsz8_seq4096_rank7_act_peak": 2203.72802734375
        },
        "2_4_1_sp": {
            "layernum[2]_bsz8_seq4096_rank0_ms": 1547.4853515625,
            "layernum[2]_bsz8_seq4096_rank0_act": 1333.06396484375,
            "layernum[2]_bsz8_seq4096_rank0_act_peak": 1873.64208984375,
            "layernum[2]_bsz8_seq4096_rank7_ms": 1548.4697265625,
            "layernum[2]_bsz8_seq4096_rank7_act": 1897.21337890625,
            "layernum[2]_bsz8_seq4096_rank7_act_peak": 2327.45849609375
        },
        "2_4_1_vtp_sp": {
            "layernum[2]_bsz8_seq4096_rank0_ms": 1548.8291015625,
            "layernum[2]_bsz8_seq4096_rank0_act": 1333.15771484375,
            "layernum[2]_bsz8_seq4096_rank0_act_peak": 1685.92333984375,
            "layernum[2]_bsz8_seq4096_rank7_ms": 1549.8916015625,
            "layernum[2]_bsz8_seq4096_rank7_act": 1897.28369140625,
            "layernum[2]_bsz8_seq4096_rank7_act_peak": 2140.76708984375
        },
        "4_1_2_sp": {
            "layernum[4]_bsz8_seq4096_rank0_ms": 2560.56494140625,
            "layernum[4]_bsz8_seq4096_rank0_act": 2662.12646484375,
            "layernum[4]_bsz8_seq4096_rank0_act_peak": 3564.25146484375,
            "layernum[4]_bsz8_seq4096_rank7_ms": 2560.59619140625,
            "layernum[4]_bsz8_seq4096_rank7_act": 3790.42431640625,
            "layernum[4]_bsz8_seq4096_rank7_act_peak": 4404.89990234375
        },
        "4_2_1_sp": {
            "layernum[4]_bsz8_seq4096_rank0_ms": 2816.64306640625,
            "layernum[4]_bsz8_seq4096_rank0_act": 2662.12646484375,
            "layernum[4]_bsz8_seq4096_rank0_act_peak": 3329.22021484375,
            "layernum[4]_bsz8_seq4096_rank7_ms": 2816.67431640625,
            "layernum[4]_bsz8_seq4096_rank7_act": 3790.42431640625,
            "layernum[4]_bsz8_seq4096_rank7_act_peak": 4404.88427734375
        },
        "4_2_1_vtp_sp": {
            "layernum[4]_bsz8_seq4096_rank0_ms": 2816.89306640625,
            "layernum[4]_bsz8_seq4096_rank0_act": 2662.28271484375,
            "layernum[4]_bsz8_seq4096_rank0_act_peak": 3205.50146484375,
            "layernum[4]_bsz8_seq4096_rank7_ms": 2816.95556640625,
            "layernum[4]_bsz8_seq4096_rank7_act": 3790.47119140625,
            "layernum[4]_bsz8_seq4096_rank7_act_peak": 4281.42333984375
        }
    }

def create_memory_sequence_config_sp() -> Dict:
    """Create memory config for sequence profiling mode with sequence parallelism"""
    return {
        "1_1_8_sp": {
            "layernum[1]_bsz8_seq512_rank0_ms": 2582.15185546875,
            "layernum[1]_bsz8_seq512_rank0_act": 300.06396484375,
            "layernum[1]_bsz8_seq512_rank0_act_peak": 2859.501953125,
            "layernum[1]_bsz8_seq512_rank7_ms": 2582.15185546875,
            "layernum[1]_bsz8_seq512_rank7_act": 300.06396484375,
            "layernum[1]_bsz8_seq512_rank7_act_peak": 2859.501953125,
            "layernum[2]_bsz8_seq512_rank0_ms": 3069.03759765625,
            "layernum[2]_bsz8_seq512_rank0_act": 431.26904296875,
            "layernum[2]_bsz8_seq512_rank0_act_peak": 2859.501953125,
            "layernum[2]_bsz8_seq512_rank7_ms": 3069.03759765625,
            "layernum[2]_bsz8_seq512_rank7_act": 431.26904296875,
            "layernum[2]_bsz8_seq512_rank7_act_peak": 2859.501953125,
            "layernum[1]_bsz8_seq1024_rank0_ms": 2582.15576171875,
            "layernum[1]_bsz8_seq1024_rank0_act": 600.1259765625,
            "layernum[1]_bsz8_seq1024_rank0_act_peak": 2859.501953125,
            "layernum[1]_bsz8_seq1024_rank7_ms": 2582.15576171875,
            "layernum[1]_bsz8_seq1024_rank7_act": 600.1259765625,
            "layernum[1]_bsz8_seq1024_rank7_act_peak": 2859.501953125,
            "layernum[2]_bsz8_seq1024_rank0_ms": 3069.04150390625,
            "layernum[2]_bsz8_seq1024_rank0_act": 861.244140625,
            "layernum[2]_bsz8_seq1024_rank0_act_peak": 2920.11865234375,
            "layernum[2]_bsz8_seq1024_rank7_ms": 3069.04150390625,
            "layernum[2]_bsz8_seq1024_rank7_act": 861.244140625,
            "layernum[2]_bsz8_seq1024_rank7_act_peak": 2920.11865234375,
            "layernum[1]_bsz8_seq2048_rank0_ms": 2582.16357421875,
            "layernum[1]_bsz8_seq2048_rank0_act": 1200.5,
            "layernum[1]_bsz8_seq2048_rank0_act_peak": 3084.37158203125,
            "layernum[1]_bsz8_seq2048_rank7_ms": 2582.16357421875,
            "layernum[1]_bsz8_seq2048_rank7_act": 1200.5,
            "layernum[1]_bsz8_seq2048_rank7_act_peak": 3084.37158203125,
            "layernum[2]_bsz8_seq2048_rank0_ms": 3069.04931640625,
            "layernum[2]_bsz8_seq2048_rank0_act": 1722.4853515625,
            "layernum[2]_bsz8_seq2048_rank0_act_peak": 3484.35693359375,
            "layernum[2]_bsz8_seq2048_rank7_ms": 3069.04931640625,
            "layernum[2]_bsz8_seq2048_rank7_act": 1722.4853515625,
            "layernum[2]_bsz8_seq2048_rank7_act_peak": 3484.35693359375,
            "layernum[1]_bsz8_seq4096_rank0_ms": 2582.55078125,
            "layernum[1]_bsz8_seq4096_rank0_act": 2400.498046875,
            "layernum[1]_bsz8_seq4096_rank0_act_peak": 3986.58935546875,
            "layernum[1]_bsz8_seq4096_rank7_ms": 2582.55078125,
            "layernum[1]_bsz8_seq4096_rank7_act": 2400.498046875,
            "layernum[1]_bsz8_seq4096_rank7_act_peak": 3986.58935546875,
            "layernum[2]_bsz8_seq4096_rank0_ms": 3069.06494140625,
            "layernum[2]_bsz8_seq4096_rank0_act": 3444.9677734375,
            "layernum[2]_bsz8_seq4096_rank0_act_peak": 4909.4306640625,
            "layernum[2]_bsz8_seq4096_rank7_ms": 3069.06494140625,
            "layernum[2]_bsz8_seq4096_rank7_act": 3444.9677734375,
            "layernum[2]_bsz8_seq4096_rank7_act_peak": 4909.4306640625,
            "layernum[1]_bsz8_seq8192_rank0_ms": 2582.58203125,
            "layernum[1]_bsz8_seq8192_rank0_act": 4801.9873046875,
            "layernum[1]_bsz8_seq8192_rank0_act_peak": 7576.17236328125,
            "layernum[1]_bsz8_seq8192_rank7_ms": 2582.58203125,
            "layernum[1]_bsz8_seq8192_rank7_act": 4801.9873046875,
            "layernum[1]_bsz8_seq8192_rank7_act_peak": 7576.17236328125,
            "layernum[2]_bsz8_seq8192_rank0_ms": 3069.09619140625,
            "layernum[2]_bsz8_seq8192_rank0_act": 6890.27685546875,
            "layernum[2]_bsz8_seq8192_rank0_act_peak": 9542.83349609375,
            "layernum[2]_bsz8_seq8192_rank7_ms": 3069.09619140625,
            "layernum[2]_bsz8_seq8192_rank7_act": 6890.27685546875,
            "layernum[2]_bsz8_seq8192_rank7_act_peak": 9542.83349609375
        },
        "1_1_8_c_sp": {
            "layernum[1]_bsz8_seq512_rank0_ms": 2582.15185546875,
            "layernum[1]_bsz8_seq512_rank0_act": 173.00439453125,
            "layernum[1]_bsz8_seq512_rank0_act_peak": 2859.501953125,
            "layernum[1]_bsz8_seq512_rank7_ms": 2582.15185546875,
            "layernum[1]_bsz8_seq512_rank7_act": 173.00439453125,
            "layernum[1]_bsz8_seq512_rank7_act_peak": 2859.501953125,
            "layernum[2]_bsz8_seq512_rank0_ms": 3069.03759765625,
            "layernum[2]_bsz8_seq512_rank0_act": 176.50439453125,
            "layernum[2]_bsz8_seq512_rank0_act_peak": 2859.501953125,
            "layernum[2]_bsz8_seq512_rank7_ms": 3069.03759765625,
            "layernum[2]_bsz8_seq512_rank7_act": 176.50439453125,
            "layernum[2]_bsz8_seq512_rank7_act_peak": 2859.501953125,
            "layernum[1]_bsz8_seq1024_rank0_ms": 2582.15576171875,
            "layernum[1]_bsz8_seq1024_rank0_act": 346.0078125,
            "layernum[1]_bsz8_seq1024_rank0_act_peak": 2859.501953125,
            "layernum[1]_bsz8_seq1024_rank7_ms": 2582.15576171875,
            "layernum[1]_bsz8_seq1024_rank7_act": 346.0078125,
            "layernum[1]_bsz8_seq1024_rank7_act_peak": 2859.501953125,
            "layernum[2]_bsz8_seq1024_rank0_ms": 3069.04150390625,
            "layernum[2]_bsz8_seq1024_rank0_act": 353.0078125,
            "layernum[2]_bsz8_seq1024_rank0_act_peak": 2859.501953125,
            "layernum[2]_bsz8_seq1024_rank7_ms": 3069.04150390625,
            "layernum[2]_bsz8_seq1024_rank7_act": 353.0078125,
            "layernum[2]_bsz8_seq1024_rank7_act_peak": 2859.501953125,
            "layernum[1]_bsz8_seq2048_rank0_ms": 2582.16357421875,
            "layernum[1]_bsz8_seq2048_rank0_act": 692.0146484375,
            "layernum[1]_bsz8_seq2048_rank0_act_peak": 2859.501953125,
            "layernum[1]_bsz8_seq2048_rank7_ms": 2582.16357421875,
            "layernum[1]_bsz8_seq2048_rank7_act": 692.0146484375,
            "layernum[1]_bsz8_seq2048_rank7_act_peak": 2859.501953125,
            "layernum[2]_bsz8_seq2048_rank0_ms": 3069.04931640625,
            "layernum[2]_bsz8_seq2048_rank0_act": 706.0146484375,
            "layernum[2]_bsz8_seq2048_rank0_act_peak": 2859.501953125,
            "layernum[2]_bsz8_seq2048_rank7_ms": 3069.04931640625,
            "layernum[2]_bsz8_seq2048_rank7_act": 706.0146484375,
            "layernum[2]_bsz8_seq2048_rank7_act_peak": 2859.501953125,
            "layernum[1]_bsz8_seq4096_rank0_ms": 2582.55078125,
            "layernum[1]_bsz8_seq4096_rank0_act": 1384.0283203125,
            "layernum[1]_bsz8_seq4096_rank0_act_peak": 2970.11962890625,
            "layernum[1]_bsz8_seq4096_rank7_ms": 2582.17919921875,
            "layernum[1]_bsz8_seq4096_rank7_act": 1384.0283203125,
            "layernum[1]_bsz8_seq4096_rank7_act_peak": 2970.4912109375,
            "layernum[2]_bsz8_seq4096_rank0_ms": 3069.06494140625,
            "layernum[2]_bsz8_seq4096_rank0_act": 1412.0283203125,
            "layernum[2]_bsz8_seq4096_rank0_act_peak": 2876.4912109375,
            "layernum[2]_bsz8_seq4096_rank7_ms": 3069.06494140625,
            "layernum[2]_bsz8_seq4096_rank7_act": 1412.0283203125,
            "layernum[2]_bsz8_seq4096_rank7_act_peak": 2876.4912109375,
            "layernum[1]_bsz8_seq8192_rank0_ms": 2582.21044921875,
            "layernum[1]_bsz8_seq8192_rank0_act": 2768.0556640625,
            "layernum[1]_bsz8_seq8192_rank0_act_peak": 5542.6123046875,
            "layernum[1]_bsz8_seq8192_rank7_ms": 2582.58203125,
            "layernum[1]_bsz8_seq8192_rank7_act": 2768.0556640625,
            "layernum[1]_bsz8_seq8192_rank7_act_peak": 5542.24072265625,
            "layernum[2]_bsz8_seq8192_rank0_ms": 3069.09619140625,
            "layernum[2]_bsz8_seq8192_rank0_act": 2824.0556640625,
            "layernum[2]_bsz8_seq8192_rank0_act_peak": 5476.6123046875,
            "layernum[2]_bsz8_seq8192_rank7_ms": 3069.09619140625,
            "layernum[2]_bsz8_seq8192_rank7_act": 2824.0556640625,
            "layernum[2]_bsz8_seq8192_rank7_act_peak": 5476.6123046875
        },
        "2_1_4_sp": {
            "layernum[2]_bsz8_seq512_rank0_ms": 3069.53759765625,
            "layernum[2]_bsz8_seq512_rank0_act": 274.61083984375,
            "layernum[2]_bsz8_seq512_rank0_act_peak": 2613.50048828125,
            "layernum[2]_bsz8_seq512_rank7_ms": 3070.04443359375,
            "layernum[2]_bsz8_seq512_rank7_act": 614.62646484375,
            "layernum[2]_bsz8_seq512_rank7_act_peak": 2673.12744140625,
            "layernum[2]_bsz8_seq1024_rank0_ms": 3070.55322265625,
            "layernum[2]_bsz8_seq1024_rank0_act": 549.22021484375,
            "layernum[2]_bsz8_seq1024_rank0_act_peak": 2627.50048828125,
            "layernum[2]_bsz8_seq1024_rank7_ms": 3070.06005859375,
            "layernum[2]_bsz8_seq1024_rank7_act": 1227.25048828125,
            "layernum[2]_bsz8_seq1024_rank7_act_peak": 2989.74853515625,
            "layernum[2]_bsz8_seq2048_rank0_ms": 3069.58447265625,
            "layernum[2]_bsz8_seq2048_rank0_act": 1098.43896484375,
            "layernum[2]_bsz8_seq2048_rank0_act_peak": 2655.50048828125,
            "layernum[2]_bsz8_seq2048_rank7_ms": 3070.09130859375,
            "layernum[2]_bsz8_seq2048_rank7_act": 2454.49853515625,
            "layernum[2]_bsz8_seq2048_rank7_act_peak": 3918.619140625,
            "layernum[2]_bsz8_seq4096_rank0_ms": 3069.64697265625,
            "layernum[2]_bsz8_seq4096_rank0_act": 2196.87646484375,
            "layernum[2]_bsz8_seq4096_rank0_act_peak": 3736.95263671875,
            "layernum[2]_bsz8_seq4096_rank7_ms": 3070.15380859375,
            "layernum[2]_bsz8_seq4096_rank7_act": 4908.99462890625,
            "layernum[2]_bsz8_seq4096_rank7_act_peak": 7561.240234375,
            "layernum[2]_bsz8_seq8192_rank0_ms": 3069.77197265625,
            "layernum[2]_bsz8_seq8192_rank0_act": 4394.49462890625,
            "layernum[2]_bsz8_seq8192_rank0_act_peak": 6582.63330078125,
            "layernum[2]_bsz8_seq8192_rank7_ms": 3070.27880859375,
            "layernum[2]_bsz8_seq8192_rank7_act": 9817.98681640625,
            "layernum[2]_bsz8_seq8192_rank7_act_peak": 14846.482421875
        },
        "4_1_2_sp": {
            "layernum[4]_bsz8_seq512_rank0_ms": 6122.33837890625,
            "layernum[4]_bsz8_seq512_rank0_act": 548.72021484375,
            "layernum[4]_bsz8_seq512_rank0_act_peak": 2108.00048828125,
            "layernum[4]_bsz8_seq512_rank7_ms": 6123.33837890625,
            "layernum[4]_bsz8_seq512_rank7_act": 1226.75048828125,
            "layernum[4]_bsz8_seq512_rank7_act_peak": 2226.2314453125,
            "layernum[4]_bsz8_seq1024_rank0_ms": 6122.86962890625,
            "layernum[4]_bsz8_seq1024_rank0_act": 1097.43896484375,
            "layernum[4]_bsz8_seq1024_rank0_act_peak": 2135.50048828125,
            "layernum[4]_bsz8_seq1024_rank7_ms": 6122.39697265625,
            "layernum[4]_bsz8_seq1024_rank7_act": 2453.49853515625,
            "layernum[4]_bsz8_seq1024_rank7_act_peak": 3155.10205078125,
            "layernum[4]_bsz8_seq2048_rank0_ms": 6122.43212890625,
            "layernum[4]_bsz8_seq2048_rank0_act": 2194.87646484375,
            "layernum[4]_bsz8_seq2048_rank0_act_peak": 2972.43896484375,
            "layernum[4]_bsz8_seq2048_rank7_ms": 6122.45947265625,
            "layernum[4]_bsz8_seq2048_rank7_act": 4906.99462890625,
            "layernum[4]_bsz8_seq2048_rank7_act_peak": 6796.72314453125,
            "layernum[4]_bsz8_seq4096_rank0_ms": 6122.55712890625,
            "layernum[4]_bsz8_seq4096_rank0_act": 4389.75146484375,
            "layernum[4]_bsz8_seq4096_rank0_act_peak": 5815.87646484375,
            "layernum[4]_bsz8_seq4096_rank7_ms": 6122.58447265625,
            "layernum[4]_bsz8_seq4096_rank7_act": 9813.98681640625,
            "layernum[4]_bsz8_seq4096_rank7_act_peak": 14079.96533203125,
            "layernum[4]_bsz8_seq8192_rank0_ms": 6121.80712890625,
            "layernum[4]_bsz8_seq8192_rank0_act": 8780.00146484375,
            "layernum[4]_bsz8_seq8192_rank0_act_peak": 11501.75146484375,
            "layernum[4]_bsz8_seq8192_rank7_ms": 6121.83447265625,
            "layernum[4]_bsz8_seq8192_rank7_act": 19628.47119140625,
            "layernum[4]_bsz8_seq8192_rank7_act_peak": 28646.94970703125
        }
    }

def save_profiler_configs(profiler_model_configs_dir: Path, type: str = "computation", mode: str = "static", sp_mode: bool = False, mixed_precision:str = "bf16", model_name:str = "test"):
    """Save profiler configs to files"""
    # Computation config
    comp_funcs = {
        "static": create_computation_static_config,
        "batch": create_computation_batch_config,
        "sequence": create_computation_sequence_config
    }
    memory_funcs = {
        ("static", False): create_memory_static_config,
        ("static", True): create_memory_static_config_sp,
        ("sequence", True): create_memory_sequence_config_sp
    }
    if type == "computation":
        comp_config = comp_funcs[mode]()
        with open(f"{profiler_model_configs_dir}/computation_profiling_{mixed_precision}_{model_name}.json", "w") as f:
            json.dump(comp_config, f, indent=4)
    else:
        mem_config = memory_funcs[(mode, sp_mode)]()
        with open(f"{profiler_model_configs_dir}/memory_profiling_{mixed_precision}_{model_name}.json", "w") as f:
            json.dump(mem_config, f, indent=4)
