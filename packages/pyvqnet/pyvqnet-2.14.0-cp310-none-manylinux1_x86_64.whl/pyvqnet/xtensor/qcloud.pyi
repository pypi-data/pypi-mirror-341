from .module import Module as Module
from .parameter import Parameter as Parameter, quantum_uniform as quantum_uniform
from .pq_utils import PQ_QCLOUD_UTILS as PQ_QCLOUD_UTILS, get_measure_number_from_ir as get_measure_number_from_ir
from .xtensor import XTensor as XTensor, cat as cat, xtensor as xtensor
from _typeshed import Incomplete
from pyvqnet.device import DEV_CPU as DEV_CPU, DEV_GPU as DEV_GPU
from typing import Callable

class QuantumBatchAsyncQcloudLayer(Module):
    '''

    Abstract Calculation module for originqc real chip using pyqpanda QCLOUD from version 3.8.2.2. It submit parameterized quantum
    circuits to real chip and get the measurement result.

    :param origin_qprog_func: callable quantum circuits function constructed by QPanda.
    :param qcloud_token: `str` - Either the type of quantum machine or the cloud token for execution.
    :param para_num: `int` - Number of parameters; parameters are one-dimensional.
    :param num_qubits: `int` - Number of qubits in the quantum circuit.
    :param num_cubits: `int` - Number of classical bits for measurement in the quantum circuit.
    :param pauli_str_dict: `dict|list` - Dictionary or list of dictionary representing the Pauli operators in the quantum circuit. Default is None.
    :param shots: `int` - Number of measurement shots. Default is 1000.
    :param initializer: Initializer for parameter values. Default is None.
    :param dtype: Data type of parameters. Default is None, which uses the default data type.
    :param name: Name of the module. Default is an empty string.
    :param diff_method: Differentiation method for gradient computation. Default is "parameter_shift".
    :param submit_kwargs: Additional keyword arguments for submitting quantum circuits,
    default:{"chip_id":pyqpanda.real_chip_type.origin_72,"is_amend":True,"is_mapping":True,
    "is_optimization": True,"default_task_group_size":200,"test_qcloud_fake":True}.
    :param query_kwargs: Additional keyword arguments for querying quantum results，default:{"timeout":2,"print_query_info":True,"sub_circuits_split_size":1}.
    :return: A module that can calculate quantum circuits.

    Examples::

        from pyqpanda import *

        import pyqpanda as pq
        from pyvqnet.xtensor.qcloud import QuantumBatchAsyncQcloudLayer
        from pyvqnet.xtensor.autograd import tape
        from pyvqnet.xtensor import arange,XTensor,ones,ones_like


        def qfun(input,param, m_machine, m_qlist,cubits):
                measure_qubits = [0,2]
                m_prog = pq.QProg()
                cir = pq.QCircuit()
                cir.insert(pq.RZ(m_qlist[0],input[0]))
                cir.insert(pq.CNOT(m_qlist[0],m_qlist[1]))
                cir.insert(pq.RY(m_qlist[1],param[0]))
                cir.insert(pq.CNOT(m_qlist[0],m_qlist[2]))
                cir.insert(pq.RZ(m_qlist[1],input[1]))
                cir.insert(pq.RY(m_qlist[2],param[1]))
                cir.insert(pq.RZ(m_qlist[2],param[2]))
                cir.insert(pq.RZ(m_qlist[2],param[3]))
                cir.insert(pq.RZ(m_qlist[1],param[4]))

                cir.insert(pq.H(m_qlist[2]))
                m_prog.insert(cir)


                return m_prog

        l = QuantumBatchAsyncQcloudLayer(qfun,
                    "302e020100301006072a8648ce3d020106052b8104001c041730150201010410def6ef7286d4a2fd143ea10e2de4638f/12570",
                    5,
                    6,
                    6,
                    pauli_str_dict=[{\'Z0 X1\':1,\'Y2\':1},{\'Y2\':1},{\'Z0 X1\':1,\'Y2\':1,\'X2\':1}],#{\'Z0 X1\':1,\'Y2\':1},#,
                    shots = 1000,
                    initializer=None,
                    dtype=None,
                    name="",
                    diff_method="parameter_shift",
                    submit_kwargs={"test_qcloud_fake":True},
                    query_kwargs={})


        x = XTensor([[0.56,1.2],[0.56,1.2],[0.56,1.2]],requires_grad= True)

        with tape():
            y = l(x)

        print(y)
        y.backward(ones_like(y))

        print(x.grad)
        print(l.m_para.grad)

        # [[-0.2554    -0.2038    -1.1429999]
        #  [-0.2936    -0.2082    -1.127    ]
        #  [-0.3144    -0.1812    -1.1208   ]]
        # <XTensor 3x3 cpu(0) kfloat32>

        # [[ 0.0241    -0.6001   ]
        #  [-0.0017    -0.5624   ]
        #  [ 0.0029999 -0.6071001]]
        # <XTensor 3x2 cpu(0) kfloat32>

        # [-1.5474    -1.0477002 -4.5562    -4.6365    -1.7573001]
        # <XTensor 5 cpu(0) kfloat32>

    '''
    backend: Incomplete
    m_prog_func: Incomplete
    m_para: Incomplete
    num_para: Incomplete
    pauli_str_dict: Incomplete
    pq_utils: Incomplete
    history_expectation: Incomplete
    submit_task_asyn_batched: Incomplete
    submit_kwargs: Incomplete
    query_kwargs: Incomplete
    shots: Incomplete
    grad_have_calc_ed: int
    w_grad_have_calc: int
    x_grad_have_calc: int
    num_qubits: Incomplete
    num_cubits: Incomplete
    qcloud_token: Incomplete
    m_machine: Incomplete
    qlists: Incomplete
    clists: Incomplete
    def __init__(self, origin_qprog_func: Callable, qcloud_token: str, para_num: int, num_qubits: int, num_cubits: int, pauli_str_dict: None | dict | list[dict] = None, shots: int = 1000, initializer: Callable = None, dtype: int | None = None, name: str = '', diff_method: str = 'parameter_shift', submit_kwargs: dict = {}, query_kwargs: dict = {}) -> None: ...
    def forward(self, x: XTensor): ...
