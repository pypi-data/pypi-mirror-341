from .base import integer_types as integer_types
from .context import Context as Context, create_context as create_context, create_context_from_str as create_context_from_str, prepare_ctx_arg_str as prepare_ctx_arg_str

def seed(seed_state, device):
    """Seeds the random number generators in XTensor.

    This affects the behavior of modules in XTensor that uses random number generators,
    like the dropout operator and `XTensor`'s random sampling operators.

    """
