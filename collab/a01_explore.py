"""合作项目 · 探索性分析 A01：这套数据能不能建模？

输入：data/kcat_km_raw.xlsx        （陈师姐给的原始数据，54 行 = 18 条件 × 3 重复）
      data/amino_acid_descriptors.csv
输出：figures/a01_explore.png      4 张图
      终端打印 5 张表

用法（在仓库根目录）：
    D:\\conda\\envs\\chem\\python.exe collab\\a01_explore.py
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

RAW = Path("data/kcat_km_raw.xlsx")
DESC = Path("data/amino_acid_descriptors.csv")
FIG = Path("figures/a01_explore.png")

ENZYMES = ["Cyt c", "lipase PS"]
CONTROLS = {"free Cyt c", "free lipase PS", "COF", "Co-COF"}

# 原始表里的氨基酸写法 -> 描述符表里的三字母码
NAME_MAP = {"Iso": "Ile", "Val": "Val", "Ly": "Lys", "Leu": "Leu",
            "Glu": "Glu", "Ser": "Ser", "Ala": "Ala"}
FEATURES = ["mw_da", "hydrophobicity_kd", "pI", "charge_pH7"]


def load():
    df = pd.read_excel(RAW)
    df.columns = ["enzyme", "aa", "Vmax", "Km", "kcat", "kcat_Km", "R2"]
    df["enzyme"] = df["enzyme"].ffill().astype(str).str.strip()
    df["aa"] = df["aa"].ffill().astype(str).str.strip()
    df = df.dropna(subset=["kcat_Km"]).reset_index(drop=True)
    df["log_kk"] = np.log10(df["kcat_Km"])
    df["aa3"] = df["aa"].str.replace("DL-", "", regex=False).map(NAME_MAP)
    df["is_control"] = df["aa"].isin(CONTROLS)
    return df


def summary_table(df):
    print("=" * 78)
    print("表1  每个条件的重复情况（能否直接建模，先看这一张）")
    print("=" * 78)
    print(f"{'酶':10s} {'氨基酸':12s} {'n':>2s} {'kcat/Km均值':>12s} "
          f"{'组内sd':>9s} {'CV%':>6s} {'R2范围':>12s}")
    rows = []
    for (e, a), g in df.groupby(["enzyme", "aa"], sort=True):
        kk = g["kcat_Km"].values
        cv = 100 * kk.std(ddof=0) / kk.mean()
        print(f"{e:10s} {a:12s} {len(g):>2d} {kk.mean():>12.5f} "
              f"{kk.std(ddof=0):>9.5f} {cv:>6.1f} "
              f"{g['R2'].min():.2f}-{g['R2'].max():.2f}")
        rows.append(dict(enzyme=e, aa=a, n=len(g), mean=kk.mean(),
                         sd=kk.std(ddof=0), cv=cv))
    return pd.DataFrame(rows)


def scale_table(df):
    print()
    print("=" * 78)
    print("表2  两个酶能不能合并？（答案：不能）")
    print("=" * 78)
    for e in ENZYMES:
        v = df.loc[df["enzyme"] == e, "kcat_Km"]
        print(f"{e:10s} n={len(v):>2d}  min {v.min():>9.5f}  max {v.max():>9.5f}  "
              f"中位 {v.median():>9.5f}  跨度 {v.max() / v.min():>6.0f} 倍")
    a = df.loc[df["enzyme"] == ENZYMES[0], "kcat_Km"].median()
    b = df.loc[df["enzyme"] == ENZYMES[1], "kcat_Km"].median()
    print(f"\n两个酶中位数差 {b / a:.0f} 倍 -> 量级完全不同，"
          f"而且底物不同，酶学上本来就不可比")


def to_conditions(df):
    """把 3 次重复压成 1 行（每组均值）。

    为什么必须压：3 次重复不是 3 个独立条件。直接拿 21 行去算相关，
    等于把同一个条件的测量噪声当成"新样本"，p 值会被算小（伪重复）。
    真正的样本量是「条件数」= 7，不是 21。
    """
    g = (df.groupby(["enzyme", "aa"], sort=False)
           .agg(Vmax=("Vmax", "mean"), Km=("Km", "mean"),
                kcat=("kcat", "mean"), kcat_Km=("kcat_Km", "mean"),
                R2=("R2", "mean"), n=("kcat_Km", "size"))
           .reset_index())
    g["log_kk"] = np.log10(g["kcat_Km"])
    g["aa3"] = g["aa"].str.replace("DL-", "", regex=False).map(NAME_MAP)
    g["is_control"] = g["aa"].isin(CONTROLS)
    return g


def kcat_km_table(df):
    print()
    print("=" * 78)
    print("表3  kcat 和 Km 是不是独立的？（决定你先预测哪个）")
    print("=" * 78)
    c = to_conditions(df)
    for e in ENZYMES:
        g = c[c["enzyme"] == e]
        r, p = spearmanr(g["kcat"], g["Km"])
        print(f"{e:10s} kcat vs Km  n = {len(g):2d}   "
              f"Spearman rho = {r:+.3f}   p = {p:.3f}")
    print("rho 接近 0 -> 两个参数独立；rho 明显为正 -> 两者同向，比值会部分抵消")


def descriptor_table(df):
    print()
    print("=" * 78)
    print("表4  哪个氨基酸描述符和目标有关？（只用 7 个氨基酸条件，n = 7）")
    print("=" * 78)
    aa = pd.read_csv(DESC)
    c = to_conditions(df)
    m = c.merge(aa, on="aa3", how="inner")
    print(f"能对上描述符的条件行: {len(m)}（对照组没有描述符，被丢掉）")
    print("n = 7 时，|rho| > 0.786 才有 p < 0.05 —— 门槛很高，别过度解读")
    for e in ENZYMES:
        g = m[m["enzyme"] == e]
        if len(g) < 5:
            print(f"{e}: 只有 {len(g)} 行，跳过")
            continue
        print(f"\n{e}（{len(g)} 个氨基酸条件）")
        for f in FEATURES:
            r, p = spearmanr(g[f], g["log_kk"])
            flag = "  ← 显著" if p < 0.05 else ""
            print(f"    {f:20s} rho = {r:+.3f}   p = {p:.3f}{flag}")
    return m


def baseline_table(df):
    print()
    print("=" * 78)
    print("表5  模型的及格线（留一验证，目标是 log10 kcat/Km，n = 7）")
    print("=" * 78)
    print(f"{'酶':10s} {'方案':28s} {'RMSE':>9s} {'RMSE/sd':>9s} {'相对基线':>9s}")
    c = to_conditions(df)
    aa = pd.read_csv(DESC)
    for e in ENZYMES:
        g = c[(c["enzyme"] == e) & (~c["is_control"])].dropna(subset=["aa3"])
        y = g["log_kk"].values
        sd = y.std(ddof=0)

        # 基线：用其余样本的平均值预测
        pred = np.array([(y[np.arange(len(y)) != i]).mean() for i in range(len(y))])
        rmse0 = np.sqrt(((pred - y) ** 2).mean())
        print(f"{e:10s} {'基线（其余样本平均）':28s} {rmse0:>9.4f} "
              f"{rmse0 / sd:>9.3f} {1.0:>9.3f}")

        # 单描述符线性回归（留一）
        m = g.merge(aa, on="aa3", how="inner")
        if len(m) >= 5:
            yv = m["log_kk"].values
            sdv = yv.std(ddof=0)
            best = None
            for f in FEATURES:
                x = m[f].values
                pr = np.zeros(len(x))
                for i in range(len(x)):
                    mask = np.arange(len(x)) != i
                    k, b = np.polyfit(x[mask], yv[mask], 1)
                    pr[i] = k * x[i] + b
                r = np.sqrt(((pr - yv) ** 2).mean())
                if best is None or r < best[1]:
                    best = (f, r)
                print(f"{'':10s} {'线性 ' + f:28s} {r:>9.4f} "
                      f"{r / sdv:>9.3f} {r / rmse0:>9.3f}")
            print(f"{'':10s} -> 最好的单特征: {best[0]}   相对基线 = "
                  f"{best[1] / rmse0:.3f}（< 1 才比瞎猜好）")


def plot(df, path):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    ax = axes[0, 0]
    for e, c in zip(ENZYMES, ["#2f7ed8", "#d64545"]):
        v = df.loc[df["enzyme"] == e, "log_kk"]
        ax.hist(v, bins=12, alpha=0.65, label=e, color=c)
    ax.set_xlabel("log10(kcat/Km)")
    ax.set_ylabel("count")
    ax.set_title("(a) target distribution — two enzymes, two worlds")
    ax.legend()

    for ax, e in zip([axes[0, 1], axes[1, 0]], ENZYMES):
        g = df[df["enzyme"] == e]
        order = g.groupby("aa")["log_kk"].median().sort_values().index
        data = [g.loc[g["aa"] == a, "log_kk"].values for a in order]
        ax.boxplot(data, patch_artist=True,
                   boxprops=dict(facecolor="#cfe3f7"))
        ax.set_ylabel("log10(kcat/Km)")
        ax.set_title(f"({'b' if e == ENZYMES[0] else 'c'}) {e}: 3 replicates per condition")
        ax.set_xticks(range(1, len(order) + 1))
        ax.set_xticklabels(order, rotation=45, ha="right")

    ax = axes[1, 1]
    for e, c in zip(ENZYMES, ["#2f7ed8", "#d64545"]):
        g = df[df["enzyme"] == e]
        ax.scatter(g["Km"], g["kcat"], s=45, alpha=0.8, label=e, color=c)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Km (mM)")
    ax.set_ylabel("kcat (1/s)")
    ax.set_title("(d) kcat vs Km — positively correlated, so the ratio partly cancels")
    ax.legend()

    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=130)
    print(f"\n图已保存: {path.resolve()}")


def main():
    df = load()
    print(f"读入 {len(df)} 行，{df['enzyme'].nunique()} 个酶，"
          f"{df.groupby(['enzyme', 'aa']).ngroups} 个条件\n")

    summary_table(df)
    scale_table(df)
    kcat_km_table(df)
    descriptor_table(df)
    baseline_table(df)
    plot(df, FIG)


if __name__ == "__main__":
    main()
