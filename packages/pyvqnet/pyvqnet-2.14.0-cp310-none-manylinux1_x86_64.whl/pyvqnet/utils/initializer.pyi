from ..tensor import QTensor as QTensor
from _typeshed import Incomplete
from pyvqnet.dtype import get_default_dtype as get_default_dtype

def set_random_seed(seed) -> None:
    """
    Set global random seed for VQNet CPU/GPU backend.

    :param seed: integer random number seed.
    """
def get_random_seed():
    """
    Get global random seed for VQNet CPU/GPU backend.
    """
def normal_(tensor: QTensor, mean: float = 0.0, std: float = 1.0) -> QTensor:
    """Fill the input Tensor with values drawn from the normal distribution.

    :math:`\\mathcal{N}(\\text{mean}, \\text{std}^2)`.

    :param tensor: an n-dimensional QTensor
    :param mean: the mean of the normal distribution
    :param std: the standard deviation of the normal distribution


    """
def constant_(tensor: QTensor, val: float) -> QTensor:
    """Fill the input Tensor with the value :math:`\\text{val}`.

    :param tensor: an n-dimensional QTensor
    :param val: the value to fill the tensor with

    Examples:
        >>> w = torch.empty(3, 5)
        >>> nn.init.constant_(w, 0.3)
    """
def xavier_uniform_(tensor: QTensor, gain: float = 1.0) -> QTensor:
    """Fill the input `Tensor` with values using a Xavier uniform distribution.

    The method is described in `Understanding the difficulty of training
    deep feedforward neural networks` - Glorot, X. & Bengio, Y. (2010).
    The resulting tensor will have values sampled from
    :math:`\\mathcal{U}(-a, a)` where

    .. math::
        a = \\text{gain} \\times \\sqrt{\\frac{6}{\\text{fan\\_in} + \\text{fan\\_out}}}

    Also known as Glorot initialization.

    """
def calculate_gain(nonlinearity, param: Incomplete | None = None):
    """Return the recommended gain value for the given nonlinearity function.

    :param nonlinearity: the non-linear function
    :param param: optional parameter for the non-linear function

    """
def normal(shape):
    """
    Normal distribution initializer

    :param shape: shape

    """
def quantum_uniform(shape):
    """
    Uniform distribution initializer for parameters in quantum circuits with range from [0,2* np.pi]

    :param shape: shape of input tensor

    """
def uniform(shape):
    """
    Uniform distribution initializer

    :param shape: 'tuple' - shape of input tensor

    """
def xavier_normal_(t, gain: int = 1) -> None:
    """
    Xavier normal distribution initializer of input.

    :param t: input tensor
    :param gain: an optional scaling factor

    """
def xavier_normal(shape, gain: int = 1):
    """
    Xavier normal distribution initializer

    :param shape: shape of input tensor
    :param gain: an optional scaling factor

    """
def xavier_uniform(shape, gain: int = 1):
    """
    Xavier uniform distribution initializer

    :param shape: shape of input tensor
    :param gain: an optional scaling factor

    """
def he_normal_(t: QTensor, a: int = 0, mode: str = 'fan_in', nonlinearity: str = 'leaky_relu'):
    """
    He normal distribution initializer of input.

    :param t: input tensor
    :param a: the negative slope of the rectifier used after this layer (only
            used with ``'leaky_relu'``)
    :param mode: either ``'fan_in'`` (default) or ``'fan_out'``. Choosing ``'fan_in'``
            preserves the magnitude of the variance of the weights in the
            forward pass. Choosing ``'fan_out'`` preserves the magnitudes in the
            backwards pass.
    :param nonlinearity: the non-linear function,
        recommended to use only with ``'relu'`` or ``'leaky_relu'`` (default).

    """
def he_normal(shape, a: int = 0, mode: str = 'fan_in', nonlinearity: str = 'leaky_relu'):
    """
    He normal distribution initializer

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
def he_uniform_for_linear(shape, a=..., mode: str = 'fan_in', nonlinearity: str = 'leaky_relu'):
    """
    He uniform initializer for vqnet linear

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
def he_uniform(shape, a=..., mode: str = 'fan_in', nonlinearity: str = 'leaky_relu'):
    """
    He uniform distribution initializer

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
def he_uniform_(input, a=..., mode: str = 'fan_in', nonlinearity: str = 'leaky_relu') -> None:
    """
    He uniform distribution initializer with input tensor.

    :param input: input tensor
    :param a: 'str' - the negative slope of the rectifier used after this layer (only
            used with ``'leaky_relu'``)
    :param mode: either ``'fan_in'`` (default) or ``'fan_out'``. Choosing ``'fan_in'``
            preserves the magnitude of the variance of the weights in the
            forward pass. Choosing ``'fan_out'`` preserves the magnitudes in the
            backwards pass.
    :param nonlinearity: the non-linear function,
        recommended to use only with ``'relu'`` or ``'leaky_relu'`` (default).

    """
def zeros_(input) -> None:
    """
    All zeros initializer of input.

    :param input: input tensor

    """
def zeros(shape):
    """
    All zeros initializer.

    :param shape: shape of input tensor

    """
def ones_(input) -> None:
    """
    All ones initializer of input.

    :param input: input tensor

    """
def ones(shape):
    """
    All one initializer.

    :param shape: shape of input tensor

    """
