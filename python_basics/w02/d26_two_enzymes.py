import numpy as np
import matplotlib.pyplot as plt
from aa_utils import load_data, add_descriptors, loo_predict, rmse

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

data = add_descriptors(load_data())

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

for ax, enz in zip(axes, ['Cyt c', 'lipase PS']):
    sub = data[data['enzyme'] == enz]
    y = sub['mean'].values
    X = sub[['mw_da', 'hydrophobicity_kd']].values
    h = sub['hydrophobicity_kd'].values
    sd = y.std()
    n = len(y)
    baseline = n / (n - 1)

    ks = list(range(1, n))
    r1, r2 = [], []
    for k in ks:
        r1.append(rmse(loo_predict(h.reshape(-1, 1), y, k=k), y) / sd)
        r2.append(rmse(loo_predict(X, y, k=k), y) / sd)

    print(f"--- {enz} (n={n}, sd={sd:.4f}) ---")
    for i, k in enumerate(ks):
        print(f"  k={k}  1特征={r1[i]:.3f}   2特征={r2[i]:.3f}")

    ax.plot(ks, r1, 'o-', lw=2, label='1 特征（疏水性）')
    ax.plot(ks, r2, 's-', lw=2, label='2 特征（疏水性+分子量）')
    ax.axhline(baseline, ls='--', color='gray', label=f'基线 = {baseline:.3f}')
    ax.set_title(f'{enz}（n = {n}）', fontsize=12)
    ax.set_xlabel('邻居个数 k', fontsize=11)
    ax.set_ylabel('RMSE / sd（越小越好）', fontsize=11)
    ax.set_xticks(ks)
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('figures/scan_k_two_enzymes.png', dpi=300)
plt.show()