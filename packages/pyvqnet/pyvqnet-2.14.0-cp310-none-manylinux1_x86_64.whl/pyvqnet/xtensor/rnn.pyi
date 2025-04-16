from ..dtype import get_xtensor_dtype_str as get_xtensor_dtype_str
from .module import Module as Module
from .parameter import Parameter as Parameter
from .xtensor import XTensor as XTensor, concatenate as concatenate, flip as flip, index_select as index_select, matmul as matmul, permute as permute, relu as relu, reshape as reshape, tanh as tanh, unsqueeze as unsqueeze, zeros as zeros
from .xtensor_addon import PackedSequence as PackedSequence
from _typeshed import Incomplete

class RNN(Module):
    '''
    Applies a multi-layer simple RNN with :math:`\\tanh` or :math:`\\text{ReLU}` non-linearity to an
    input .

    For each element in the input , each layer computes the following
    function:

    .. math::
        h_t = \\tanh(W_{ih} x_t + b_{ih} + W_{hh} h_{(t-1)} + b_{hh})

    where :math:`h_t` is the hidden state at time `t`, :math:`x_t` is
    the input at time `t`, and :math:`h_{(t-1)}` is the hidden state of the
    previous layer at time `t-1` or the initial hidden state at time `0`.
    If :attr:`nonlinearity` is ``\'relu\'``, then :math:`\\text{ReLU}` is used instead of :math:`\\tanh`.

    :param input_size: Input feature dimension.
    :param hidden_size:  Hidden feature dimension.
    :param num_layers: Number of recurrent layers. Default: 1
    :param nonlinearity: nonlinearity function, `tanh` or `relu` , Default: `tanh`.
    :param batch_first: If True, input shape is provided as [batch_size,seq_len,feature_dim],
    if False, input shape is provided as [seq_len,batch_size,feature_dim],default True
    :param use_bias: If False, then the layer does not use bias weights b_ih and b_hh. Default: True.
    :param bidirectional: If RNN, becomes a bidirectional RNN. Default: False.
    :param dtype: data type of parameters,default: None,use default data type.
    :param name: name of module,default:"".

    :return: a RNN class

    '''
    backend: Incomplete
    mode: Incomplete
    n_inputs: Incomplete
    hidden_size: Incomplete
    concat_size: Incomplete
    batch_first: Incomplete
    num_layers: Incomplete
    use_bias: Incomplete
    num_directions: Incomplete
    def __init__(self, input_size, hidden_size, num_layers: int = 1, nonlinearity: str = 'tanh', batch_first: bool = True, use_bias: bool = True, bidirectional: bool = False, dtype: int | None = None, name: str = '') -> None: ...
    def reset_parameters(self) -> None: ...
    def __setattr__(self, attr, value) -> None: ...
    def step(self, x_t, h_t, w_list_in_l):
        """
        rnn formula impl
        """
    def forward(self, x, init_states: Incomplete | None = None):
        """
        x.shape is (batch_size, seq_length, feature_size)
        recurrent_activation -> sigmoid
        activation -> tanh
        """

class Dynamic_RNN(Module):
    '''
    Applies a multi-layer dynamic sequence legnth input RNN with :math:`\\tanh` or :math:`\\text{ReLU}` non-linearity to an
    input .

    The fisrt input should be a batched sequences input with variable length defined 
    by a ``tensor.PackedSequence`` class.
    The ``tensor.PackedSequence`` class could be construced by 
    Consecutive calling of the next functions: ``pad_sequence``, ``pack_pad_sequence``.

    The first output of Dynamic_RNN is also a ``tensor.PackedSequence`` class, 
    which can be unpacked to normal QTensor using ``tensor.pad_pack_sequence``.
 
    For each element in the input , each layer computes the following
    function:

    .. math::
        h_t = \\tanh(W_{ih} x_t + b_{ih} + W_{hh} h_{(t-1)} + b_{hh})

    where :math:`h_t` is the hidden state at time `t`, :math:`x_t` is
    the input at time `t`, and :math:`h_{(t-1)}` is the hidden state of the
    previous layer at time `t-1` or the initial hidden state at time `0`.
    If :attr:`nonlinearity` is ``\'relu\'``, then :math:`\\text{ReLU}` is used instead of :math:`\\tanh`.

    :param input_size: Input feature dimension.
    :param hidden_size:  Hidden feature dimension.
    :param num_layers: Number of recurrent layers. Default: 1.
    :param nonlinearity: nonlinearity function, `tanh` or `relu` , Default: `tanh`.
    :param batch_first: If True, input shape is provided as [batch_size,seq_len,feature_dim],
    if False, input shape is provided as [seq_len,batch_size,feature_dim],default True
    :param use_bias: If False, then the layer does not use bias weights b_ih and b_hh. Default: True.
    :param bidirectional: If RNN, becomes a bidirectional RNN. Default: False.

    :param dtype: data type of parameters,default: None,use default data type.
    :param name: name of module,default:"".
    :return: a Dynamic_RNN class

    '''
    backend: Incomplete
    mode: Incomplete
    n_inputs: Incomplete
    hidden_size: Incomplete
    concat_size: Incomplete
    batch_first: Incomplete
    num_layers: Incomplete
    use_bias: Incomplete
    num_directions: Incomplete
    def __init__(self, input_size, hidden_size, num_layers: int = 1, nonlinearity: str = 'tanh', batch_first: bool = True, use_bias: bool = True, bidirectional: bool = False, dtype: int | None = None, name: str = '') -> None: ...
    def reset_parameters(self) -> None: ...
    def __setattr__(self, attr, value) -> None: ...
    def step(self, x_t, h_t, w_list_in_l): ...
    def permute_hidden(self, hx: XTensor, permutation): ...
    def __call__(self, x, *args, **kwargs): ...
    def forward(self, x, init_states: Incomplete | None = None):
        """
        x.shape is (batch_size, seq_length, feature_size)
        recurrent_activation -> sigmoid
        activation -> tanh
        """

def reset_zeros(input_tensor, hidden_size) -> None: ...
def reset_layer_params(layer_input_size, hidden_size, use_bias, device, dtype: int | None = None): ...
def reset_params_names(layer, direction, use_bias): ...
