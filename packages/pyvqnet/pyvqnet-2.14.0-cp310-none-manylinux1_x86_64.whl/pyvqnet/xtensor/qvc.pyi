from .module import Module as Module
from .parameter import Parameter as Parameter, quantum_uniform as quantum_uniform
from .xtensor import XTensor as XTensor, cat as cat, xtensor as xtensor
from _typeshed import Incomplete

class QuantumLayer(Module):
    '''
    Abstract Calculation module for Variational Quantum Layer. It simulate a parameterized quantum
    circuit and get the measurement result. It inherits from Module,so that it can calculate
    gradients of circuits parameters,and trains Variational Quantum Circuits model or embeds
    Variational Quantum Circuits into hybird Quantum and Classic model.

    :param qprog_function: callable quantum circuits functions ,cosntructed by qpanda
    :param para_num: `int` - Number of parameter. parameter in this module is construct as 1-dim (para_num,).
    You can reshape it in qprog_function.
    :param machine_type: qpanda machine type , `cpu` or `gpu`.
    :param measure_type: qpanda measure type , `expval` is only accept parameter.
    :param measure_args: qpanda pauli operator string, such as "Z0 X1:10,Y2:-0.543".
    :param num_of_qubits: num of qubits
    :param num_of_cbits: num of classic bits,default:1.
    :param dtype: data type of parameters,default: None,use default data type.
    :param name: name of module,default:"".
    :return: a module can calculate quantum circuits .

    Note:
        qprog_function is quantum circuits function defined in pyQPanda :
        https://pyqpanda-toturial.readthedocs.io/zh/latest/QCircuit.html.

        This function should return a origin ir.

        qprog_function prototype should be f(x, w, pyqpanda.machine,pyqpanda.qlists)

        Currently, only expectation value of the Hamiltonian is supported,which means `measure_type` should be "expval",
        and measure_args pauli operator string, such as "Z0 X1:10,Y2:-0.543".

    '''
    backend: Incomplete
    m_prog_func: Incomplete
    machine_type: Incomplete
    measure_type: Incomplete
    measure_args: Incomplete
    m_machine: Incomplete
    m_qubits: Incomplete
    m_cubits: Incomplete
    m_para: Incomplete
    history_expectation: Incomplete
    num_para: Incomplete
    def __init__(self, qprog_function, para_num, machine_type, measure_type, measure_args, num_of_qubits: int, num_of_cbits: int = 1, dtype: int | None = None, name: str = '') -> None: ...
    def forward(self, x: XTensor, *args, **kwargs): ...
