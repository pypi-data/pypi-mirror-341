from .convert import *
from ..tensor import OPNodesInfo as OPNodesInfo, get_global_onnx_convert_config as get_global_onnx_convert_config, get_global_onnx_node_id as get_global_onnx_node_id, init_global_onnx_init_dict as init_global_onnx_init_dict, init_global_onnx_node_id as init_global_onnx_node_id, recursive_tuple_to_list as recursive_tuple_to_list, reset_global_onnx_init_dict as reset_global_onnx_init_dict, reset_global_onnx_node_id as reset_global_onnx_node_id, set_global_onnx_convert_config_value as set_global_onnx_convert_config_value, set_global_onnx_init_dict as set_global_onnx_init_dict
from ..tensor.op_nodes_info import get_opinfo as get_opinfo
from _typeshed import Incomplete
from pyvqnet.dtype import kbool as kbool, kcomplex128 as kcomplex128, kcomplex64 as kcomplex64, kfloat32 as kfloat32, kfloat64 as kfloat64, kint16 as kint16, kint32 as kint32, kint64 as kint64, kint8 as kint8, kuint8 as kuint8
from pyvqnet.tensor import QTensor as QTensor

dtype_map_onnx: Incomplete

def find_input_output(operator_dict): ...
def export(operator_dict, param_name_init_list): ...
def get_tensorproto_dtype(dtype_int): ...
def helper_function_convert1d_tensor(opname, value): ...
def helper_function_convert_layer_norm_2d(op, value): ...
def export_model(model, x: QTensor, *args, **kwargs):
    """
    convert vqnet model to onnx model.

    :param model: vqnet model
    :param x: a input QTensor with correct shape to feed into model.

    :return: a onnx model
    """
