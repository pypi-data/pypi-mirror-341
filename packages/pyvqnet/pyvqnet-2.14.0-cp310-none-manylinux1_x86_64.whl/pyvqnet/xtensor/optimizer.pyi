import abc
from .autograd import not_record as not_record
from .xtensor import XTensor as XTensor, abs as abs, maximum as maximum, sqrt as sqrt, square as square, zeros as zeros
from _typeshed import Incomplete

class Optimizer(metaclass=abc.ABCMeta):
    """
    Base class for all optimizers.

    :param params: params of model which need to be optimized
    :param lr: learning_rate of model (default: 0.01)
    """
    params: Incomplete
    lr: Incomplete
    wd: int
    states: Incomplete
    states_synced: Incomplete
    t: int
    begin_num_update: int
    num_update: int
    def __init__(self, params, lr: float = 0.01) -> None: ...
    def step(self) -> None: ...
    def zero_grad(self) -> None: ...
    def sync_state_context(self, state, context):
        """sync state context."""
    def general_step(self, step_func) -> None: ...

class Adadelta(Optimizer):
    """
    Adadelta: An Adaptive Learning Rate Method (https://arxiv.org/abs/1212.5701)

    :param params: params of model which need to be optimized
    :param lr: learning_rate of model (default: 0.01)
    :param beta: for computing a running average of squared gradients (default: 0.99)
    :param epsilon: term added to the denominator to improve numerical stability (default: 1e-8)
    :return: a Adadelta optimizer

    """
    epsilon: Incomplete
    beta: Incomplete
    def __init__(self, params, lr: float = 0.01, beta: float = 0.99, epsilon: float = 1e-08) -> None: ...
    def create_state(self, index, weight): ...

class SGD(Optimizer):
    """
    Stochastic gradient descent Optimizer.
    https://en.wikipedia.org/wiki/Stochastic_gradient_descent


    :param params: params of model which need to be optimized
    :param lr: learning_rate of model (default: 0.01)
    :param momentum: momentum factor (default: 0)
    :param nesterov: enables Nesterov momentum (default: False)
    :return: a SGD optimizer

    """
    momentum: Incomplete
    nesterov: Incomplete
    def __init__(self, params, lr: float = 0.01, momentum: int = 0, nesterov: bool = False) -> None: ...
    def create_state(self, index, weight): ...

class RMSProp(Optimizer):
    """
    RMSProp Optimizer.

    https://towardsdatascience.com/understanding-rmsprop-faster-neural-network-learning-62e116fcf29a?gi=94196933b149


    :param params: params of model which need to be optimized
    :param lr: learning_rate of model (default: 0.01)
    :param beta: coefficients used for computing running averages of gradient and
     its square (default: 0.99)
    :param epsilon: term added to the denominator to improve numerical stability (default: 1e-8)
    :return: a RMSProp optimizer


    """
    t: int
    epsilon: Incomplete
    beta: Incomplete
    def __init__(self, params, lr: float = 0.01, beta: float = 0.99, epsilon: float = 1e-08) -> None: ...
    def create_state(self, index, weight): ...

class Adagrad(Optimizer):
    """
    Adagrad Optimizer.
    https://databricks.com/glossary/adagrad


    :param params: params of model which need to be optimized
    :param lr: learning_rate of model (default: 0.01)
    :param epsilon: term added to the denominator to improve numerical stability (default: 1e-8)
    :return: a Adagrad optimizer

    """
    epsilon: Incomplete
    t: int
    def __init__(self, params, lr: float = 0.01, epsilon: float = 1e-08) -> None: ...
    def create_state(self, index, weight): ...

class Adam(Optimizer):
    """
    Adam: A Method for Stochastic Optimization (https://arxiv.org/abs/1412.6980)

    :param params: params of model which need to be optimized
    :param lr: learning_rate of model (default: 0.01)
    :param beta1: coefficients used for computing running averages of gradient and
     its square (default: 0.9)
    :param beta2: coefficients used for computing running averages of gradient and
     its square (default: 0.999)
    :param epsilon: term added to the denominator to improve numerical stability (default: 1e-8)
    :param amsgrad: whether to use the AMSGrad variant of this algorithm from
     the paper `On the Convergence of Adam and Beyond`_(default: False)
    :return: a Adam optimizer


    """
    beta1: Incomplete
    beta2: Incomplete
    epsilon: Incomplete
    t: int
    amsgrad: Incomplete
    def __init__(self, params, lr: float = 0.01, beta1: float = 0.9, beta2: float = 0.999, epsilon: float = 1e-08, amsgrad: bool = False) -> None: ...
    def create_state(self, index, weight): ...

class Adamax(Optimizer):
    """
    Adamax Optimizer.
    https://machinelearningmastery.com/gradient-descent-optimization-with-adamax-from-scratch/


    :param params: params of model which need to be optimized
    :param lr: learning_rate of model (default: 0.01)
    :param beta1: coefficients used for computing running averages of gradient and
     its square (default: 0.9)
    :param beta2: coefficients used for computing running averages of gradient and
     its square (default: 0.999)
    :param epsilon: term added to the denominator to improve numerical stability (default: 1e-8)
    :return: a Adamax optimizer


    """
    beta1: Incomplete
    beta2: Incomplete
    epsilon: Incomplete
    t: int
    def __init__(self, params, lr: float = 0.01, beta1: float = 0.9, beta2: float = 0.999, epsilon: float = 1e-08) -> None: ...
    def create_state(self, index, weight): ...
RMSprop = RMSProp
