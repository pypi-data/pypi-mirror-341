from .module import Module as Module
from .parameter import Parameter as Parameter
from .xtensor import XTensor as XTensor, concatenate as concatenate, flip as flip, index_select as index_select, matmul as matmul, permute as permute, relu as relu, reshape as reshape, sigmoid as sigmoid, tanh as tanh, unsqueeze as unsqueeze, zeros as zeros
from .xtensor_addon import PackedSequence as PackedSequence
from _typeshed import Incomplete

class GRU(Module):
    '''
    Applies a multi-layer gated recurrent unit (GRU) RNN to an input sequence.

    For each element in the input sequence, each layer computes the following
    function:

    .. math::
        \\begin{array}{ll}
            r_t = \\sigma(W_{ir} x_t + b_{ir} + W_{hr} h_{(t-1)} + b_{hr}) \\\\\n            z_t = \\sigma(W_{iz} x_t + b_{iz} + W_{hz} h_{(t-1)} + b_{hz}) \\\\\n            n_t = \\tanh(W_{in} x_t + b_{in} + r_t * (W_{hn} h_{(t-1)}+ b_{hn})) \\\\\n            h_t = (1 - z_t) * n_t + z_t * h_{(t-1)}
        \\end{array}

    :param input_size: Input feature dimension.
    :param hidden_size: Hidden feature dimension.
    :param num_layers: Number of recurrent layers. Default: 1
    :param batch_first: If True, input shape is provided as [batch_size,seq_len,feature_dim],
    if False, input shape is provided as [seq_len,batch_size,feature_dim],default True
    :param use_bias: If False, then the layer does not use bias weights b_ih and b_hh. Default: True.
    :param bidirectional: If True, becomes a bidirectional GRU. Default: False.
    :param dtype: data type of parameters,default: None,use default data type.
    :param name: name of module,default:"".

    :return: a GRU class

        '''
    backend: Incomplete
    n_inputs: Incomplete
    hidden_size: Incomplete
    concat_size: Incomplete
    batch_first: Incomplete
    num_layers: Incomplete
    use_bias: Incomplete
    num_directions: Incomplete
    def __init__(self, input_size, hidden_size, num_layers: int = 1, batch_first: bool = True, use_bias: bool = True, bidirectional: bool = False, dtype: int | None = None, name: str = '') -> None: ...
    def reset_parameters(self) -> None: ...
    def __setattr__(self, attr, value) -> None: ...
    def step(self, x_t, h_t, w_list_in_l): ...
    def forward(self, x, init_states: Incomplete | None = None):
        """

        """

class Dynamic_GRU(Module):
    '''
    Applies a multi-layer gated recurrent unit (GRU) RNN to an dyanmaic length input sequence.

    The fisrt input should be a batched sequences input with variable length defined 
    by a ``tensor.PackedSequence`` class.
    The ``tensor.PackedSequence`` class could be construced by 
    Consecutive calling of the next functions: ``pad_sequence``, ``pack_pad_sequence``.

    The first output of Dynamic_GRU is also a ``tensor.PackedSequence`` class, 
    which can be unpacked to normal QTensor using ``tensor.pad_pack_sequence``.

    For each element in the input sequence, each layer computes the following
    function:

    .. math::
        \\begin{array}{ll}
            r_t = \\sigma(W_{ir} x_t + b_{ir} + W_{hr} h_{(t-1)} + b_{hr}) \\\\\n            z_t = \\sigma(W_{iz} x_t + b_{iz} + W_{hz} h_{(t-1)} + b_{hz}) \\\\\n            n_t = \\tanh(W_{in} x_t + b_{in} + r_t * (W_{hn} h_{(t-1)}+ b_{hn})) \\\\\n            h_t = (1 - z_t) * n_t + z_t * h_{(t-1)}
        \\end{array}

    :param input_size: Input feature dimension.
    :param hidden_size: Hidden feature dimension.
    :param num_layers: Number of recurrent layers. Default: 1
    :param batch_first: If True, input shape is provided as [batch_size,seq_len,feature_dim],
    if False, input shape is provided as [seq_len,batch_size,feature_dim],default True
    :param use_bias: If False, then the layer does not use bias weights b_ih and b_hh. Default: True.
    :param bidirectional: If True, becomes a bidirectional GRU. Default: False.

    :param dtype: data type of parameters,default: None,use default data type.
    :param name: name of module,default:"".
    :return: a Dynamic_GRU class


        '''
    backend: Incomplete
    n_inputs: Incomplete
    hidden_size: Incomplete
    concat_size: Incomplete
    batch_first: Incomplete
    num_layers: Incomplete
    use_bias: Incomplete
    num_directions: Incomplete
    def __init__(self, input_size, hidden_size, num_layers: int = 1, batch_first: bool = True, use_bias: bool = True, bidirectional: bool = False, dtype: int | None = None, name: str = '') -> None: ...
    def reset_parameters(self) -> None: ...
    def __setattr__(self, attr, value) -> None: ...
    def step(self, x_t, h_t, w_list_in_l): ...
    def permute_hidden(self, hx: XTensor, permutation: list): ...
    def __call__(self, x, *args, **kwargs): ...
    def forward(self, x, init_states: Incomplete | None = None):
        """
        x.shape is (batch_size, seq_length, feature_size)
        recurrent_activation -> sigmoid
        activation -> tanh
        """

def reset_zeros(input_tensor, hidden_size) -> None: ...
def reset_param_names(layer, direction, use_bias): ...
def reset_layer_params(layer_input_size, hidden_size, use_bias, device, dtype: int | None = None): ...
