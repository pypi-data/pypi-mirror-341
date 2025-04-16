from .module import Module as Module
from .parameter import Parameter as Parameter
from .xtensor import XTensor as XTensor, ones as ones, zeros as zeros
from _typeshed import Incomplete

class BatchNorm(Module):
    '''Applies Batch Normalization over a 4D input (B,C,H,W) or (B,C,H) or (B,C) as described in the paper
    `Batch Normalization: Accelerating Deep Network Training by Reducing
    Internal Covariate Shift <https://arxiv.org/abs/1502.03167>`__ .

    .. math::

        y = \\frac{x - \\mathrm{E}[x]}{\\sqrt{\\mathrm{Var}[x] + \\epsilon}} * \\gamma + \\beta

    where :math:`\\gamma` and :math:`\\beta` are learnable parameters.
    Also by default, during training this layer keeps running
    estimates of its computed mean and variance,
    which are then used for normalization during evaluation.
    The running estimates are kept with a default momentum of 0.1.

    :param channel_num: `int` - the number of input features channels
    :param momentum: `float` - momentum when calculation exponentially weighted average,
     defaults to 0.1
    :param beta_initializer: `callable` - defaults to zeros
    :param gamma_initializer: `callable` - defaults to ones
    :param epsilon: `float` - numerical stability constant, defaults to 1e-5
    :param dtype: data type of parameters,default: None,use default data type.
    :param name: name of module,default:"".
    :return: a BatchNorm2d class


    '''
    backend: Incomplete
    momentum: Incomplete
    beta: Incomplete
    gamma: Incomplete
    epsilon: Incomplete
    def __init__(self, channel_num: int, momentum: float = 0.1, epsilon: float = 1e-05, beta_initializer=..., gamma_initializer=..., dtype: int | None = None, name: str = '') -> None: ...
    def forward(self, x, *args, **kwargs): ...
BatchNorm1d = BatchNorm
BatchNorm2d = BatchNorm
