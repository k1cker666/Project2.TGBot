import pytest
from src.helpfuncs.menu import build_menu

@pytest.mark.parametrize(
    "array, cols, res",
    [
        (['a'], 1, [['a']]),
        (['a'], 2, [['a']]),
        (['a', 'b'], 1, [['a'], ['b']]),
        (['a', 'b'], 2, [['a', 'b']]),
        (['a', 'b', 'c'], 1, [['a'], ['b'], ['c']]),
        (['a', 'b', 'c'], 2, [['a', 'b'], ['c']]),
        (['a', 'b', 'c'], 3, [['a', 'b', 'c']])
    ]
)
def test_menu(array, cols, res):
    assert build_menu(array, cols) == res