import numpy as np
from aa_utils import load_data, add_descriptors

data = add_descriptors(load_data())
cyt = data[data['enzyme'] == 'Cyt c']
names = cyt['aa3'].values
y = cyt['mean'].values
n = len(y)

X = cyt[['mw_da', 'hydrophobicity_kd']].values      # (7, 2) 两个特征
h = cyt['hydrophobicity_kd'].values                  # (7,)   一个特征

print("X.shape:", X.shape, " n:", n)
def loo_predict(X, k=3):
    """留一法：每次留出一个样本，用剩下样本的最近 k 个邻居预测它。"""
    preds = np.zeros(n)
    for i in range(n):
        mask = np.arange(n) != i
        d = np.sqrt(((X[mask] - X[i])**2).sum(axis=1))
        idx = np.argsort(d)[:k]
        preds[i] = y[mask][idx].mean()
    return preds
def rmse(p):
    return np.sqrt(((p - y)**2).mean())

def mae(p):
    return np.abs(p - y).mean()

# 基线：用剩下 6 个的平均去"预测"
base = np.zeros(n)
for i in range(n):
    mask = np.arange(n) != i
    base[i] = y[mask].mean()

print(f"全局基线        RMSE={rmse(base):.6f}   MAE={mae(base):.6f}")
# ① 只有 1 个特征（疏水性）→ 要变成「7 行 1 列」
X_hh = h.reshape(-1, 1)

# ② 2 个特征，原始 → 直接用 X
# ③ 2 个特征，标准化
mu = X.mean(axis=0)
sd = X.std(axis=0)
Z = (X - mu) / sd

p1 = loo_predict(X_hh)
p2 = loo_predict(X)
p3 = loo_predict(Z)

print(f"1 特征(疏水性)  RMSE={rmse(p1):.6f}   MAE={mae(p1):.6f}")
print(f"2 特征(原始)    RMSE={rmse(p2):.6f}   MAE={mae(p2):.6f}")
print(f"2 特征(标准化)  RMSE={rmse(p3):.6f}   MAE={mae(p3):.6f}")