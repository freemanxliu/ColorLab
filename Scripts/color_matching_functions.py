import numpy as np
# 定义一个矩阵
A = np.array([
    [1.0510, -0.0150, 0.0],
    [0.1940, 0.8338, -0.0282],
    [0.0406, -0.0407, 0.9985]])

B = np.array([
    [1.3978, 0.0140, 0.0005],
    [-0.3276, 9479, 0.0326],
    [-0.0702, 0.0381, 0.9669]
])
# 计算反矩阵
A_inv = np.linalg.inv(A)


# print(A_inv)
#
# print(np.linalg.norm(A_inv, axis=0, keepdims=True))
# print(A_inv / np.linalg.norm(A_inv, axis=1, keepdims=True))
#

print(A_inv)
print(A_inv[:,0].sum())
print()
print(A_inv.sum(axis=0))
print()
print(A_inv / A_inv.sum(axis=0))
