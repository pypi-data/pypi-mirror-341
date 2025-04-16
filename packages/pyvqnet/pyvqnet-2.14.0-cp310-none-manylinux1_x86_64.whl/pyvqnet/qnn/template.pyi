from _typeshed import Incomplete

__all__ = ['AmplitudeEmbeddingCircuit', 'AngleEmbeddingCircuit', 'RotCircuit', 'CRotCircuit', 'IQPEmbeddingCircuits', 'BasicEmbeddingCircuit', 'CSWAPcircuit', 'StronglyEntanglingTemplate', 'ComplexEntangelingTemplate', 'BasicEntanglerTemplate', 'CCZ', 'Controlled_Hadamard', 'FermionicSingleExcitation', 'BasisState', 'UCCSD', 'QuantumPoolingCircuit', 'FermionicSimulationGate', 'Random_Init_Quantum_State', 'BlockEncode']

def FermionicSimulationGate(qlist_1, qlist_2, theta, phi):
    """

    Fermionic SimulationG ate represent fermionic simulation gate.

    The matrix is:

    .. math::

        {\rm FSim}(\theta, \\phi) =
        \x08egin{pmatrix}
            1 & 0 & 0 & 0\\\n            0 & \\cos(\theta) & -i\\sin(\theta) & 0\\\n            0 & -i\\sin(\theta) & \\cos(\theta) & 0\\\n            0 & 0 & 0 & e^{i\\phi}\\\n        \\end{pmatrix}

    :param qlist_1: first qubit allocated by pyqpanda.
    :param qlist_2: second qubit allocated by pyqpanda.
    :param theta: First parameter for gate.
    :param phi: Second parameter for gate.
    :return:
            pyqpanda QCircuit

    Examples::
        import pyqpanda as pq
        from pyvqnet.qnn.template import FermionicSimulationGate
        m_machine = pq.init_quantum_machine(pq.QMachineType.CPU)

        m_qlist = m_machine.qAlloc_many(3)
        c = FermionicSimulationGate(m_qlist[0],m_qlist[1],0.2,0.5)


    """
def CSWAPcircuit(qlists):
    """
    The controlled-swap circuit

    .. math:: CSWAP = \\begin{bmatrix}
            1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\\\\n            0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 \\\\\n            0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 \\\\\n            0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 \\\\\n            0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 \\\\\n            0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 \\\\\n            0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 \\\\\n            0 & 0 & 0 & 0 & 0 & 0 & 0 & 1
        \\end{bmatrix}.

    .. note:: The first qubits provided corresponds to the **control qubit**.

    :param qlists: list of qubits allocated by pyQpanda.qAlloc_many() the
    first qubits is control qubit.Length of qlists have to be 3.
    :return: quantum circuits

    Example::

        from pyvqnet.qnn.template import CSWAPcircuit
        import pyqpanda as pq
        m_machine = pq.init_quantum_machine(pq.QMachineType.CPU)

        m_qlist = m_machine.qAlloc_many(3)

        c =CSWAPcircuit([m_qlist[1],m_qlist[2],m_qlist[0]])
        print(c)
        pq.destroy_quantum_machine(m_machine)

    """
def IQPEmbeddingCircuits(input_feat, qlist, rep: int = 1):
    """

    Encodes :math:`n` features into :math:`n` qubits using diagonal gates of an IQP circuit.

    The embedding was proposed by `Havlicek et al. (2018) <https://arxiv.org/pdf/1804.11326.pdf>`_.

    The basic IQP circuit can be repeated by specifying ``n_repeats``.

    :param input_feat: numpy array which represents paramters
    :param qlist: qubits allocated by pyQpanda.qAlloc_many()
    :param rep: repeat circuits block
    :return: quantum circuits

    Example::

        input_feat = np.arange(1,100)
        m_machine = pq.init_quantum_machine(pq.QMachineType.CPU)
        qlist = m_machine.qAlloc_many(3)
        circuit = IQPEmbeddingCircuits(input_feat,qlist,rep = 3)
        print(circuit)

    """
def Random_Init_Quantum_State(qlists):
    """
    Generate random quantum state using AmplitudeEmbeddingCircuit.

    :param qlists: qubits allocated by pyqpanda.

    :return:
         pq.QCircuit
    """
def AmplitudeEmbeddingCircuit(input_feat, qlist):
    """

    Encodes :math:`2^n` features into the amplitude vector of :math:`n` qubits.
    To represent a valid quantum state vector, the L2-norm of ``features`` must be one.

    :param input_feat: numpy array which represents paramters
    :param qlist: qubits allocated by pyQpanda.qAlloc_many()
    :return: quantum circuits

    Example::

        input_feat = np.array([2.2, 1, 4.5, 3.7])
        m_machine = pq.init_quantum_machine(pq.QMachineType.CPU)
        m_qlist = m_machine.qAlloc_many(2)
        m_clist = m_machine.cAlloc_many(2)
        m_prog = pq.QProg()
        cir = AmplitudeEmbeddingCircuit(input_feat,m_qlist)
        pq.destroy_quantum_machine(m_machine)
    """
def QuantumPoolingCircuit(sources_wires, sinks_wires, params, qubits):
    """
        A quantum circuit to down samples the data.
        To ‘artificially’ reduce the number of qubits in our circuit, we first begin by creating pairs of the qubits in our system.
        After initially pairing all the qubits, we apply our generalized 2 qubit unitary to each pair.
        After applying this two qubit unitary, we then ignore one qubit from each pair of qubits for the remainder of the neural network.

        :param sources_wires: source qubits index which will be ignored.
        :param sinks_wires: target qubits index which will be reserverd.
        :param params: input parameters.
        :param qubits: qubits list allocated by pyqpanda.

        :return:
            the quantum pooling circuit
    Exmaple::

        from pyvqnet.qnn import QuantumPoolingCircuit
        import pyqpanda as pq
        from pyvqnet import tensor
        machine = pq.CPUQVM()
        machine.init_qvm()
        qlists = machine.qAlloc_many(4)
        p = tensor.full([6], 0.35)
        cir = QuantumPoolingCircuit([0, 1], [2, 3], p, qlists)
        print(cir)
    """
