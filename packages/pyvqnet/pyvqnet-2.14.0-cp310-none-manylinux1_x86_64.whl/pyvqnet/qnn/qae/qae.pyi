from _typeshed import Incomplete
from pyvqnet.nn.module import Module as Module, Parameter as Parameter
from pyvqnet.tensor.tensor import AutoGradNode as AutoGradNode, QTensor as QTensor

CoreTensor: Incomplete

class QAElayer(Module):
    """
    parameterized quantum circuit Layer.It contains paramters can be trained.

    """
    machine: Incomplete
    qlist: Incomplete
    clist: Incomplete
    history_prob: Incomplete
    n_qubits: Incomplete
    n_aux_qubits: Incomplete
    n_trash_qubits: Incomplete
    weights: Incomplete
    def __init__(self, trash_qubits_number: int = 2, total_qubits_number: int = 7, machine: str = 'cpu') -> None:
        """

        trash_qubits_number: 'int' - should tensor's gradient be tracked, defaults to False
        total_qubits_number: 'int' - Ansatz circuits repeat block times
        machine: 'str' - compute machine
        """
    def forward(self, x):
        """
            forward function
        """

def SWAP_CIRCUITS(input, param, qubits, n_qubits: int = 7, n_aux_qubits: int = 1, n_trash_qubits: int = 2):
    """
    SWAP_CIRCUITS
    """
def paramterized_quautum_circuits(input: CoreTensor, param: CoreTensor, qubits, clist, n_qubits: int = 7, n_aux_qubits: int = 1, n_trash_qubits: int = 2):
    """
    use qpanda to define circuit

    """
