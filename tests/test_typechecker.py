import pytest
import numpydoc
from numpydoc.docscrape import ParseError

from numpydoc_types import check_types


def test_decorator():
    """Test whether the decorator properly extracts the docstring."""

    @check_types
    def foo(a, b):
        """Some function.

        Let's see if the docstring is properly extracted and the types parsed.

        Parameters
        ----------
        a : int
            A parameter
        b : str
            Some other parameter

        Returns
        -------
        Nothing

        Notes
        -----
        Some more sections of the numpydoc compatible docstring.
        """
        pass

    # Try calling the function. This should work.
    foo(1, 'hello')

    # Typechecker should catch this type error on the second parameter.
    with pytest.raises(TypeError, match='parameter `b` should be of type str'):
        foo(1, 2)


def test_invalid_docstring():
    """Test detection of invalid docstrings."""

    with pytest.raises(ParseError, match='do not match'):
        @check_types
        def no_docstring(a, b):
            pass

    with pytest.raises(ParseError, match='do not match'):
        @check_types
        def wrong_number_of_parameters(a, b):
            '''The numer of parameters does not match.

            Parameters
            ----------
            a : int
            b : int
            c : int
            '''
            pass

    with pytest.raises(ParseError, match='do not match'):
        @check_types
        def wrong_order(a, b):
            '''The parameter order does not match.

            Parameters
            ----------
            b : int
            a : int
            '''
            pass


def test_basic_types():
    """Test checking basic Python buildin types."""
    def gen():
        yield 1

    @check_types
    def foo(a=1, b=1.1, c='test', d=True, e=list(), f=dict(), g=set(),
            h=tuple(), i=lambda x: 1, j=gen, k=object):
        """Some function.

        Parameters
        ----------
        a : int
        b : float
        c : str
        d : bool
        e : list
        f : dict
        g : set
        h : tuple
        i : function
        j : generator
        k : object
        """

    # Proper invocation of this function
    foo()
    foo(1, 1.1, 'test', True, list(), dict(), set(), tuple(), foo, gen(), None)
    foo(c='test', k='a string is an object')

    # Non-proper invocations
    with pytest.raises(TypeError, match='parameter `a`'):
        foo(1.1)
    with pytest.raises(TypeError, match='parameter `a`'):
        foo(a=1.1)
    with pytest.raises(TypeError, match='parameter `b`'):
        foo(1, 1)
    with pytest.raises(TypeError, match='parameter `b`'):
        foo(b=1)
    with pytest.raises(TypeError, match='parameter `c`'):
        foo(1, 1.1, 1)
    with pytest.raises(TypeError, match='parameter `c`'):
        foo(c=1)
    with pytest.raises(TypeError, match='parameter `d`'):
        foo(1, 1.1, 'test', 1)
    with pytest.raises(TypeError, match='parameter `d`'):
        foo(d=1)
    with pytest.raises(TypeError, match='parameter `e`'):
        foo(1, 1.1, 'test', True, 1)
    with pytest.raises(TypeError, match='parameter `e`'):
        foo(e=1)
    with pytest.raises(TypeError, match='parameter `f`'):
        foo(1, 1.1, 'test', True, list(), 1)
    with pytest.raises(TypeError, match='parameter `f`'):
        foo(f=1)
    with pytest.raises(TypeError, match='parameter `g`'):
        foo(1, 1.1, 'test', True, list(), dict(), 1)
    with pytest.raises(TypeError, match='parameter `g`'):
        foo(g=1)
    with pytest.raises(TypeError, match='parameter `h`'):
        foo(1, 1.1, 'test', True, list(), dict(), set(), 1)
    with pytest.raises(TypeError, match='parameter `h`'):
        foo(h=1)
    with pytest.raises(TypeError, match='parameter `i`'):
        foo(1, 1.1, 'test', True, list(), dict(), set(), tuple(), 1)
    with pytest.raises(TypeError, match='parameter `i`'):
        foo(i=1)
    with pytest.raises(TypeError, match='parameter `j`'):
        foo(1, 1.1, 'test', True, list(), dict(), set(), tuple(), foo, 1)
    with pytest.raises(TypeError, match='parameter `j`'):
        foo(j=1)
    # parameter `k` can be anything


def test_package_defined_types():
    """Test checking types defined by some python package."""
    @check_types
    def foo(a):
        """Some function.

        Parameters
        ----------
        a : numpydoc.docscrape.NumpyDocString
        """
        pass

    # Proper invocation of the function
    foo(numpydoc.docscrape.NumpyDocString(''))

    # Non-proper invocation
    with pytest.raises(TypeError, match='NumpyDocString'):
        foo(1)


def test_user_types():
    """Test checking user defined types."""
    class SomeClass:
        pass

    @check_types
    def foo(a):
        """Some function.

        Parameters
        ----------
        a : SomeClass
        """
        pass

    # Proper invocation of the function
    foo(SomeClass())

    # Non-proper invocation
    with pytest.raises(TypeError, match='SomeClass'):
        foo(1)


def test_compound_types():
    """Testing checking arguments that can be one of multiple types."""
    @check_types
    def foo(a):
        """Some function.

        Parameters
        ----------
        a : int | float | numpydoc.docscrape.NumpyDocString
        """
        pass

    # Proper invocations
    foo(1)
    foo(1.1)
    foo(numpydoc.docscrape.NumpyDocString(''))

    # Non-proper invocation
    with pytest.raises(TypeError, match='`a` should be on of int | float'):
        foo('bar')


"""
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
"""
