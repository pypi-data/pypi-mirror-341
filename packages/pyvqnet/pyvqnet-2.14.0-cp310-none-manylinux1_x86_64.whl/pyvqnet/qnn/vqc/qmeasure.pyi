from ..measure import generate_basis_states as generate_basis_states, unique_wires as unique_wires
from .qcircuit import I as I, op_class_dict as op_class_dict, save_op_history as save_op_history
from .qmachine import QMachine as QMachine
from .qmatrix import COMPLEX_2_FLOAT as COMPLEX_2_FLOAT
from .qop import Observable as Observable
from .utils.utils import expand_matrix as expand_matrix, helper_parse_paulisum as helper_parse_paulisum, qpanda_paulisum_str_parse as qpanda_paulisum_str_parse, vqc_paulisum_str_parse as vqc_paulisum_str_parse
from _typeshed import Incomplete
from functools import reduce as reduce
from pyvqnet import tensor as tensor
from pyvqnet.dtype import dtype_map_from_numpy as dtype_map_from_numpy, kint64 as kint64
from pyvqnet.nn import Module as Module

def append_measure_proc(f): ...

class Measurements(Module):
    obs: Incomplete
    wires: Incomplete
    q_machine: Incomplete
    def __init__(self, wires: Incomplete | None = None, obs: Incomplete | None = None, name: str = '') -> None: ...

def flatten_state(state, num_wires):
    """
    Given a non-flat, potentially batched state, flatten it.

    Args:
        state (TensorLike): A state that needs flattening
        num_wires (int): The number of wires the state represents

    Returns:
        A flat state, with an extra batch dimension if necessary
    """

class Samples(Measurements):
    '''
    Get Samples result on specific wires with shots

    :param obs:Not valid.
    :param wires: sample qubits index.default:None.
    :param shots: sample repeat times,default:1.
    :param name: name of this module, defualt:"".

    Example::

        from pyvqnet.qnn.vqc import Samples,rx,ry,cnot,QMachine,rz
        from pyvqnet.tensor import kfloat64, QTensor
        x = QTensor([[0.56, 0.1],[0.56, 0.1]],requires_grad=True)

        qm = QMachine(4)
        qm.reset_states(2)
        rz(q_machine=qm,wires=0,params=x[:,[0]])
        rz(q_machine=qm,wires=1,params=x[:,[0]])
        cnot(q_machine=qm,wires=[0,1])
        ry(q_machine=qm,wires=2,params=x[:,[1]])
        cnot(q_machine=qm,wires=[0,2])
        rz(q_machine=qm,wires=3,params=x[:,[1]])


        ma = Samples(wires=[0,1,2],shots=3)
        y =ma(q_machine=qm)
        print(y)
    '''
    obs: Incomplete
    wires: Incomplete
    q_machine: Incomplete
    shots: Incomplete
    def __init__(self, wires: Incomplete | None = None, obs: Incomplete | None = None, shots: int = 1, name: str = '') -> None: ...
    def measure_sample(self, samples, wire_order): ...
    def sample_state(self, q_machine): ...
    def forward(self, q_machine: QMachine): ...
    def __call__(self, *args, **kwargs): ...

class Probability(Measurements):
    """
    the wrap class of Probability measure.
    
    :param wires: The idx of qubit。

    :return: measure result。

    Example::
        
        from pyvqnet.qnn.vqc import Probability,rx,ry,cnot,QMachine,rz
        from pyvqnet.tensor import kfloat64, QTensor
        x = QTensor([[0.56, 0.1],[0.56, 0.1]],requires_grad=True)
        qm = QMachine(4)
        qm.reset_states(2)
        rz(q_machine=qm,wires=0,params=x[:,[0]])
        rz(q_machine=qm,wires=1,params=x[:,[0]])
        cnot(q_machine=qm,wires=[0,1])
        ry(q_machine=qm,wires=2,params=x[:,[1]])
        cnot(q_machine=qm,wires=[0,2])
        rz(q_machine=qm,wires=3,params=x[:,[1]])
        ma = Probability(wires = 1)
        y =ma(q_machine=qm)

        # [[1.0000002 0.       ]
        #  [1.0000002 0.       ]]        

    """
    q_machine: Incomplete
    def __init__(self, wires, name: str = '') -> None: ...
    def forward(self, q_machine: QMachine): ...
    def __call__(self, *args, **kwargs): ...

def expval(q_machine: QMachine, wires: int | list[int], observables: Observable | list[Observable]): ...
def sparse_hamiltonian_run(batch_states, H, wires): ...

