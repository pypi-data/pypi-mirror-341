import abc
from ..dtype import get_xtensor_dtype_str as get_xtensor_dtype_str, kint64 as kint64
from .autograd import set_if_record as set_if_record, set_if_training as set_if_training
from .parameter import Parameter as Parameter, he_normal as he_normal, he_uniform as he_uniform, xavier_normal as xavier_normal
from .xtensor import XTensor as XTensor, flatten as flatten, permute as permute, reshape as reshape
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from collections import namedtuple as namedtuple
from pyvqnet.device import DEV_GPU_0 as DEV_GPU_0
from typing import Iterable, Iterator

class Module(ABC, metaclass=abc.ABCMeta):
    """Base class for all neural network modules including quantum modules or classic modules.

        Your models should also be subclass of this class for autograd calculation.

        Modules can also contain other Modules, allowing to nest them in
        a tree structure. You can assign the submodules as regular attributes::

            class Model(Module):
                def __init__(self):
                    super(Model, self).__init__()
                    self.conv1 = pyvqnet.nn.Conv2d(1, 20, (5,5))
                    self.conv2 = pyvqnet.nn.Conv2d(20, 20, (5,5))

                def forward(self, x):
                    x = pyvqnet.nn.activation.relu(self.conv1(x))
                    return pyvqnet.nn.activation.relu(self.conv2(x))

        Submodules assigned in this way will be registered

        """
    train_mode: bool
    name: Incomplete
    backend: int
    def __init__(self, name: str = '') -> None:
        """
        Represents abstract module in a neural network.
        """
    def merge_opinfo(self, opinfo_deque): ...
    def register_buffer(self, name: str, tensor_buffer: XTensor | None) -> None:
        """Adds a buffer to the module.

        This is typically used to register a buffer that should not to be
        considered a model parameter. For example, BatchNorm's ``running_mean``
        is not a parameter, but is part of the module's state.

        Buffers can be accessed as attributes using given names.

        Args:
            :param name: name of the buffer. The buffer can be accessed
                from this module using the given name
            :param tensor_buffer: buffer to be registered.

        Example::

            self.register_buffer('running_mean', XTensor.zeros(num_features))

        """
    def register_parameter(self, name: str, param: Parameter | None) -> None:
        """Adds a parameter to the module.

        The parameter can be accessed as an attribute using given name.

        Args:
            :param name: name of the parameter. The parameter can be accessed
                from this module using the given name
            :param tensor: parameter to be added to the module.

        Example::

            self.register_parameter('weights', XTensor.zeros(num_features))
        """
    def add_module(self, name: str, module: Module | None) -> None:
        """Adds a child module to the current module.

        The module can be accessed as an attribute using the given name.

        Args:
            name (string): name of the child module. The child module can be
                accessed from this module using the given name
            module (Module): child module to be added to the module.
        """
    def __getattr__(self, name: str) -> XTensor | Module: ...
    def __setattr__(self, name: str, value: XTensor | Module) -> None: ...
    def __delattr__(self, name) -> None: ...
    def children(self) -> Iterator['Module']:
        """Returns an iterator over immediate children modules.

        Yields:
            Module: a child module
        """
    def named_children(self) -> Iterator[tuple[str, 'Module']]:
        """Returns an iterator over immediate children modules, yielding both
        the name of the module as well as the module itself.

        Yields:
            (string, Module): Tuple containing a name and child module

        Example::

            >>> for name, module in model.named_children():
            >>>     if name in ['conv4', 'conv5']:
            >>>         print(module)

        """
    def named_modules(self, memo: set['Module'] | None = None, prefix: str = '', remove_duplicate: bool = True):
        """Returns an iterator over all modules in the network, yielding
        both the name of the module as well as the module itself.

        Args:
            memo: a memo to store the set of modules already added to the result
            prefix: a prefix that will be added to the name of the module
            remove_duplicate: whether to remove the duplicated module instances in the result
                or not

        Yields:
            (str, Module): Tuple of name and module

        Note:
            Duplicate modules are returned only once. In the following
            example, ``l`` will be returned only once.

        """
    def named_parameters(self, prefix: str = '', recurse: bool = True) -> Iterator[tuple[str, Parameter]]:
        """Returns an iterator over module parameters, yielding both the
        name of the parameter as well as the parameter itself.

        Args:
            prefix (str): prefix to prepend to all parameter names.
            recurse (bool): if True, then yields parameters of this module
                and all submodules. Otherwise, yields only parameters that
                are direct members of this module.

        Yields:
            (str, Parameter): Tuple containing the name and parameter

        """
    def state_dict(self, destination: Incomplete | None = None, prefix: str = ''):
        """Returns a dictionary containing a whole state of the module.

        Both parameters and persistent buffers (e.g. running averages) are
        included. Keys are corresponding parameter and buffer names.

        :param destination: a dict where state will be stored
        :param prefix: the prefix for parameters and buffers used in this
            module

        :return: a dictionary containing a whole state of the module

        Example::

            module.state_dict().keys()
            ['bias', 'weight']

        """
    def to_gpu(self, device=...):
        """
        Alias for toGPU()
        """
    def toGPU(self, device=...):
        """
        Move Module and it's paramters and buffers into specific GPU device.

        device specifies the device where the it's inner data is stored. When device = 0,
        the data is stored on the CPU, and when device >= DEV_GPU_0, the data is stored on the GPU.
        If your computer has multiple GPUs, you can specify different devices for data storage.
        For example, device = 1001, 1002, 1003, ... means stored on GPUs with different serial numbers.
        
        Note:

            Module in different GPU could not do calculation. 
            If you try to create a XTensor on GPU with id more than maximum number
            of validate GPUs, will raise Cuda Error.

        :param device: current device to save XTensor , default = 0,stored in cpu. device= pyvqnet.DEV_GPU_0,
        stored in 1st GPU, devcie  = 1001,stored in 2nd GPU,and so on

        :return: the module move to GPU device

        Example::

        """
    def to_cpu(self):
        """
        Alias for toCPU()
        """
    def toCPU(self):
        """
        Move Module and it's paramters and buffers into CPU device.

        :return: the module move to CPU device

        """
    def load_state_dict(self, state_dict) -> None:
        '''Copies parameters and buffers from :attr:`state_dict` into
        this module and its descendants.

        :param state_dict : a dict containing parameters and persistent buffers.

        Example::

            from pyvqnet.xtensor import Module,Conv2D,load_parameters,save_parameters
            class Net(Module):
                def __init__(self):
                    super(Net, self).__init__()
                    self.conv1 = Conv2D(input_channels=1, output_channels=6, kernel_size=(5, 5),
                        stride=(1, 1), padding="valid")

                def forward(self, x):
                    return super().forward(x)

            model = Net()
            save_parameters(model.state_dict(), "tmp.model")
            model_param = load_parameters("tmp.model")
            model.load_state_dict(model_param)
        '''
    def parameters(self):
        """
        Returns all the parameters of module and subclass.
        """
    def modules(self):
        """
        Returns all the modules for current class.
        """
    def __call__(self, x, *args, **kwargs):
        """
        Redefined call operator.
        """
    @abstractmethod
    def forward(self, x, *args, **kwargs):
        """
        Abstract method which performs forward pass.

        :param x: input XTensor
        :param *args: non keyword variable arguments
        :param **kwargs : keyword variable arguments
        :return: module output
        """
    def train(self) -> None:
        """
        Prepares module for training.
        """
    def eval(self) -> None:
        """
        Prepares module for evaluation.
        """
    def zero_grad(self) -> None: ...

