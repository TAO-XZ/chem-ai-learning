"""氨基酸微环境分析 —— 公共数据函数。

这个文件不是用来"直接运行"的，是给其他脚本 import 用的。
"""

import pandas as pd
import numpy as np

def load_data(path=r"data\enzyme_data.xlsx"):
    """读 Excel + 清洗 + 分组统计，返回一张扁平的汇总表。"""
    df = pd.read_excel(path)

    df.columns = ['enzyme', 'amino_acid', 'Vmax', 'Km', 'kcat', 'kcat_Km', 'R2']
    df['enzyme'] = df['enzyme'].ffill()
    df['amino_acid'] = df['amino_acid'].ffill()

    summary = df.groupby(['enzyme', 'amino_acid'])['kcat_Km'].agg(['mean', 'std', 'count'])
    return summary.reset_index()


def add_descriptors(flat):
    """把氨基酸描述符合并进来，并去掉对照组（free / COF / Co-COF）。"""
    aa = pd.read_csv("data/amino_acid_descriptors.csv")

    name_map = {'Iso': 'Ile', 'Val': 'Val', 'Ly': 'Lys', 'Leu': 'Leu',
                'Glu': 'Glu', 'Ser': 'Ser', 'Ala': 'Ala'}

    flat['aa3'] = flat['amino_acid'].str.replace('DL-', '', regex=False).map(name_map)
    merged = flat.merge(aa, on='aa3', how='left')
    return merged.dropna(subset=['mw_da'])

def loo_predict(X, y, k=3, weighted=False):
    """留一法 + kNN 预测。

    X: (n, d) 特征矩阵
    y: (n,)   目标值
    k: 邻居个数
    weighted: True 时用反距离加权
    返回: (n,) 每个样本的留一预测值
    """
    n = len(y)
    preds = np.zeros(n)
    for i in range(n):
        mask = np.arange(n) != i
        d = np.sqrt(((X[mask] - X[i])**2).sum(axis=1))
        idx = np.argsort(d)[:k]
        yy = y[mask][idx]
        if weighted:
            w = 1.0 / (d[idx] + 1e-9)
            preds[i] = (w * yy).sum() / w.sum()
        else:
            preds[i] = yy.mean()
    return preds


def rmse(pred, y):
    """均方根误差。"""
    return np.sqrt(((pred - y)**2).mean())


def mae(pred, y):
    """平均绝对误差。"""
    return np.abs(pred - y).mean()
# 只有直接运行本文件时，才会执行下面这段
if __name__ == '__main__':    
    flat = load_data()
    print(f"条件数: {len(flat)}")
    print(flat.head())

    data = add_descriptors(flat)
    print(f"带描述符的行数: {len(data)}")
    cyt = data[data['enzyme'] == 'Cyt c']
    Xc = cyt[['mw_da', 'hydrophobicity_kd']].values
    yc = cyt['mean'].values
    print(f"LOO 2特征        RMSE = {rmse(loo_predict(Xc, yc), yc):.6f}")
    print(f"LOO 2特征 加权   RMSE = {rmse(loo_predict(Xc, yc, weighted=True), yc):.6f}")