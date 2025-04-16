"""
inti for tensor
"""
# pylint: disable=redefined-builtin
from .tensor import *
from .tensor import _tensordot
from .op_nodes_info import OPNodesInfo,set_global_onnx_convert_config_value,get_global_onnx_convert_config,\
    get_global_onnx_node_id,reset_global_onnx_node_id,init_global_onnx_node_id,\
    reset_global_onnx_init_dict,set_global_onnx_init_dict,init_global_onnx_init_dict,\
    recursive_tuple_to_list,get_opinfo

from .utils import no_grad