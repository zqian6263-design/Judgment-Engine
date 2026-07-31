# ①级物体 2：认领 softmax + 交叉熵（.Prime/Phase0/Softmax.py、cross_entropy.py）

1. 解释关：softmax 里为什么先减 max？cross_entropy 里 eps=1e-15 是干嘛的？
2. 验真关：手算小例 [0.5, 1.0] 验证 softmax 输出；对完全正确的预测，cross_entropy 应接近 0
3. 边界攻击：输入 [1000, 1001, 1002] 分别给 Softmax.py 的实现和"减 max"的稳定版，记录差异
4. 预测：softmax 的输出之和一定等于 1 吗？先预测再验证
5. 闭卷关：合上原码，重写 softmax 和 cross_entropy（不用 AI）
6. 评判关：为什么工程里 softmax 和交叉熵要合并计算？（数值稳定性；梯度简化——答不出留到③级）
7. 记账：ledgers/ #003
