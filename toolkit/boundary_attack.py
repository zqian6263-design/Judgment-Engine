"""验证工具箱：边界攻击（判断力训练机）"""
import numpy as np


def run_boundary_cases(func, cases):
    """对一组极端输入逐个运行 func，返回 (标签, 输出/异常, 是否通过) 列表。

    cases: [(label, input), ...]
    通过 = 输出全部有限（无 NaN/Inf）且无异常。
    """
    results = []
    for label, x in cases:
        try:
            y = func(x)
            arr = np.asarray(y, dtype=float)
            ok = bool(np.all(np.isfinite(arr)))
            results.append((label, y, ok))
        except Exception as e:
            results.append((label, f"{type(e).__name__}: {e}", False))
    return results


def assert_all_pass(func, cases):
    """断言 func 在所有边界输入上输出有限；否则抛 AssertionError。"""
    for label, y, ok in run_boundary_cases(func, cases):
        assert ok, f"boundary attack failed [{label}]: {y}"
