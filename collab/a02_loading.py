"""合作项目 · A02：负载量到底解释了活性差异的多少？

背景：
    负载量(%) 一直都在 —— 在 课题介绍.pdf 第 6-7 页（陈莉 2026.09.21）的原始表里，
    18 个条件每个都有。xlsx 导出时丢了这一列。

要回答的两个问题：
    Q1  负载量 是不是活性差异的来源？（如果 ρ 很大，那"氨基酸效应"其实是"负载量效应"）
    Q2  kcat 的归一化有没有问题？（kcat = Vmax/[E]，如果 [E] 每个条件都不同，kcat 不可比）

用法（仓库根目录）：
    D:\\conda\\envs\\chem\\python.exe collab\\a02_loading.py
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

RAW = Path("data/kcat_km_raw.xlsx")
FIG = Path("figures/a02_loading.png")

ENZYMES = ["Cyt c", "lipase PS"]
CONTROLS = {"free Cyt c", "free lipase PS", "COF", "Co-COF"}

# ── 从 课题介绍.pdf 第 6-7 页抄下来的负载量(%) ────────────────────────────
# 键 = (酶, 条件名去掉 DL- 前缀)。注意：xlsx 里 Cyt c 的条件带 DL-，lipase 的不带，
# 所以统一剥掉再查表。
LOADING = {
    ("Cyt c", "Iso"): 6.97,
    ("Cyt c", "Leu"): 6.10,
    ("Cyt c", "Val"): 5.54,
    ("Cyt c", "Ly"): 6.92,
    ("Cyt c", "Ala"): 5.23,
    ("Cyt c", "Glu"): 7.29,
    ("Cyt c", "Ser"): 6.69,
    ("lipase PS", "Iso"): 5.50,
    ("lipase PS", "Leu"): 4.91,
    ("lipase PS", "Val"): 4.94,
    ("lipase PS", "Ly"): 4.45,
    ("lipase PS", "Ala"): 5.25,
    ("lipase PS", "Glu"): 7.50,
    ("lipase PS", "Ser"): 3.62,
    ("lipase PS", "Co-COF"): 6.63,
    ("lipase PS", "COF"): 4.64,
}


def load_groups():
    df = pd.read_excel(RAW)
    df.columns = ["enzyme", "aa", "Vmax", "Km", "kcat", "kcat_Km", "R2"]
    df["enzyme"] = df["enzyme"].ffill().astype(str).str.strip()
    df["aa"] = df["aa"].ffill().astype(str).str.strip()
    df = df.dropna(subset=["kcat_Km"]).reset_index(drop=True)

    g = (df.groupby(["enzyme", "aa"], sort=False)
           .agg(n=("kcat_Km", "size"),
                Vmax=("Vmax", "mean"),
                Km=("Km", "mean"),
                kcat=("kcat", "mean"),
                kk=("kcat_Km", "mean"),
                kk_sd=("kcat_Km", "std"),
                R2=("R2", "mean"))
           .reset_index())
    g["cv"] = g["kk_sd"] / g["kk"] * 100
    g["log_kk"] = np.log10(g["kk"])
    g["is_control"] = g["aa"].isin(CONTROLS)
    g["loading"] = [LOADING.get((e, a.replace("DL-", ""))) for e, a in
                    zip(g["enzyme"], g["aa"])]
    g["E_conc"] = g["Vmax"] / g["kcat"]          # [E] = Vmax / kcat
    return g


def show_table(g):
    print("=" * 96)
    print("表 1  合并表（活性来自 xlsx 3 次重复均值；负载量来自 课题介绍.pdf）")
    print("=" * 96)
    print(f"{'酶':<10}{'条件':<12}{'负载量%':>8}{'Vmax':>9}{'Km':>9}{'kcat':>10}"
          f"{'kcat/Km':>11}{'CV%':>7}{'R²':>7}{'Vmax/kcat':>11}")
    print("-" * 96)
    for _, r in g.iterrows():
        load = f"{r['loading']:.2f}" if pd.notna(r["loading"]) else "  --"
        print(f"{r['enzyme']:<10}{r['aa']:<12}{load:>8}{r['Vmax']:>9.4f}"
              f"{r['Km']:>9.2f}{r['kcat']:>10.2f}{r['kk']:>11.5f}"
              f"{r['cv']:>7.1f}{r['R2']:>7.3f}{r['E_conc']:>11.5f}")
    print()


def check_enormalization(g):
    print("=" * 96)
    print("表 2  Q2 检查：[E] = Vmax / kcat 在同一个酶内是不是常数？")
    print("=" * 96)
    for e in ENZYMES:
        s = g[g["enzyme"] == e]
        imm = s[~s["aa"].str.startswith("free")]["E_conc"].values
        free = s[s["aa"].str.startswith("free")]["E_conc"].values
        ok = "✓ 常数 → kcat 已正确归一化" if imm.max() / imm.min() < 1.001 else "✗ 不恒定 → kcat 不可比"
        print(f"  {e:<10} 固定化组 {imm.min():.5f} – {imm.max():.5f}  "
              f"跨 {imm.max() / imm.min():.3f} 倍   {ok}")
        if len(free):
            print(f"  {'':<10} 游离酶   {free[0]:.5f}"
                  f"（与其他组差 {(free[0] / imm.min() - 1) * 100:+.0f}%，属于另一份酶液，正常）")
    print()

    print("  （附）我上一轮说的『Vmax/kcat 跨 22 倍』是怎么来的：")
    a = g[g["enzyme"] == "Cyt c"]["E_conc"]
    b = g[g["enzyme"] == "lipase PS"]["E_conc"]
    print(f"       Cyt c 全是 {a.min():.5f}；lipase 全是 {b.min():.5f}；两者之比 = {a.min() / b.min():.1f}")
    print(f"       → 22 倍是【跨酶】比值，不是酶内波动。同一酶内是常数字。")
    print()


def corr_loading(g):
    print("=" * 96)
    print("表 3  Q1 负载量 与 各个指标的相关性（Spearman，只用 7 个氨基酸条件）")
    print("=" * 96)
    print(f"{'酶':<10}{'对比':<22}{'ρ':>9}{'p':>9}   判定")
    print("-" * 96)
    out = {}
    for e in ENZYMES:
        s = g[(g["enzyme"] == e) & (~g["is_control"])].dropna(subset=["loading"])
        for yname, ycol in [("kcat/Km", "log_kk"), ("kcat", "kcat"),
                            ("Km", "Km"), ("Vmax", "Vmax")]:
            rho, p = spearmanr(s["loading"], s[ycol])
            judge = "显著" if p < 0.05 else "不显著"
            if abs(rho) < 0.3:
                judge += " · 无关系"
            print(f"{e:<10}{'负载量 vs ' + yname:<22}{rho:>9.3f}{p:>9.3f}   {judge}")
            out[(e, yname)] = (rho, p)
        print("-" * 96)
    print("  n = 7 时，|ρ| > 0.786 才有 p < 0.05")
    print()
    return out


def spread(g):
    print("=" * 96)
    print("表 4  幅度对比：负载量的跨度 够不够解释 活性的跨度？")
    print("=" * 96)
    print(f"{'酶':<10}{'负载量跨度':>14}{'kcat/Km 跨度':>16}{'倍数比':>10}")
    print("-" * 96)
    for e in ENZYMES:
        s = g[(g["enzyme"] == e) & (~g["is_control"])].dropna(subset=["loading"])
        lr = s["loading"].max() / s["loading"].min()
        ar = s["kk"].max() / s["kk"].min()
        print(f"{e:<10}{lr:>13.2f}×{ar:>15.2f}×{ar / lr:>9.1f}×")
    print()
    print("  解读：如果比值 ≈ 1，说明负载量的变化幅度和活性差不多，得认真排除；")
    print("        如果比值 >> 1，说明活性变化远大于负载量，负载量最多只能解释一小部分。")
    print()


def plot(g):
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    colors = {"Cyt c": "#1f77b4", "lipase PS": "#ff7f0e"}

    # (a)(b) 每个酶：负载量 vs kcat/Km
    for ax, e in zip(axes[:2], ENZYMES):
        s = g[g["enzyme"] == e]
        aa = s[~s["is_control"]].dropna(subset=["loading"])
        ctl = s[s["is_control"] & s["loading"].notna()]
        free = s[s["aa"].str.startswith("free")]

        ax.scatter(aa["loading"], aa["log_kk"], s=90, c=colors[e],
                   edgecolors="k", zorder=3, label="AA condition")
        ax.scatter(ctl["loading"], ctl["log_kk"], s=90, marker="s",
                   facecolors="none", edgecolors="gray", zorder=3, label="control")
        for _, r in s.dropna(subset=["loading"]).iterrows():
            ax.annotate(r["aa"].replace("DL-", ""), (r["loading"], r["log_kk"]),
                        textcoords="offset points", xytext=(6, 5), fontsize=8)
        if len(free):
            ax.axhline(free["log_kk"].iloc[0], ls="--", c="gray", lw=1,
                       label="free enzyme")

        rho, p = spearmanr(aa["loading"], aa["log_kk"])
        ax.set_title(f"({chr(97 + ENZYMES.index(e))}) {e}\n"
                     f"Spearman ρ = {rho:+.3f}   p = {p:.3f}   n = {len(aa)}",
                     fontsize=11)
        ax.set_xlabel("Loading (%)")
        ax.set_ylabel("log10(kcat/Km)")
        ax.legend(fontsize=8, loc="best")
        ax.grid(alpha=0.25)

    # (c) 两酶归一化后叠在一起，看有没有共同趋势
    ax = axes[2]
    for e in ENZYMES:
        s = g[(g["enzyme"] == e) & (~g["is_control"])].dropna(subset=["loading"])
        x = s["loading"] / s["loading"].median()
        y = s["kk"] / s["kk"].median()
        ax.scatter(x, y, s=90, c=colors[e], edgecolors="k", zorder=3, label=e)
        for xi, yi, lab in zip(x, y, s["aa"].str.replace("DL-", "")):
            ax.annotate(lab, (xi, yi), textcoords="offset points",
                        xytext=(6, 4), fontsize=8)
    ax.axhline(1.0, ls="--", c="gray", lw=1)
    ax.axvline(1.0, ls="--", c="gray", lw=1)
    ax.set_xlabel("Loading / median loading")
    ax.set_ylabel("kcat/Km  /  median kcat/Km")
    ax.set_title("(c) Normalised: both enzymes on one scale", fontsize=11)
    ax.legend(fontsize=8)
    ax.grid(alpha=0.25)

    fig.suptitle("A02  Does loading explain the activity differences?", fontsize=13)
    fig.tight_layout()
    FIG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG, dpi=150, bbox_inches="tight")
    print(f"图已保存: {FIG}")


def main():
    g = load_groups()
    show_table(g)
    check_enormalization(g)
    corr_loading(g)
    spread(g)
    plot(g)


if __name__ == "__main__":
    main()
