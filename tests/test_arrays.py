import pytest
import numpy as np

from numpydoc_types import check_types


def test_array_ndims():
    """Test checking the number of dimensions of an array."""
    @check_types
    def foo(a):
        """A function that takes an array as parameter.

        Parameters
        ----------
        a : array, shape (a, b, c)
            A 3-dimensional array.
        """
        pass

    # Proper invocation
    foo(np.atleast_3d(1))

    # Non-proper invocations
    with pytest.raises(TypeError, match='scalar value'):
        foo(1)
    with pytest.raises(TypeError, match='has 0'):
        foo(np.array(1))
    with pytest.raises(TypeError, match=r'has 1 \(2,\)'):
        foo(np.array([1, 2]))
    with pytest.raises(TypeError, match=r'has 2 \(1, 2\)'):
        foo(np.array([[1, 2]]))
