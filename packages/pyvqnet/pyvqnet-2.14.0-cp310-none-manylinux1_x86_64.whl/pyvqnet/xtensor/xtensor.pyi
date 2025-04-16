from .autograd import get_if_record as get_if_record, get_if_training as get_if_training, set_if_record as set_if_record, set_if_training as set_if_training
from .base import integer_types as integer_types, numeric_types as numeric_types
from .context import Context as Context, create_context as create_context, current_context as current_context, parse_context as parse_context
from .utils import check_attr_same as check_attr_same, check_boolean_array_dimension as check_boolean_array_dimension, get_oshape_of_gather_nd_op as get_oshape_of_gather_nd_op
from _typeshed import Incomplete
from collections import OrderedDict as OrderedDict
from functools import reduce as reduce
from pyvqnet.device import DEV_CPU as DEV_CPU, DEV_CPU_PIN as DEV_CPU_PIN, DEV_GPU_0 as DEV_GPU_0, DEV_GPU_1 as DEV_GPU_1, DEV_GPU_2 as DEV_GPU_2, DEV_GPU_3 as DEV_GPU_3, DEV_GPU_4 as DEV_GPU_4, DEV_GPU_5 as DEV_GPU_5, DEV_GPU_6 as DEV_GPU_6, DEV_GPU_7 as DEV_GPU_7
from pyvqnet.dtype import dtype_map as dtype_map, dtype_map_from_numpy as dtype_map_from_numpy, get_default_dtype as get_default_dtype, get_readable_dtype_str as get_readable_dtype_str, get_xtensor_default_dtype as get_xtensor_default_dtype, get_xtensor_dtype as get_xtensor_dtype, kbool as kbool, kcomplex128 as kcomplex128, kcomplex64 as kcomplex64, kfloat32 as kfloat32, kfloat64 as kfloat64, kint16 as kint16, kint32 as kint32, kint64 as kint64, kint8 as kint8, kuint8 as kuint8

