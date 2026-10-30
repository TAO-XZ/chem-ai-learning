import numpy as np
from aa_utils import load_data, add_descriptors, loo_predict, rmse, mae

data = add_descriptors(load_data())
cyt = data[data['enzyme'] == 'Cyt c']
names = cyt['aa3'].values
y = cyt['mean'].values
n = len(y)

X = cyt[['mw_da', 'hydrophobicity_kd']].values      # (7, 2) 两个特征
h = cyt['hydrophobicity_kd'].values                  # (7,)   一个特征

print("X.shape:", X.shape, " n:", n)

# 基线：用剩下 6 个的平均去"预测"
base = np.zeros(n)
for i in range(n):
    mask = np.arange(n) != i
    base[i] = y[mask].mean()

print(f"全局基线        RMSE={rmse(base, y):.6f}   MAE={mae(base, y):.6f}")
# ① 只有 1 个特征（疏水性）→ 要变成「7 行 1 列」
X_hh = h.reshape(-1, 1)

# ② 2 个特征，原始 → 直接用 X
# ③ 2 个特征，标准化
mu = X.mean(axis=0)
sd = X.std(axis=0)
Z = (X - mu) / sd

p1 = loo_predict(X_hh, y)
p2 = loo_predict(X, y)
p3 = loo_predict(Z, y)

print(f"1 特征(疏水性)  RMSE={rmse(p1, y):.6f}   MAE={mae(p1, y):.6f}")
print(f"2 特征(原始)    RMSE={rmse(p2, y):.6f}   MAE={mae(p2, y):.6f}")
print(f"2 特征(标准化)  RMSE={rmse(p3, y):.6f}   MAE={mae(p3, y ):.6f}")