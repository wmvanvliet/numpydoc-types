"""
Proof of concept for a numpydoc based type checker.
"""
import importlib
import inspect
from functools import wraps, partial
import numpy as np
from numpydoc.docscrape import FunctionDoc, ParseError
import types

from . import checker_functions as cf
from . import arrays


def find_type_object(type_name):
    """Try to find the type object given the name of the type.

    Deals with cases such as `argparse.ArgumentParser` where a module needs to
    be imported before we can find the correct type object. If the type object
    cannot be found, a `NameError` is raised.

    Parameters
    ----------
    type_name : str
        The name of the type to search for.

    Returns
    -------
    type_object : type
        The type object corresponding to the given type name.
    """
    if '.' in type_name:
        # Full module name specified. Try to import it.
        module_name, object_name = type_name.rsplit('.', maxsplit=1)
        try:
            module = importlib.import_module(module_name)
        except ModuleNotFoundError:
            raise NameError(f'Type checker could not import `{module_name}`.')
        if object_name not in module.__dict__:
            raise NameError(f'Type checker could not find `{type_name}`.')
        return module.__dict__[object_name]
    else:
        # No module name specified. Assume it's a python buildin type.
        return eval(type_name)


def find_checker_function(param_name, param_type):
    """Find the proper type checking function for the given type name.

    Parameters
    ----------
    param_name : str
        The name of the parameter being checked. Used for clean error messages.
    param_type : str
        The name of the type of the parameter.

    Returns
    -------
    checker : function
        The function that will type check the parameters. The function
        parameters will be partially filled in already. Only the `arg_value`
        parameter is left blank.
    """
    if param_type == '' or param_type == ':':  # No type info
        checker = cf.check_ok
    if '|' in param_type:  # Compound types
        possible_types = [p.strip() for p in param_type.split('|')]
        checkers = [find_checker_function(param_name, possible_type)
                    for possible_type in possible_types]
        checker = partial(cf.compound_checker, name=param_name,
                          desired_type_desc=param_type, checkers=checkers)
    elif param_type == 'function':
        checker = partial(cf.check_type, name=param_name,
                          desired_type=types.FunctionType)
    elif param_type == 'generator':
        checker = partial(cf.check_type, name=param_name,
                          desired_type=types.GeneratorType)
    elif param_type == 'array':  # NumPy ndarray's
        checker = partial(cf.check_type, name=param_name,
                          desired_type=np.ndarray)
    elif param_type.startswith('array, shape'):  # array with shape information
        checker = arrays.make_array_checker(param_name, param_type)
    else:  # Explicit type
        try:
            desired_type = find_type_object(param_type)
            checker = partial(cf.check_type, name=param_name,
                              desired_type=desired_type)
        except NameError:
            # The code that defines the type could not be found. Fall back to
            # just testing whether the name of the type matches.
            checker = partial(cf.check_type_name, name=param_name,
                              desired_type_name=param_type)
    return checker


def check_types(f):
    """Decorator that adds runtime type checking.

    Parmeters
    ---------
    f : function
        The function to wrap a type checker around.

    Returns
    -------
    wrapper : function
        The wrapped function.
    """
    doc = FunctionDoc(f)
    checkers = dict()
    for param in doc['Parameters']:
        checkers[param.name] = find_checker_function(param.name, param.type)

    # Make sure that the checkers match the function parameters
    if list(checkers.keys()) != inspect.getargspec(f).args:
        raise ParseError('The arguments listed in the docstring for '
                         f'function `{f.__name__}` do not match the '
                         'arguments in the function signature.')

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
