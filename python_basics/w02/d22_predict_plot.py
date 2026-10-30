import numpy as np
import matplotlib.pyplot as plt
from aa_utils import load_data, add_descriptors, loo_predict, rmse

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

data = add_descriptors(load_data())
cyt = data[data['enzyme'] == 'Cyt c']
names = cyt['aa3'].values
y = cyt['mean'].values
n = len(y)
X = cyt[['mw_da', 'hydrophobicity_kd']].values
h = cyt['hydrophobicity_kd'].values

p1 = loo_predict(h.reshape(-1, 1), y)
p2 = loo_predict(X, y)

fig, axes = plt.subplots(1, 2, figsize=(11, 5))
lo, hi = 0, 0.036

for ax, pred, title in [(axes[0], p1, '疏水性（1 个特征）'),
                        (axes[1], p2, '疏水性 + 分子量（2 个特征）')]:
    ax.plot([lo, hi], [lo, hi], 'k--', lw=1, alpha=0.7)      # 45° 完美线
    ax.scatter(y, pred, s=70, c='steelblue', edgecolor='black', zorder=3)
    for i in range(n):
        ax.annotate(names[i], (y[i], pred[i]), textcoords='offset points',
                    xytext=(6, 4), fontsize=9)
    ax.set_xlim(lo, hi)
    ax.set_ylim(lo, hi)
    ax.set_xlabel('真实 kcat/Km', fontsize=11)
    ax.set_ylabel('预测 kcat/Km', fontsize=11)
    ax.set_title(f'{title}\nRMSE = {rmse(pred, y):.6f}', fontsize=11)
    ax.grid(alpha=0.25)

plt.tight_layout()
plt.savefig('figures/pred_vs_true.png', dpi=300)
plt.show()