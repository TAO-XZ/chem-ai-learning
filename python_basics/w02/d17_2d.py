#读 CSV，同时取两列：
#X = df[['mw_da', 'hydrophobicity_kd']].values
#🔴 注意是双层中括号 df[[ ... ]]，不是 df[...]。 双层 = 选多列 → 得到一个二维数组；单层 = 选一列 → 得到 Series。
#打印 X.shape（应该是 (20, 2)）
#打印 X[0]（第 1 个氨基酸的两个特征）
#打印 X[:, 0]（全部 20 个分子量）
#mu = X.mean(axis=0)，打印出来
#打印 X.mean(axis=1)[:3]（每个氨基酸的"两特征平均"，只取前 3 个看看）
#centered = X - mu，打印 centered[0]
#打印 centered.mean(axis=0)
import pandas as pd
import numpy as np
df = pd.read_csv('data/amino_acid_descriptors.csv')
X = df[['mw_da', 'hydrophobicity_kd']].values
print(f"X.shape: {X.shape}")
print(f"X[0]: {X[0]}")
print(f"X[:, 0]: {X[:, 0]}")
mu = X.mean(axis=0)
print(f"mu: {mu}")
row_means = X.mean(axis=1)
print(f"X.mean(axis=1)[:3]: {row_means[:3]}")
centered = X - mu
print(f"centered[0]: {centered[0]}")
print(f"centered.mean(axis=0): {centered.mean(axis=0)}")
