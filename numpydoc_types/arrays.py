from functools import partial
import numpy as np
import re


def array_checker(arg_value, name, shape, shape_desc):
    """Checks the shape of an array.

    Parameters
    ----------
    arg_value : object
        The value of the argument that needs to be type checked.
    name : str
        The name of the argument. Used for generating a clear error message.
    shape : tuple of int
        The desired dimensions of the array.
    shape_desc : str
        The string description of the array shape, used in the error message.
    """
    if not isinstance(arg_value, np.ndarray):
        if np.isscalar(arg_value):
            raise TypeError(f'parameter `{name}` should be a NumPy array, but '
                            f'got a scalar value ({arg_value}) instead.')
        else:
            raise TypeError(f'parameter `{name}` should be a NumPy array, but '
                            f'got {arg_value!r} instead.')

    if arg_value.ndim != len(shape):
        raise TypeError(f'parameter `{name}` should have {len(shape)} '
                        f'dimensions ({shape_desc}), but given array has '
                        f'{arg_value.ndim} {arg_value.shape!r}.')


def make_array_checker(param_name, type_desc):
    """Make a checker function that will type check the numpy array.

    Parameters
    ----------
    param_name : str
        The name of the parameter to check.
    type_desc : str
        The type description of the parameter, containing array shape
        information
    """
    shape_desc = re.match(r'^array, shape \((.*)\)$', type_desc).groups()[0]
    shape = [dim.strip() for dim in shape_desc.split(',')]
    return partial(array_checker, name=param_name, shape=shape,
                   shape_desc=shape_desc)