class SparseHamiltonian(Measurements):
    '''
    calculate Sparse Hamiltonian of observables like {"observables":H,"wires":[0,2,3]}.

    :param obs:observables like {"observables":H,"wires":[0,2,3]}.

    Example::

        import pyvqnet
        pyvqnet.utils.set_random_seed(42)
        from pyvqnet import tensor
        from pyvqnet.nn import Module
        from pyvqnet.qnn.vqc import QMachine,CRX,PauliX,paulix,crx,SparseHamiltonian
        H = tensor.QTensor(
        [[ 0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,
        0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j, -1.+0.j,],
        [ 0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,
        0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  1.+0.j,  0.+0.j,],
        [ 0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,
        0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  1.+0.j,  0.+0.j,  0.+0.j,],
        [ 0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,
        0.+0.j,  0.+0.j,  0.+0.j, -1.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,],
        [ 0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,
        0.+0.j,  0.+0.j, -1.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,],
        [ 0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,
        0.+0.j,  1.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,],
        [ 0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,
        1.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,],
        [ 0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j, -1.+0.j,
        0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,],
        [ 0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j, -1.+0.j,  0.+0.j,
        0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,],
        [ 0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  1.+0.j,  0.+0.j,  0.+0.j,
        0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,],
        [ 0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  1.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,
        0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,],
        [ 0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j, -1.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,
        0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,],
        [ 0.+0.j,  0.+0.j,  0.+0.j, -1.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,
        0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,],
        [ 0.+0.j,  0.+0.j,  1.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,
        0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,],
        [ 0.+0.j,  1.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,
        0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,],
        [-1.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,
        0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,]],dtype=pyvqnet.kcomplex64)
        cpu_csr = tensor.dense_to_csr(H)
        class QModel(Module):
            def __init__(self, num_wires, dtype,grad_mode=""):
                super(QModel, self).__init__()

                self._num_wires = num_wires
                self._dtype = dtype
                self.qm = QMachine(num_wires)
                self.measure = SparseHamiltonian(obs = {"observables":cpu_csr, "wires":[2, 1, 3, 5]})


            def forward(self, x, *args, **kwargs):
                self.qm.reset_states(x.shape[0])
                paulix(q_machine=self.qm, wires= 0)
                paulix(q_machine=self.qm, wires = 2)
                crx(q_machine=self.qm,wires=[0, 1],params=tensor.full((x.shape[0],1),0.1,dtype=pyvqnet.kcomplex64))
                crx(q_machine=self.qm,wires=[2, 3],params=tensor.full((x.shape[0],1),0.2,dtype=pyvqnet.kcomplex64))
                crx(q_machine=self.qm,wires=[1, 2],params=tensor.full((x.shape[0],1),0.3,dtype=pyvqnet.kcomplex64))
                crx(q_machine=self.qm,wires=[2, 4],params=tensor.full((x.shape[0],1),0.3,dtype=pyvqnet.kcomplex64))
                crx(q_machine=self.qm,wires=[5, 3],params=tensor.full((x.shape[0],1),0.3,dtype=pyvqnet.kcomplex64))
                
                rlt = self.measure(q_machine=self.qm)
                return rlt

        model = QModel(6,pyvqnet.kcomplex64)
        y = model(tensor.ones([1,1]))
        #y.backward()
        print(y)
    '''
    q_machine: Incomplete
    def __init__(self, obs, name: str = '') -> None: ...
    def measure_fun(self, q_machine: QMachine, obs): ...
    def forward(self, q_machine: QMachine): ...
    def __call__(self, *args, **kwargs): ...

