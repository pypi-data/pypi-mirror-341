#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <iostream>
#include <vector>
#include <limits>
#include<algorithm>

namespace py = pybind11;

template <typename ForwardIterator>
inline size_t argmin(const ForwardIterator begin, const ForwardIterator end)
{
    return std::distance(begin, std::min_element(begin, end));
}

template <typename ForwardIterator>
inline size_t argmax(const ForwardIterator begin, const ForwardIterator end) 
{
    return std::distance(begin, std::max_element(begin, end));
}

std::pair<double, int> dynamic_programming_core(int layer_num,
                                                int max_mem,
                                                int strategy_num,
                                                py::array_t<int> v_data,
                                                py::array_t<int> _mark,
                                                py::array_t<double> _f,
                                                py::array_t<double> inter_cost,
                                                py::array_t<double> intra_cost,
                                                py::array_t<int> res_list) {

    py::buffer_info v_data_info = v_data.request();
    int* v_data_ptr = static_cast<int*>(v_data_info.ptr);

    py::buffer_info _mark_info = _mark.request();
    int* _mark_ptr = static_cast<int*>(_mark_info.ptr);

    py::buffer_info _f_info = _f.request();
    double* _f_ptr = static_cast<double*>(_f_info.ptr);

    py::buffer_info inter_cost_info = inter_cost.request();
    double* inter_cost_ptr = static_cast<double*>(inter_cost_info.ptr);

    py::buffer_info intra_cost_info = intra_cost.request();
    double* intra_cost_ptr = static_cast<double*>(intra_cost_info.ptr);

    py::buffer_info res_list_info = res_list.request();
    int* res_list_ptr = static_cast<int*>(res_list_info.ptr);

    for (int i = 0; i < layer_num; ++i) {
        for (int v = max_mem - 1; v >= 0; --v) {
            for (int s = 0; s < strategy_num; ++s) {
                if (v < v_data_ptr[i * strategy_num + s]) {
                    _mark_ptr[i * max_mem * strategy_num + v * strategy_num + s] = -1;
                    _f_ptr[v * strategy_num + s] = std::numeric_limits<double>::infinity();
                    continue;
                }
                std::vector<double> candidates(strategy_num);
                for (int si = 0; si < strategy_num; ++si) {
                    candidates[si] = _f_ptr[(v - v_data_ptr[i * strategy_num + s]) * strategy_num + si] + inter_cost_ptr[i * strategy_num * strategy_num + si * strategy_num + s] + intra_cost_ptr[i * strategy_num + s];
                }

                int min_index = argmin(candidates.begin(), candidates.end());

                _mark_ptr[i * max_mem * strategy_num + v * strategy_num + s] = min_index;
                _f_ptr[v * strategy_num + s] = candidates[min_index];
            }
        }
    }

    double* ptr = _f_ptr + (max_mem - 1) * strategy_num;
    int next_index = argmin(ptr , ptr + strategy_num), next_v = max_mem - 1;
    double total_cost = ptr[next_index];

    if (!(total_cost < std::numeric_limits<double>::infinity())) {
        return {std::numeric_limits<double>::infinity(), -1};
    }

    res_list_ptr[layer_num - 1] = next_index;
    int cur_index;

    for (int i = layer_num - 1; i > 0; --i) {
        cur_index = next_index;
        next_index = _mark_ptr[i * max_mem * strategy_num + next_v * strategy_num + next_index];
        next_v -= v_data_ptr[i * strategy_num + cur_index];
        res_list_ptr[i - 1] = next_index;
    }

    return {total_cost, next_v - v_data_ptr[0 * strategy_num + next_index]};
}

PYBIND11_MODULE(galvatron_dp_core, m) {
    m.def("dynamic_programming_core", &dynamic_programming_core, "A dynamic programming function");
}
