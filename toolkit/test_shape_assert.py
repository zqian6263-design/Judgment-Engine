import numpy as np
import pytest
from shape_assert import assert_shape, assert_same_shape, matmul_result_shape


def test_assert_shape_matches():
    assert_shape(np.zeros((3, 4)), (3, 4))


def test_assert_shape_fails_on_mismatch():
    with pytest.raises(AssertionError):
        assert_shape(np.zeros((3, 4)), (4, 3))


def test_assert_same_shape():
    assert_same_shape(np.zeros((2, 2)), np.ones((2, 2)))
    with pytest.raises(AssertionError):
        assert_same_shape(np.zeros((2, 2)), np.ones((3, 2)))


def test_matmul_2d_2d():
    assert matmul_result_shape((2, 3), (3, 4)) == (2, 4)


def test_matmul_2d_1d():
    assert matmul_result_shape((2, 3), (3,)) == (2,)


def test_matmul_1d_2d():
    assert matmul_result_shape((3,), (3, 4)) == (4,)


def test_matmul_1d_1d():
    assert matmul_result_shape((3,), (3,)) == ()


def test_matmul_batched():
    assert matmul_result_shape((2, 3, 4), (4, 5)) == (2, 3, 5)


def test_matmul_invalid_inner_dim():
    with pytest.raises(ValueError):
        matmul_result_shape((5, 3), (4, 5))


def test_matmul_invalid_broadcast():
    with pytest.raises(ValueError):
        matmul_result_shape((2, 3, 4), (5, 4, 6))
