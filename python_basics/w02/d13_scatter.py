# ========== 1. 导入 ==========
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

# ========== 2. 中文显示 ==========
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# ========== 3. 读原始数据 + 清洗 ==========
df = pd.read_excel(r"data\enzyme_data.xlsx")
df.columns = ['enzyme', 'amino_acid', 'Vmax', 'Km', 'kcat', 'kcat_Km', 'R2']
df['enzyme'] = df['enzyme'].ffill()
df['amino_acid'] = df['amino_acid'].ffill()

# ========== 4. 分组统计 ==========
summary = df.groupby(['enzyme', 'amino_acid'])['kcat_Km'].agg(['mean', 'std', 'count'])
flat = summary.reset_index()

# ========== 5. 合并氨基酸描述符 ==========
aa = pd.read_csv("data/amino_acid_descriptors.csv")

name_map = {'Iso': 'Ile', 'Val': 'Val', 'Ly': 'Lys', 'Leu': 'Leu',
            'Glu': 'Glu', 'Ser': 'Ser', 'Ala': 'Ala'}

flat['aa3'] = flat['amino_acid'].str.replace('DL-', '', regex=False).map(name_map)
merged = flat.merge(aa, on='aa3', how='left')

# ========== 6. 去掉对照组（free / COF / Co-COF）==========
merged_aa = merged.dropna(subset=['mw_da'])

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