class XTensor:
    """
    XTensor Class
    """
    data: Incomplete
    name: Incomplete
    have_grad: bool
    def __init__(self, data, device: int = 0, dtype: int | None = None, requires_grad: bool = False, name: str = '') -> None: ...
    @property
    def device(self): ...
    @property
    def requires_grad(self): ...
    @requires_grad.setter
    def requires_grad(self, value) -> None: ...
    @property
    def grad(self):
        """Returns gradient buffer attached to this XTensor."""
    @property
    def ctx(self):
        """Device context of the array.

        """
    @property
    def context(self):
        """Device context of the array.

        """
    @property
    def dtype_str(self):
        """        Returns data type

        :return: data type
        """
    @property
    def dtype(self):
        """        Returns data type

        :return: data type
        """
    @property
    def ndim(self):
        """        Returns number of dimensions

        :return: number of dimensions
        """
    def dim(self): ...
    @property
    def size(self):
        """
        Returns the number of elements in the tensor.

        :return: number of elements
        """
    @property
    def shape(self):
        """
        Returns the shape of the tensor.

        :return: number of shape
        """
    def getdata(self): ...
    @property
    def data_repr(self): ...
    def detach(self):
        """
        return new copy of self xtensor ,detached from computing graph.
        """
    def attach_grad(self, grad_req: str = 'write') -> None: ...
    def backward(self, out_grad: Incomplete | None = None, retain_graph: bool = False) -> None:
        """Compute the gradients of this XTensor w.r.t variables.

        :param out_grad: Gradient with respect to output.
        :param retain_graph: Whether to retain the computaion graph for another backward
            pass on the same graph. By default the computaion history
            is cleared.default:false.

        """
    def data_str(self):
        """
        String representation of XTensor data .
        """
    def __len__(self) -> int:
        """Number of elements along the first axis."""
    def __eq__(self, other):
        """x.__eq__(y) <=> x==y <=> mx.nd.equal(x, y) """
    def __hash__(self):
        """Default hash function."""
    def __ne__(self, other):
        """x.__ne__(y) <=> x!=y <=> mx.nd.not_equal(x, y) """
    def __gt__(self, other):
        """x.__gt__(y) <=> x>y <=> mx.nd.greater(x, y) """
    def __ge__(self, other):
        """x.__ge__(y) <=> x>=y <=> mx.nd.greater_equal(x, y) """
    def __lt__(self, other):
        """x.__lt__(y) <=> x<y <=> mx.nd.lesser(x, y) """
    def __le__(self, other):
        """x.__le__(y) <=> x<=y <=> mx.nd.less_equal(x, y) """
    def __add__(self, other): ...
    def __iadd__(self, other): ...
    def __radd__(self, other): ...
    def __sub__(self, other): ...
    def __isub__(self, other): ...
    def __rsub__(self, other): ...
    def __mul__(self, other): ...
    def __neg__(self): ...
    def __imul__(self, other): ...
    def __rmul__(self, other): ...
    def __div__(self, other): ...
    def __rdiv__(self, other): ...
    def __idiv__(self, other): ...
    def __truediv__(self, other): ...
    def __rtruediv__(self, other): ...
    def __itruediv__(self, other): ...
    def __pow__(self, other): ...
    def __rpow__(self, other): ...
    def broadcast_to(self, shape): ...
    def to_numpy(self, copy: bool = True): ...
    def item(self): ...
    def numel(self):
        """
        Returns the number of elements in the tensor.

        :return: number of elements
        """
    def astype(self, dtype):
        """Returns a copy of the array after casting to a specified type.

        :param dtype: target data type.
        """
    def fill_rand_binary_(self, v: float = 0.5):
        """        Fills a tensor with values randomly sampled from a binary distribution

        Binarization threshold. compare each data with v ,return 1 if data >= v, 0 otherwise

        :param v: threshold a scalar value 1 if data >= t, 0 otherwise
        :return: None
        """
    def fill_rand_normal_(self, m: int = 0, s: int = 1):
        """        Fills a tensor with values randomly sampled from a normal distribution
        Mean of the normal distribution. Standard deviation of the normal distribution.
        Whether to use or not the fast math mode.

        :param m: mean a scalar value,default = 0.
        :param s: std a scalar value,default = 1.
        :return: None
        """
    def fill_rand_signed_uniform_(self, v: int = 1):
        """
        Fills a tensor with values randomly sampled from a signed uniform distribution

        Scale factor of the values generated by the signed uniform distribution.

        :param v: a scalar value,default = 1.
        :return: None
        """
    def fill_rand_uniform_(self, v: int = 1):
        """
        Fills a tensor with values randomly sampled from a signed uniform distribution

        Scale factor of the values generated by the signed uniform distribution.

        :param v: a scalar value,default = 1.
        :return: None
        """
    def fill_rand_uniform_with_bound_(self, min, max):
        """
        Fills a tensor with values randomly sampled from a uniform distribution
         in the range of (min,max)

        :param min: down bound
        :param max: up bound
        :return: None
        """
    def sign(self):
        """
        Compute the element-wise sign (-1 if x < 0, 0 if x == 0, 1 if x > 0)
        of the tensor.

        :return: A XTensor
        """
    def view(self, new_shape):
        """        Change the tensor's shape,return a view of input XTensor.

        :param new_shape: the new shape (list of integers)
        :return: new XTensor

        """
    def reshape(self, new_shape):
        """
        Change the tensor's shape ,return a new Tensor.

        :param new_shape: the new shape (list of integers)
        :return: new XTensor
        """
    def all(self):
        """        Return if all tensor value is non-zero.

        :return: True,if all tensor value is non-zero.

        """
    def any(self):
        """        Return if any tensor value is non-zero.

        :return: True,if any tensor value is non-zero.

        """
    def nonzero(self):
        """
        Returns a tensor containing the indices of nonzero elements.

        :param a: input tensor
        :return: A new XTensor
        """
    def nonzero_for_indexing(self):
        """
        Returns a tensor containing the indices of nonzero elements.

        :param a: input tensor
        :return: A new XTensor
        """
    def argmax(self, axis: Incomplete | None = None, keepdims: bool = False):
        """        Returns the indices of the maximum value of all elements in the input tensor,or
        Returns the indices of the maximum values of a tensor across a dimension.


        :param dim: axis (int) – the dimension to reduce,only accepts single axis.
                    if dim is None, returns the indices of the maximum value of all
                    elements in the input tensor.

        :param keepdims: keepdim (bool) – whether the output tensor has dim retained or not.

        :return: the indices of the maximum value in the input tensor.


        """
    def argmin(self, axis: Incomplete | None = None, keepdims: bool = False):
        """        Returns the indices of the minimum value of all elements in the input tensor, or
        Returns the indices of the minimum values of a tensor across a dimension.

        :param dim: axis (int) – the dimension to reduce,only accepts single axis.
                    if dim is None, returns the indices of the minimum value of all
                    elements in the input tensor.

        :param keepdims: keepdim (bool) – whether the output tensor has dim retained or not.

        :return: the indices of the minimum value in the input tensor.
        """
    def transpose(self, *axes):
        """
        Reverse or permute the axes of an array.if dim = None, revsers the dim.
        if dim is a list with two elements, transpose() will permute these two dim.

        :param t: input XTensor
        :param dim: the new order of the dimensions (list of integers).
        :return: result XTensor.
        """
    def squeeze(self, axis: Incomplete | None = None):
        """
        Remove axes of length one .if `axis` is not specified, remove all single-dimensional axis from the shape of a tensor. 

        :param t: input XTensor
        :param axis: squeeze axis
        :return: A XTensor

        """
    def neg_(self): ...
    def cpu(self):
        """
        Clone XTensor into specific CPU device.

        device specifies the device where the it's inner data is stored. When device = 0, the data is stored on the CPU, and when device >= DEV_GPU, the data is stored on the GPU. If your computer has multiple GPUs, you can specify different devices for data storage. For example, device = 1001, 1002, 1003, ... means stored on GPUs with different serial numbers.
           
        The output of CPU() will remove current GraphNode.

        :return: the XTensor move to CPU device
        """
    CPU = cpu
    def copy(self): ...
    def copyto(self, other):
        """Copies the value of this array to another array.

        If ``other`` is a ``XTensor`` object, then ``other.shape`` and
        ``self.shape`` should be the same. This function copies the value from
        ``self`` to ``other``.

        If ``other`` is a context, a new ``XTensor`` will be first created on
        the target context, and the value of ``self`` is copied.

        :param other: other XTensor or Context.
        """
    def isGPU(self): ...
    def isCPU(self): ...
    def isCPU_PINNED(self): ...
    def to_device(self, device): ...
    def GPU(self, device_id=...):
        """
        Clone a new XTensor into specific GPU device.

        device specifies the device where the it's inner data is stored. When device = 0, the data is stored on the CPU, and when device >= DEV_GPU_0, the data is stored on the GPU. If your computer has multiple GPUs, you can specify different devices for data storage. For example, device = 1001, 1002, 1003, ... means stored on GPUs with different serial numbers.

        Note:

            XTensor in different GPU could not do calculation. 
            If you try to create a XTensor on GPU with id more than maximum number of validate GPUs, will raise Cuda Error.
            new Tensor will remove its GraphNode.
        :param device: current device to save XTensor , default = 0,stored in cpu. device= pyvqnet.DEV_GPU_0, stored in 1st GPU, devcie  = 1001,stored in 2nd GPU,and so on

        :return: the XTensor clone to GPU device
        """
    gpu = GPU
    def toGPU(self, device_id=...):
        """
        Move XTensor into specific GPU device.

        device specifies the device where the it's inner data is stored. When device = 0, the data is stored on the CPU, and when device >= DEV_GPU, the data is stored on the GPU. If your computer has multiple GPUs, you can specify different devices for data storage. For example, device = 1001, 1002, 1003, ... means stored on GPUs with different serial numbers.

        Note:

            XTensor in different GPU could not do calculation. 
            If you try to create a XTensor on GPU with id more than maximum number of validate GPUs, will raise Cuda Error.
           
        :param device: current device to save XTensor , default = 0,stored in cpu. device= pyvqnet.DEV_GPU_0, stored in 1st GPU, devcie  = 1001,stored in 2nd GPU,and so on

        :return: the XTensor move to GPU device

        """
    def get_if_scalar(self): ...
    def set_if_scalar(self, flag) -> None: ...
    def toCPU(self):
        """
        Move XTensor into specific CPU device or return self, if self is on CPU already.

        device specifies the device where the it's inner data is stored. When device = 0, the data is stored on the CPU, and when device >= DEV_GPU, the data is stored on the GPU. If your computer has multiple GPUs, you can specify different devices for data storage. For example, device = 1001, 1002, 1003, ... means stored on GPUs with different serial numbers.
           
        :return: the XTensor move to CPU device
        """
    def CPU_PINNED(self): ...
    def as_in_context(self, context):
        """Returns an array on the target device with the same value as this array.

        If the target context is the same as ``self.context``, then ``self`` is
        returned.  Otherwise, a copy is made.

        """
    def slice_assign(self, rhs, begin, end, step):
        """
        Assign the rhs to a cropped subset of this NDarray in place.
        Returns the view of this XTensor.
        """
    def slice_assign_scalar(self, value, begin, end, step):
        """
        Assign the scalar to a cropped subset of this XTensor. 
        Value will broadcast to the shape of the cropped shape
        and will be cast to the same dtype of the XTensor.

        """
    def boolean_mask(self, bool_mask): ...
    def __getitem__(self, key):
        """x.__getitem__(i) <=> x[i]

        Returns a sliced view of this array if the elements fetched are contiguous in memory;
        otherwise, returns a newly created XTensor.
        This functions supports advanced indexing defined in the following reference with
        some restrictions.

        For basic indexing, i.e., if ``key`` consists only of integers,
        ``slice``, ``Ellipsis`` (``...``) and ``None``, a mutable view is
        returned that shares memory with this array if the accessed portion is
        contiguous in memory.
        Otherwise, a newly created ``XTensor`` is returned.

        This functions supports advanced indexing as defined in `the NumPy
        advanced indexing documentation
        <https://docs.scipy.org/doc/numpy/reference/arrays.indexing.html#advanced-indexing>`_,
        with the restriction that boolean array indexing is not supported.

        Parameters
        ----------
        key : int, ndarray.slice, list, np.ndarray, XTensor, or tuple of all previous types
            Indexing key.

        """
    def __setitem__(self, key, value) -> None: ...
    def is_float(self): ...
    def is_complex(self): ...

