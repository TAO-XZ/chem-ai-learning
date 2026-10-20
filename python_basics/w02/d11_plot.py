import matplotlib.pyplot as plt

import pandas as pd

df = pd.read_excel(r"data\enzyme_data.xlsx")
# ① 改列名
df.columns = ['enzyme', 'amino_acid', 'Vmax', 'Km', 'kcat', 'kcat_Km', 'R2']

# ② 向前填充空缺
df['enzyme'] = df['enzyme'].ffill()
df['amino_acid'] = df['amino_acid'].ffill()

print(df.head(12))
print(df.shape)
print(df.head(12))
summary = df.groupby(['enzyme', 'amino_acid'])['kcat_Km'].agg(['mean', 'std', 'count'])
print(summary)
summary = summary.sort_values(['enzyme', 'mean'], ascending=[True, False])
print(summary)

# 中文显示设置（Windows 必加，否则中文全是方框）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 取出 lipase PS 这一组
lipase = summary.loc['lipase PS']

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# ===== 左：Cyt c =====
cyt = summary.loc['Cyt c']

colors_cyt = []
for name in cyt.index:
    if 'free' in name:
        colors_cyt.append('lightgrey')
    else:
        colors_cyt.append('steelblue')

axes[0].bar(cyt.index, cyt['mean'], yerr=cyt['std'],
            color=colors_cyt, capsize=5, edgecolor='black', linewidth=0.5)
axes[0].set_title('细胞色素 c（Cyt c）', fontsize=13)
axes[0].set_ylabel(r'kcat/Km (mM$^{-1}$s$^{-1}$)')
axes[0].tick_params(axis='x', rotation=45)

# ===== 右：lipase PS =====
lip = summary.loc['lipase PS']

colors_lip = []
for name in lip.index:
    if 'free' in name:
        colors_lip.append('lightgrey')
    elif 'COF' in name:
        colors_lip.append('orange')
    else:
        colors_lip.append('steelblue')

axes[1].bar(lip.index, lip['mean'], yerr=lip['std'],
            color=colors_lip, capsize=5, edgecolor='black', linewidth=0.5)
axes[1].set_title('脂肪酶 PS（lipase PS）', fontsize=13)
axes[1].set_ylabel(r'kcat/Km (mM$^{-1}$s$^{-1}$)')
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('figures/two_enzymes.png', dpi=300)
plt.show()