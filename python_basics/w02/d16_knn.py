#用 pandas 读这个 CSV data/amino_acid_descriptors.csv
#取出 aa3（三字母缩写）和 hydrophobicity_kd（疏水性）两列
#用 .values 变成 numpy 数组（d13 里你用过这个）
#设一个查询值 q = 2.0
#用 np.abs() 算出每个氨基酸的疏水性离 2.0 有多远
#用 np.argsort() 找出最接近的 3 个
#打印这 3 个的：名字、疏水性、差距
import pandas as pd
import numpy as np
df = pd.read_csv('data/amino_acid_descriptors.csv')
aa3 = df['aa3'].values
hydrophobicity_kd = df['hydrophobicity_kd'].values
q = 2.0
distances = np.abs(hydrophobicity_kd - q)
closest_indices = np.argsort(distances)[:3]

for i in closest_indices:
    print(f"名字：{aa3[i]}, 疏水性：{hydrophobicity_kd[i]:.4f}, 差距：{distances[i]:.4f}")
