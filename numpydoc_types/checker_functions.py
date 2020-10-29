def check_ok(arg):
    """Type check that always passes."""
    pass


def compound_checker(arg_value, name, desired_type_desc, checkers):
    """Run multiple checkers, at least one of which should match.

    Parameters
    ----------
    arg_value : object
        The value of the argument that needs to be type checked.
    name : str
        The name of the argument. Used for generating a clear error message.
    desired_type_desc : str
        The type description that `arg_value` should be, the way it was written
        in the docstring, so including the "|" symbols.
    checkers : list of function
        The checker functions that will check for each possible type. These
        checker functions should only take the `arg_value` parameter, the rest
        should be pre-filled using `functools.partial`.
    """
    for checker in checkers:
        try:
            checker(arg_value)
            return  # A check succeeded, type is good!
        except TypeError:
            # Check failed, but suppress the error, maybe the next checker will
            # succeed.
            pass
    else:
        # All checks failed
        raise TypeError(f'the type of parameter `{name}` should be one of '
                        f'{desired_type_desc}, but got {arg_value!r} '
                        'instead.')


def check_type(arg_value, name, desired_type):
    """Type check for an explicit type.

    Raises a `TypeError` if the type of the argument value does not match
    the desired type.

    Parameters
    ----------
    arg_value : object
        The value of the argument that needs to be type checked.
    name : str
        The name of the argument. Used for generating a clear error message.
    desired_type : type
        The type that `arg_value` should be.
    """
    if not isinstance(arg_value, desired_type):
        raise TypeError(f'parameter `{name}` should be of type '
                        f'{desired_type.__name__}, but got {arg_value!r} '
                        'instead.')


def check_type_name(arg_value, name, desired_type_name):
    """Check that the name of the type matches the desired type.

    Does not actually check the type, but rather whether the name of the type
    of `arg_value` matches.

    Parameters
    ----------
    arg_value : object
        The value of the argument that needs to be type checked.
    name : str
        The name of the argument. Used for generating a clear error message.
    desired_type_name : str
        The name of the type that `arg_value` should be.
    """
    if type(arg_value).__name__ != desired_type_name:
        raise TypeError(f'parameter `{name}` should be of type '
                        f'{desired_type_name}, but got {arg_value!r} '
                        'instead.')