class ModuleList(Module):
    """    
    
    Holds submodules in a list. ModuleList can be indexed like a regular Python list, but
    modules it contains are properly registered, sucn as Parameters.

    :param modules: lists of nn.Modules

    :return: a ModuleList


    """
    def __init__(self, modules: Iterable[Module] | None = None) -> None: ...
    def __getitem__(self, idx: int) -> Module | ModuleList: ...
    def __setitem__(self, idx: int, module: Module) -> None: ...
    def __delitem__(self, idx: int | slice) -> None: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[Module]: ...
    def __iadd__(self, modules: Iterable[Module]) -> ModuleList: ...
    def __add__(self, other: Iterable[Module]) -> ModuleList: ...
    def __dir__(self): ...
    def insert(self, index: int, module: Module) -> None:
        """Insert a given module before a given index in the list.

        Args:
            index (int): index to insert.
            module (nn.Module): module to insert
        """
    def append(self, module: Module) -> ModuleList:
        """Appends a given module to the end of the list.

        Args:
            module (nn.Module): module to append
        """
    def extend(self, modules: Iterable[Module]) -> ModuleList:
        """Appends modules from a Python iterable to the end of the list.

        Args:
            modules (iterable): iterable of modules to append
        """
    def forward(self, x, *args, **kwargs) -> None:
        """

        """

