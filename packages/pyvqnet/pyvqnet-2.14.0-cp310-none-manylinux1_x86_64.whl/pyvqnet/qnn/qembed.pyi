from _typeshed import Incomplete
from pyvqnet.qnn.measure import expval as expval

class Quantum_Embedding:
    """
    use RZ,RY,RZ to create a Variational Quantum Circuit to encode classic data into quantum state.

    Quantum embeddings for machine learning
    Seth Lloyd, Maria Schuld, Aroosa Ijaz, Josh Izaac, Nathan Killoran
    https://arxiv.org/abs/2001.03622

    :param qubits: qubits allocated by pyqpanda.
    :param machine: machine allocated by pyqpanda.
    :param num_repetitions_input: number of repeat times to encode input in a submodule.
    :param depth_input: number of input dimension .
    :param num_unitary_layers: number of repeat times of variational quantum gates.
    :param num_repetitions: number of repeat times of submodule.

    Example::

        from pyvqnet.qnn import QuantumLayerV2,Quantum_Embedding
        from pyvqnet.tensor import tensor
        depth_input = 2
        num_repetitions = 2
        num_repetitions_input = 2
        num_unitary_layers = 2

        loacl_machine = pq.CPUQVM()
        loacl_machine.init_qvm()
        nq = depth_input * num_repetitions_input
        qubits = loacl_machine.qAlloc_many(nq)
        cubits = loacl_machine.cAlloc_many(nq)

        data_in = tensor.ones([12, depth_input])

        qe = Quantum_Embedding(qubits, loacl_machine, num_repetitions_input,
                            depth_input, num_unitary_layers, num_repetitions)
        qlayer = QuantumLayerV2(qe.compute_circuit,
                                qe.param_num)

        data_in.requires_grad = True
        y = qlayer.forward(data_in)
        # [
        # [0.2302894],
        #  [0.2302894],
        #  [0.2302894],
        #  [0.2302894],
        #  [0.2302894],
        #  [0.2302894],
        #  [0.2302894],
        #  [0.2302894],
        #  [0.2302894],
        #  [0.2302894],
        #  [0.2302894],
        #  [0.2302894]
        # ]
    """
    param_num: Incomplete
    def __init__(self, qubits, machine, num_repetitions_input, depth_input, num_unitary_layers, num_repetitions) -> None: ...
    def compute_circuit(self, x, w): ...
