from _typeshed import Incomplete

class _XTensorClassPropertyDescriptor:
    fget: Incomplete
    fset: Incomplete
    def __init__(self, fget, fset: Incomplete | None = None) -> None: ...
    def __get__(self, obj, clas: Incomplete | None = None): ...
    def __set__(self, obj, value): ...
    def setter(self, func): ...

class XTensorClassPropertyMetaClass(type):
    def __setattr__(cls, key, value): ...

def with_metaclass(meta, *bases):
    """Create a base class with a metaclass."""
def classproperty(func): ...
basestring = str
long = int
numeric_types: Incomplete
integer_types: Incomplete