class ConvT2D(Module):
    '''
    2D ConvTransposed module. Inputs to the module are of shape
     (batch_size, input_channels, height, width)

    :param input_channels: `int` - Number of input channels
    :param output_channels: `int` - Number of kernels
    :param kernel_size: `int` - Size of a single kernel. Each kernel is kernel_size x kernel_size
    :param stride: `tuple` - Stride, defaults to (1, 1)
    :param padding:  Padding, controls the amount of padding of the input. It can be either a string {‘valid’, ‘same’} or a tuple of ints giving the amount of implicit padding applied on the input,defaults to "valid"
    :param use_bias: `bool` - if use bias, defaults to True
    :param kernel_initializer: `callable` - Defaults to xavier_normal
    :param bias_initializer: `callable` - Defaults to zeros
    :param dilation_rate: `int` - Spacing between kernel elements. Default: 1
    :param group: `int` - Number of group. Default: 1
    :param output_padding: `tuple` -
    Controls the amount of implicit zero-paddings on both sides of the
        output for output_padding number of points for each dimension,default=(0,0).
    :param dtype: data type of parameters,default: None,use default data type.
    :param name: name of module,default:"".
    :return: a ConvT2D class

    Note:
        ``padding=\'valid\'`` is the same as no padding.

        out_length = input_size*stride + (kernel_size - stride) + output_padding

        ``padding=\'same\'`` pads the input so the output has the shape as the input.

        out_length = input_size*stride + output_padding


    '''
    backend: Incomplete
    use_bias: Incomplete
    bias: Incomplete
    weights: Incomplete
    def __init__(self, input_channels: int, output_channels: int, kernel_size: tuple, stride: tuple = (1, 1), padding: str | tuple = 'valid', use_bias: bool = True, kernel_initializer: Incomplete | None = None, bias_initializer: Incomplete | None = None, dilation_rate: tuple = (1, 1), group: int = 1, out_padding: tuple = (0, 0), dtype: int | None = None, name: str = '') -> None: ...
    def forward(self, x, *args, **kwargs): ...

