# ①级物体 1：认领矩阵乘法（.Prime/Phase0/multipy.py）

目标：通过完整循环把这份 AI 敲的代码变成自己的。

1. 解释关：逐行讲清楚 multiply(A,B) 在做什么（三层循环的含义、C 的初始化方式）
2. 验真关：随机生成若干 (m,n)@(n,p) 矩阵，与 np.dot 比对，误差应 < 1e-10
3. 边界攻击：用 toolkit/boundary_attack.run_boundary_cases 测空矩阵 (0,3)@(3,2)、非方阵、非 2D 输入（run_boundary_cases 只收单参函数，二元 multiply 需包装：lambda pair: multiply(pair[0], pair[1])，cases 传 [(label, (A, B)), ...]）
4. 预测：不运行，先预测 (2,3)@(3,1) 的输出形状和 [0,0] 元素值，再验证
5. 闭卷关：合上原码，重写 multiply（不用 AI），与本实现对比
6. 评判关：这个实现和 np.dot 比有什么缺点？（速度：三重 Python 循环；可读性；广播支持）
7. 记账：按 ledgers/_template.md 格式写入 ledgers/，编号 #002
