from _typeshed import Incomplete
from pyvqnet.dtype import kfloat32 as kfloat32
from pyvqnet.nn import LeakyReLu as LeakyReLu, Linear as Linear, Module as Module, Parameter as Parameter, Sigmoid as Sigmoid
from pyvqnet.optim import Adam as Adam
from pyvqnet.tensor import AutoGradNode as AutoGradNode, QTensor as QTensor, tensor as tensor
from pyvqnet.utils import initializer as initializer
from pyvqnet.utils.initializer import ones as ones

def qgenrator_cir(x, param, num_of_qubits, rep):
    """
    quantum generator circuits
    """

class QGANAPI:
    """
    QGAN class for random distribution generations
    """
    def __init__(self, data, num_qubits: int = 3, batch_size: int = 2000, num_epochs: int = 2000, q_g_cir: Incomplete | None = None, opt_g: Incomplete | None = None, opt_d: Incomplete | None = None, bounds: Incomplete | None = None, reps: int = 1, metric: str = 'kl', tol_rel_ent: float = 0.001, if_save_param_dir: str = 'tmp') -> None:
        '''
            Init QGAN class for train and eval

            :param data: real data for train, should be numpy array
            :param num_qubits: number of qubits ,should be same as your
             defined quantum generator "s qubits number.
            :param batch_size: batch sizee for training.
            :param num_epochs: number of train iters.
            :param q_g_cir: quantum circuits run function for generator,it should be defined like
            `qgenrator_cir`.otherwise, it cannot run.
            :param opt_g: optimizator instance for generator,use vqnet optim class
            :param opt_g: optimizator instance for discriminator,use vqnet optim class
            :param bounds: boundary for real data distribution
            :param reps: repeat times for default circuits block in papers.
            :param metric: metric for eval gan result.
            "KL" stands for kl divergence, "CE": stands for CrossEntropy.
            :param tol_rel_ent: tolerence for metric
            :param if_save_param_dir: save dir for parameters file and evaluations results.

        '''
    def get_trained_quantum_parameters(self):
        """
            get best trained quantum parameters numpy array based on metric

            return : parameters array
        """
    def train(self) -> None:
        """
            train function
        """
    def eval_metric(self, param, metric: str):
        """
            eval metric with input param

            param param: quantum generator parameters array
            param metric: metric string
            return: metric
        """
    def eval(self, compare_dist: Incomplete | None = None) -> None:
        """
            eval real data distribution with trained best param.

            :param compare_dist: numpy real data distribution 1-dim
        """
    def get_circuits_with_trained_param(self, qubits):
        """
        get qpanda circuit instance with trained parameters for qgan

        param qubits: pyqpanda allocated qubits.
        """
    def load_param_and_eval(self, param):
        """
            load param array and plot pdf

            param param: quantum generator parameters array
            return: prob of quantum generator each statevector
        """

class QGANLayer(Module):
    """
        a pyvqnet module for qgan quantum circuit calculation. modified for qgan only.
    """
    m_prog_func: Incomplete
    m_para: Incomplete
    delta: Incomplete
    history_expectation: Incomplete
    w_jacobian: Incomplete
    x_jacobian: Incomplete
    def __init__(self, qprog_with_meansure, para_num, data_grid, num_qubits, diff_method: str = 'parameter_shift', delta: float = 0.01) -> None:
        """
           a pyvqnet module for qgan quantum circuit calculation. modified for qgan only.
        """
    def forward(self, x: QTensor): ...

class QuantumGenerator(Module):
    """
    Quantum generator module, contains a trainable QGANLayer
    """
    qgenrator: Incomplete
    def __init__(self, cir, num_of_qubits, data_grid, reps: int = 1) -> None: ...
    def forward(self, x): ...

class ClassicDiscriminator(Module):
    """
    Classic discriminator module, contains a trainable Classic nerual network.
    """
    mlp1: Incomplete
    mlp2: Incomplete
    mlp3: Incomplete
    def __init__(self) -> None: ...
    def forward(self, x): ...
