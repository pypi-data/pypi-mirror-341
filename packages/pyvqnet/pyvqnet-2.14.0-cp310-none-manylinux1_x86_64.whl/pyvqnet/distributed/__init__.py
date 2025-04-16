"""
Init for distributrd
"""
import platform

if "linux" in platform.platform() or "Linux" in platform.platform():
    from .datasplit import *
    from .ControllComm import *
    from .runner import *
    from .tensor_parallel import *
    from .zero import *