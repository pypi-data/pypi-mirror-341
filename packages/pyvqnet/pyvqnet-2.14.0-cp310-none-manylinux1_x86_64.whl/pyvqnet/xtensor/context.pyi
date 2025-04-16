from ..device import DEV_CPU as DEV_CPU, DEV_CPU_PIN as DEV_CPU_PIN, DEV_GPU_0 as DEV_GPU_0, DEV_GPU_1 as DEV_GPU_1, DEV_GPU_2 as DEV_GPU_2, DEV_GPU_3 as DEV_GPU_3, DEV_GPU_4 as DEV_GPU_4, DEV_GPU_5 as DEV_GPU_5, DEV_GPU_6 as DEV_GPU_6, DEV_GPU_7 as DEV_GPU_7, if_gpu_compiled as if_gpu_compiled
from .base import XTensorClassPropertyMetaClass as XTensorClassPropertyMetaClass, classproperty as classproperty, with_metaclass as with_metaclass
from _typeshed import Incomplete

class Context(Incomplete):
    """Constructs a context.

    XTensor can run operations on CPU or different GPUs.
    A context describes the device type and ID on which computation should be carried on.


    """
    devtype2str: Incomplete
    devstr2type: Incomplete
    device_typeid: Incomplete
    device_id: Incomplete
    def __init__(self, device_type, device_id: int = 0) -> None:
        """
        :param device_type: device type, 1: 'cpu', 2: 'gpu'.
        :param device_id: device id, default:0, use cpu or gpu(0).
        """
    @property
    def device_type(self):
        """Returns the device type of current context.

        """
    def __hash__(self):
        """Compute hash value of context for dictionary lookup"""
    def __eq__(self, other):
        """Compares two contexts. Two contexts are equal if they
        have the same device type and device id.
        """
    def __enter__(self): ...
    def __exit__(self, ptype: type[BaseException] | None, value: BaseException | None, trace: types.TracebackType | None) -> None: ...
    def empty_cache(self) -> None:
        """Empties the memory cache for the current contexts device.

        XTensor utilizes a memory pool to avoid excessive allocations.
        Calling empty_cache will empty the memory pool of the contexts
        device. This will only free the memory of the unreferenced data.

        """

def current_context():
    """Returns the current context.

    """
def cpu(device_id: int = 0):
    """Returns a CPU context.

    This function is a short cut for ``Context('cpu', device_id)``.
    For most operations, when no context is specified, the default context is `cpu()`.

    :param device_id: device_id ,default =0 .

    """
def cpu_pinned(device_id: int = 0):
    """Returns a CPU pinned memory context. Copying from CPU pinned memory to GPU
    is faster than from normal CPU memory.

    This function is a short cut for ``Context('cpu_pinned', device_id)``.

    :param device_id: device_id ,default =0 .
    """
def gpu(device_id: int = 0):
    """Returns a GPU context.

    This function is a short cut for Context('gpu', device_id).
    The K GPUs on a node are typically numbered as 0,...,K-1.

    :param device_id: device_id ,default =0 .
    """
def create_context_from_str(ctx_input): ...
def prepare_ctx_arg_str(ctx_input): ...
def parse_context(ctx: Context): ...
def create_context(vqnet_device): ...
