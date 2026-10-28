# d19_local.py —— 局部预测：只用最近邻建模型
import numpy as np
from aa_utils import load_data, add_descriptors

# ===== 1. 拿到 Cyt c 的 7 行 =====
data = add_descriptors(load_data())
cyt = data[data['enzyme'] == 'Cyt c']

names = cyt['aa3'].values
h = cyt['hydrophobicity_kd'].values
y = cyt['mean'].values

print(f"样本数: {len(y)}")
print(f"全局平均: {y.mean():.5f}")
print()

# ===== 2. 查询 q = 2.0 =====
q = 2.0
d = np.abs(h - q)
idx = np.argsort(d)[:3]
print(f"q = {q:>5}  最近3: {list(names[idx])}  距离: {d[idx].round(1)}  局部预测: {y[idx].mean():.5f}")

# ===== 3. 查询 q = -4.0 =====
q = -4.0
d = np.abs(h - q)
idx = np.argsort(d)[:3]
print(f"q = {q:>5}  最近3: {list(names[idx])}  距离: {d[idx].round(1)}  局部预测: {y[idx].mean():.5f}")