"""验证工具箱：形状断言与形状预测（判断力训练机）"""
import numpy as np


def assert_shape(tensor, expected, name="tensor"):
    """断言 tensor 的形状等于 expected，否则抛 AssertionError。"""
    actual = tuple(np.asarray(tensor).shape)
    expected = tuple(expected)
    assert actual == expected, f"{name}: expected {expected}, got {actual}"


def assert_same_shape(a, b, name_a="a", name_b="b"):
    """断言两个数组形状相同。"""
    sa = np.asarray(a).shape
    sb = np.asarray(b).shape
    assert sa == sb, f"{name_a}.shape {sa} != {name_b}.shape {sb}"


def matmul_result_shape(a_shape, b_shape):
    """给定两个数组形状，返回 A@B 的结果形状；不合法则抛 ValueError。

    支持：1D@1D、2D@2D、2D@1D、1D@2D、以及带批处理广播的 N-D 情形。
    """
    A = tuple(a_shape)
    B = tuple(b_shape)
    # 1D @ 1D -> 标量 ()
    if len(A) == 1 and len(B) == 1:
        if A[0] != B[0]:
            raise ValueError(f"inner dim mismatch: {a_shape} @ {b_shape}")
        return ()
    # 把 1D 视作 (1, n) 或 (n, 1)，算完再还原
    if len(A) == 1:
        A = (1,) + A
    if len(B) == 1:
        B = B + (1,)
    if A[-1] != B[-2]:
        raise ValueError(f"inner dim mismatch: {a_shape} @ {b_shape}")
    batch = _broadcast(A[:-2], B[:-2], a_shape, b_shape)
    row = A[-2]
    col = B[-1]
    if len(a_shape) == 1:
        return tuple(batch) + (col,)
    if len(b_shape) == 1:
        return tuple(batch) + (row,)
    return tuple(batch) + (row, col)


def _broadcast(a, b, a_shape, b_shape):
    """numpy 广播规则：逐维对齐，1 可以广播到任意维。"""
    la, lb = len(a), len(b)
    if la > lb:
        b = (1,) * (la - lb) + b
    elif lb > la:
        a = (1,) * (lb - la) + a
    out = []
    for da, db in zip(a, b):
        if da == db:
            out.append(da)
        elif da == 1:
            out.append(db)
        elif db == 1:
            out.append(da)
        else:
            raise ValueError(f"batch dims not broadcastable: {a_shape} @ {b_shape}")
    return tuple(out)
