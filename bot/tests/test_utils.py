from src.utils import sum
import pytest

@pytest.mark.parametrize(
    "x, y, res",
    [
        (2, 3, 5),
        (1.0, 2, 3),
        (1.2, 2.8, 4),
        (1.5, 4, 5.5),
        ("1", 6, 7),
        ("f", 2, "Error"),
        (None, 1, "Error"),
        (1, True, "Error")
    ]
)
def test_sum(x, y, res):
    assert sum(x, y) == res