from .module import Module as Module
from .parameter import Parameter as Parameter
from .xtensor import XTensor as XTensor, concatenate as concatenate, flip as flip, index_select as index_select, matmul as matmul, permute as permute, relu as relu, reshape as reshape, sigmoid as sigmoid, tanh as tanh, unsqueeze as unsqueeze, zeros as zeros
from .xtensor_addon import PackedSequence as PackedSequence
from _typeshed import Incomplete

class Dynamic_LSTM(Module):
    '''
    Applies a multi-layer dynamic sequence legnth input LSTM(Long Short Term Memory) Module.

    The fisrt input should be a batched sequences input with variable length defined 
    by a ``tensor.PackedSequence`` class.
    The ``tensor.PackedSequence`` class could be construced by 
    Consecutive calling of the next functions: ``pad_sequence``, ``pack_pad_sequence``.

    The first output of Dynamic_LSTM is also a ``tensor.PackedSequence`` class, 
    which can be unpacked to normal QTensor using ``tensor.pad_pack_sequence``.
    
    Each call computes the following function:

    .. math::
        \x08egin{array}{ll} \\\n            i_t = \\sigma(W_{ii} x_t + b_{ii} + W_{hi} h_{t-1} + b_{hi}) \\\n            f_t = \\sigma(W_{if} x_t + b_{if} + W_{hf} h_{t-1} + b_{hf}) \\\n            g_t = \tanh(W_{ig} x_t + b_{ig} + W_{hg} h_{t-1} + b_{hg}) \\\n            o_t = \\sigma(W_{io} x_t + b_{io} + W_{ho} h_{t-1} + b_{ho}) \\\n            c_t = f_t \\odot c_{t-1} + i_t \\odot g_t \\\n            h_t = o_t \\odot \tanh(c_t) \\\n        \\end{array}

    :param input_size: Input feature dimension.
    :param hidden_size:  Hidden feature dimension.
    :param num_layers: Number of recurrent layers. Default: 1
    :param batch_first: If True, input shape is provided as [batch_size,seq_len,feature_dim],
    if False, input shape is provided as [seq_len,batch_size,feature_dim],default True
    :param use_bias: If False, then the layer does not use bias weights b_ih and b_hh. Default: True.
    :param bidirectional: If True, becomes a bidirectional LSTM. Default: False.

    :param dtype: data type of parameters,default: None,use default data type.
    :param name: name of module,default:"".
    :return: a LSTM class

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
    def step(self, x_t, h_t, c_t, w_list_in_l): ...
    def __call__(self, x, *args, **kwargs): ...
    def permute_hidden(self, hx: XTensor, permutation: list): ...
    def forward(self, x, init_states: Incomplete | None = None):
        """
        x.shape is (batch_size, seq_length, feature_size)
        recurrent_activation -> sigmoid
        activation -> tanh
        """

class LSTM(Module):
    '''
    Long-Short Term Memory (LSTM) network cell.

    Each call computes the following function:

    .. math::
        \x08egin{array}{ll} \\\n            i_t = \\sigma(W_{ii} x_t + b_{ii} + W_{hi} h_{t-1} + b_{hi}) \\\n            f_t = \\sigma(W_{if} x_t + b_{if} + W_{hf} h_{t-1} + b_{hf}) \\\n            g_t = \tanh(W_{ig} x_t + b_{ig} + W_{hg} h_{t-1} + b_{hg}) \\\n            o_t = \\sigma(W_{io} x_t + b_{io} + W_{ho} h_{t-1} + b_{ho}) \\\n            c_t = f_t \\odot c_{t-1} + i_t \\odot g_t \\\n            h_t = o_t \\odot \tanh(c_t) \\\n        \\end{array}

    :param input_size: Input feature dimension.
    :param hidden_size:  Hidden feature dimension.
    :param num_layers: Number of recurrent layers. Default: 1
    :param batch_first: If True, input shape is provided as [batch_size,seq_len,feature_dim],
    if False, input shape is provided as [seq_len,batch_size,feature_dim],default True
    :param use_bias: If False, then the layer does not use bias weights b_ih and b_hh. Default: True.
    :param bidirectional: If True, becomes a bidirectional LSTM. Default: False.
    :param dtype: data type of parameters,default: None,use default data type.
    :param name: name of module,default:"".

    :return: a LSTM class

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
    def step(self, x_t, h_t, c_t, w_list_in_l): ...
    def forward(self, x, init_states: Incomplete | None = None):
        """
        x.shape is (batch_size, seq_length, feature_size)
        recurrent_activation -> sigmoid
        activation -> tanh
        """

def reset_zeros(input_tensor, hidden_size) -> None: ...
def reset_layer_params(layer_input_size, hidden_size, use_bias, device, dtype: int | None = None): ...
def reset_params_names(layer, direction, use_bias): ...
