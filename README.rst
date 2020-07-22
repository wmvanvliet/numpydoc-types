This is something I wish existed. Anyone want to help me build this?

An automatic type checker for numpydoc 
--------------------------------------

This will be an automatic type checker that parses docstrings in
`numpydoc <https://numpydoc.readthedocs.io/en/latest/format.html>`_
style. It operates at runtime and generates friendly error messages.

Usage
=====

Simply decorate your function or class with the ``check_types`` decorator::

    from numpydoc_types import check_types

    @check_types
    def my_function(a, b):
        """The type information in this docstring will be used to generate
        automatic type checks.

        Parameters
        ----------
        a : int
        b : array, shape (n, m)
        """

Then, when you call the function, type checking is performed::

    >>> my_function('foo', np.array([1]))
    TypeError: parameter `a` should be an integer, but got 'foo' instead
               parameter `b` should be a 2D array, but got 'bar' instead


Ideas for the kind of checks it could do
========================================

Basic type checking::

    """
    a : int
        A parameter
    b : str
        Some other parameter
    c : array
        Yet another parameter
    """
    if type(a) != int: raise TypeError(...)
    if type(b) != str: raise TypeError(...)
    if not isinstance(c, ndarray): raise TypeError(...)


Advanced type checking::

    """
    a : list of int
        A parameter
    b : tuple of str
        Some other parameter
    c : array of bool
        Yet another parameter
    """
    if type(a) != list or any([type(a_) != int for a_ in a]): raise TypeError(...)
    if type(b) != list or any([type(b_) != str for b_ in b]): raise TypeError(...)
    if not isinstance(c, ndarray) or c.dtype != np.bool: raise TypeError(...)

NumPy array dimensions checking::

    """
    a : array, shape (n, m)
        A parameter
    b : array, shape (n, k)
        Some other parameter
    c : array, shape (m, k, l)
        Yet another parameter
    """
    if not isinstance(a, ndarray): raise TypeError(...)
    if not isinstance(b, ndarray): raise TypeError(...)
    if not isinstance(c, ndarray): raise TypeError(...)
    if a.ndim != 2: raise TypeError(...)
    if b.ndim != 2: raise TypeError(...)
    if c.ndim != 3: raise TypeError(...)
    if b.shape[0] != a.shape[0]: raise TypeError(...)
    if c.shape[0] != a.shape[1]: raise TypeError(...)
    if c.shape[1] != b.shape[1]: raise TypeError(...)

Union types::

    """
    a : {array, None}
        An optional parameter
    b : {'foo', 'bar'}
        A toggle option
    c : {'foo', 'bar', None}
        An optional toggle option
    """
    if not isinstance(a, ndarray) or a is None: raise TypeError(...)
    if b not in ['foo', 'bar']: raise TypeError(...)
    if c not in ['foo', 'bar', None]: raise TypeError(...)
