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