def AngleEmbeddingCircuit(input_feat, qlist, rotation: str = 'X'):
    """

    Encodes :math:`N` features into the rotation angles of :math:`n` qubits, where :math:`N \\leq n`.

    The rotations can be chosen as either : 'X' , 'Y' , 'Z',
    as defined by the ``rotation`` parameter:

    * ``rotation='X'`` uses the features as angles of RX rotations

    * ``rotation='Y'`` uses the features as angles of RY rotations

    * ``rotation='Z'`` uses the features as angles of RZ rotations

    The length of ``features`` has to be smaller or equal to the number of qubits.
    If there are fewer entries in ``features`` than qlists, the circuit does
    not apply the remaining rotation gates.

    :param input_feat: numpy array which represents paramters
    :param qlist: qubits allocated by pyQpanda.qAlloc_many()
    :return: quantum circuits

    Example::

        m_machine = pq.init_quantum_machine(pq.QMachineType.CPU)
        m_qlist = m_machine.qAlloc_many(2)
        m_clist = m_machine.cAlloc_many(2)
        m_prog = pq.QProg()

        input_feat = np.array([2.2, 1])
        C = AngleEmbeddingCircuit(input_feat,m_qlist,'X')
        print(C)
        C = AngleEmbeddingCircuit(input_feat,m_qlist,'Y')
        print(C)
        C = AngleEmbeddingCircuit(input_feat,m_qlist,'Z')
        print(C)
        pq.destroy_quantum_machine(m_machine)
    """
def RotCircuit(para, qlist):
    """

    Arbitrary single qubit rotation.Number of qlist should be 1,and number of parameters should
    be 3

    .. math::

        R(\\phi,\\theta,\\omega) = RZ(\\omega)RY(\\theta)RZ(\\phi)= \\begin{bmatrix}
        e^{-i(\\phi+\\omega)/2}\\cos(\\theta/2) & -e^{i(\\phi-\\omega)/2}\\sin(\\theta/2) \\\\\n        e^{-i(\\phi-\\omega)/2}\\sin(\\theta/2) & e^{i(\\phi+\\omega)/2}\\cos(\\theta/2)
        \\end{bmatrix}.


    :param para: numpy array which represents paramters [\\phi, \\theta, \\omega]
    :param qlist: qubits allocated by pyQpanda.qAlloc_many()
    :return: quantum circuits

    Example::

        m_machine = pq.init_quantum_machine(pq.QMachineType.CPU)
        m_clist = m_machine.cAlloc_many(2)
        m_prog = pq.QProg()
        m_qlist = m_machine.qAlloc_many(1)
        param = np.array([3,4,5])
        c = RotCircuit(param,m_qlist)
        print(c)
        pq.destroy_quantum_machine(m_machine)

    """
def BasicEmbeddingCircuit(input_feat, qlist):
    """

    For example, for ``features=([0, 1, 1])``, the quantum system will be
    prepared in state :math:`|011 \\rangle`.

    :param input_feat: binary input of shape ``(n, )``
    :param qlist: qlist that the template acts on
    :return: quantum circuits

    Example::

        input_feat = np.array([1,1,0]).reshape([3])
        print(input_feat.ndim   )
        m_machine = pq.init_quantum_machine(pq.QMachineType.CPU)

        qlist = m_machine.qAlloc_many(3)
        circuit = BasicEmbeddingCircuit(input_feat,qlist)
        print(circuit)

    """
def CRotCircuit(para, control_qlists, rot_qlists):
    """

    The controlled-Rot operator

    .. math:: CR(\\phi, \\theta, \\omega) = \\begin{bmatrix}
            1 & 0 & 0 & 0 \\\\\n            0 & 1 & 0 & 0\\\\\n            0 & 0 & e^{-i(\\phi+\\omega)/2}\\cos(\\theta/2) & -e^{i(\\phi-\\omega)/2}\\sin(\\theta/2)\\\\\n            0 & 0 & e^{-i(\\phi-\\omega)/2}\\sin(\\theta/2) & e^{i(\\phi+\\omega)/2}\\cos(\\theta/2)
        \\end{bmatrix}.

    :param para: numpy array which represents paramters [\\phi, \\theta, \\omega]
    :param control_qlists: control qubit allocated by pyQpanda.qAlloc_many()
    :param rot_qlists: Rot qubit allocated by pyQpanda.qAlloc_many()
    :return: quantum circuits

    Example::

        m_machine = pq.init_quantum_machine(pq.QMachineType.CPU)
        m_clist = m_machine.cAlloc_many(2)
        m_prog = pq.QProg()
        m_qlist = m_machine.qAlloc_many(1)
        control_qlist = m_machine.qAlloc_many(1)
        param = np.array([3,4,5])
        c = CRotCircuit(param,control_qlist,m_qlist)
        print(c)
        pq.destroy_quantum_machine(m_machine)
    """

