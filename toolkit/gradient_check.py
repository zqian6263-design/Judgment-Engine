"""验证工具箱：数值梯度检查（判断力训练机）"""
import numpy as np


def numerical_gradient(f, x, h=1e-5):
    """中心差分法，计算标量函数 f 在 x 处的数值梯度。

    f: ndarray -> 标量 float
    x: ndarray（任意形状）
    h: 扰动步长
    返回: 与 x 同形状的梯度数组
    """
    x = np.asarray(x, dtype=float)
    grad = np.zeros_like(x)
    it = np.nditer(x, flags=['multi_index'])
    while not it.finished:
        idx = it.multi_index
        xp = x.copy()
        xm = x.copy()
        xp[idx] += h
        xm[idx] -= h
        grad[idx] = (f(xp) - f(xm)) / (2.0 * h)
        it.iternext()
    return grad


def assert_gradients_close(numerical, manual, tol=1e-5, name="gradient"):
    """断言数值梯度与手写/解析梯度一致（相对误差 < tol，或绝对误差 < 1e-8 视为通过）。

    真实梯度≈0 时，中心差分截断误差（h=1e-5 时约 1e-10）会使相对误差超过 tol，
    此时若绝对误差 < 1e-8 同样通过（绝对误差逃生条款）。
    numerical: ndarray（数值梯度）
    manual: ndarray（手写梯度）
    tol: 相对误差上限
    name: 出错提示用名称
    """
    n = np.asarray(numerical, dtype=float).ravel()
    m = np.asarray(manual, dtype=float).ravel()
    assert n.shape == m.shape, f"{name}: shape mismatch {n.shape} vs {m.shape}"
    denom = np.abs(n) + np.abs(m) + 1e-12
    rel = np.max(np.abs(n - m) / denom)
    assert rel < tol or np.max(np.abs(n - m)) < 1e-8, \
        f"{name}: relative error {rel:.2e} exceeds tol {tol:.1e}"
