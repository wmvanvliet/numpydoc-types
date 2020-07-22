An automatic type checker for numpydoc 
--------------------------------------

I'm thinking about writing an automatic type checker that parses docstrings in numpydoc style. It would operate at runtime and generate friendly error messages.

Ideas for the kind of checks it could do
========================================

Basic type checking

    """
    a : int
    b : str
    c : bool
    """
    if type(a) != int: raise TypeError(...)
    if type(b) != str: raise TypeError(...)
    if type(c) != bool: raise TypeError(...)
