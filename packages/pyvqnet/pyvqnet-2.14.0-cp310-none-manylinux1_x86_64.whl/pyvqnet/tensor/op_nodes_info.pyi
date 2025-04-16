from _typeshed import Incomplete
from collections.abc import Generator

def set_global_onnx_convert_config_value(key, value) -> None: ...
def get_global_onnx_convert_config(key): ...

class OPNodesInfo:
    opid: Incomplete
    opname: Incomplete
    op_input_id_lists: Incomplete
    op_input_shape_lists: Incomplete
    op_output_id_lists: Incomplete
    op_output_shape_list: Incomplete
    op_attribute: Incomplete
    op_para_buffer_id_lists: Incomplete
    op_para_buffer_shape_lists: Incomplete
    op_input_dtype_lists: Incomplete
    op_output_dtype_lists: Incomplete
    def __init__(self, opid, opname, op_input_id_lists, op_input_shape_lists, op_output_id_list, op_output_shape_list, op_attribute, op_para_buffer_id_lists, op_para_buffer_shape_lists, op_input_dtype_lists: Incomplete | None = None, op_output_dtype_lists: Incomplete | None = None) -> None: ...

def get_prev_onnx(q): ...
def toposort_onnx(end_node, parents=...) -> Generator[Incomplete]:
    """
    toposort for bp
    """
def get_opinfo(end_node): ...
def summary(model, x, *args, **kwargs): ...
def get_global_onnx_node_id(): ...
def init_global_onnx_node_id() -> None:
    """
    set node idx to zero
    """
def reset_global_onnx_node_id() -> None: ...
def reset_global_onnx_init_dict() -> None: ...
def init_global_onnx_init_dict() -> None: ...
def set_global_onnx_init_dict(key, value): ...
def recursive_tuple_to_list(input_tuple, global_list) -> None: ...

onnx_init_dict: Incomplete
node_idx: int
