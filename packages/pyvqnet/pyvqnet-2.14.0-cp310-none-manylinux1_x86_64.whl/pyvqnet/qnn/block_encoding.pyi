from ..device import DEV_CPU as DEV_CPU
from ..tensor import QTensor as QTensor, tensor as tensor
from .vqc.block_encoding import qsvt as qsvt
from _typeshed import Incomplete

def gray_code(rank):
    """Generates the Gray code of given rank.

    Args:
        rank (int): rank of the Gray code (i.e. number of bits)
    """
def compute_theta(alpha):
    """Maps the angles alpha of the multi-controlled rotations decomposition of a uniformly controlled rotation
     to the rotation angles used in the Gray code implementation.

    Args:
        alpha (tensor_like): alpha parameters

    Returns:
        (tensor_like): rotation angles theta
    """

class QPANDA_FABLE:
    """
    Construct a pyQPanda QCircuit with the fast approximate block encoding method.

    The FABLE method allows to simplify block encoding circuits without reducing accuracy,
    for matrices of specific structure [`arXiv:2205.00081 <https://arxiv.org/abs/2205.00081>`_].


    :param input_matrix (tensor_like): a :math:`(2^n \\times 2^n)` matrix to be encoded,
            where :math:`n` is the number of wires used
    :param wires (Any or Iterable[Any]): qlist index that the operator acts on.

    Raises:
        ValueError: if the number of wires doesn't fit the dimensions of the matrix

    Example:: 

        from pyvqnet.qnn import QPANDA_FABLE
        import pyqpanda as pq
        import numpy as np

        qvm = pq.CPUQVM()
        qvm.init_qvm()

        qlist = qvm.qAlloc_many(3)
        A = np.array([[0.1, 0.2 ], [0.3, 0.4 ]]) 
        qf = QPANDA_FABLE(A, list(range(3)))
        qcir = qf.create_qcircuit(qlist,0.001)

        prog = pq.QProg()
        prog.insert(qcir)
        qvm.directly_run(prog)
        result = qvm.get_qstate()
        z = np.array(result)

    """
    wires: Incomplete
    input_matrix: Incomplete
    def __init__(self, input_matrix, wires) -> None: ...
    def create_qcircuit(self, qlist, tol: int = 0):
        """create pyqpanda circuit produced by the FABLE technique

        :param input_matrix (tensor_like): an :math:`(N \\times N)` matrix to be encoded
        :param tol (float): rotation gates that have an angle value smaller than this tolerance are removed,default:0.
        Return:
            pyqpanda qcircuit.
        """

def block_encoding_LCU(A, qlist, wires): ...

class QPANDA_LCU:
    """
    Construct a VQC based QCircuit with the Linear Combination of Unitaries (LCU), `Hamiltonian Simulation by Qubitization <https://arxiv.org/abs/1610.06546>`_.
    Input should be Hermitian.


    :param input_matrix: input Hermitian matrix.
    :param wires: wires order which the input matrix act on,excluding ancillary qubits .
    :param check_hermitian; check if input is Hermitian, defulat: True.

    Examples::

        from pyvqnet.qnn import QPANDA_LCU
        import pyqpanda as pq
        import numpy as np

        qvm = pq.CPUQVM()
        qvm.init_qvm()

        qlist = qvm.qAlloc_many(3)
        A = np.array([[0.25,0,0,0.75],[0,-0.25,0.75,0],[0,0.75,0.25,0],[0.75,0,0,-0.25]] )
        qf = QPANDA_LCU(A,[1,2])
        qcir = qf.create_qcircuit(qlist)

        prog = pq.QProg()
        prog.insert(qcir)
        qvm.directly_run(prog)
        result = qvm.get_qstate()
        z = np.array(result)
    """
    check_hermitian: Incomplete
    input_matrix: Incomplete
    wires: Incomplete
    def __init__(self, input_matrix, wires: Incomplete | None = None, check_hermitian: bool = True) -> None: ...
    def create_qcircuit(self, qlist):
        """create pyqpanda circuit produced by the LCU technique

        :param input_matrix (tensor_like): an :math:`(N \\times N)` matrix to be encoded
        :param qlist: qpanda qvm allcoates qubits vector, should have no less than length of np.log2(input_matrix.shape[0]) + ancillary qubits.
        
        Return:
            pyqpanda qcircuit.
        """

def sqrt_matrix(density_matrix): ...