class ComplexEntangelingTemplate:
    """
        Strongly entangled layers consisting of U3 gates and CNOT gates.
        This ansatz is from the following paper: https://arxiv.org/abs/1804.00633.

        :param weights: parameters, shape of [depth,num_qubits,3]
        :param num_qubits: number of qubits.
        :param depth: depth of sub-circuit.
        
        Example::

            from pyvqnet.qnn import ComplexEntangelingTemplate
            import pyqpanda as pq
            from pyvqnet.tensor import *
            depth =3
            num_qubits = 8
            shape = [depth, num_qubits, 3]
            weights = tensor.randn(shape)

            machine = pq.CPUQVM()
            machine.init_qvm()
            qubits = machine.qAlloc_many(num_qubits)

            circuit = ComplexEntangelingTemplate(weights, num_qubits=num_qubits,depth=depth)
            result = circuit.create_circuit(qubits)
            circuit.print_circuit(qubits)

            # q_0:  |0>─┤U3(1.115555,-0.025096,1.326895)├── ───■── ────── ───────────────────────────────── ────────────────────────────────── >
            #           ├───────────────────────────────┴─┐ ┌──┴─┐        ┌───────────────────────────────┐                                    >
            # q_1:  |0>─┤U3(-0.884622,-0.239700,-0.701955)├ ┤CNOT├ ───■── ┤U3(0.811768,0.537290,-0.433107)├ ────────────────────────────────── >
            #           ├────────────────────────────────┬┘ └────┘ ┌──┴─┐ └───────────────────────────────┘ ┌────────────────────────────────┐ >
            # q_2:  |0>─┤U3(-0.387148,-0.322480,0.238582)├─ ────── ┤CNOT├ ───■───────────────────────────── ┤U3(-0.188015,-1.828407,0.070222)├ >
            #           ├────────────────────────────────┤         └────┘ ┌──┴─┐                            └────────────────────────────────┘ >
            # q_3:  |0>─┤U3(-0.679633,1.638090,-1.341497)├─ ────── ────── ┤CNOT├─────────────────────────── ───■────────────────────────────── >
            #           ├──────────────────────────────┬─┘                └────┘                            ┌──┴─┐                             >
            # q_4:  |0>─┤U3(2.073888,1.251795,0.238305)├─── ────── ────── ───────────────────────────────── ┤CNOT├──────────────────────────── >
            #           ├──────────────────────────────┤                                                    └────┘                             >
            # q_5:  |0>─┤U3(0.247473,2.772012,1.864166)├─── ────── ────── ───────────────────────────────── ────────────────────────────────── >
            #           ├──────────────────────────────┴─┐                                                                                     >
            # q_6:  |0>─┤U3(-1.421337,-0.866551,0.739282)├─ ────── ────── ───────────────────────────────── ────────────────────────────────── >
            #           ├────────────────────────────────┤                                                                                     >
            # q_7:  |0>─┤U3(-3.707045,0.690364,-0.979904)├─ ────── ────── ───────────────────────────────── ────────────────────────────────── >
            #           └────────────────────────────────┘                                                                                     >

            #                                                                                                                 >
            # q_0:  |0>────────────────────────────────── ────────────────────────────────── ──────────────────────────────── >
            #                                                                                                                 >
            # q_1:  |0>────────────────────────────────── ────────────────────────────────── ──────────────────────────────── >
            #                                                                                                                 >
            # q_2:  |0>────────────────────────────────── ────────────────────────────────── ──────────────────────────────── >
            #          ┌────────────────────────────────┐                                                                     >
            # q_3:  |0>┤U3(0.516395,-0.823623,-0.804430)├ ────────────────────────────────── ──────────────────────────────── >
            #          └────────────────────────────────┘ ┌────────────────────────────────┐                                  >
            # q_4:  |0>───■────────────────────────────── ┤U3(-1.420068,1.063462,-0.107385)├ ──────────────────────────────── >
            #          ┌──┴─┐                             └────────────────────────────────┘ ┌──────────────────────────────┐ >
            # q_5:  |0>┤CNOT├──────────────────────────── ───■────────────────────────────── ┤U3(0.377809,0.204278,0.386830)├ >
            #          └────┘                             ┌──┴─┐                             └──────────────────────────────┘ >
            # q_6:  |0>────────────────────────────────── ┤CNOT├──────────────────────────── ───■──────────────────────────── >
            #                                             └────┘                             ┌──┴─┐                           >
            # q_7:  |0>────────────────────────────────── ────────────────────────────────── ┤CNOT├────────────────────────── >
            #                                                                                └────┘                           >

            #          ┌────┐                                 ┌────────────────────────────────┐                                                  >
            # q_0:  |0>┤CNOT├──────────────────────────────── ┤U3(-0.460444,-1.150054,0.318044)├ ───■── ────── ────────────────────────────────── >
            #          └──┬─┘                                 └────────────────────────────────┘ ┌──┴─┐        ┌────────────────────────────────┐ >
            # q_1:  |0>───┼────────────────────────────────── ────────────────────────────────── ┤CNOT├ ───■── ┤U3(-1.255487,0.589956,-0.378491)├ >
            #             │                                                                      └────┘ ┌──┴─┐ └────────────────────────────────┘ >
            # q_2:  |0>───┼────────────────────────────────── ────────────────────────────────── ────── ┤CNOT├ ───■────────────────────────────── >
            #             │                                                                             └────┘ ┌──┴─┐                             >
            # q_3:  |0>───┼────────────────────────────────── ────────────────────────────────── ────── ────── ┤CNOT├──────────────────────────── >
            #             │                                                                                    └────┘                             >
            # q_4:  |0>───┼────────────────────────────────── ────────────────────────────────── ────── ────── ────────────────────────────────── >
            #             │                                                                                                                       >
            # q_5:  |0>───┼────────────────────────────────── ────────────────────────────────── ────── ────── ────────────────────────────────── >
            #             │┌────────────────────────────────┐                                                                                     >
            # q_6:  |0>───┼┤U3(-0.760777,-0.867848,0.016680)├ ────────────────────────────────── ────── ────── ────────────────────────────────── >
            #             │└────────────────────────────────┘ ┌────────────────────────────────┐                                                  >
            # q_7:  |0>───■────────────────────────────────── ┤U3(-1.462434,-0.173843,1.211081)├ ────── ────── ────────────────────────────────── >
            #                                                 └────────────────────────────────┘                                                  >

            #                                                                                                               >
            # q_0:  |0>───────────────────────────────── ───────────────────────────────── ──────────────────────────────── >
            #                                                                                                               >
            # q_1:  |0>───────────────────────────────── ───────────────────────────────── ──────────────────────────────── >
            #          ┌───────────────────────────────┐                                                                    >
            # q_2:  |0>┤U3(0.558638,0.218889,-0.241834)├ ───────────────────────────────── ──────────────────────────────── >
            #          └───────────────────────────────┘ ┌───────────────────────────────┐                                  >
            # q_3:  |0>───■───────────────────────────── ┤U3(0.740361,-0.336978,0.171089)├ ──────────────────────────────── >
            #          ┌──┴─┐                            └───────────────────────────────┘ ┌──────────────────────────────┐ >
            # q_4:  |0>┤CNOT├─────────────────────────── ───■───────────────────────────── ┤U3(0.585393,0.204842,0.682543)├ >
            #          └────┘                            ┌──┴─┐                            └──────────────────────────────┘ >
            # q_5:  |0>───────────────────────────────── ┤CNOT├─────────────────────────── ───■──────────────────────────── >
            #                                            └────┘                            ┌──┴─┐                           >
            # q_6:  |0>───────────────────────────────── ───────────────────────────────── ┤CNOT├────────────────────────── >
            #                                                                              └────┘                           >
            # q_7:  |0>───────────────────────────────── ───────────────────────────────── ──────────────────────────────── >
            #                                                                                                               >

            #                                              ┌────┐                               ┌───────────────────────────────┐ >
            # q_0:  |0>─────────────────────────────────── ┤CNOT├────────────────────────────── ┤U3(0.657827,1.434924,-0.328996)├ >
            #                                              └──┬─┘                               └───────────────────────────────┘ >
            # q_1:  |0>─────────────────────────────────── ───┼──────────────────────────────── ───────────────────────────────── >
            #                                                 │                                                                   >
            # q_2:  |0>─────────────────────────────────── ───┼──────────────────────────────── ───────────────────────────────── >
            #                                                 │                                                                   >
            # q_3:  |0>─────────────────────────────────── ───┼──────────────────────────────── ───────────────────────────────── >
            #                                                 │                                                                   >
            # q_4:  |0>─────────────────────────────────── ───┼──────────────────────────────── ───────────────────────────────── >
            #          ┌─────────────────────────────────┐    │                                                                   >
            # q_5:  |0>┤U3(-2.134247,-0.783461,-0.200094)├ ───┼──────────────────────────────── ───────────────────────────────── >
            #          └─────────────────────────────────┘    │┌──────────────────────────────┐                                   >
            # q_6:  |0>───■─────────────────────────────── ───┼┤U3(1.816030,0.572931,1.683584)├ ───────────────────────────────── >
            #          ┌──┴─┐                                 │└──────────────────────────────┘ ┌───────────────────────────────┐ >
            # q_7:  |0>┤CNOT├───────────────────────────── ───■──────────────────────────────── ┤U3(0.661537,0.214565,-0.325014)├ >
            #          └────┘                                                                   └───────────────────────────────┘ >

            #                                                           ┌────┐
            # q_0:  |0>───■── ────── ────── ────── ────── ────── ────── ┤CNOT├
            #          ┌──┴─┐                                           └──┬─┘
            # q_1:  |0>┤CNOT├ ───■── ────── ────── ────── ────── ────── ───┼──
            #          └────┘ ┌──┴─┐                                       │
            # q_2:  |0>────── ┤CNOT├ ───■── ────── ────── ────── ────── ───┼──
            #                 └────┘ ┌──┴─┐                                │
            # q_3:  |0>────── ────── ┤CNOT├ ───■── ────── ────── ────── ───┼──
            #                        └────┘ ┌──┴─┐                         │
            # q_4:  |0>────── ────── ────── ┤CNOT├ ───■── ────── ────── ───┼──
            #                               └────┘ ┌──┴─┐                  │
            # q_5:  |0>────── ────── ────── ────── ┤CNOT├ ───■── ────── ───┼──
            #                                      └────┘ ┌──┴─┐           │
            # q_6:  |0>────── ────── ────── ────── ────── ┤CNOT├ ───■── ───┼──
            #                                             └────┘ ┌──┴─┐    │
            # q_7:  |0>────── ────── ────── ────── ────── ────── ┤CNOT├ ───■──
    """
    weights: Incomplete
    num_of_qubits: Incomplete
    depth: Incomplete
    def __init__(self, weights, num_qubits, depth) -> None: ...
    def create_circuit(self, qubits): ...
    def compute_circuit(self, input_data, weights, num_qbits, num_cbits): ...
    def print_circuit(self, qubits) -> None: ...