def xtensor(data, device: Incomplete | None = None, dtype: int | None = None):
    """
    Create new xtensor from array-like object.

    :param device: which device stores data,default:None,use cpu.
    :param dtype: which data type is used,default:None, use float32.
    :return:
            new XTensor
    """
def make_array(data, device: Incomplete | None = None, dtype: int | None = None):
    """
    Create new xtensor from array-like object.

    :param device: which device stores data,default:None,use cpu.
    :param dtype: which data type is used,default:None, use float32.
    :return:
            new XTensor
    """
def argmax(self, axis: Incomplete | None = None, keepdims: bool = False): ...
def argmin(self, axis: Incomplete | None = None, keepdims: bool = False): ...
def cat(seqs, axis: int = 0):
    """
    concatenate with channels, i.e. concatenate C of Tensor shape (N,C,H,W)

    :param seqs: tuple or list consist of XTensor
    :param axis: along which aixs to concat,default = 0
    :return: cat of inputs.
    """
def concatenate(seqs, axis: int = 0):
    """
    concatenate with channels, i.e. concatenate C of Tensor shape (N,C,H,W)

    :param seqs: tuple or list consist of XTensor
    :param axis: along which aixs to concat,default = 0
    :return: cat of inputs.
    """
def concat(seqs, axis: int = 0):
    """
    concatenate with channels, i.e. concatenate C of Tensor shape (N,C,H,W)

    :param seqs: tuple or list consist of XTensor
    :param axis: along which aixs to concat,default = 0
    :return: cat of inputs.
    """
def stack(arrays, axis: int = 0):
    """    Join a sequence of arrays along a new axis,return a new Tensor.

    :param arrays: list contains QTensors
    :param axis: stack axis
    :return: A XTensor
    """
def divide(lhs, rhs):
    """
    Left-hand side / right-hand side.

    :param lhs: Left-hand side,XTensor or scalar.
    :param rhs: right-hand side,XTensor or scalar.
    """
def broadcast_div(lhs, rhs, out: Incomplete | None = None):
    """
    lhs - rhs
    """
def kron(t1, t2):
    """
    Computes the Kronecker product, denoted by :math:`\\otimes`, of :attr:`input` and :attr:`other`.

    If :attr:`input` is a :math:`(a_0 \times a_1 \times \\dots \times a_n)` tensor and :attr:`other` is a
    :math:`(b_0 \times b_1 \times \\dots \times b_n)` tensor, the result will be a
    :math:`(a_0*b_0 \times a_1*b_1 \times \\dots \times a_n*b_n)` tensor with the following entries:

    .. math::
        (\text{input} \\otimes \text{other})_{k_0, k_1, \\dots, k_n} =
            \text{input}_{i_0, i_1, \\dots, i_n} * \text{other}_{j_0, j_1, \\dots, j_n},

    where :math:`k_t = i_t * b_t + j_t` for :math:`0 \\leq t \\leq n`.
    If one tensor has fewer dimensions than the other it is unsqueezed until it has the same number of dimensions.

    Supports real-valued and complex-valued inputs.


    :param t1: input XTensor 1.
    :param t2:  input XTensor 2.
    :return:
            kron prodcut of inputs

    """