class ConvT1D(Module):
    '''\\\n    1D Transposed Convolution module. Inputs to the conv module are of shape
    (batch_size, input_channels, height)

    :param input_channels: `int` - Number of input channels.
    :param output_channels: `int` - Number of kernels.
    :param kernel_size: `int` - Size of a single kernel.
     kernel shape = [input_channels,output_channels,kernel_size].
    :param stride: `int` - Stride, defaults to 1.
    :param padding: `str` - Padding, controls the amount of padding applied to the input.
      It can be either a string {‘valid’, ‘same’} or a tuple of ints giving the 
      amount of implicit padding applied on both sides.defaults to "valid"
    :param use_bias: `bool` - if use bias, defaults to True.
    :param kernel_initializer: `callable` - Defaults to _xavier_normal.
    :param bias_initializer: `callable` - Defaults to _zeros.
    :param dilation_rate: `int` - Dilation rate,defaults: 1.
    :param group: `int` -  Number of group. Default: 1.
    :param output_padding: `tuple` -
    Controls the amount of implicit zero-paddings on both sides of the
        output for output_padding number of points for each dimension,default=(0,0).
    :param dtype: data type of parameters,default: None,use default data type.
    :param name: name of module,default:"".
    :return: a Conv1D class

    Note:
        ``padding=\'valid\'`` is the same as no padding.

        out_length = ceil((input_size - (kerkel_size - 1) )/stride)

        ``padding=\'same\'`` pads the input so the output has the shape as the input.

        out_length = ceil(input_size/stride)


    '''
    backend: Incomplete
    use_bias: Incomplete
    bias: Incomplete
    weights: Incomplete
    def __init__(self, input_channels: int, output_channels: int, kernel_size: int, stride: int = 1, padding: str | int = 'valid', use_bias: bool = True, kernel_initializer: Incomplete | None = None, bias_initializer: Incomplete | None = None, dilation_rate: int = 1, group: int = 1, out_padding: int = 0, dtype: int | None = None, name: str = '') -> None: ...
    def forward(self, x, *args, **kwargs): ...

class Conv1D(Module):
    '''\\\n    1D Convolution module. Inputs to the conv module are of shape
    (batch_size, input_channels, height)

    :param input_channels: `int` - Number of input channels.
    :param output_channels: `int` - Number of kernels.
    :param kernel_size: `int` - Size of a single kernel.
     kernel shape = [input_channels,output_channels,kernel_size].
    :param stride: `int` - Stride, defaults to 1.
    :param padding: `str` - Padding, controls the amount of padding applied to the input.
      It can be either a string {‘valid’, ‘same’} or a tuple of ints giving the 
      amount of implicit padding applied on both sides.defaults to "valid"
    :param use_bias: `bool` - if use bias, defaults to True.
    :param kernel_initializer: `callable` - Defaults to _xavier_normal.
    :param bias_initializer: `callable` - Defaults to _zeros.
    :param dilation_rate: `int` - Dilation rate,defaults: 1.
    :param group: `int` -  Number of group. Default: 1.

    :param dtype: data type of parameters,default: None,use default data type.
    :param name: name of module,default:"".
    :return: a Conv1D class

    Note:
        ``padding=\'valid\'`` is the same as no padding.

        out_length = ceil((input_size - (kerkel_size - 1) )/stride)

        ``padding=\'same\'`` pads the input so the output has the shape as the input.

        out_length = ceil(input_size/stride)


    '''
    backend: Incomplete
    use_bias: Incomplete
    bias: Incomplete
    weights: Incomplete
    def __init__(self, input_channels: int, output_channels: int, kernel_size: int, stride: int = 1, padding: str | int = 'valid', use_bias: bool = True, kernel_initializer: Incomplete | None = None, bias_initializer: Incomplete | None = None, dilation_rate: int = 1, group: int = 1, dtype: int | None = None, name: str = '') -> None: ...
    def forward(self, x, *args, **kwargs): ...

