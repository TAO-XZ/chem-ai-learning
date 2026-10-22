import numpy as np
import pandas as pd

df = pd.read_csv("data/amino_acid_descriptors.csv")
names = df['aa3'].values
X = df[['mw_da', 'hydrophobicity_kd']].values
q = np.array([120.0, -4.0])

print("X.shape:", X.shape)
print("q.shape:", q.shape)

d_raw = np.sqrt(((X - q)**2).sum(axis=1))
print("d_raw.shape:", d_raw.shape)

idx_raw = np.argsort(d_raw)[:3]
print("原始 最近3:", list(names[idx_raw]))

mu = X.mean(axis=0)
sd = X.std(axis=0)
Z  = (X - mu) / sd
qz = (q - mu) / sd

print("mu =", mu)
print("sd =", sd)
print("Z.shape:", Z.shape, " qz.shape:", qz.shape)

d_std = np.sqrt(((Z - qz)**2).sum(axis=1))
idx_std = np.argsort(d_std)[:3]
print("标准化 最近3:", list(names[idx_std]))

print("原始距离:", d_raw[idx_raw].round(3))
print("标准化距离:", d_std[idx_std].round(3))