def mul(lhs, rhs):
    """
    Left-hand side * right-hand side.

    :param lhs: Left-hand side,XTensor or scalar.
    :param rhs: right-hand side,XTensor or scalar.
    """
def broadcast_mul(lhs, rhs, out: Incomplete | None = None):
    """
    lhs - rhs
    """
def sub(lhs, rhs):
    """
    Left-hand side - right-hand side.

    :param lhs: Left-hand side,XTensor or scalar.
    :param rhs: right-hand side,XTensor or scalar.
    """
def broadcast_sub(lhs, rhs, out: Incomplete | None = None):
    """
    lhs - rhs
    """
def add(lhs, rhs):
    """
    Left-hand side + right-hand side.

    :param lhs: Left-hand side,XTensor or scalar.
    :param rhs: right-hand side,XTensor or scalar.
    """
def broadcast_add(lhs, rhs, out: Incomplete | None = None): ...
def floor(x):
    """
    Compute the element-wise floor (largest integer i such that i <= t)
    of the tensor.

    :param x: input XTensor
    :return: A XTensor
    """
def ceil(x):
    """
    Compute the element-wise ceiling (smallest integer i such that i >= x)
    of the tensor.

    :param x: input XTensor
    :return: A XTensor
    """
def round(x):
    """    Round tensor values to the nearest integer.
    
    This function implements the “round half to even” to break ties when a number is equidistant from two integers (e.g. round(2.5) is 2).

    :param x: input tensor
    :return: A XTensor
    """
def neg(x):
    """
    Unary negation of tensor elements.

    :param x: 'XTensor' - input tensor
    :return:  XTensor
    """
def exp(x):
    """
    Applies exp function to all the elements of the input tensor.

    :param x: 'XTensor' - input tensor
    :return:  XTensor

    """
def abs(x):
    """
    Applies abs function to all the elements of the input tensor.

    :param x: 'XTensor' - input tensor
    :return:  XTensor

    """
def log(x):
    """
    Applies log function to all the elements of the input tensor.

    :param x: 'XTensor' - input tensor
    :return:  XTensor

    """
def softmax(x, axis: int = -1):
    """
    Apply a softmax activation function to the given input.

    :param x: input xtensor.
    :param axis: dimension on which to operate (-1 for last axis)

    :return: softmax Activation result
    """
def log_softmax(x, axis: int = -1):
    """
    Apply a log softmax activation function to the given input.

    :param x: input xtensor.
    :param axis: dimension on which to operate (-1 for last axis)

    :return: log softmax Activation result
    """
def square(x):
    """
    Apply square activation function to the given input.

    :param x: input xtensor.

    :return: XTensor
    """
def sqrt(x):
    """
    Apply square root of the given input.

    :param x: input xtensor.

    :return: XTensor
    """
def sin(x):
    """
    Apply sin function of the given input.

    :param x: input xtensor.

    :return: XTensor
    """
def asin(x):
    """
    Apply arcsin function of the given input.

    :param x: input xtensor.

    :return: XTensor
    """
def sinh(x):
    """
    Apply Hyperbolic sin function of the given input.

    :param x: input xtensor.

    :return: XTensor
    """
def cos(x):
    """
    Apply cos function of the given input.

    :param x: input xtensor.

    :return: XTensor
    """
def cosh(x):
    """
    Apply Hyperbolic cos function of the given input.

    :param x: input xtensor.

    :return: XTensor
    """
def acos(x):
    """
    Apply arccos function of the given input.

    :param x: input xtensor.

    :return: XTensor
    """
def tanh(x):
    """
    Apply Hyperbolic tan function of the given input.

    :param x: input xtensor.

    :return: XTensor
    """
def atan(x):
    """
    Apply arctan function of the given input.

    :param x: input xtensor.

    :return: XTensor
    """
def tan(x):
    """
    Apply tan function of the given input.

    :param x: input xtensor.

    :return: XTensor
    """
def relu(x):
    """
    Apply relu function of the given input.

    :param x: input xtensor.

    :return: XTensor
    """
def sigmoid(x):
    """
    Apply sigmoid function of the given input.

    :param x: input xtensor.

    :return: XTensor
    """
def leaky_relu(x, alpha: float = 0.01):
    """
    Apply the leaky version of a rectified linear unit activation
    function to the given input.

    .. math::
        \text{LeakyRelu}(x) =
        \x08egin{cases}
        x, & \text{ if } x \\geq 0 \\\n        \x07lpha * x, & \text{ otherwise }
        \\end{cases}
    :param x: input xtensor.
    :param alpha: LeakyRelu coefficient, default: 0.01
    :return: XTensor
    """
def hard_sigmoid(x):
    """
    Apply a hard sigmoid activation function to the given input.

    .. math::
        \text{Hardsigmoid}(x) = \x08egin{cases}
            0 & \text{ if } x \\le -3, \\\n            1 & \text{ if } x \\ge +3, \\\n            x / 6 + 1 / 2 & \text{otherwise}
        \\end{cases}

    :param x: input xtensor.
    :return: XTensor
    """
def elu(x, alpha: int = 1):
    """
    Apply the exponential linear unit activation function to the given input.

    .. math::
        \text{ELU}(x) = \x08egin{cases}
        x, & \text{ if } x > 0\\\n        \x07lpha * (\\exp(x) - 1), & \text{ if } x \\leq 0
        \\end{cases}

    :param x: input xtensor.
    :param alpha: Elu coefficient, default: 1.0

    :return: XTensor
    """