class Conv2D(Module):
    '''
    Convolution module. Inputs to the conv module are of shape
     (batch_size, input_channels, height, width)


    :param input_channels: `int` - Number of input channels
    :param output_channels: `int` - Number of kernels
    :param kernel_size: `tuple` - Size of a single kernel.
    :param stride: `tuple` - Stride, defaults to (1, 1)
    :param padding: Padding, controls the amount of padding of the input. 
    It can be either a string {‘valid’, ‘same’} or a tuple of 
    ints giving the amount of implicit padding applied on the input,defaults to "valid"
    :param use_bias: `bool` - if use bias, defaults to True
    :param kernel_initializer: `callable` - Defaults to _xavier_normal
    :param bias_initializer: `callable` - Defaults to _zeros
    :param dilation_rate: `int` - Spacing between kernel elements. Default: 1
    :param group: `int` - Number of group. Default: 1

    :param dtype: data type of parameters,default: None,use default data type.
    :param name: name of module,default:"".
    :return: a Conv2D class

    Note:
        ``padding=\'valid\'`` is the same as no padding.

        out_length = ceil((input_size - (kerkel_size - 1) )/stride)

        ``padding=\'same\'`` pads the input so the output has the shape as the input.

        out_length = ceil(input_size/stride)


    '''
    backend: Incomplete
    use_bias: Incomplete
    bias: Incomplete
    weights: Incomplete
    def __init__(self, input_channels: int, output_channels: int, kernel_size: tuple, stride: tuple = (1, 1), padding: str = 'valid', use_bias: bool = True, kernel_initializer: Incomplete | None = None, bias_initializer: Incomplete | None = None, dilation_rate: tuple = (1, 1), group: int = 1, dtype: int | None = None, name: str = '') -> None: ...
    def forward(self, x, *args, **kwargs): ...

class Linear(Module):
    '''
    Linear module (fully-connected layer).
    :math:`y = xA^T + b`

    :param inputs: `int` - number of inputs features
    :param output: `int` - number of output features
    :param weight_initializer: `callable` - defaults to normal
    :param bias_initializer: `callable` - defaults to zeros
    :param use_bias: `bool` - defaults to True
    :param device: default: None,use cpu. if use GPU,set DEV_GPU_0.
    :param dtype: default: None,use default data type.
    :param name: name of module,default:"".
    :return: a Linear class

    '''
    backend: Incomplete
    use_bias: Incomplete
    output_channels: Incomplete
    bias: Incomplete
    weights: Incomplete
    def __init__(self, input_channels, output_channels, weight_initializer: Incomplete | None = None, bias_initializer: Incomplete | None = None, use_bias: bool = True, dtype: int | None = None, name: str = '') -> None: ...
    def forward(self, x, *args, **kwargs): ...

class PoolingLayer(Module, metaclass=abc.ABCMeta):
    """
    PoolingLayer
    """
    pool_func: Incomplete
    backend: Incomplete
    dtype: Incomplete
    @abstractmethod
    def __init__(self, kernel, stride, padding: str = 'valid', dtype: int | None = None, name: str = ''):
        """
        Represents abstract pooling layer
        """
    def forward(self, x) -> None: ...

class MaxPool2D(PoolingLayer):
    '''
    Maximum 2D pooling layer

    :param kernel: size of the average pooling windows
    :param strides: factor by which to downscale
    :param padding: one of "none", "valid" or "same"
    :param name: name of module,default:"".
    :return: MaxPool2D layer

    Note:
        ``padding=\'valid\'`` is the same as no padding.

        out_length = ceil((input_size - (kerkel_size - 1) )/stride)

        ``padding=\'same\'`` pads the input so the output has the shape as the input.

        out_length = ceil(input_size/stride)


    '''
    def __init__(self, kernel: tuple, stride: tuple, padding: str = 'valid', dtype: int | None = None, name: str = '') -> None: ...
    def forward(self, x, *args, **kwargs): ...

class AvgPool2D(PoolingLayer):
    '''
    Average 2D pooling layer

    :param kernel: size of the average pooling windows
    :param strides: factor by which to downscale
    :param padding: one of "none", "valid" or "same"
    :param name: name of module,default:"".
    :return: AvgPool2D layer

    Note:
        ``padding=\'valid\'`` is the same as no padding.

        out_length = ceil((input_size - (kerkel_size - 1) )/stride)

        ``padding=\'same\'`` pads the input so the output has the shape as the input.

        out_length = ceil(input_size/stride)


    '''
    def __init__(self, kernel: tuple, stride: tuple, padding: str = 'valid', dtype: int | None = None, name: str = '') -> None: ...
    def forward(self, x, *args, **kwargs): ...

