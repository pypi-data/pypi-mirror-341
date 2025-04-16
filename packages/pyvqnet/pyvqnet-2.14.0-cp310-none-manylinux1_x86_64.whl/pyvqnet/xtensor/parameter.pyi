from .xtensor import XTensor as XTensor
from _typeshed import Incomplete
from pyvqnet.dtype import get_default_dtype as get_default_dtype, get_xtensor_default_dtype as get_xtensor_default_dtype, get_xtensor_dtype as get_xtensor_dtype, kcomplex128 as kcomplex128, kcomplex64 as kcomplex64, kfloat32 as kfloat32, kfloat64 as kfloat64, valid_param_dtype as valid_param_dtype

def calculate_gain(nonlinearity, param: Incomplete | None = None):
    """Return the recommended gain value for the given nonlinearity function.

    :param nonlinearity: the non-linear function
    :param param: optional parameter for the non-linear function

    """
def normal(shape, dtype):
    """
    Normal initializer

    :param shape: shape

    """
def quantum_uniform(shape, dtype):
    """
    Quantum Uniform initializer with range from [0,2* np.pi]

    :param shape: shape of input tensor

    """
def uniform(shape, dtype):
    """
    Uniform initializer

    :param shape: 'tuple' - shape of input tensor

    """
def xavier_normal(shape, dtype, gain: int = 1):
    """
    Xavier normal initializer

    :param shape: shape of input tensor
    :param gain: an optional scaling factor

    """
def xavier_uniform(shape, dtype, gain: int = 1):
    """
    Xavier uniform initializer

    :param shape: shape of input tensor
    :param gain: an optional scaling factor

    """
def he_normal(shape, dtype, a: int = 0, mode: str = 'fan_in', nonlinearity: str = 'leaky_relu'):
    """
    He normal initializer

    :param shape: shape of input tensor
    :param a: the negative slope of the rectifier used after this layer (only
            used with ``'leaky_relu'``)
    :param mode: either ``'fan_in'`` (default) or ``'fan_out'``. Choosing ``'fan_in'``
            preserves the magnitude of the variance of the weights in the
            forward pass. Choosing ``'fan_out'`` preserves the magnitudes in the
            backwards pass.
    :param nonlinearity: the non-linear function,
        recommended to use only with ``'relu'`` or ``'leaky_relu'`` (default).

    """
def he_uniform(shape, dtype, a=..., mode: str = 'fan_in', nonlinearity: str = 'leaky_relu'):
    """
    He uniform initializer

    :param shape: 'tuple' - shape of input tensor
    :param a: 'str' - the negative slope of the rectifier used after this layer (only
            used with ``'leaky_relu'``)
    :param mode: either ``'fan_in'`` (default) or ``'fan_out'``. Choosing ``'fan_in'``
            preserves the magnitude of the variance of the weights in the
            forward pass. Choosing ``'fan_out'`` preserves the magnitudes in the
            backwards pass.
    :param nonlinearity: the non-linear function,
        recommended to use only with ``'relu'`` or ``'leaky_relu'`` (default).

    """
def zeros(shape, dtype):
    """
    Zeros initializer.

    :param shape: shape of input tensor

    """
def ones(shape, dtype):
    """
    Ones initializer.

    :param shape: shape of input tensor

    """

class Parameter(XTensor):
    def __init__(self, shape=(1, 1), initializer=..., device: Incomplete | None = None, dtype: int | None = None) -> None:
        """
        Represents one parameter in a neural network


        :param shape: `tuple` - shape of the parameter
        :param initializer: 'callable' - parameter initializer, default to normal
        :param device: run on device, default: None,use cpu. if use GPU,set DEV_GPU_0.
        :param dtype: data type of parameters,default: None,use default data type.
        """
    def init_from_tensor(self, other_tensor) -> None: ...
    def zero_grad(self) -> None:
        """
        Sets gradient to zero. Will be used by optimizer in the optimization process.

        :return: None

        """
