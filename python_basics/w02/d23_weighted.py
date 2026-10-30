import numpy as np
from aa_utils import load_data, add_descriptors
data = add_descriptors(load_data())
cyt = data[data['enzyme'] == 'Cyt c']
names = cyt['aa3'].values
y = cyt['mean'].values
n = len(y)
X = cyt[['mw_da', 'hydrophobicity_kd']].values
h = cyt['hydrophobicity_kd'].values

def loo_predict(Xf, k=3):
    preds = np.zeros(n)
    for i in range(n):
        mask = np.arange(n) != i
        d = np.sqrt(((Xf[mask] - Xf[i])**2).sum(axis=1))
        preds[i] = y[mask][np.argsort(d)[:k]].mean()
    return preds

def rmse(p):
    return np.sqrt(((p - y)**2).mean())


def loo_weighted(Xf, k=3):
    preds = np.zeros(n)
    for i in range(n):
        mask = np.arange(n) != i
        d = np.sqrt(((Xf[mask] - Xf[i])**2).sum(axis=1))
        idx = np.argsort(d)[:k]
        dd = d[idx]                       # 3 个邻居的距离
        yy = y[mask][idx]                 # 3 个邻居的活性
        w = 1.0 / (dd + 1e-9)             # 越近权重越大
        preds[i] = (w * yy).sum() / w.sum()
    return preds
span_true = y.max() - y.min()

for name, Xf in [('1 特征', h.reshape(-1, 1)), ('2 特征', X)]:
    for tag, pred in [('平均', loo_predict(Xf)), ('加权', loo_weighted(Xf))]:
        span = pred.max() - pred.min()
        print(f"{name} {tag}  RMSE={rmse(pred):.6f}  压缩到={100*span/span_true:.0f}%")