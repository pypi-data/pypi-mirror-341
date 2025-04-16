from . import Operation as Operation, QMachine as QMachine, apply_unitary_bmm as apply_unitary_bmm, load_measure_obs as load_measure_obs, op_history_to_modulelist as op_history_to_modulelist, operation_derivative as operation_derivative
from ... import nn as nn, tensor as tensor
from ...device import get_readable_device_str as get_readable_device_str
from ...dtype import complex_dtype_to_float_dtype as complex_dtype_to_float_dtype, get_readable_dtype_str as get_readable_dtype_str
from ...tensor import AutoGradNode as AutoGradNode, QTensor as QTensor, adjoint as adjoint
from .qmachine_utils import find_qmachine as find_qmachine
from _typeshed import Incomplete

def apply_operation(ket, op: Operation, if_adjoint: bool = False): ...
def adjoint_grad_calc(qm: QMachine, num_wires): ...

class QuantumLayerAdjoint(nn.Module):
    general_module: Incomplete
    qm: Incomplete
    def __init__(self, general_module: nn.Module, q_machine: QMachine, name: str = '') -> None:
        '''
        A python QuantumLayer wrapper for adjoint gradient calculation.
        Only support vqc module consists of single paramter quantum gates.

        :param general_module: a vqc nn.Module instance.
        :param q_machine: q_machine from general_module.
        :name name: name

        .. note::

            general_module\'s QMachine should set grad_method = "adjoint"

        Example::

            from pyvqnet import tensor
            from pyvqnet.qnn.vqc import QuantumLayerAdjoint, QMachine, RX, RY, CNOT, PauliX, qmatrix, PauliZ, T, MeasureAll, RZ, VQC_RotCircuit, VQC_HardwareEfficientAnsatz
            import pyvqnet


            class QModel(pyvqnet.nn.Module):
                def __init__(self, num_wires, dtype, grad_mode=""):
                    super(QModel, self).__init__()

                    self._num_wires = num_wires
                    self._dtype = dtype
                    self.qm = QMachine(num_wires, dtype=dtype, grad_mode=grad_mode)
                    self.rx_layer = RX(has_params=True, trainable=False, wires=0)
                    self.ry_layer = RY(has_params=True, trainable=False, wires=1)
                    self.rz_layer = RZ(has_params=True, trainable=False, wires=1)
                    self.rz_layer2 = RZ(has_params=True, trainable=True, wires=1)

                    self.rot = VQC_HardwareEfficientAnsatz(6, ["rx", "RY", "rz"],
                                                        entangle_gate="cnot",
                                                        entangle_rules="linear",
                                                        depth=5)
                    self.tlayer = T(wires=1)
                    self.cnot = CNOT(wires=[0, 1])
                    self.measure = MeasureAll(obs={
                        \'wires\': [1],
                        \'observables\': [\'x\'],
                        \'coefficient\': [1]
                    })

                def forward(self, x, *args, **kwargs):
                    self.qm.reset_states(x.shape[0])

                    self.rx_layer(params=x[:, [0]], q_machine=self.qm)
                    self.cnot(q_machine=self.qm)
                    self.ry_layer(params=x[:, [1]], q_machine=self.qm)
                    self.tlayer(q_machine=self.qm)
                    self.rz_layer(params=x[:, [2]], q_machine=self.qm)
                    self.rz_layer2(q_machine=self.qm)
                    self.rot(q_machine=self.qm)
                    rlt = self.measure(q_machine=self.qm)

                    return rlt


            input_x = tensor.QTensor([[0.1, 0.2, 0.3]])

            input_x = tensor.broadcast_to(input_x, [40, 3])

            input_x.requires_grad = True

            qunatum_model = QModel(num_wires=6,
                                dtype=pyvqnet.kcomplex64,
                                grad_mode="adjoint")

            adjoint_model = QuantumLayerAdjoint(qunatum_model, qunatum_model.qm)

            batch_y = adjoint_model(input_x)
            batch_y.backward()

        '''
    def forward(self, x, *args, **kwargs): ...
