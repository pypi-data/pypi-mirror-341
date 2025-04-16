from _typeshed import Incomplete
from pyvqnet.qnn.measure import expval as expval

CoreTensor: Incomplete

class Quantum_Circuit:
    """
    Quantum Variational Circuit. a class contains several commen varational quantum circuits.
    """
    input_gate: Incomplete
    q_depth: Incomplete
    def __init__(self, input_gate: Incomplete | None = None, q_depth: Incomplete | None = None) -> None:
        """
        :param input_gate: Input encoding gate for VQC circuit, used in ``compute_qvc_circuit``.
        :param q_depth: Controlling the quantum convolution depth parameters for quantum transfer learning circuit,
        used in ``compute_qtransfer_vqc_circuit``.
        """
    def build_qvc_circuit(self, input_data, weights, nqubits):
        """

        """
    def compute_qvc_circuit(self, input_data, weights, num_qbits, num_cbits):
        """
        run quantum varational circuit described in `Schuld et al. (2018) <https://arxiv.org/abs/1804.00633>`__
        
        :param input_data: input data.
        :param weights: input trainalbe parameters.
        :param nqubits: number of qubits.
        :param num_cbits : number of classic bits.

        :return: Probabilistic measurements of target qubits 
        """
    def build_qnlp_forget(self, input_data, weights, nqubits): ...
    def compute_qnlp_forget(self, input_data, weights, num_qbits, num_cbits): ...
    def build_qnlp_encode(self, input_data, weights, nqubits): ...
    def compute_qnlp_encode(self, input_data, weights, num_qbits, num_cbits): ...
    def build_qnlp_updata(self, input_data, weights, nqubits): ...
    def compute_qnlp_updata(self, input_data, weights, num_qbits, num_cbits): ...
    def build_qnlp_output(self, input_data, weights, nqubits): ...
    def compute_qnlp_output(self, input_data, weights, num_qbits, num_cbits): ...
    def build_qtransfer_vqc_circuit(self, input_data, q_weights, nqubits, num_qbits, q_depth):
        """
        The variational quantum circuit.
        """
    def compute_qtransfer_vqc_circuit(self, input_data, weights, num_qbits, num_cbits):
        """
        run quantum varational circuit described in `Transfer learning in hybrid classical-quantum neural networks <https://arxiv.org/abs/1912.08278>`__

        :param input_data: input data.
        :param weights: input trainalbe parameters.
        :param nqubits: number of qubits.
        :param num_cbits: number of classic bits.

        :return: expectation of pauli z.
        """
    def build_qkmeans_circuit(self, x, y, nqubits, ncubits):
        """
        Quantum Circuit for kmeans
        """
    def compute_qkmeans_circuit(self, input_data, weights, num_qbits, num_cbits): ...
    def build_qrnn_circuit(self, input_data, weights, num_qbits, nqubits, ncubits, amp, n_qlayers): ...
    def compute_qrnn_circuit(self, input_data, weights, num_qbits, num_cbits): ...
    def build_qgnn_circuit(self, input_data, weights, nqubits, q_depth): ...
    def compute_qgnn_circuit(self, input_data, weights, num_qbits, num_cbits): ...
