"""
Proof of concept for a numpydoc based type checker.
"""
from numpydoc.docscrape import FunctionDoc
from functools import wraps, partial
import numpy as np


def check_ok(arg):
    """Type check that always passes."""
    pass


def check_type(arg, name, desired_type):
    """Type check for an explicit type."""
    if type(arg) != desired_type:
        raise TypeError(f"parameter `{name}` should be of type "
                        f"{desired_type.__name__}, but got {arg!r} instead.")


def check_types(f):
    """Decorator that adds runtime type checking."""
    doc = FunctionDoc(f)
    checkers = dict()  # List of all typechecker functions that will be run.
    for i, param in enumerate(doc['Parameters']):
        if param.type == 'array':  # NumPy ndarray's
            c = partial(check_type, name=param.name, desired_type=np.ndarray)
        elif param.type == '' or param.type == ':':  # No type info
            c = check_ok
        else:  # Explicit type
            c = partial(check_type, name=param.name,
                        desired_type=eval(param.type))
        checkers[param.name] = c

    @wraps(f)
    def wrapper(*args, **kwds):
        # Check positional arguments
        for arg, checker in zip(args, checkers.values()):
            checker(arg)
        # Check keyword arguments
        for name, arg in kwds.items():
            checkers[name](arg)
        return f(*args, **kwds)
    return wrapper


@check_types
def foo(a, b, c, d=None):
    """Some function

    Parameters
    ----------
    a : int
        A parameter
    b : str
        Some other parameter
    c : array
        Yet another parameter
    d :
        Undocumented type
    """
    pass


try:
    foo(1, 'hello', np.array([1, 2, 3]))
except TypeError as e:
    print(1, e)

try:
    foo(1, 2, np.array([1, 2, 3]))
except TypeError as e:
    print(2, e)

try:
    foo(1, 'hello', 'bar')
except TypeError as e:
    print(3, e)

try:
    foo('foo', 'hello', np.array([1, 2, 3]))
except TypeError as e:
    print(4, e)

try:
    foo('foo', b='hello', c=np.array([1, 2, 3]))
except TypeError as e:
    print(5, e)

try:
    foo(a='foo', b='hello', c=np.array([1, 2, 3]))
except TypeError as e:
    print(6, e)

try:
    foo(b='hello', a='foo', c=np.array([1, 2, 3]))
except TypeError as e:
    print(7, e)