class MaxPool1D(PoolingLayer):
    '''
    Maximum 1D pooling layer

    :param kernel: size of the average pooling windows
    :param strides: factor by which to downscale
    :param padding: one of "none", "valid" or "same"
    :param name: name of module,default:"".
    :return: MaxPool1D layer

    Note:
        ``padding=\'valid\'`` is the same as no padding.

        out_length = ceil((input_size - (kerkel_size - 1) )/stride)

        ``padding=\'same\'`` pads the input so the output has the shape as the input.

        out_length = ceil(input_size/stride)


    '''
    def __init__(self, kernel: int, stride: int, padding: str = 'valid', dtype: int | None = None, name: str = '') -> None: ...
    def forward(self, x, *args, **kwargs): ...

class AvgPool1D(PoolingLayer):
    '''
    Average 1D pooling layer

    :param kernel: size of the average pooling windows
    :param strides: factor by which to downscale
    :param padding: one of "none", "valid" or "same"
    :param name: name of module,default:"".
    :return: AvgPool1D layer

    Note:
        ``padding=\'valid\'`` is the same as no padding.

        out_length = ceil((input_size - (kerkel_size - 1) )/stride)

        ``padding=\'same\'`` pads the input so the output has the shape as the input.

        out_length = ceil(input_size/stride)


    '''
    def __init__(self, kernel: int, stride: int, padding: str = 'valid', dtype: int | None = None, name: str = '') -> None: ...
    def forward(self, x, *args, **kwargs): ...

class Embedding(Module):
    '''
    This module is often used to store word embeddings and retrieve them using indices.
    The input to the module is a list of indices, and the output is the corresponding
    word embeddings.


    :param num_embeddings: `int` - number of inputs features
    :param embedding_dim: `int` - number of output features
    :param weight_initializer: `callable` - defaults to normal
    :param dtype: data type of parameters,default: None,use default data type.
    :param name: name of module,default:"".
    :return: a Embedding class

    '''
    backend: Incomplete
    weight: Incomplete
    def __init__(self, num_embeddings, embedding_dim, weight_initializer=..., dtype: int | None = None, name: str = '') -> None: ...
    def forward(self, x: XTensor, *args, **kwargs): ...

class LayerNorm1d(Module):
    '''Applies Layer Normalization over a mini-batch of 2-dim inputs as described in
    the paper `Layer Normalization <https://arxiv.org/abs/1607.06450>`__

    .. math::
        y = \\frac{x - \\mathrm{E}[x]}{ \\sqrt{\\mathrm{Var}[x] + \\epsilon}} * \\gamma + \\beta

    The mean and standard deviation are calculated on the last dimension size, where "norm_size" is the value of norm_size.

    :param norm_shape: `float` - normalize shape
    :param epsilon: `float` - numerical stability constant, defaults to 1e-5
    :param affine: `bool` - whether use apply affine transform, defaults to True

    :param dtype: data type of parameters,default: None,use default data type.
    :param name: name of module,default:"".

    :return: a LayerNorm1d class

    '''
    backend: Incomplete
    beta: Incomplete
    gamma: Incomplete
    epsilon: Incomplete
    normalized_shape: Incomplete
    begin_norm_axis: int
    affine: Incomplete
    def __init__(self, normalized_shape: int | list[int], epsilon: float = 1e-05, affine: bool = True, dtype: int | None = None, name: str = '') -> None: ...
    def forward(self, x: XTensor, *args, **kwargs): ...

