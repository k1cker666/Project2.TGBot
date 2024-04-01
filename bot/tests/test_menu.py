import pytest
from src.helpfuncs.menu import build_menu

@pytest.mark.parametrize(
    "array, cols, head, foot, res",
    [
        (['a'], 1, None, None, [['a']]),
        (['a'], 1, ['b'], None, [['b'], ['a']]),
        (['a'], 1, ['b', 'c'], None, [['b', 'c'], ['a']]),
        (['a'], 1, None, ['b'], [['a'], ['b']]),
        (['a'], 1, None, ['b', 'c'], [['a'], ['b', 'c']]),
        (['a'], 2, None, None, [['a']]),
        (['a'], 2, ['b'], None, [['b'], ['a']]),
        (['a'], 2, None, ['b'], [['a'], ['b']]),
        (['a', 'b'], 1, None, None, [['a'], ['b']]),
        (['a', 'b'], 2, None, None, [['a', 'b']]),
        (['a', 'b', 'c'], 2, None, None, [['a', 'b'], ['c']]),
        (['a', 'b', 'c'], 3, None, None, [['a', 'b', 'c']])
    ]
)
def test_menu(array, cols, head, foot, res):
    assert build_menu(array, cols, head, foot) == res