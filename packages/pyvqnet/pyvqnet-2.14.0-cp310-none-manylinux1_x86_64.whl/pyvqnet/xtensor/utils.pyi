def check_attr_same(attr1, attr2): ...
def get_dim_size(start, stop, step):
    """Given start, stop, and step, calculate the number of elements
    of this slice.
    """
def int_to_slice(idx):
    """Return a slice that indexes the same entries as a single int."""
def get_index_range(start, stop, length, step: int = 1):
    """Given start, stop, step and array length, return
    absolute values of start, stop, and step for generating index range.
    The returned values have been compensated by adding length if they
    are less than zero for all the cases but slice(None, None, -1).
    Note that the returned value of stop is not necessarily >= 0, since
    absolute stop is -1 in the case of slice(None, None, -1)."""
def get_slice_len(slc, seq_length):
    """Given a python slice object and the length of the sequence, calculate the number of elements
     in the slice.

    Parameters
    ----------
    slc : py_slice
        The slice object
    seq_length : int
        The length of the object you are going to apply the slice on

    Returns
    -------
    ret : int
        Total number of elements in the slice
    """
def broadcast_shapes(seq):
    """Return the broadcast shape of all advanced indices in ``seq``.

    All entries are assumed to have a ``shape`` property.
    """
def get_oshape_of_gather_nd_op(dshape, ishape):
    """Given data and index shapes, get the output `XTensor` shape.
    This basically implements the infer shape logic of op gather_nd."""
def shape_for_bcast(shape, target_ndim, new_axes):
    """Return shape with added axes for broadcasting in ``target_ndim`` dimensions.

    If ``shape`` is shorter than ``target_ndim``, fixed ``1`` entries are inserted
    into the returned shape, in locations indexed by ``new_axes``. The rest is
    filled from the back with ``shape`` while possible.
    """
def check_boolean_array_dimension(array_shape, axis, bool_shape) -> None:
    """
    Advanced boolean indexing is implemented through the use of `nonzero`.
    Size check is necessary to make sure that the boolean array
    has exactly as many dimensions as it is supposed to work with before the conversion
    """
