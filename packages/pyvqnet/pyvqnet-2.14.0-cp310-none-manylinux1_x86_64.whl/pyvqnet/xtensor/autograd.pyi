def not_record(train_mode: bool = False):
    """Returns an autograd recording scope context to be used in 'with' statement
    and captures code that needs gradients to be calculated.

    .. note:: When forwarding with train_mode=False, the corresponding backward
              should also use train_mode=False, otherwise gradient is undefined.

    :param train_mode: train mode ,defalut:False

    """
def record(train_mode: bool = True):
    """Returns an autograd recording scope context to be used in 'with' statement
    and captures code that needs gradients to be calculated.

    .. note:: When forwarding with train_mode=False, the corresponding backward
              should also use train_mode=False, otherwise gradient is undefined.

    :param train_mode: train mode,defalut:True
    """
tape = record

class RecordingStateScope:
    """Scope for managing training state.

    """
    def __init__(self, is_record, train_mode) -> None:
        """

        :param is_record: if record.
        :param train_mode: train mode.

        """
    def __enter__(self) -> None: ...
    def __exit__(self, ptype: type[BaseException] | None, value: BaseException | None, trace: types.TracebackType | None) -> None: ...

def set_if_record(flag): ...
def set_if_training(flag): ...
def get_if_record(): ...
def get_if_training(): ...
