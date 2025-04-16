"""
Init for qnn
"""
# pylint: disable=redefined-builtin
from .measure import expval, expval_qcloud, ProbsMeasure,QuantumMeasure,\
    DensityMatrixFromQstate,VN_Entropy,Mutal_Info,Hermitian_expval,MeasurePauliSum,VarMeasure,Purity
from .quantumlayer import NoiseQuantumLayer,QuantumLayer,QuantumLayerWithQProg,\
    QuantumLayerMultiProcess,QuantumLayerV2,grad,\
        QuantumLayer_WITH_GRAD_DATA_PARALLED, QuantumBatchAsyncQcloudLayer, QuantumBatchAsyncQcloudLayerES, \
        QuantumBatchAsyncQPilotOSMachineLayer,QuantumLayerV3,\
        QpandaQCircuitVQCLayer,QpandaQCircuitVQCLayerLite,QpandaQProgVQCLayer


from .template import CSWAPcircuit,IQPEmbeddingCircuits,\
    AmplitudeEmbeddingCircuit,AngleEmbeddingCircuit,\
        RotCircuit,BasicEmbeddingCircuit,CRotCircuit,CCZ,Controlled_Hadamard,QuantumPoolingCircuit,\
            FermionicSingleExcitation,FermionicDoubleExcitation,BasisState,UCCSD,\
           StronglyEntanglingTemplate, BasicEntanglerTemplate,RandomTemplate,SimplifiedTwoDesignTemplate,FermionicSimulationGate,\
            Random_Init_Quantum_State,BlockEncode,ComplexEntangelingTemplate
from . import pqc, qae, qdrl, qgan, qlinear, qcnn, qvc, utils, svm, qp
from .opt import SPSA, QNG, insert_pauli_for_mt, get_metric_tensor, Gradient_Prune_Instance, quantum_fisher
from .qembed import Quantum_Embedding
from .mitigating import zne_with_poly_extrapolate

from .ansatz import HardwareEfficientAnsatz
from .ansatz import qnn_stack_layer
from .pq_utils import PQ_QCLOUD_UTILS
from .qft_arithemtics import pyqpanda_qft_add_to_register,pyqpanda_qft_mul,pyqpanda_qft_add_two_register
from .block_encoding import QPANDA_FABLE, QPANDA_LCU,QPANDA_QSVT_Block_Encoding,QPANDA_QSVT