class HermitianExpval(Measurements):
    """
    Create a module to Obtain the expectation value of all the qubits based on Hermitian observables.
    Hermitian observables should be [2**len(wires), 2**len(wires)].

    
    :param obs: Hermitian observables,valid input such as 
    {`wires`:[1,0],
    `observables`:H = QTensor([[8, 4, 0, -6], [4, 0, 4, 0], [0, 4, 8, 0], [-6, 0, 0, 0]])}.
    :return:
        exepectation of Hermitian matrix.

    Example::


        from pyvqnet.qnn.vqc import qcircuit
        from pyvqnet.qnn.vqc import QMachine, RX, RY, CNOT, PauliX, qmatrix, PauliZ, VQC_RotCircuit,HermitianExpval
        from pyvqnet.tensor import QTensor, tensor
        import pyvqnet
        from pyvqnet.nn import Parameter
        import numpy as np
        bsz = 3
        H = np.array([[8, 4, 0, -6], [4, 0, 4, 0], [0, 4, 8, 0], [-6, 0, 0, 0]])
        class QModel(pyvqnet.nn.Module):
            def __init__(self, num_wires, dtype):
                super(QModel, self).__init__()
                self.rot_param = Parameter((3, ))
                self.rot_param.copy_value_from(tensor.QTensor([-0.5, 1, 2.3]))
                self._num_wires = num_wires
                self._dtype = dtype
                self.qm = QMachine(num_wires, dtype=dtype)
                self.rx_layer1 = VQC_RotCircuit
                self.ry_layer2 = RY(has_params=True,
                                    trainable=True,
                                    wires=0,
                                    init_params=tensor.QTensor([-0.5]))
                self.xlayer = PauliX(wires=0)
                self.cnot = CNOT(wires=[0, 1])
                self.measure = HermitianExpval(obs = {'wires':(1,0),'observables':tensor.to_tensor(H)})

            def forward(self, x, *args, **kwargs):
                self.qm.reset_states(x.shape[0])

                qcircuit.rx(q_machine=self.qm, wires=0, params=x[:, [1]])
                qcircuit.ry(q_machine=self.qm, wires=1, params=x[:, [0]])
                self.xlayer(q_machine=self.qm)
                self.rx_layer1(params=self.rot_param, wire=1, q_machine=self.qm)
                self.ry_layer2(q_machine=self.qm)
                self.cnot(q_machine=self.qm)
                rlt = self.measure(q_machine = self.qm)

                return rlt


        input_x = tensor.arange(1, bsz * 2 + 1,
                                dtype=pyvqnet.kfloat32).reshape([bsz, 2])
        input_x.requires_grad = True

        qunatum_model = QModel(num_wires=2, dtype=pyvqnet.kcomplex64)

        batch_y = qunatum_model(input_x)
        batch_y.backward()

        print(batch_y)


        # [[5.3798223],
        #  [7.1294155],
        #  [0.7028297]]

    """
    q_machine: Incomplete
    def __init__(self, obs, name: str = '') -> None: ...
    def measure_fun(self, q_machine: QMachine, obs): ...
    def forward(self, q_machine: QMachine): ...
    def __call__(self, *args, **kwargs): ...

class MeasureAll(Measurements):
    """
    Obtain the expectation value of all the qubits based on Pauli opearators.
    If measure the observable like:
    {'wires': [0,  1], 'observables': ['x', 'i'],'coefficient':[0.23,-3.5]} or {'X0': 0.23}.

    If measure the Paulisum observales, use:
        [{
        'wires': [0, 2, 3],
        'observables': ['X', 'Y', 'Z'],
        'coefficient': [1, 0.5, 0.4]
    }, {
        'wires': [0, 1, 2],
        'observables': ['X', 'Y', 'Z'],
        'coefficient': [1, 0.5, 0.4]
    }]

    :param obs: observable
    :return: measure result.

    Example::

        from pyvqnet.qnn.vqc import MeasureAll,rx,ry,cnot,QMachine,rz
        from pyvqnet.tensor import kfloat64, QTensor
        x = QTensor([[0.56, 0.1],[0.56, 0.1]],requires_grad=True)

        qm = QMachine(4)
        qm.reset_states(2)
        rz(q_machine=qm,wires=0,params=x[:,[0]])
        rz(q_machine=qm,wires=1,params=x[:,[0]])
        cnot(q_machine=qm,wires=[0,1])
        ry(q_machine=qm,wires=2,params=x[:,[1]])
        cnot(q_machine=qm,wires=[0,2])
        rz(q_machine=qm,wires=3,params=x[:,[1]])

        obs_list = [{
            'wires': [0, 2, 3],
            'observables': ['X', 'Y', 'Z'],
            'coefficient': [1, 0.5, 0.4]
        }, {
            'wires': [0, 1, 2],
            'observables': ['X', 'Y', 'Z'],
            'coefficient': [1, 0.5, 0.4]
        }]
        ma = MeasureAll(obs=obs_list)
        y =ma(q_machine=qm)

        # [[0.4000001 0.3980018]
        #  [0.4000001 0.3980018]]
    """
    q_machine: Incomplete
    def __init__(self, *, obs, name: str = '') -> None: ...
    def measure_fun(self, q_machine: QMachine, obs): ...
    def forward(self, q_machine: QMachine): ...
    def __call__(self, *args, **kwargs): ...

