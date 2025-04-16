from .pq_op_wrapper import PQ_1BIT_VQC_GATES as PQ_1BIT_VQC_GATES, PQ_2BIT_NONVQC_GATES as PQ_2BIT_NONVQC_GATES, PQ_QNode as PQ_QNode, QuantumTape as QuantumTape, QueuingManager as QueuingManager
from _typeshed import Incomplete
from pyvqnet.optim import SGD as SGD

def append_gate(input_qnode, params, gates, machine, qlists):
    """Append parameterized gates to an existing tape.

    """
def get_prog_func(x, w, input_queue, machine, qlists): ...
def compare_pq_op_dict_info(pq1, pq2): ...

class AdaptiveOptimizer:
    """Optimizer for building fully trained quantum circuits by adding gates adaptively.

    Quantum circuits can be built by adding gates
    `adaptively <https://www.nature.com/articles/s41467-019-10988-2>`_. The adaptive optimizer
    implements an algorithm that grows and optimizes an input quantum circuit by selecting and
    adding gates from a user-defined collection of operators. The algorithm starts by adding all
    the gates to the circuit and computing the circuit gradients with respect to the gate
    parameters. The algorithm then retains the gate which has the largest gradient and optimizes its
    parameter. The process of growing the circuit can be repeated until the computed gradients
    converge to zero within a given threshold. The optimizer returns the fully trained and
    adaptively-built circuit. The adaptive optimizer can be used to implement
    algorithms such as `ADAPT-VQE <https://www.nature.com/articles/s41467-019-10988-2>`_.

    Args:
        param_steps (int): number of steps for optimizing the parameter of a selected gate
        stepsize (float): step size for optimizing the parameter of a selected gate

    """
    param_steps: Incomplete
    stepsize: Incomplete
    m_machine: Incomplete
    m_qubits: Incomplete
    m_cubits: Incomplete
    def __init__(self, machine_type_or_cloud_token, num_of_qubits, param_steps: int = 10, stepsize: float = 0.5) -> None: ...
    def step(self, circuit, operator_pool, params_zero: bool = True):
        """Update the circuit with one step of the optimizer.

        """
    def grad_of_vqc(self, g, prog_func, xdata, param, machine, qlists):
        """
        _grad
        """
    def step_and_cost(self, circuit, xdata, operator_pool, drain_pool: bool = False):
        """Update the circuit with one step of the optimizer, return the corresponding
        objective function value prior to the step, and return the maximum gradient

        """