class StronglyEntanglingTemplate:
    """
    Layers consisting of single qubit rotations and entanglers, inspired by the `circuit-centric classifier design
     <https://arxiv.org/abs/1804.00633>`__ .

    The argument ``weights`` contains the weights for each layer. The number of layers :math:`L` is therefore derived
    from the first dimension of ``weights``.

    The 2-qubit CNOT gate,act on the :math:`M` number of qubits, :math:`i = 1,...,M`. The second qubit of each gate is given by
    :math:`(i+r)\\mod M`, where :math:`r` is a  hyperparameter called the *range*, and :math:`0 < r < M`.

    :param weights: weight tensor of shape ``(L, M, 3)`` , default: None, use random tensor with shape ``(1,1,3)`` .
    :param num_qubits: number of qubits, default: 1.
    :param ranges: sequence determining the range hyperparameter for each subsequent layer; default: None
                                using :math: `r=l \\mod M` for the :math:`l` th layer and :math:`M` qubits.
    :return: quantum circuits

    Example::

        import pyqpanda as pq
        import numpy as np
        from pyvqnet.qnn.template import StronglyEntanglingTemplate
        np.random.seed(42)
        num_qubits = 3
        shape = [2, num_qubits, 3]
        weights = np.random.random(size=shape)

        machine = pq.CPUQVM()
        machine.init_qvm()
        qubits = machine.qAlloc_many(num_qubits)

        circuit = StronglyEntanglingTemplate(weights, num_qubits=num_qubits)
        result = circuit.create_circuit(qubits)
        circuit.print_circuit(qubits)

        prob = machine.prob_run_dict(result, qubits[0], -1)
        prob = list(prob.values())
        print(prob)
        # q_0:  |0>─┤RZ(0.374540)├ ┤RY(0.950714)├ ┤RZ(0.731994)├ ───■── ────── ┤CNOT├──────────── ┤RZ(0.708073)├ >
        #           ├────────────┤ ├────────────┤ ├────────────┤ ┌──┴─┐        └──┬┬┴───────────┐ ├────────────┤ >
        # q_1:  |0>─┤RZ(0.598658)├ ┤RY(0.156019)├ ┤RZ(0.155995)├ ┤CNOT├ ───■── ───┼┤RZ(0.832443)├ ┤RY(0.212339)├ >
        #           ├────────────┤ ├────────────┤ ├────────────┤ └────┘ ┌──┴─┐    │└────────────┘ ├────────────┤ >
        # q_2:  |0>─┤RZ(0.058084)├ ┤RY(0.866176)├ ┤RZ(0.601115)├ ────── ┤CNOT├ ───■────────────── ┤RZ(0.183405)├ >
        #           └────────────┘ └────────────┘ └────────────┘        └────┘                    └────────────┘ >

        #          ┌────────────┐ ┌────────────┐        ┌────┐
        # q_0:  |0>┤RY(0.020584)├ ┤RZ(0.969910)├ ───■── ┤CNOT├ ──────
        #          ├────────────┤ └────────────┘    │   └──┬─┘ ┌────┐
        # q_1:  |0>┤RZ(0.181825)├ ────────────── ───┼── ───■── ┤CNOT├
        #          ├────────────┤ ┌────────────┐ ┌──┴─┐        └──┬─┘
        # q_2:  |0>┤RY(0.304242)├ ┤RZ(0.524756)├ ┤CNOT├ ────── ───■──
        #          └────────────┘ └────────────┘ └────┘
        #[0.6881335561525671, 0.31186644384743273]

    """
    n_layers: Incomplete
    num_qubits: Incomplete
    weights: Incomplete
    ranges: Incomplete
    imprimitive: Incomplete
    def __init__(self, weights: Incomplete | None = None, num_qubits: int = 1, ranges: Incomplete | None = None) -> None: ...
    def Rot(self, qubits, l, weights):
        """
        :param qubits: quantum bits
        :param l: enter the number of layers
        :param weights: input weight
        :return: quantum circuit
        """
    def create_circuit(self, qubits): ...
    def compute_circuit(self, input_data, weights, num_qbits, num_cbits): ...
    def print_circuit(self, qubits) -> None: ...

