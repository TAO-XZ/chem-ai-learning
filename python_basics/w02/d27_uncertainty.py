import numpy as np
from scipy.stats import spearmanr
from aa_utils import load_data, add_descriptors

data = add_descriptors(load_data())

U_all, E_all, U_norm, E_norm = [], [], [], []
covered = 0
total = 0

for enz in ['Cyt c', 'lipase PS']:
    sub = data[data['enzyme'] == enz]
    y = sub['mean'].values
    h = sub['hydrophobicity_kd'].values
    n = len(y)
    sd = y.std()

    pred = np.zeros(n)
    unc = np.zeros(n)
    for i in range(n):
        m = np.arange(n) != i
        d = np.abs(h[m] - h[i])
        idx = np.argsort(d)[:3]
        yy = y[m][idx]
        pred[i] = yy.mean()
        unc[i] = yy.std()          # 邻居之间的分歧 = 不确定性

    err = np.abs(pred - y)
    r, p = spearmanr(unc, err)
    print(f"{enz}: rho（不确定性 vs 误差）= {r:+.3f}  p = {p:.3f}")

    for i in range(n):
        U_all.append(unc[i]);      E_all.append(err[i])
        U_norm.append(unc[i]/sd);  E_norm.append(err[i]/sd)
        if err[i] <= 1.96 * unc[i]:
            covered += 1
        total += 1

r1, p1 = spearmanr(U_all, E_all)
r2, p2 = spearmanr(U_norm, E_norm)
print(f"绝对值合并 14 点: rho = {r1:+.3f}  p = {p1:.3f}")
print(f"归一化合并 14 点: rho = {r2:+.3f}  p = {p2:.3f}")
print(f"95% 区间覆盖率: {covered}/{total} = {100*covered/total:.0f}%")