class QPANDA_QSVT_Block_Encoding:
    """

    Construct a pyqpanda circuit of unitary :math:`U(A)` such that an arbitrary matrix :math:`A`
    is encoded in the top-left block.

    .. math::

        \\begin{align}
            U(A) &=
            \\begin{bmatrix}
                A & \\sqrt{I-AA^\\dagger} \\\\\n                \\sqrt{I-A^\\dagger A} & -A^\\dagger
            \\end{bmatrix}.
        \\end{align}

    :param A: input matrix to encode in the circuit.
    :param qlist: qpanda allocated qubits list.

    Example::

        from pyvqnet.tensor import QTensor
        import pyvqnet
        import pyqpanda as pq
        from pyvqnet.qnn import QPANDA_QSVT_Block_Encoding
        A = QTensor([[0.1, 0.2], [0.3, 0.4]], dtype=pyvqnet.kfloat32)
        machine = pq.CPUQVM()
        machine.init_qvm()
        qlist = machine.qAlloc_many(2)
        cbits = machine.cAlloc_many(2)

        cir = QPANDA_QSVT_Block_Encoding(A,qlists)
        cir = cir.create_qcircuit()

        prog = pq.QProg()
        prog.insert(cir)
        result = machine.directly_run(prog)
        print(cir)

        #           ┌───────────┐ 
        # q_0:  |0>─┤0          ├ 
        #           │  Unitary  │ 
        # q_1:  |0>─┤1          ├ 
        #           └───────────┘ 



    """
    u: Incomplete
    qlist: Incomplete
    def __init__(self, A, qlists) -> None: ...
    def create_qcircuit(self): ...

class QPANDA_QSVT:
    """
    Implements the
    `quantum singular value transformation <https://arxiv.org/abs/1806.01838>`__ (QSVT) circuit by pyQpanda QCircuits.
    
    Given an :class:`~.Operator` :math:`U`, which block encodes the matrix :math:`A`, and a list of
    projector-controlled phase shift operations :math:`\x0bec{\\Pi}_\\phi`, this template applies a
    circuit for the quantum singular value transformation as follows.

    When the number of projector-controlled phase shifts is even (:math:`d` is odd), the QSVT
    circuit is defined as:

    .. math::

        U_{QSVT} = \tilde{\\Pi}_{\\phi_1}U\\left[\\prod^{(d-1)/2}_{k=1}\\Pi_{\\phi_{2k}}U^\\dagger
        \tilde{\\Pi}_{\\phi_{2k+1}}U\right]\\Pi_{\\phi_{d+1}}.


    And when the number of projector-controlled phase shifts is odd (:math:`d` is even):

    .. math::

        U_{QSVT} = \\left[\\prod^{d/2}_{k=1}\\Pi_{\\phi_{2k-1}}U^\\dagger\tilde{\\Pi}_{\\phi_{2k}}U\right]
        \\Pi_{\\phi_{d+1}}.

    This circuit applies a polynomial transformation (:math:`Poly^{SV}`) to the singular values of
    the block encoded matrix:

    .. math::

        \x08egin{align}
             U_{QSVT}(A, \x0bec{\\phi}) &=
             \x08egin{bmatrix}
                Poly^{SV}(A) & \\cdot \\\n                \\cdot & \\cdot
            \\end{bmatrix}.
        \\end{align}


    :param A: a general :math:`(n \times m)` matrix to be encoded.
    :param angles: a list of angles by which to shift to obtain the desired polynomial.
    :param wires: the qubits index the A acts on.

    Example::

        from pyvqnet.qnn import QPANDA_QSVT
        import numpy as np
        import pyqpanda as pq
        A = np.array([[0.1, 0.2], [0.3, 0.4]])
        angles = np.array([0.1, 0.2, 0.3])
        qm = pq.CPUQVM()
        qm.init_qvm()
        qlist = qm.qAlloc_many(2)
        qsvt_layer = QPANDA_QSVT(A,angles,[0,1])
        cir = qsvt_layer.create_qcircuit(qlist=qlist)
        qporg = pq.QProg()
        qporg << cir
        qm.directly_run(qporg)
        result = np.array(qm.get_qstate())

    """
    A: Incomplete
    angles: Incomplete
    wires: Incomplete
    def __init__(self, A, angles, wires) -> None: ...
    def compute_ops(self): ...
    def create_qcircuit(self, qlist):
        """create pyqpanda QSVT circuit.

        :param qlist: qpanda qvm allcoates qubits vector.
        Return:
            pyqpanda qcircuit.
        """
