import pytest


def test_sum():
    assert 1 + 1 == 2


def test_fail():
    assert 1 + 1 == 3


@pytest.mark.skip
def test_mark_skip():
    assert 1 + 1 == 3


@pytest.mark.parametrize(
    "a, b, result",
    [
        (1, 1, 2),
        (1, 2, 3),
    ],
)
def test_mark(a, b, result):
    assert a + b == result
