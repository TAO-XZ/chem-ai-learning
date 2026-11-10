import os, sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[2]      # 仓库根目录
sys.path.insert(0, str(ROOT / "python_basics" / "w02"))
os.chdir(ROOT)                                   # aa_utils 用相对路径读 data/

from aa_utils import load_data, add_descriptors

data = add_descriptors(load_data())
cyt  = data[data["enzyme"] == "Cyt c"]
X    = cyt[["mw_da", "hydrophobicity_kd"]].values   # (7, 2)
y    = cyt["mean"].values                           # (7,)
# ── 7 个探针（今天做前 4 个）─────────────────────────
rows = []

mu, sd = X.mean(axis=0), X.std(axis=0)

# 探针 1：中心化
c = X - mu
rows.append(("X - mu", c.shape, np.abs(c.mean(axis=0)).max(), "中心化"))

# 探针 2：对角缩放
z = (X - mu) / sd
rows.append(("(X - mu) / sd", z.shape, np.abs(z.std(axis=0) - 1).max(), "对角矩阵缩放 D⁻¹"))

# 探针 3：L2 范数（手写 vs 库）
d1 = np.sqrt(((X - X[0])**2).sum(axis=1))
d2 = np.linalg.norm(X - X[0], axis=1)
rows.append(("norm(X - X[0])", d1.shape, np.abs(d1 - d2).max(), "L2 范数 / 欧氏距离"))

# 探针 4：列子集
rows.append(("X[:, 0]", X[:, 0].shape, float("nan"), "列子集（掉一维）"))
rows.append(("X[:, [0]]", X[:, [0]].shape, float("nan"), "列子集（保二维）"))

# 探针 5：内积 / 加权平均
q = X[0]                                    # 查询点 = Ala
d = np.sqrt(((X - q)**2).sum(axis=1))
keep = np.arange(len(X)) != 0                # 留一：把自己排除
idx = np.argsort(d[keep])[:3]                # 最近的 3 个
d3, y3 = d[keep][idx], y[keep][idx]

w = 1.0 / (d3 + 1e-9)
pred = np.dot(w, y3) / w.sum()

print("\n邻居距离 :", np.round(d3, 3))
print("邻居真值 :", np.round(y3, 5))
print("权重 w   :", np.round(w, 4))
print("加权平均 :", round(pred, 5))
print("直接平均 :", round(y3.mean(), 5))
print("真实值   :", round(y[0], 5))
print("dot 与 (w*y3).sum() 的差 :", abs(np.dot(w, y3) - (w * y3).sum()))

rows.append(("dot(w, y3) / Σw", (), pred, "内积 → 一个数"))

# 探针 6：局部方差
unc = y3.std()
err = abs(pred - y[0])
print("\n局部标准差 unc :", round(unc, 5))
print("实际误差   err :", round(err, 5))
print("err / unc      :", round(err / unc, 3))

rows.append(("y3.std()", (), unc, "局部标准差 → 不确定性"))

# 探针 7：k 扫描 → 选择偏差
ks = np.arange(1, len(X))
rmses = []
for k in ks:
    pr = np.zeros(len(y))
    for i in range(len(y)):
        dd = np.sqrt(((X - X[i])**2).sum(axis=1))
        m = np.arange(len(y)) != i
        ii = np.argsort(dd[m])[:k]
        pr[i] = y[m][ii].mean()
    rmses.append(np.sqrt(((pr - y)**2).mean()))

rmses = np.array(rmses)
print("\nk    :", ks)
print("RMSE :", np.round(rmses, 5))
best = int(ks[np.argmin(rmses)])
print("挑中的 k =", best, " RMSE =", round(float(rmses.min()), 5))
print("k=6 全局平均 RMSE =", round(float(rmses[-1]), 5))

rows.append((f"k 扫描 (k={best} 最小)", ks.shape, rmses.min(),
             "模型选择 → 选择偏差"))
# ── 打印对照表 ─────────────────────────────────────
print(f"{'操作':<16} | {'shape':<10} | {'校验数字':<10} | 学名")
print("-" * 64)
for op, shape, num, name in rows:
    n = "   —   " if num != num else f"{num:.1e}"
    print(f"{op:<16} | {str(shape):<10} | {n:<10} | {name}")