class BasicEntanglerTemplate:
    """
    Layers consisting of one-parameter single-qubit rotations on each qubit, followed by a closed chain or *ring* of
     CNOT gates.
     
    The ring of CNOT gates connects every qubit with its neighbour, with the last qubit being considered as a neighbour to the first qubit.

    The number of layers :math:`L` is determined by the first dimension of the argument ``weights``.
    When using a single wire, the template only applies the single
    qubit gates in each layer.


    :param weights: Weight tensor of shape ``(L, len(qubits))`` . Each weight is used as a parameter
                                for the rotation, default: None, use random tensor with shape ``(1,1)`` .
    :param num_qubits: number of qubits, default: 1.
    :param rotation: one-parameter single-qubit gate to use, default: `pyqpanda.RX`

    Example::

        import pyqpanda as pq
        import numpy as np
        from pyvqnet.qnn.template import BasicEntanglerTemplate
        np.random.seed(42)
        num_qubits = 5
        shape = [1, num_qubits]
        weights = np.random.random(size=shape)

        machine = pq.CPUQVM()
        machine.init_qvm()
        qubits = machine.qAlloc_many(num_qubits)

        circuit = BasicEntanglerTemplate(weights=weights, num_qubits=num_qubits, rotation=pq.RZ)
        result = circuit.create_circuit(qubits)
        circuit.print_circuit(qubits)

        prob = machine.prob_run_dict(result, qubits[0], -1)
        prob = list(prob.values())
        print(prob)
        #           ┌────────────┐                             ┌────┐
        # q_0:  |0>─┤RZ(0.374540)├ ───■── ────── ────── ────── ┤CNOT├
        #           ├────────────┤ ┌──┴─┐                      └──┬─┘
        # q_1:  |0>─┤RZ(0.950714)├ ┤CNOT├ ───■── ────── ────── ───┼──
        #           ├────────────┤ └────┘ ┌──┴─┐                  │
        # q_2:  |0>─┤RZ(0.731994)├ ────── ┤CNOT├ ───■── ────── ───┼──
        #           ├────────────┤        └────┘ ┌──┴─┐           │
        # q_3:  |0>─┤RZ(0.598658)├ ────── ────── ┤CNOT├ ───■── ───┼──
        #           ├────────────┤               └────┘ ┌──┴─┐    │
        # q_4:  |0>─┤RZ(0.156019)├ ────── ────── ────── ┤CNOT├ ───■──
        #           └────────────┘                      └────┘

        # [1.0, 0.0]

    """
    n_layers: Incomplete
    num_qubits: Incomplete
    weights: Incomplete
    rotation: Incomplete
    def __init__(self, weights: Incomplete | None = None, num_qubits: int = 1, rotation=...) -> None: ...
    def Rot(self, qubits, l, weights):
        """
        :param qubits: quantum bits
        :param l: enter the number of layers
        :param weights: input weight
        :return: quantum circuit
        """
    def create_circuit(self, qubits): ...
    def compute_circuit(self, input_data, weights, num_qbits, num_cbits): ...
    def print_circuit(self, qubits) -> None: ...

