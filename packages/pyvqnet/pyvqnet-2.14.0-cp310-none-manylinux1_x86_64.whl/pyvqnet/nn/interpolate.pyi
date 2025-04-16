from ..tensor import AutoGradNode as AutoGradNode, OPNodesInfo as OPNodesInfo, QTensor as QTensor, get_global_onnx_convert_config as get_global_onnx_convert_config
from _typeshed import Incomplete
from pyvqnet.nn.module import Module as Module

def interpolate(x, size: Incomplete | None = None, scale_factor: Incomplete | None = None, mode: str = 'nearest', align_corners: Incomplete | None = None, recompute_scale_factor: Incomplete | None = None): ...

class Interpolate(Module):
    '''The interface is consistent with PyTorch.    
    
    The documentation is referenced from: https://pytorch.org/docs/1.10/_modules/torch/nn/functional.html#interpolate.

    Down/up samples the input to either the given :attr:`size` or the given
    :attr:`scale_factor`.

    The algorithm used for interpolation is determined by :attr:`mode`.

    Currently only supports data with a 4-D input.

    The input dimensions are interpreted in the form: `mini-batch x channels x height x width`.

    The modes available for resizing are: `nearest`, `bilinear`, `bicubic`.

    :param size: output spatial size.
    :param scale_factor: multiplier for spatial size. Has to match input size if it is a tuple.
    :param mode: algorithm used for upsampling: ``\'nearest\'`` | ``\'bilinear\'`` | ``\'bicubic\'``.
    :param align_corners: Geometrically, we consider the pixels of the
            input and output as squares rather than points.
            If set to ``True``, the input and output tensors are aligned by the
            center points of their corner pixels, preserving the values at the corner pixels.
            If set to ``False``, the input and output tensors are aligned by the corner
            points of their corner pixels, and the interpolation uses edge value padding
            for out-of-boundary values, making this operation *independent* of input size
            when :attr:`scale_factor` is kept the same. This only has an effect when :attr:`mode`
            is ``\'bilinear\'``.
            Default: ``False``
    :param recompute_scale_factor: recompute the scale_factor for use in the
            interpolation calculation.  When `scale_factor` is passed as a parameter, it is used
            to compute the `output_size`.
    :param name: name of module,default:"".
    
    .. note::
        With ``mode=\'bicubic\'``, it\'s possible to cause overshoot, in other words it can produce
        negative values or values greater than 255 for images.
        Explicitly call ``result.clamp(min=0, max=255)`` if you want to reduce the overshoot
        when displaying the image.

    .. warning::
        With ``align_corners = True``, the linearly interpolating modes
        (`linear`, `bilinear`, and `trilinear`) don\'t proportionally align the
        output and input pixels, and thus the output values can depend on the
        input size. This was the default behavior for these modes up to version
        0.3.1. Since then, the default behavior is ``align_corners = False``.
        See :class:`~torch.nn.Upsample` for concrete examples on how this
        affects the outputs.

    .. warning::
        When scale_factor is specified, if recompute_scale_factor=True,
        scale_factor is used to compute the output_size which will then
        be used to infer new scales for the interpolation.

    For example:
    
        from pyvqnet.nn import Interpolate
        from pyvqnet.tensor import tensor 
        import pyvqnet
        pyvqnet.utils.set_random_seed(1)

        import numpy as np
        np.random.seed(0)

        from time import time
        np_ = np.random.randn(36).reshape((1, 1, 6, 6)).astype(np.float32)
        mode_ = "bilinear"
        size_ = 3

        class model_vqnet(pyvqnet.nn.Module):

            def __init__(self):
                super().__init__()
                self.inter = Interpolate(size = size_, mode=mode_)
                self.ln = pyvqnet.nn.Linear(9, 1)
                self.ln.weights.init_from_tensor(tensor.QTensor([[-0.0553,  0.3315,  0.1469,  0.2884, -0.3333, -0.2479, -0.1318,  0.3327, -0.2355]], requires_grad=True).toGPU())
                self.ln.bias.init_from_tensor(tensor.QTensor([[-0.1759]], requires_grad=True).toGPU())
                
            def forward(self, x):
                x = self.inter(x).reshape((1,-1))
                x = self.ln(x)
                return 2 * x 

        input_vqnet = tensor.QTensor(np_,  dtype=pyvqnet.kfloat32, requires_grad=True).toGPU()
        model = model_vqnet().toGPU()
        loss_pyvqnet = pyvqnet.nn.MeanSquaredError()
        time3 = time()
        output_vqnet = model(input_vqnet)
        time4 = time()
        print(f"output_vqnet {output_vqnet} time {time4 - time3}")

        l = loss_pyvqnet(tensor.QTensor([[1.0]]).toGPU(), output_vqnet)
        l.backward()
        print(model.parameters()[0].grad)

    '''
    size: Incomplete
    scale_factor: Incomplete
    mode: Incomplete
    recompute_scale_factor: Incomplete
    align_corners: Incomplete
    height_scale: Incomplete
    width_scale: Incomplete
    def __init__(self, size: int | tuple[int, ...] | None = None, scale_factor: float | tuple[float, ...] | None = None, mode: str = 'nearest', align_corners: bool | None = None, recompute_scale_factor: bool | None = None, name: str = '') -> None: ...
    def forward(self, x): ...
