import numpy as np
from aa_utils import load_data, add_descriptors, loo_predict, rmse

data = add_descriptors(load_data())
cyt = data[data['enzyme'] == 'Cyt c']
y = cyt['mean'].values
X = cyt[['mw_da', 'hydrophobicity_kd']].values
h = cyt['hydrophobicity_kd'].values

span_true = y.max() - y.min()

for name, Xf in [('1 特征', h.reshape(-1, 1)), ('2 特征', X)]:
    for tag, pred in [('平均', loo_predict(Xf, y)),
                      ('加权', loo_predict(Xf, y, weighted=True))]:
        span = pred.max() - pred.min()
        print(f"{name} {tag}  RMSE={rmse(pred, y):.6f}  压缩到={100*span/span_true:.0f}%")