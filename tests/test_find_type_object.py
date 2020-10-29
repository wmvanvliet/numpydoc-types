import pytest

from numpydoc_types.typechecker import find_type_object


def test_find_class_builtin():
    """Test finding buildin objects based on type names."""
    assert find_type_object('int') == int
    assert find_type_object('float') == float
    assert find_type_object('bool') == bool
    assert find_type_object('str') == str
    assert find_type_object('list') == list
    assert find_type_object('set') == set
    assert find_type_object('dict') == dict
    assert find_type_object('tuple') == tuple

    with pytest.raises(NameError, match='foo'):
        find_type_object('foo')


def test_find_class_module():
    """Test finding objects defined in modules."""
    from argparse import ArgumentParser
    from numpydoc.docscrape import NumpyDocString as NDS
    assert find_type_object('argparse.ArgumentParser') == ArgumentParser
    assert find_type_object('numpydoc.docscrape.NumpyDocString') == NDS

    with pytest.raises(NameError, match='could not import `foo`'):
        find_type_object('foo.bar')

    with pytest.raises(NameError, match='could not find `argparse.foo`'):
        find_type_object('argparse.foo')
