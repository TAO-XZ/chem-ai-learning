import numpy as np
from aa_utils import load_data, add_descriptors

data = add_descriptors(load_data())
cyt = data[data['enzyme'] == 'Cyt c']
names = cyt['aa3'].values
h = cyt['hydrophobicity_kd'].values
y = cyt['mean'].values
n = len(y)

print("样本数:", n)

preds = np.zeros(n)          # 先准备 7 个 0，一会儿往里填

for i in range(n):
    mask = np.arange(n) != i           # 留出第 i 个
    h_tr = h[mask]                     # 训练集：6 个疏水性
    y_tr = y[mask]                     # 训练集：6 个活性

    d = np.abs(h_tr - h[i])            # 训练集里每个离「被留出的那个」多远
    idx = np.argsort(d)[:3]            # 最近的 3 个
    preds[i] = y_tr[idx].mean()        # 用它们平均，填进 preds

print(preds.round(5))

err = preds - y

rmse = np.sqrt((err**2).mean())
mae  = np.abs(err).mean()

print(f"RMSE = {rmse:.6f}")
print(f"MAE  = {mae:.6f}")
base = np.zeros(n)
for i in range(n):
    mask = np.arange(n) != i
    base[i] = y[mask].mean()          # 用剩下 6 个的平均去"预测"
print(f"基线 RMSE = {np.sqrt(((base - y)**2).mean()):.6f}")
