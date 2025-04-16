from .xtensor import XTensor as XTensor, cat as cat, full as full, index_select as index_select, make_array as make_array, stack as stack, swapaxis as swapaxis
from _typeshed import Incomplete

class PackedSequence:
    """
    Packed dynamic length XTensor data class.

    :param data: data of input XTensor.
    :param batch_sizes: sub batch sizes of inputs.
    :param sort_indice:  descending sorted indice of inputs.
    :param unsorted_indice: origin unsorted indice.

    """
    data: Incomplete
    batch_sizes: Incomplete
    sort_indice: Incomplete
    unsorted_indice: Incomplete
    def __init__(self, data, batch_sizes, sort_indice, unsorted_indice) -> None: ...

def invert_permutation(sort_indice): ...
def pack_pad_sequence(input, lengths, batch_first: bool = False, enforce_sorted: bool = True):
    """Packs a Tensor containing padded sequences of variable length.
    `input` should be shape of [batch_size,length,*] if batch_first is True, 
    be [length,batch_size,*] otherwise.
    `*` is any number of dimensions represent feature dimensions.
    For unsorted sequences, use `enforce_sorted = False`. If :attr:`enforce_sorted` is
        ``True``, the sequences should be sorted by length in a decreasing order.

    :param input: 'QTensor' - padded batch of variable length sequences.
    :param lengths: 'list' - list of sequence lengths of each batch
        element.
    :param batch_first : 'bool' - if ``True``, the input is expected in ``B x T x *``
        format,default:False.
    :param enforce_sorted:  'bool' - if ``True``, the input is expected to
        contain sequences sorted by length in a decreasing order. If
        ``False``, the input will get sorted unconditionally. Default: ``True``.

    :return: a :class:`PackedSequence` object.

    """
def pad_sequence(sequences, batch_first: bool = False, padding_value: int = 0):
    """Pad a list of variable length Tensors with ``padding_value``

    ``pad_sequence`` stacks a list of Tensors along a new dimension,
    and pads them to equal length.the input is list of
    sequences with size ``L x *``. L is variable length.

    :param qtensor_list: `list[QTensor]`- list of variable length sequences.
    :param batch_first: 'bool' - output will be in ``bacth_size x the longest sequence legnth x *`` if True, or in
        `` the longest sequence legnth x bacth_size x *`` otherwise. Default: False.
    :param padding_value: 'float' - padding value. Default: 0.

    :return:
        Tensor of size ``bacth_size x the longest sequence legnth x *`` if :attr:`batch_first` is ``False``.
        Tensor of size `` the longest sequence legnth x bacth_size x *`` otherwise.
    """
def pad_packed_sequence(sequence, batch_first: bool = False, padding_value: int = 0, total_length: Incomplete | None = None):
    """Pads a packed batch of variable length sequences.

    It is an inverse operation to :func:`pack_pad_sequence`.

    The returned Tensor's data will be of size ``T x B x *``, where `T` is the length
    of the longest sequence and `B` is the batch size. If ``batch_first`` is True,
    the data will be transposed into ``B x T x *`` format.

    :param sequence: 'QTensor' - batch data to pad
    :param batch_first: 'bool' - if ``True``, batch would be the first dim of input.default:False.
    :param padding_value: 'bool' - values for padded elements.default:0.
    :param total_length: 'bool' - if not ``None``, the output will
     be padded to have length :attr:`total_length`.default:None.
    :return:
        Tuple of Tensor containing the padded sequence, and a list of lengths of each sequence in the batch.
        Batch elements will be re-ordered as they were ordered originally.

    """