def soft_plus(x):
    """
        Apply the softplus activation function to the given input.

        .. math::
            \text{Softplus}(x) = \\log(1 + \\exp(x))

        :param x: input xtensor.
        :return: XTensor
    """
softplus = soft_plus

def softsign(x):
    """\\\n    Apply the softsign activation function to the given input.

    .. math::
        \\text{SoftSign}(x) = \\frac{x}{ 1 + |x|}

    :param x: input xtensor.
    :return: XTensor
    """
def mean(x, axis: Incomplete | None = None, keepdims: bool = False):
    """
    Obtain the mean of XTensor along a specific axis or get mean value of all elements.

    :param x:  the input tensor.
    :param dim:  the dimension to reduce,default None: get mean value of all elements.
    :param keepdims:  whether the output tensor has dim retained or not,default False.
    :return: returns the mean value of the input tensor.

    """
def var(x, axis: Incomplete | None = None, keepdims: bool = False, unbiased: bool = True):
    """
    Obtain the variance of XTensor along a specific axis or get mean value of all elements.

    :param x:  the input tensor.
    :param dim:  the dimension to reduce,default None: get mean value of all elements.
    :param keepdims:  whether the output tensor has dim retained or not,default False.
    :param unbiased:  whether unbiased variance,default True.
    :return: returns the variance value of the input tensor.

    """
def std(x, axis: Incomplete | None = None, keepdims: bool = False, unbiased: bool = True):
    """
    Obtain the standard variance of XTensor along a specific axis or get mean value of all elements.

    :param x:  the input tensor.
    :param dim:  the dimension to reduce,default None: get mean value of all elements.
    :param keepdims:  whether the output tensor has dim retained or not,default False.
    :param unbiased:  whether unbiased variance,default True.
    :return: returns the variance value of the input tensor.

    """
def sums(x, axis: Incomplete | None = None, keepdims: bool = False): ...
def sum(x, axis: Incomplete | None = None, keepdims: bool = False):
    """
    Obtain the standard variance of XTensor along a specific axis or get mean value of all elements.

    :param x:  the input tensor.
    :param dim:  the dimension to reduce,default None: get mean value of all elements.
    :param keepdims:  whether the output tensor has dim retained or not,default False.
    :return: returns the variance value of the input tensor.

    """
def median(x: XTensor, axis: Incomplete | None = None, keepdims: bool = False):
    """    Obtain the median value of XTensor along a specific axis or get median value of all elements.

    :param x: the input tensor.
    :param axis: the dimension to reduce,default None: get median value of all elements.default:None.
    :param keepdims: whether the output tensor has dim retained or not,default False.

    :return: Returns the median of the values in input.


    """
def topk(x, k, axis: int = -1, if_descent: bool = True):
    """
    Returns the k largest elements of the given input tensor along a given dimension.

    If if_descent is False then the k smallest elements are returned.

    :param t: input XTensor
    :param k: top K
    :param axis: the dimension to sort along.default = -1 ,last axis
    :param if_descent: if set to true, algorithm will sort by if_descent order,
            otherwise sort by ascending order.default is True.
    :return: A XTensor
    """
def argtopk(x, k, axis: int = -1, if_descent: bool = True):
    """
    Returns the k largest elements of the given input tensor along a given dimension.

    If if_descent is False then the k smallest elements are returned.

    :param t: input XTensor
    :param k: top K
    :param axis: the dimension to sort along.default = -1 ,last axis
    :param if_descent: if set to true, algorithm will sort by if_descent order,
            otherwise sort by ascending order.default is True.
    :return: A XTensor
    """
topK = topk
argtopK = argtopk

def sort(x, axis: Incomplete | None = None, descending: bool = False, stable: bool = True):
    """
    Sort tensor along the axis

    :param x: input tensor
    :param axis: sort axis
    :param descending: sort order if desc,default= False
    :param stable:  Whether to use stable sorting or not,default = True
    :return: A XTensor

    """
def argsort(x, axis: Incomplete | None = None, descending: bool = False, stable: bool = True):
    """
    Sort tensor along the axis

    :param x: input tensor
    :param axis: sort axis
    :param descending: sort order if desc,default= False
    :param stable:  Whether to use stable sorting or not,default = True
    :return: A XTensor

    """
def frobenius_norm(x: XTensor, axis: int = None, keepdims: bool = False):
    """
    Sums all the elements in tensor along given axis

    :param x: 'XTensor' - input tensor
    :param axis: 'int' - defaults to None
    :param keepdims: 'bool' - defaults to False
    :return:  XTensor

    """
def maximum(x1: XTensor, x2: XTensor):
    """
    Element-wise maximum of two tensor.

    :param x1: 'XTensor' - first tensor
    :param x2: 'XTensor' - second tensor
    :return:  XTensor

    """
def minimum(x1: XTensor, x2: XTensor):
    """
    Element-wise maximum of two tensor.

    :param x1: 'XTensor' - first tensor
    :param x2: 'XTensor' - second tensor
    :return:  XTensor

    """
def power(x1, x2): ...
def where(condition, x: Incomplete | None = None, y: Incomplete | None = None):
    """where(condition, [x, y])
    Return elements chosen from `x` or `y` depending on `condition`.

    :param condition: 'XTensor' - condition tensor
    :param x: 'XTensor' - tensor from which to take elements if condition is met
    :param y: 'XTensor' - tensor from which to take elements if condition is not met
    defaults to None
    :return: XTensor

    """
