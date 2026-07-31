import numpy as np
import pytest
from gradient_check import numerical_gradient, assert_gradients_close


def test_quadratic_gradient():
    x = np.array([1.0, 2.0, 3.0])
    g = numerical_gradient(lambda t: np.sum(t**2), x)
    assert np.allclose(g, 2 * x, atol=1e-4)


def test_matches_analytic_cubic():
    x = np.array([0.5, -1.2, 2.0])
    g = numerical_gradient(lambda t: np.sum(t**3), x)
    assert_gradients_close(g, 3 * x**2)


def test_multidim_input():
    x = np.ones((2, 3))
    g = numerical_gradient(lambda t: np.sum(t * t), x)
    assert g.shape == (2, 3)
    assert np.allclose(g, 2 * x, atol=1e-4)


def test_assertion_fires_on_bad_gradient():
    x = np.array([1.0, 2.0])
    g = numerical_gradient(lambda t: np.sum(t**2), x)
    with pytest.raises(AssertionError):
        assert_gradients_close(g, np.array([0.0, 0.0]))


def test_passes_at_near_zero_gradient():
    # 真实梯度≈0 时，中心差分截断误差≈1e-10，相对误差会超过 tol，
    # 但绝对误差远小于 1e-8，应通过（绝对误差逃生条款）
    g = numerical_gradient(lambda t: np.sum(t**3), np.array([0.0]))
    assert_gradients_close(g, np.array([0.0]))
