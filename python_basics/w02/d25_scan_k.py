import numpy as np
import matplotlib.pyplot as plt
from aa_utils import load_data, add_descriptors, loo_predict, rmse

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

data = add_descriptors(load_data())
cyt = data[data['enzyme'] == 'Cyt c']
y = cyt['mean'].values
n = len(y)
X = cyt[['mw_da', 'hydrophobicity_kd']].values
h = cyt['hydrophobicity_kd'].values

ks = list(range(1, 7))          # [1, 2, 3, 4, 5, 6]
res1, res2 = [], []

for k in ks:
    res1.append(rmse(loo_predict(h.reshape(-1, 1), y, k=k), y))
    res2.append(rmse(loo_predict(X, y, k=k), y))

for i, k in enumerate(ks):
    print(f"k={k}  1特征 RMSE={res1[i]:.6f}   2特征 RMSE={res2[i]:.6f}")

plt.figure(figsize=(7.5, 5))
plt.plot(ks, res1, 'o-', lw=2, ms=8, label='1 特征（疏水性）')
plt.plot(ks, res2, 's-', lw=2, ms=8, label='2 特征（疏水性 + 分子量）')
plt.axhline(0.010396, ls='--', color='gray', label='全局基线 = 0.010396')

plt.xlabel('邻居个数 k', fontsize=12)
plt.ylabel('LOO 的 RMSE（越小越好）', fontsize=12)
plt.title('k 怎么选：太少会被噪音带偏，太多会被平均值拉平', fontsize=12)
plt.xticks(ks)
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('figures/scan_k.png', dpi=300)
plt.show()