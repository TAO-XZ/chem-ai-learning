import itertools
import numpy as np
from aa_utils import load_data, add_descriptors, rmse

data = add_descriptors(load_data())
cyt = data[data['enzyme'] == 'Cyt c']
y = cyt['mean'].values
X = cyt[['mw_da', 'hydrophobicity_kd']].values
n = len(y)

METHODS = {'k=2': dict(k=2), 'k=2 加权': dict(k=2, weighted=True),
           'k=5': dict(k=5), 'k=5 加权': dict(k=5, weighted=True)}


def holdout_rmse(X, y, test, k=3, weighted=False):
    """留出 test 这几个点，用剩下的训练，返回留出点上的 RMSE。"""
    train = [i for i in range(len(y)) if i not in test]
    pred = []
    for i in test:
        d = np.sqrt(((X[train] - X[i]) ** 2).sum(axis=1))
        order = np.argsort(d)[:k]
        idx = np.array(train)[order]
        if weighted:
            w = 1.0 / (d[order] + 1e-9)
            pred.append((w * y[idx]).sum() / w.sum())
        else:
            pred.append(y[idx].mean())
    return rmse(np.array(pred), y[list(test)])


splits = list(itertools.combinations(range(n), 2))
print(f'Cyt c   n={n}   每次留 2 点   共 {len(splits)} 种切法')

sd = y.std()
scores = {}
for name, kw in METHODS.items():
    s = np.array([holdout_rmse(X, y, te, **kw) for te in splits])
    scores[name] = s
    print(f'  {name:8s} 平均 {s.mean():.6f}   波动 {s.std():.6f}   归一化 {s.mean()/sd:.3f}')

base = scores['k=5']
print(f'\n在 {len(splits)} 种切法里，各方法赢过 "k=5(等于平均)" 的次数：')
for name, s in scores.items():
    print(f'  {name:8s} {(s < base).sum():2d}/{len(splits)}')