def vqc_purity(state, qubits_idx, num_wires):
    """
    Computes the purity from a state vector.

    .. math::
        \\gamma = \text{Tr}(\rho^2)

    where :math:`\rho` is the density matrix. The purity of a normalized quantum state satisfies
    :math:`\x0crac{1}{d} \\leq \\gamma \\leq 1`, where :math:`d` is the dimension of the Hilbert space.
    A pure state has a purity of 1.

    :param state: quantum state from pyqpanda get_qstate()
    :param qubits_idx:List of indices in the considered subsystem.
    :param num_wires: number of wires.
    :return:
            purity

    Examples::

        from pyvqnet.qnn.vqc import VQC_Purity, rx, ry, cnot, QMachine
        from pyvqnet.tensor import kfloat64, QTensor
        x = QTensor([[0.7, 0.4], [1.7, 2.4]], requires_grad=True)

        qm = QMachine(3)
        qm.reset_states(2)
        rx(q_machine=qm, wires=0, params=x[:, [0]])
        ry(q_machine=qm, wires=1, params=x[:, [1]])
        ry(q_machine=qm, wires=2, params=x[:, [1]])
        cnot(q_machine=qm, wires=[0, 1])
        cnot(q_machine=qm, wires=[2, 1])
        y = VQC_Purity(qm.states, [0, 1], num_wires=3)
        y.backward()
        print(y)

        # [0.9356751 0.875957 ]
    """
VQC_Purity = vqc_purity

def vqc_partial_trace(state, indices):
    """Compute the partial trace from a state vector.

        :param state: quantum state from QMachine.
        :param indices: - List of indices in the considered subsystem.

        :return: XTensor of partial trace 
    """
VQC_PartialTrace = vqc_partial_trace

def vqc_meyer_wallach_measure(state):
    """
        Return the values of entanglement capability using meyer-wallach measure.

        :param state: quantum states from QMachine.states
        :return: XTensor of meyer-wallach measure.
    """
VQC_MeyerWallachMeasure = vqc_meyer_wallach_measure

def vqc_var_measure(q_machine, obs):
    """
        Compute the Variance of the supplied observable from a q_machine.

        :param q_machine: quantum machine
        :param wires: - List of indices in the considered subsystem.
        :return: variance of q_machine ,size= (batch,1)

    Exmaple::

        from pyvqnet.tensor import QTensor
        from pyvqnet.qnn.vqc import VQC_VarMeasure, rx, cnot, hadamard, QMachine,PauliY

        x = QTensor([[0.5]], requires_grad=True)
        qm = QMachine(3)

        rx(q_machine=qm, wires=0, params=x)

        var_result = VQC_VarMeasure(q_machine= qm, obs=PauliY(wires=0))

        var_result.backward()
        print(var_result)

        # [[0.7701511]]
    """
VQC_VarMeasure = vqc_var_measure

def vqc_densitymatrixfromqstate(state, indices):
    """Compute the density matrix from a state vector.

    :param state: batch state vector. This list should of size ``(batch,2,...2)`` for some integer value ``N``.qstate should start from 000 ->111
    :param indices: - List of indices in the considered subsystem.
    :return: Density matrix of size ``(batch_size, 2**len(indices), 2**len(indices))``

    Example::

        from pyvqnet.qnn.vqc import VQC_DensityMatrixFromQstate,rx,ry,cnot,QMachine
        from pyvqnet.tensor import kfloat64, QTensor
        x = QTensor([[0.7,0.4],[1.7,2.4]],requires_grad=True)

        qm = QMachine(3)
        qm.reset_states(2)
        rx(q_machine=qm,wires=0,params=x[:,[0]])
        ry(q_machine=qm,wires=1,params=x[:,[1]])
        ry(q_machine=qm,wires=2,params=x[:,[1]])
        cnot(q_machine=qm,wires=[0,1])
        cnot(q_machine=qm,wires=[2, 1])
        y = VQC_DensityMatrixFromQstate(qm.states,[0,1])
        print(y)

        # [[[0.8155131+0.j        0.1718155+0.j        0.       +0.0627175j
        #   0.       +0.2976855j]
        #  [0.1718155+0.j        0.0669081+0.j        0.       +0.0244234j
        #   0.       +0.0627175j]
        #  [0.       -0.0627175j 0.       -0.0244234j 0.0089152+0.j
        #   0.0228937+0.j       ]
        #  [0.       -0.2976855j 0.       -0.0627175j 0.0228937+0.j
        #   0.1086637+0.j       ]]
        # 
        # [[0.3362115+0.j        0.1471083+0.j        0.       +0.1674582j
        #   0.       +0.3827205j]
        #  [0.1471083+0.j        0.0993662+0.j        0.       +0.1131119j
        #   0.       +0.1674582j]
        #  [0.       -0.1674582j 0.       -0.1131119j 0.1287589+0.j
        #   0.1906232+0.j       ]
        #  [0.       -0.3827205j 0.       -0.1674582j 0.1906232+0.j
        #   0.4356633+0.j       ]]]   

    """
