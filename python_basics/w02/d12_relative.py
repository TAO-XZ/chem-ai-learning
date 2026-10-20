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

# ===== 归一化：以游离酶为 100% =====
flat = summary.reset_index()

free_map = flat[flat['amino_acid'].str.contains('free')].set_index('enzyme')['mean']
flat['relative'] = flat['mean'] / flat['enzyme'].map(free_map) * 100

print(flat[['enzyme', 'amino_acid', 'mean', 'relative']].to_string(index=False))

# ===== 画图 =====
colors = []
for enzyme in flat['enzyme']:
    if enzyme == 'Cyt c':
        colors.append('steelblue')
    else:
        colors.append('darkorange')

labels = flat['enzyme'] + '\n' + flat['amino_acid']

plt.figure(figsize=(13, 7))
plt.bar(labels, flat['relative'], color=colors, edgecolor='black', linewidth=0.5)
plt.axhline(100, color='red', linestyle='--', linewidth=1.2)
plt.ylabel('相对活性（%，以游离酶 = 100%）', fontsize=12)
plt.title('孔内微环境对两种酶催化效率（kcat/Km）的影响', fontsize=14)
plt.xticks(rotation=90, fontsize=8)
plt.tight_layout()
plt.savefig('figures/relative_activity.png', dpi=300)
plt.show()