from _typeshed import Incomplete
from pyvqnet.nn import Module as Module, Parameter as Parameter
from pyvqnet.tensor import tensor as tensor

def pyvnqet_l2normalize(v, eps: float = 1e-12): ...

class Spectral_Norm(Module):
    '''
    Applies spectral normalization to a parameter in the given module.
    Spectral normalization stabilizes the training of discriminators (critics) in GAN by
    rescaling the weight tensor with spectral norm \\sigmaσ of the weight matrix calculated
    using power iteration method.
    If the dimension of the weight tensor is greater than 2,
    it is reshaped to 2D in power iteration method to get spectral norm.

    :param module: containing module.
    :param name: name of weight parameter, default "weights".
    :param power_iterations: number of power iterations to calculate spectral norm,default 1.
    :return: The original module with the spectral norm hook

    '''
    module: Incomplete
    power_iterations: Incomplete
    def __init__(self, module, name: str = 'weights', power_iterations: int = 1) -> None: ...
    def forward(self, *args): ...
