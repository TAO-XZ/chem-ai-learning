"""氨基酸微环境分析 —— 公共数据函数。

这个文件不是用来"直接运行"的，是给其他脚本 import 用的。
"""

import pandas as pd


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


# 只有直接运行本文件时，才会执行下面这段
if __name__ == '__main__':
    flat = load_data()
    print(f"条件数: {len(flat)}")
    print(flat.head())

    data = add_descriptors(flat)
    print(f"带描述符的行数: {len(data)}")