def tril(x, k: int = 0):
    """
    Returns the lower triangular part of the matrix (2-D tensor) or batch of matrices input,
    the other elements of the result tensor out are set to 0.
    The lower triangular part of the matrix is defined as the elements on and below the diagonal.
    The argument diagonal controls which diagonal to consider. If diagonal = 0, all elements on and
    below the main diagonal are retained. A positive value includes
    just as many diagonals above the main diagonal,
    and similarly a negative value excludes just as many diagonals below the main diagonal.

    :param x: 'XTensor' - input XTensor
    :param k: offset (0 for the main diagonal, positive for the nth
        diagonal above the main one, negative for the nth diagonal below the
        main one), default =0.
    :return: output XTensor
    """
def triu(x, k: int = 0):
    """
    Returns the upper triangular part of a matrix (2-D tensor) or batch of matrices input,
    the other elements of the result tensor out are set to 0.
    The upper triangular part of the matrix is defined as the elements on and above the diagonal.
    The argument diagonal controls which diagonal to consider. If diagonal = 0, all elements on and
    above the main diagonal are retained. A positive value excludes
    just as many diagonals above the main diagonal,
    and similarly a negative value includes just as many diagonals below the main diagonal.

    :param x: 'XTensor' - input XTensor
    :param k: offset (0 for the main diagonal, positive for the nth
        diagonal above the main one, negative for the nth diagonal below the
        main one), default =0.
    :return: output XTensor
    """
def matmul(x1, x2):
    """
    Matrix multiplications of 2d matrixs or batch matrix multiplications of 3d,4d matrix.

    :param x1: 'XTensor' - first tensor
    :param x2: 'XTensor' - second tensor
    :return:  XTensor

    """
def reciprocal(x):
    """    Compute the element-wise reciprocal of the tensor.

    :param t: input tensor
    :return: A XTensor

    """
def trace(x, k: int = 0):
    """    Sum diagonal elements.

    :param x: 'XTensor' - input tensor
    :param k: offset (0 for the main diagonal, positive for the nth
        diagonal above the main one, negative for the nth diagonal below the
        main one)
    :return: float

    """
def logspace(start, stop, num, base, device: Incomplete | None = None, dtype: int | None = None):
    """

    Create a 1D tensor with evenly spaced values on a log scale.
    Bool, Complex128, Complex64 type is not supported.
    
    :param start: ``base ** start`` is the starting value
    :param stop: ``base ** end`` is the final value of the sequence
    :param num: number of samples to generate
    :param base: the base of the log space
    :param device: device to use,default = 0,use cpu device.
    :param dtype: data type, default: None, use default data type.

    :return: XTensor
    """
def linspace(start, stop, num, device: Incomplete | None = None, dtype: int | None = None):
    """Return evenly spaced numbers within a specified interval.

    :param start: starting value
    :param stop: end value
    :param num: number of samples to generate
    :param device: device to use,default = 0,use cpu device.
    :param dtype: data type, default: None, use default data type.

    :return: XTensor

    """
def arange(start, stop, step: float = 1.0, device: Incomplete | None = None, dtype: int | None = None):
    """Returns evenly spaced values within a given interval.

    :param start: start of interval
    :param stop: end of interval
    :param step: spacing between values
    :param device: device to use,default = 0,use cpu device.
    :param dtype: data type, default: None, use default data type.

    :return: XTensor

    """
def zeros_like(xtensor):
    """
    Return zero-tensor with the same shape as the input tensor.

    :param xtensor: 'XTensor' - input parameter

    :return:  XTensor

    """
def ones_like(xtensor):
    """
    Return one-tensor with the same shape as the input tensor.

    :param xtensor: 'XTensor' - input parameter

    :return:  XTensor

    """
def empty_like(xtensor):
    """
    Return empty tensor with the same shape as the input tensor.

    :param xtensor: 'XTensor' - reference tensor.

    :return:  XTensor

    """
def empty(shape, device: Incomplete | None = None, dtype: int | None = None):
    """
    Return empty XTensor with the input shape.

    :param shape: shape to created.
    :param device: which device(cpu/gpu),default = None,use cpu device.
    :param dtype: data type, default: None, use default data type.
    :return: XTensor with the input shape.

    """
def zeros(shape, device: Incomplete | None = None, dtype: int | None = None):
    """
    Return XTensor contains 0 with the input shape.

    :param shape: shape to created.
    :param device: which device(cpu/gpu),default = None,use cpu device.
    :param dtype: data type, default: None, use default data type.
    :return: XTensor with the input shape.

    """
def ones(shape, device: Incomplete | None = None, dtype: int | None = None):
    """
    Return XTensor contains 1 with the input shape.

    :param shape: shape to created.
    :param device: which device(cpu/gpu),default = None,use cpu device.
    :param dtype: data type, default: None, use default data type.
    :return: XTensor with the input shape.

    """
def full(shape, val, device: Incomplete | None = None, dtype: int | None = None):
    """
    Create a tensor of the specified shape and fill it with ``value``.

    :param shape: shape of the tensor to create
    :param val: value to fill the tensor with
    :param device: device to use,default = None,use cpu device.
    :param dtype: data type, default: None, use default data type.
    :return: A XTensor

    """
def full_like(other_tensor, val):
    """
    Create a tensor of the specified shape and fill it with ``value``.

    :param other_tensor:  input XTensor
    :param value: value to fill the tensor with.

    :return: A XTensor

    """
def randn(shape, mean: float = 0.0, std: float = 1.0, device: Incomplete | None = None, dtype: int | None = None):
    """

    Create a tensor with noraml distributed random values.

    :param shape: shape of the tensor to create
    :param mean: minimum of uniform distribution,default:0.
    :param std: maximum of uniform distribution,default:1.
    :param device: device to use,default = None
    :param dtype: data type, default: None ,use default data type.

    :return: XTensor
    """