class RandomTemplate:
    """
    Layers of randomly chosen single qubit rotations and 2-qubit entangling gates, acting on randomly chosen qubits.

    The argument ``weights`` contains the weights for each layer. The number of layers :math:`L` is therefore derived
    from the first dimension of ``weights``.

    The number of random rotations is derived from the second dimension of ``weights``. The number of
    two-qubit gates is determined by ``ratio_imprim``. For example, a ratio of ``0.3`` with ``30`` rotations
    will lead to the use of ``10`` two-qubit gates.

    :param weights: weight tensor of shape ``(L, k)``. Each weight is used as a parameter
                                for the rotation, default: None, use random tensor with shape ``(1,1)`` .
    :param num_qubits: number of qubits, default: 1.
    :param ratio_imprim: value between 0 and 1 that determines the ratio of imprimitive to rotation gates.
    :param rotation: List of Pauli-X, Pauli-Y and/or Pauli-Z gates. The frequency determines how often a particular
     rotation type is used. Defaults to the use of all three rotations with equal frequency.
    :param seed: seed to generate random architecture, defaults to 42.


    Example::

        import pyqpanda as pq
        import numpy as np
        from pyvqnet.qnn.template import RandomTemplate
        num_qubits = 2
        weights = np.array([[0.1, -2.1, 1.4]])

        machine = pq.CPUQVM()
        machine.init_qvm()
        qubits = machine.qAlloc_many(num_qubits)

        circuit = RandomTemplate(weights, num_qubits=num_qubits, seed=12)
        result = circuit.create_circuit(qubits)
        circuit.print_circuit(qubits)

        prob = machine.prob_run_dict(result, qubits[0], -1)
        prob = list(prob.values())
        print(prob)

        #           ┌────┐ ┌────────────┐         ┌────┐
        # q_0:  |0>─┤CNOT├ ┤RZ(0.100000)├─ ───■── ┤CNOT├ ──────────────
        #           └──┬─┘ ├────────────┴┐ ┌──┴─┐ └──┬─┘ ┌────────────┐
        # q_1:  |0>────■── ┤RX(-2.100000)├ ┤CNOT├ ───■── ┤RZ(1.400000)├
        #                  └─────────────┘ └────┘        └────────────┘

        # [0.2475769477000712, 0.7524230522999289]

    """
    seed: Incomplete
    rotations: Incomplete
    n_layers: Incomplete
    num_qubits: Incomplete
    weights: Incomplete
    ratio_imprimitive: Incomplete
    def __init__(self, weights: Incomplete | None = None, num_qubits: int = 1, ratio_imprim: float = 0.3, rotations: Incomplete | None = None, seed: int = 42) -> None: ...
    def select_random(self, n_samples, seed: Incomplete | None = None):
        """
        Returns a randomly sampled subset of Wires of length 'n_samples'.

        Args:
            n_samples (int): number of subsampled wires
            seed (int): optional random seed used for selecting the wires

        Returns:
            Wires: random subset of wires
        """
    def create_circuit(self, qubits): ...
    def compute_circuit(self, input_data, weights, num_qbits, num_cbits): ...
    def print_circuit(self, qubits) -> None: ...

class SimplifiedTwoDesignTemplate:
    '''
    Layers consisting of a simplified 2-design architecture of Pauli-Y rotations and controlled-Z entanglers
    proposed in `Cerezo et al. (2020) <https://arxiv.org/abs/2001.00550>`_.

    A 2-design is an ensemble of unitaries whose statistical properties are the same as sampling random unitaries
    with respect to the Haar measure up to the first 2 moments.

    The template is not a strict 2-design, since
    it does not consist of universal 2-qubit gates as building blocks, but has been shown in
    `Cerezo et al. (2020) <https://arxiv.org/abs/2001.00550>`_ to exhibit important properties to study "barren plateaus"
    in quantum optimization landscapes.

    The template starts with an initial layer of single qubit Pauli-Y rotations, before the main
    :math:`L` layers are applied. The basic building block of the main layers are controlled-Z entanglers
    followed by a pair of Pauli-Y rotation gates (one for each wire).
    Each layer consists of an "even" part whose entanglers start with the first qubit,
    and an "odd" part that starts with the second qubit.

    The argument ``initial_layer_weights`` contains the rotation angles of the initial layer of Pauli-Y rotations,
    while ``weights`` contains the pairs of Pauli-Y rotation angles of the respective layers. Each layer takes
    :math:`\\lfloor M/2 \\rfloor + \\lfloor (M-1)/2 \\rfloor = M-1` pairs of angles, where :math:`M` is the number of wires.
    The number of layers :math:`L` is derived from the first dimension of ``weights``.

    :param initial_layer_weights: weight tensor for the initial rotation block, shape ``(M,)`` .
    :param weights: tensor of rotation angles for the layers, shape ``(L, M-1, 2)``.
    :param num_qubits: number of qubits, default: 1.


    Example::

        import pyqpanda as pq
        import numpy as np
        from pyvqnet.qnn.template import SimplifiedTwoDesignTemplate
        num_qubits = 3
        init_weights = [pi, pi, pi]
        weights_layer1 = [[0., pi],
                          [0., pi]]
        weights_layer2 = [[pi, 0.],
                          [pi, 0.]]
        weights = [weights_layer1, weights_layer2]

        machine = pq.CPUQVM()
        machine.init_qvm()
        qubits = machine.qAlloc_many(num_qubits)

        circuit = SimplifiedTwoDesignTemplate(init_weights, weights, num_qubits=num_qubits)
        result = circuit.create_circuit(qubits)
        circuit.print_circuit(qubits)

        prob = machine.prob_run_dict(result, qubits[0], -1)
        prob = list(prob.values())
        print(prob)

        #           ┌────────────┐      ┌────────────┐                          ┌────────────┐
        # q_0:  |0>─┤RY(3.141593)├ ──■─ ┤RY(0.000000)├ ──── ────────────── ──■─ ┤RY(3.141593)├ ──── ──────────────
        #           ├────────────┤ ┌─┴┐ ├────────────┤      ┌────────────┐ ┌─┴┐ ├────────────┤      ┌────────────┐
        # q_1:  |0>─┤RY(3.141593)├ ┤CZ├ ┤RY(3.141593)├ ──■─ ┤RY(0.000000)├ ┤CZ├ ┤RY(0.000000)├ ──■─ ┤RY(3.141593)├
        #           ├────────────┤ └──┘ └────────────┘ ┌─┴┐ ├────────────┤ └──┘ └────────────┘ ┌─┴┐ ├────────────┤
        # q_2:  |0>─┤RY(3.141593)├ ──── ────────────── ┤CZ├ ┤RY(3.141593)├ ──── ────────────── ┤CZ├ ┤RY(0.000000)├
        #           └────────────┘                     └──┘ └────────────┘                     └──┘ └────────────┘

        # [1.0, 5.622455701440236e-65]


    '''
    weights: Incomplete
    initial_layer_weights: Incomplete
    num_qubits: Incomplete
    wires: Incomplete
    n_layers: Incomplete
    def __init__(self, initial_layer_weights, weights, num_qubits: int = 1) -> None: ...
    def create_circuit(self, qubits): ...
    def compute_circuit(self, input_data, weights, num_qbits, num_cbits): ...
    def print_circuit(self, qubits) -> None: ...

