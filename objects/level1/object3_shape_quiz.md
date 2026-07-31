# ①级物体 3：形状预测小测

目标：不运行代码，预测下列每个运算的结果形状（或错误类型）；再用 toolkit/shape_assert.matmul_result_shape 和 numpy 验证。

题目：
1. `np.zeros((5, 3)) @ np.zeros((3, 7))` → ?
2. `np.zeros((5, 3)) @ np.zeros((3,))` → ?
3. `np.zeros((3,)) @ np.zeros((3, 4))` → ?
4. `np.zeros((3,)) @ np.zeros((3,))` → ?
5. `np.zeros((2, 3, 4)) @ np.zeros((4, 5))` → ?（提示：批处理广播）
6. `(5, 3) @ (4, 5)` 会发生什么？（先预测：报错？什么错误？）

方法：每题先写预测（形状 or 错误类型），再用 `matmul_result_shape` 和 numpy 实测核对。
记账：ledgers/ #004 —— 这是①级的核心练习，命中率计入升级判定。