def randu(shape, low: float = 0.0, high: float = 1.0, device: Incomplete | None = None, dtype: int | None = None):
    """

    Create a tensor with uniformly distributed random values.

    :param shape: shape of the tensor to create
    :param low: minimum of uniform distribution,default:0.
    :param high: maximum of uniform distribution,default:1.
    :param device: device to use,default = None
    :param dtype: data type, default: None ,use default data type.

    :return: XTensor
    """
def multinomial(t, num_samples):
    """
    Returns a tensor where each row contains num_samples indices sampled
    from the multinomial probability distribution located in the corresponding row of tensor input.

    :param t: the input tensor containing probabilities.
    :param num_samples: number of samples to draw

    :return:
         the output index.
    """
def masked_fill(t, mask, value):
    """
    Fills elements of self tensor with value where mask ==1.
    The shape of mask must be broadcastable with the shape of the underlying XTensor.

    :param t: input XTensor
    :param mask: mask XTensor
    :param value: filled value
    :return: A XTensor

    """
def cumsum(x, axis: int = -1):
    """
    Returns the cumulative sum of elements of input in the dimension axis.

    :param t: 'XTensor' - input XTensor
    :param axis: 'int' - defaults -1, ues last axis
    :return:  XTensor

    """
def diag(t, k: int = 0):
    """    Select diagonal elements or construct a diagonal XTensor.

    If input is 2-D XTensor,returns a new tensor which is the same as this one, except that
    elements other than those in the selected diagonal are set to zero.

    If t is a 1-D XTensor, return a 2-D XTensor with v on the k-th diagonal.

    :param t: input tensor
    :param k: offset (0 for the main diagonal, positive for the nth
        diagonal above the main one, negative for the nth diagonal below the
        main one)

    :return: A XTensor

    """
def eye(size, offset: int = 0, device: Incomplete | None = None, dtype: int | None = None):
    """    Create a ``size x size`` tensor with ones on the diagonal and zeros
    elsewhere.

    :param size: size of the (square) tensor to create
    :param offset: Index of the diagonal: 0 (the default) refers to the main diagonal,
    a positive value refers to an upper diagonal, and a negative value to a lower diagonal.
    :param device: device to use,default = 0,use cpu device.
    :param dtype: data type, default: None, use default data type.
    :return: XTensor

    Examples::

        size = 3
        t = eye(size)
    """
def broadcast_to(self, shape):
    """Broadcasts the input array to a new shape.

    Subject to certain constraints, the array t is “broadcast” to the
    reference shape, so that they have compatible shapes.

    https://numpy.org/doc/stable/user/basics.broadcasting.html

    :param t: input XTensor
    :param ref: reference shape.
    :return :  new broadcasted XTensor of t.
    
    """
def broadcast(t1, t2):
    """
    Subject to certain constraints, the smaller array is “broadcast” across the
    larger array so that they have compatible shapes.

    https://numpy.org/doc/stable/user/basics.broadcasting.html

    :param t1: input XTensor 1
    :param t2: input XTensor 2
    :return t1 :  t1 with new broadcasted shape.
    :return t2 :  t2 with new broadcasted shape.

    """
def sign(self): ...
def flip(x, filp_dims):
    """
    Reverse the order of a n-D tensor along given axis in dims.

    :param t: 'XTensor' - input XTensor
    :param flip_dims: a list or tuple,axis to flip on
    :return:  XTensor
    """
def tile(x, reps):
    """
    Construct an array by repeating tensors the number of times given by reps.

    If reps has length d, the result will have dimension of max(d, t.ndim).

    If t.ndim < d, t is promoted to be d-dimensional by prepending new axes.
    So a shape (4,) array is promoted to (1, 4) for 2-D replication,
    or shape (1, 1, 4) for 3-D replication.

    If this is not the desired behavior, promote t to d-dimensions manually
    before calling this function.

    If t.ndim > d, reps is promoted to t.ndim by pre-pending 1’s to it.
    Thus for an A of shape (4, 1, 2, 5), a reps of (3, 2) is treated as (1, 1, 3, 2).

    :param t: input XTensor
    :param reps: the number of repetitions per dimension.
    :return: new tensor

    """
def flatten(x, start: int = 0, end: int = -1):
    """
    Flatten tensor from dim start to dim end.

    :param start: 'int' - dim start
    :param end: 'int' - dim start
    :return:  XTensor
    """
def squeeze(t, axis: Incomplete | None = None):
    """
    Remove axes of length one .if `axis` is not specified, remove all single-dimensional axis from the shape of a tensor. 

    :param t: input XTensor
    :param axis: squeeze axis
    :return: A XTensor


    """
def unsqueeze(t, axis: int = 0):
    """
    Returns a new tensor with a dimension of size one added at the specified position.

    :param t: input XTensor
    :param axis: unsqueeze axis,default:0.
    :return: A XTensor
    """
def boolean_mask_assign_scalar(data, mask, value, start_axis) -> None: ...
def boolean_mask_assign_xtensor(data, mask, value, start_axis) -> None: ...
def slice_with_step(self, begin, end, step):
    """
    crop subset of this NDarray in place.
    Returns the view of this XTensor.
    """
def swapaxis(x, axis1: int, axis2: int):
    """
    Interchange two axes of an array.
    :param x: input xtensor
    :param axis1: First axis.
    :param axis2:  Destination position for the original axis. These must also be unique
    :return: A XTensor

    """
def reshape(self, new_shape):
    """    Change the tensor's shape ,return a new Tensor.

    :param new_shape: the new shape (list of integers)
    :return: new XTensor

    """
def permute(self, *axes): ...
def transpose(self, *axes):
    """        
    Reverse or permute the axes of an array.if new_dims = None, revsers the dim.

    :param axes: the new order of the dimensions (list of integers).
    :return: a new XTensor.
    """
def nonzero_for_indexing(a):
    """
    Returns a tensor containing the indices of nonzero elements.

    :param a: input tensor
    :return: A new XTensor
    """