def Controlled_Hadamard(qubits):
    """
    The controlled-Hadamard gates

    .. math:: CH = \\begin{bmatrix}
            1 & 0 & 0 & 0 \\\\\n            0 & 1 & 0 & 0 \\\\\n            0 & 0 & \\frac{1}{\\sqrt{2}} & \\frac{1}{\\sqrt{2}} \\\\\n            0 & 0 & \\frac{1}{\\sqrt{2}} & -\\frac{1}{\\sqrt{2}}
        \\end{bmatrix}.

    :param qubits: qubits allocated by pyqpanda.

    Examples::

        import pyqpanda as pq

        machine = pq.CPUQVM()
        machine.init_qvm()
        qubits = machine.qAlloc_many(2)
        from pyvqnet.qnn import Controlled_Hadamard

        cir = Controlled_Hadamard(qubits)
        print(cir)
        # q_0:  |0>──────────────── ──■─ ──────────────
        #           ┌─────────────┐ ┌─┴┐ ┌────────────┐
        # q_1:  |0>─┤RY(-0.785398)├ ┤CZ├ ┤RY(0.785398)├
        #           └─────────────┘ └──┘ └────────────┘

    """
def CCZ(qubits):
    """
    CCZ (controlled-controlled-Z) gate.

    .. math::

        CCZ =
        \\begin{pmatrix}
        1 & 0 & 0 & 0 & 0 & 0 & 0 & 0\\\\\n        0 & 1 & 0 & 0 & 0 & 0 & 0 & 0\\\\\n        0 & 0 & 1 & 0 & 0 & 0 & 0 & 0\\\\\n        0 & 0 & 0 & 1 & 0 & 0 & 0 & 0\\\\\n        0 & 0 & 0 & 0 & 1 & 0 & 0 & 0\\\\\n        0 & 0 & 0 & 0 & 0 & 1 & 0 & 0\\\\\n        0 & 0 & 0 & 0 & 0 & 0 & 1 & 0\\\\\n        0 & 0 & 0 & 0 & 0 & 0 & 0 & -1
        \\end{pmatrix}
    
    :param qubits: qubits allocated by pyqpanda。

    :return:
            pyqpanda QCircuit
    
    Examples::

        import pyqpanda as pq

        machine = pq.CPUQVM()
        machine.init_qvm()
        qubits = machine.qAlloc_many(3)
        from pyvqnet.qnn import CCZ

        cir = CCZ(qubits)
        print(cir)
    """
def FermionicSingleExcitation(weight, wires, qubits):
    '''Circuit to exponentiate the tensor product of Pauli matrices representing the
    single-excitation operator entering the Unitary Coupled-Cluster Singles
    and Doubles (UCCSD) ansatz. UCCSD is a VQE ansatz commonly used to run quantum
    chemistry simulations.

    The Coupled-Cluster single-excitation operator is given by

    .. math::

        \\hat{U}_{pr}(\\theta) = \\mathrm{exp} \\{ \\theta_{pr} (\\hat{c}_p^\\dagger \\hat{c}_r
        -\\mathrm{H.c.}) \\},

    :param weight: input paramter acts on qubits p.
    :param wires: Wires that the template acts on. The wires represent the subset of orbitals in the interval [r, p]. Must be of minimum length 2. The first wire is interpreted as r and the last wire as p.
                Wires in between are acted on with CNOT gates to compute the parity of the set of qubits.
    :param qubits: qubits list allocated by pyqpanda.

    :return:
            pyqpanda QCircuit

    Examples::

        from pyvqnet.qnn import FermionicSingleExcitation, expval

        weight = 0.5
        import pyqpanda as pq
        machine = pq.CPUQVM()
        machine.init_qvm()
        qlists = machine.qAlloc_many(3)

        cir = FermionicSingleExcitation(weight, [1, 0, 2], qlists)

        prog = pq.QProg()
        prog.insert(cir)
        pauli_dict = {\'Z0\': 1}
        exp2 = expval(machine, prog, pauli_dict, qlists)
        print(f"vqnet {exp2}")
        #vqnet 1.0000000000000013

    '''