VQC_DensityMatrixFromQstate = vqc_densitymatrixfromqstate

def vqc_density_matrix(q_machine, indices):
    """Compute the density matrix from a state vector.

    :param q_machine: quantum machine.
    :param indices: - List of indices in the considered subsystem.
    :return: Density matrix of size ``(2**len(indices), 2**len(indices))``

    Example::

        from pyvqnet.qnn.vqc import VQC_DensityMatrixFromQstate,rx,ry,cnot,QMachine
        from pyvqnet.tensor import kfloat64, QTensor
        x = QTensor([[0.7,0.4],[1.7,2.4]],requires_grad=True)

        qm = QMachine(3)
        qm.reset_states(2)
        rx(q_machine=qm,wires=0,params=x[:,[0]])
        ry(q_machine=qm,wires=1,params=x[:,[1]])
        ry(q_machine=qm,wires=2,params=x[:,[1]])
        cnot(q_machine=qm,wires=[0,1])
        cnot(q_machine=qm,wires=[2, 1])
        y = VQC_DensityMatrix(qm,[0,1])

    """
VQC_DensityMatrix = vqc_density_matrix

def vqc_mutal_info(q_machine, indices0, indices1, base: Incomplete | None = None):
    """Compute the mutual information between two subsystems given a state:

    .. math::

        I(A, B) = S(\\rho^A) + S(\\rho^B) - S(\\rho^{AB})

    where :math:`S` is the von Neumann entropy.

    The mutual information is a measure of correlation between two subsystems.
    More specifically, it quantifies the amount of information obtained about
    one system by measuring the other system.

    Each state can be given as a state vector in the computational basis, or
    as a density matrix.

    :param q_machine: quantum machine.
    :param indices0: - List of indices in the first subsystem.
    :param indices1: - List of indices in the second subsystem.
    :param base: Base for the logarithm. If None, the natural logarithm is used.

    :return: Mutual information between the subsystems

    Example::


    """
VQC_Mutal_Info = vqc_mutal_info

def vqc_vn_entropy(q_machine, indices, base: Incomplete | None = None):
    """Compute the Von Neumann entropy from a state vector or density matrix on a given qubits list.

    .. math::
        S( \\rho ) = -\\text{Tr}( \\rho \\log ( \\rho ))

    :param q_machine: quantum machine.
    :param indices: - List of indices in the considered subsystem.
    :param base: Base for the logarithm. If None, the natural logarithm is used.

    :return: float value of  Von Neumann entropy

    Example::

        from pyvqnet.qnn.vqc import VQC_VN_Entropy, rx, ry, cnot, QMachine
        from pyvqnet.tensor import kfloat64, QTensor

        x = QTensor([[0.2, 0.4], [1.7, 2.4]], requires_grad=True)

        qm = QMachine(3)
        qm.reset_states(2)
        rx(q_machine=qm, wires=0, params=x[:, [0]])
        ry(q_machine=qm, wires=1, params=x[:, [1]])
        ry(q_machine=qm, wires=2, params=x[:, [1]])
        cnot(q_machine=qm, wires=[0, 1])
        cnot(q_machine=qm, wires=[2, 1])
        y = VQC_VN_Entropy(qm, [0, 2])

    """
VQC_VN_Entropy = vqc_vn_entropy

def hermitian_expval(H, state: tensor.QTensor, wires):
    """
    input a Hermitian matrix acted on `wires`, return analytic expectation of quantum states.
    
    Supports batch input like [b,2,2...] on CPU/GPU

    :param H: Hermitian matrix of shape [2,2,..].
    :param state: batch quantum state.
    :param wires: the Hermitian matrix acts on.
    :return:
        exepectation of Hermitian matrix.
    """
Hermitian_expval = hermitian_expval
measure_name_dict: Incomplete
