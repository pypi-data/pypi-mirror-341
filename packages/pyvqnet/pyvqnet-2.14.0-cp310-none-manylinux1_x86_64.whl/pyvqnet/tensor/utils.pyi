if_show_bp_info: bool
if_grad_enabled: int

def get_if_grad_enabled():
    """
    get if_grad_enabled
    """
def set_if_grad_enabled(flag) -> None:
    """
    set flag of if_show_bp_info
    """

class no_grad:
    prev: bool
    def __init__(self) -> None: ...
    def __enter__(self) -> None: ...
    def __exit__(self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: types.TracebackType | None) -> None: ...

def get_if_show_bp_info():
    """
    get flag of if_show_bp_info
    """
def set_if_show_bp_info(flag) -> None:
    """
    set flag of if_show_bp_info
    """
def init_if_show_bp() -> None:
    """
    init flag of if_show_bp_info to False
    """
def is_opt_einsum_available() -> bool:
    """Return a bool indicating if opt_einsum is currently available."""
