import pyvqnet.nn as nn
import pyvqnet.tensor as tensor
from .e2eqvit import scaled_dot_product_attention as scaled_dot_product_attention
from _typeshed import Incomplete
from pyvqnet import kbool as kbool
from pyvqnet.tensor import AutoGradNode as AutoGradNode, QTensor as QTensor

class SDPA(nn.Module):
    """
    SDPA (scaled dot product attention) layer .

    :param attn_mask: Attention mask; shape must be broadcastable to the shape of attention weights.
    :param dropout_p:  Dropout probability; if greater than 0.0, dropout is applied.
    :param scale:  Scaling factor applied prior to softmax.
    :param is_causal: If true, assumes upper left causal attention masking and errors if both attn_mask and is_causal are set.
    
    Examples::

        from pyvqnet.transformer import SDPA
        from pyvqnet import tensor
        import pyvqnet
        from time import time
        import pyvqnet.nn as nn
        import numpy as np

        np.random.seed(42)

        query_np = np.random.randn(3, 3, 3, 5).astype(np.float32) 
        key_np = np.random.randn(3, 3, 3, 5).astype(np.float32)   
        value_np = np.random.randn(3, 3, 3, 5).astype(np.float32) 

        model = SDPA(tensor.QTensor([1.]))

        query_p = tensor.QTensor(query_np, dtype=pyvqnet.kfloat32, requires_grad=True)
        key_p = tensor.QTensor(key_np, dtype=pyvqnet.kfloat32, requires_grad=True)
        value_p = tensor.QTensor(value_np, dtype=pyvqnet.kfloat32, requires_grad=True)

        out_sdpa = model(query_p, key_p, value_p)

        out_sdpa.backward()

    """
    attn_mask: Incomplete
    dropout_p: Incomplete
    scale: Incomplete
    is_causal: Incomplete
    def __init__(self, attn_mask: Incomplete | None = None, dropout_p: float = 0.0, scale: Incomplete | None = None, is_causal: bool = False) -> None: ...
    def forward(self, query: tensor.QTensor, key: tensor.QTensor, value: tensor.QTensor): ...