class LayerNorm2d(Module):
    '''Applies Layer Normalization over a mini-batch of 4-dim inputs as described in
    the paper `Layer Normalization <https://arxiv.org/abs/1607.06450>`__

    .. math::
        y = \\frac{x - \\mathrm{E}[x]}{ \\sqrt{\\mathrm{Var}[x] + \\epsilon}} * \\gamma + \\beta

    The mean and standard deviation are computed on the remaining dimensional data excluding the first dimension. 
    For an input like (B,C,H,W), norm_size should be equal to C * H * W.

    :param norm_shape: `float` - normalize shape
    :param epsilon: `float` - numerical stability constant, defaults to 1e-5
    :param affine: `bool` - whether use apply affine transform, defaults to True

    :param dtype: data type of parameters,default: None,use default data type.
    :param name: name of module,default:"".

    :return: a LayerNorm2d class

    '''
    backend: Incomplete
    beta: Incomplete
    gamma: Incomplete
    epsilon: Incomplete
    normalized_shape: Incomplete
    begin_norm_axis: int
    affine: Incomplete
    def __init__(self, normalized_shape: int | list[int], epsilon: float = 1e-05, affine: bool = True, dtype: int | None = None, name: str = '') -> None: ...
    def forward(self, x: XTensor, *args, **kwargs): ...

class LayerNormNd(Module):
    '''Applies Layer Normalization over a mini-batch of N-dim inputs as described in
    the paper `Layer Normalization <https://arxiv.org/abs/1607.06450>`__

    .. math::
        y = \\frac{x - \\mathrm{E}[x]}{ \\sqrt{\\mathrm{Var}[x] + \\epsilon}} * \\gamma + \\beta

    The mean and standard-deviation are calculated over the last `D` dimensions size.
    
    For example, if :attr:`normalized_shape`
    is ``(3, 5)`` (a 2-dimensional shape), the mean and standard-deviation are computed over
    the last 2 dimensions of the input (i.e. ``input.mean((-2, -1))``).

    For input like (B,C,H,W,D), :attr:`norm_shape` can be [C,H,W,D],[H,W,D],[W,D] or [D].

    :param norm_shape: `float` - normalize shape
    :param epsilon: `float` - numerical stability constant, defaults to 1e-5
    :param affine: `bool` - whether use apply affine transform, defaults to True

    :param dtype: data type of parameters,default: None,use default data type.
    :param name: name of module,default:"".

    :return: a LayerNormNd class

    '''
    backend: Incomplete
    beta: Incomplete
    gamma: Incomplete
    epsilon: Incomplete
    normalized_shape: Incomplete
    begin_norm_axis: int
    affine: Incomplete
    def __init__(self, normalized_shape: int | list[int], epsilon: float = 1e-05, affine: bool = True, dtype: int | None = None, name: str = '') -> None: ...
    def forward(self, x: XTensor, *args, **kwargs): ...

class Pixel_Unshuffle(Module):
    '''
    Reverses the Pixel_Shuffle operation by rearranging elements
        in a tensor of shape :math:`(*, C, H \\times r, W \\times r)` to a tensor of shape
        :math:`(*, C \\times r^2, H, W)`, where r is a downscale factor.

    :param downscale_factors: factor to decrease spatial resolution by.
    :param name: name,default is "".
    
    :return: 
        Pixel_Unshuffle Module

    '''
    downscale_factors: Incomplete
    def __init__(self, downscale_factors, name: str = '') -> None: ...
    def forward(self, x, *args, **kwargs): ...

class Pixel_Shuffle(Module):
    '''
    Rearranges elements in a tensor of shape :math:`(*, C \\times r^2, H, W)`
    to a tensor of shape :math:`(*, C, H \\times r, W \\times r)`, where r is an upscale factors.

    :param upscale_factors: factor to increase spatial resolution by
    :param name: name,default is "".
    :return: 
        Pixel_Shuffle Module


    '''
    upscale_factors: Incomplete
    def __init__(self, upscale_factors, name: str = '') -> None: ...
    def forward(self, x, *args, **kwargs): ...

class Dropout(Module):
    '''
    Dropout module.

    :param dropout_rate: `float` - probability that a neuron will be set to zero
    :param name: module name ,default="".
    :return: a Dropout class

    .. note::
            if dropout layer is in `with autograd.record():` scope,it is in train mode,is in eval mode otherwise.

    '''
    dropout_rate: Incomplete
    def __init__(self, dropout_rate: float = 0.5, name: str = '') -> None: ...
    def forward(self, x): ...
