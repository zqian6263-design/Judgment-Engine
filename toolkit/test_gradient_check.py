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