def nonzero(a):
    """
    Returns a tensor containing the indices of nonzero elements.

    :param a: input tensor
    :return: A new XTensor
    """
def greater(lhs, rhs):
    """
        Compute the truth value of ``lhs > rhs`` element-wise.
        if element is 0, it presents False,else True.

        :param lhs: a XTensor
        :param rhs: a XTensor
        :return: XTensor
    """
def greater_equal(lhs, rhs):
    """
        Compute the truth value of ``lhs >= rhs`` element-wise.
        if element is 0, it presents False,else True.

        :param lhs: a XTensor
        :param rhs: a XTensor
        :return: XTensor
    """
def equal(lhs, rhs):
    """
        Compute the truth value of ``lhs == rhs`` element-wise.
        if element is 0, it presents False,else True.

        :param lhs: a XTensor
        :param rhs: a XTensor
        :return: XTensor
    """
def not_equal(lhs, rhs):
    """
        Compute the truth value of ``lhs != rhs`` element-wise.
        if element is 0, it presents False,else True.

        :param lhs: a XTensor
        :param rhs: a XTensor
        :return: XTensor
    """
def lesser_equal(lhs, rhs):
    """
        Compute the truth value of ``lhs <= rhs`` element-wise.
        if element is 0, it presents False,else True.

        :param lhs: a XTensor
        :param rhs: a XTensor
        :return: XTensor
    """
less_equal = lesser_equal

def lesser(lhs, rhs):
    """
        Compute the truth value of ``lhs < rhs`` element-wise.
        if element is 0, it presents False,else True.

        :param lhs: a XTensor
        :param rhs: a XTensor
        :return: XTensor
    """
less = lesser

def logical_and(lhs, rhs):
    """
        Compute the truth value of ``lhs and rhs`` element-wise.
        if element is 0, it presents False,else True.

        :param lhs: a XTensor
        :param rhs: a XTensor
        :return: XTensor
    """
def logical_xor(lhs, rhs):
    """
        Compute the truth value of ``lhs xor rhs`` element-wise.
        if element is 0, it presents False,else True.

        :param lhs: a XTensor
        :param rhs: a XTensor
        :return: XTensor
    """
def logical_or(lhs, rhs):
    """
        Compute the truth value of ``lhs or rhs`` element-wise.
        if element is 0, it presents False,else True.

        :param lhs: a XTensor
        :param rhs: a XTensor
        :return: XTensor
    """
def logical_not(t):
    """
        Compute the truth value of ``not t`` element-wise.if element is 0, it presents False,else True.

        :param t: a XTensor
        :return: XTensor
    """
def isfinite(t):
    """    Test element-wise for finiteness (not infinity or not Not a Number).

    :param t: input XTensor
    :return: XTensor with each elements presents 1, if the tensor value is isfinite. else 0.

    """
def isinf(t):
    """    Test element-wise for positive or negative infinity.

    :param t: input XTensor
    :return: XTensor with each elements presents 1, if the tensor value is isinf. else 0.

    """
def isnan(t):
    """    Test element-wise for Nan.

    :param t: input XTensor
    :return: XTensor with each elements presents 1, if the tensor value is isnan. else 0.

    """
def isneginf(t):
    """    Test element-wise for negative infinity.

    :param t: a XTensor
    :return: XTensor with each elements presents 1, if the tensor value is isneginf. else 0.
    """
def isposinf(t):
    """    Test element-wise for positive infinity.

    :param t: a XTensor
    :return: XTensor with each elements presents 1, if the tensor value is isposinf. else 0.

    """
def max(self, axis: Incomplete | None = None, keepdims: bool = False):
    """    Returns the maximum value of all elements in the input tensor,or
    Returns the maximum values of a tensor across a dimension.

    :param self: 'XTensor' - input tensor
    :param axis: 'int' - defaults to None
    :param keepdims: 'bool' - defaults to False
    :return: XTensor

    """
def min(self, axis: Incomplete | None = None, keepdims: bool = False):
    """    Returns the minimum value of all elements in the input tensor, or
    Returns the minimum values of a tensor across a dimension.

    :param self: 'XTensor' - input tensor
    :param axis: 'int' - defaults to None
    :param keepdims: 'bool' - defaults to False
    :return: XTensor

    """
def clip(t: XTensor, min_val, max_val):
    """
    Clips input tensor to minimum and maximum value.

    :param t: 'XTensor' - input tensor
    :param min_val: 'float' - minimum value
    :param max_val: 'float' - maximum value
    :return:  XTensor

    """
def index_select(x, dim, indices: XTensor):
    """
    Returns a new tensor which indexes the input tensor along dimension ``dim`` 
    using the entries in index.

    The returned tensor has the same number of dimensions as the original tensor (input). 
    The ``dim`` dimension has the same size as the length of index;
    other dimensions have the same size as in the original tensor.

    :param t: input XTensor
    :param dim: the dimension which we index
    :param indice: the 1D XTensor containing index

    :return: A new XTensor
    """
def copyto(self, other):
    """Copies the value of this array to another array.

    If ``other`` is a ``XTensor`` object, then ``other.shape`` and
    ``self.shape`` should be the same. This function copies the value from
    ``self`` to ``other``.

    If ``other`` is a context, a new ``XTensor`` will be first created on
    the target context, and the value of ``self`` is copied.

    """
def attach_new_grad(self, new_grad, grad_req: str = 'write'): ...
to_xtensor = xtensor

def get_indexing_dispatch_code(key):
    """Returns a dispatch code for calling basic or advanced indexing functions."""
def indexing_key_expand_implicit_axes(key, shape):
    """
    Make implicit axes explicit by adding ``slice(None)``
    and convert boolean array to integer array through `nonzero`.

    """
def maybe_wrap_dim(dim: int, dim_post_expr: int, wrap_scalar: bool = True):
    """    check dim valid
    """
