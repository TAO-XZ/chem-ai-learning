# ========== 1. 导入 ==========
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
from aa_utils import load_data, add_descriptors     # ← 新增

# ========== 2. 中文显示 ==========
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# ==========  3. 取数据（全部交给模块） ==========
flat = load_data()
merged_aa = add_descriptors(flat)

# ========== 7. 画图 ==========
fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.2))

for ax, enzyme, color in [(axes[0], 'Cyt c', 'steelblue'),
                          (axes[1], 'lipase PS', 'darkorange')]:
    sub = merged_aa[merged_aa['enzyme'] == enzyme]
    x = sub['hydrophobicity_kd'].values
    y = sub['mean'].values

    ax.errorbar(x, y, yerr=sub['std'].values, fmt='o', color=color,
                ecolor='grey', capsize=4, markersize=8,
                markeredgecolor='black', zorder=3)

    for _, row in sub.iterrows():
        ax.annotate(row['aa3'], (row['hydrophobicity_kd'], row['mean']),
                    textcoords='offset points', xytext=(7, 5), fontsize=9)

    k, b = np.polyfit(x, y, 1)
    xs = np.linspace(x.min() - 0.4, x.max() + 0.4, 50)
    ax.plot(xs, k * xs + b, '--', color=color, alpha=0.7)

    r, p = spearmanr(x, y)
    ax.text(0.03, 0.96, f'Spearman ρ = {r:+.2f}\np = {p:.3f}',
            transform=ax.transAxes, va='top', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    ax.set_title(f'{enzyme}（n = {len(sub)}）', fontsize=13)
    ax.set_xlabel('氨基酸疏水性（Kyte-Doolittle）', fontsize=11)
    ax.set_ylabel(r'kcat/Km (mM$^{-1}$s$^{-1}$)', fontsize=11)
    ax.grid(alpha=0.25)

plt.suptitle('氨基酸疏水性 与 催化效率 的关系（虚线为线性趋势）', fontsize=13)
plt.tight_layout()
plt.savefig('figures/scatter_hydrophobicity.png', dpi=300)
plt.show()