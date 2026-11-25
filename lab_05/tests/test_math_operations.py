from src.math_operations import add, subtract


def test_add():
    assert add(1, 2) == 3


def test_subtract():
    assert subtract(2, 1) == 1