def BasisState(basis_state, wires, qubits):
    """
    Prepares a basis state on the given wires using a sequence of Pauli-X gates.

    :param wires:wires that the template acts on.
    :param qubits: qubits list allocated by pyqpanda.

    :return:
          pyqpanda QCircuit
    """
def UCCSD(weights, wires, s_wires, d_wires, init_state, qubits):
    '''
    
    Implements the Unitary Coupled-Cluster Singles and Doubles (UCCSD) ansatz.

    The UCCSD ansatz calls the
     `FermionicSingleExcitation` and `FermionicDoubleExcitation`
    templates to exponentiate the coupled-cluster excitation operator. UCCSD is a VQE ansatz
    commonly used to run quantum chemistry simulations.

    The UCCSD unitary, within the first-order Trotter approximation, is given by:

    .. math::

        \\hat{U}(\\vec{\\theta}) =
        \\prod_{p > r} \\mathrm{exp} \\Big\\{\\theta_{pr}
        (\\hat{c}_p^\\dagger \\hat{c}_r-\\mathrm{H.c.}) \\Big\\}
        \\prod_{p > q > r > s} \\mathrm{exp} \\Big\\{\\theta_{pqrs}
        (\\hat{c}_p^\\dagger \\hat{c}_q^\\dagger \\hat{c}_r \\hat{c}_s-\\mathrm{H.c.}) \\Big\\}

    where :math:`\\hat{c}` and :math:`\\hat{c}^\\dagger` are the fermionic annihilation and
    creation operators and the indices :math:`r, s` and :math:`p, q` run over the occupied and
    unoccupied molecular orbitals, respectively. Using the `Jordan-Wigner transformation
    <https://arxiv.org/abs/1208.5986>`_ the UCCSD unitary defined above can be written in terms
    of Pauli matrices as follows (for more details see
    `arXiv:1805.04340 <https://arxiv.org/abs/1805.04340>`_):

    .. math::

        \\hat{U}(\\vec{\\theta}) = && \\prod_{p > r} \\mathrm{exp} \\Big\\{ \\frac{i\\theta_{pr}}{2}
        \\bigotimes_{a=r+1}^{p-1} \\hat{Z}_a (\\hat{Y}_r \\hat{X}_p - \\mathrm{H.c.}) \\Big\\} \\\\\n        && \\times \\prod_{p > q > r > s} \\mathrm{exp} \\Big\\{ \\frac{i\\theta_{pqrs}}{8}
        \\bigotimes_{b=s+1}^{r-1} \\hat{Z}_b \\bigotimes_{a=q+1}^{p-1}
        \\hat{Z}_a (\\hat{X}_s \\hat{X}_r \\hat{Y}_q \\hat{X}_p +
        \\hat{Y}_s \\hat{X}_r \\hat{Y}_q \\hat{Y}_p +
        \\hat{X}_s \\hat{Y}_r \\hat{Y}_q \\hat{Y}_p +
        \\hat{X}_s \\hat{X}_r \\hat{X}_q \\hat{Y}_p -
        \\{\\mathrm{H.c.}\\}) \\Big\\}.


    :param weights : Size ``(len(s_wires) + len(d_wires),)`` tensor containing the parameters
        :math:`\\theta_{pr}` and :math:`\\theta_{pqrs}` entering the Z rotation in
        `FermionicSingleExcitation` and `FermionicDoubleExcitation`.
    :param wires: wires that the template acts on
    :param s_wires: Sequence of lists containing the wires ``[r,...,p]``
        resulting from the single excitation
        :math:`\\vert r, p \\rangle = \\hat{c}_p^\\dagger \\hat{c}_r \\vert \\mathrm{HF} \\rangle`,
        where :math:`\\vert \\mathrm{HF} \\rangle` denotes the Hartee-Fock reference state.
    :param d_wires: Sequence of lists, each containing two lists that
        specify the indices ``[s, ...,r]`` and ``[q,..., p]`` defining the double excitation
        :math:`\\vert s, r, q, p \\rangle = \\hat{c}_p^\\dagger \\hat{c}_q^\\dagger \\hat{c}_r
        \\hat{c}_s \\vert \\mathrm{HF} \\rangle`.
    :param init_state: Length ``len(wires)`` occupation-number vector representing the
        HF state. ``init_state`` is used to initialize the wires.
    :param qubits: quantum qubits allocated by pyqpanda.

    Examples::

        import pyqpanda as pq
        from pyvqnet.tensor import tensor
        from pyvqnet.qnn import UCCSD, expval
        machine = pq.CPUQVM()
        machine.init_qvm()
        qlists = machine.qAlloc_many(6)
        weight = tensor.zeros([8])
        cir = UCCSD(weight,wires = [0,1,2,3,4,5,6],
                                        s_wires=[[0, 1, 2], [0, 1, 2, 3, 4], [1, 2, 3], [1, 2, 3, 4, 5]],
                                        d_wires=[[[0, 1], [2, 3]], [[0, 1], [2, 3, 4, 5]], [[0, 1], [3, 4]], [[0, 1], [4, 5]]],
                                        init_state=[1, 1, 0, 0, 0, 0],
                                        qubits=qlists)

        prog = pq.QProg()
        prog.insert(cir)
        pauli_dict = {\'Z0\': 1}
        exp2 = expval(machine, prog, pauli_dict, qlists)
        print(f"vqnet {exp2}")
        #vqnet -1.0000000000000004

    '''
def BlockEncode(A, qlist): ...
