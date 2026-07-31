import numpy as np
import pytest
from boundary_attack import run_boundary_cases, assert_all_pass


def test_stable_softmax_passes_large_input():
    def stable_softmax(x):
        e = np.exp(x - np.max(x))
        return e / np.sum(e)

    results = run_boundary_cases(stable_softmax, [("large", np.array([1000.0, 1001.0, 1002.0]))])
    assert results[0][2]


def test_raw_softmax_nan_on_large_input():
    def raw_softmax(x):
        with np.errstate(over="ignore"):
            e = np.exp(x)
        return e / np.sum(e)

    results = run_boundary_cases(raw_softmax, [("large", np.array([1000.0, 1001.0, 1002.0]))])
    assert not results[0][2]


def test_assert_all_pass_with_good_func():
    def safe_relu(x):
        return np.maximum(0, np.asarray(x, dtype=float))

    assert_all_pass(safe_relu, [("neg", np.array([-1.0])), ("zero", np.array([0.0]))])


def test_assert_all_pass_fires():
    def bad_relu(x):
        return np.asarray(x, dtype=float) * np.nan

    with pytest.raises(AssertionError):
        assert_all_pass(bad_relu, [("nan", np.array([1.0]))])
