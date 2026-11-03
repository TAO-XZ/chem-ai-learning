"""一条命令跑完整个分析流程：读数据 -> 建模 -> 验证 -> 汇总。

用法（任何目录都行）：
    python python_basics/w02/analyze.py

换数据集：只改下面 CONFIG 区的 DATA / ENZYMES。
"""

import sys
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]          # 仓库根目录
sys.path.insert(0, str(Path(__file__).parent))      # 让 import aa_utils 生效
import os
os.chdir(ROOT)                                      # 保证相对路径 data\... 能找到

from aa_utils import load_data, add_descriptors, loo_predict, rmse, mae

# ================== CONFIG：换数据集只改这里 ==================
DATA     = r"data\enzyme_data.xlsx"         # ← 数据文件（.xlsx 走 aa_utils，.csv 直接读）
ENZYMES  = ["Cyt c", "lipase PS"]           # ← 分析哪几个体系
FEATURES = ["mw_da", "hydrophobicity_kd"]   # ← 用哪些特征列
TARGET   = "mean"                           # ← 预测哪一列
K_SCAN   = [1, 2, 3, 4, 5, 6]               # ← 扫哪些 k
K_MAIN   = 3                                # ← 主结果用哪个 k
PLOT     = True                             # ← 要不要存一张 parity 图
# ==============================================================

PLOT_PATH = ROOT / "reports" / "analyze_parity.png"


# ---------- 小工具：按显示宽度补空格，让中文表格对齐 ----------
def _w(s):
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in s)


def pad(s, width):
    return s + " " * max(0, width - _w(s))


def line(widths):
    return "-+-".join("-" * w for w in widths)


# ---------- 1. 拿数据 ----------
def load_table(path):
    """Excel -> 走 aa_utils 的清洗流程；CSV -> 直接读。"""
    if path.lower().endswith((".xlsx", ".xls")):
        return add_descriptors(load_data(path))
    return pd.read_csv(path)


# ---------- 2. 一次完整分析 ----------
def run_one(sub, name):
    """对一个体系跑完整的 LOO 分析，返回结果字典。"""
    y = sub[TARGET].values
    X = sub[FEATURES].values
    n = len(y)
    sd = y.std()

    # 基线：不用特征，只拿"其余所有样本的平均值"去预测
    base = rmse(loo_predict(X, y, k=n - 1), y)

    rows = []
    for k in K_SCAN:
        k = min(k, n - 1)
        # k=1 时"加权"没有意义（只有一个邻居），只算一次
        for weighted in ((False,) if k == 1 else (False, True)):
            pred = loo_predict(X, y, k=k, weighted=weighted)
            r = rmse(pred, y)
            rows.append({
                "k": k,
                "加权": "是" if weighted else "否",
                "RMSE": r,
                "MAE": mae(pred, y),
                "归一化": r / sd,
                "降幅%": 100 * (1 - r / base),
            })

    main = [r for r in rows
            if r["k"] == min(K_MAIN, n - 1) and r["加权"] == "否"][0]

    return {"name": name, "n": n, "sd": sd, "base": base,
            "rows": rows, "main": main, "y": y, "X": X}


# ---------- 3. 打印 ----------
def print_main(results):
    widths = [14, 5, 7, 12, 12, 10, 10]
    head = ["体系", "n", "特征数", "RMSE", "MAE", "归一化", "降幅%"]
    print(f"\n=== 主结果（k={K_MAIN}，不加权） ===")
    print("  ".join(pad(h, w) for h, w in zip(head, widths)))
    print(line(widths))
    for r in results:
        m = r["main"]
        cells = [r["name"], str(r["n"]), str(len(FEATURES)),
                 f"{m['RMSE']:.6f}", f"{m['MAE']:.6f}",
                 f"{m['归一化']:.3f}", f"{m['降幅%']:.0f}%"]
        print("  ".join(pad(c, w) for c, w in zip(cells, widths)))


def print_baseline(results):
    print(f"\n=== 基线（不用特征，直接用平均值预测） ===")
    for r in results:
        print(f"  {pad(r['name'], 14)}RMSE = {r['base']:.6f}   "
              f"（等于 标准差 × {r['base'] / r['sd']:.3f}）")


def print_scan(results):
    widths = [14, 5, 5, 12, 12, 10]
    head = ["体系", "k", "加权", "RMSE", "归一化", "降幅%"]
    print(f"\n=== k 扫描（越小越好） ===")
    print("  ".join(pad(h, w) for h, w in zip(head, widths)))
    print(line(widths))
    for r in results:
        best = min(x["RMSE"] for x in r["rows"])
        for x in r["rows"]:
            mark = "  <-- 本体系最好" if x["RMSE"] == best else ""
            cells = [r["name"], str(x["k"]), x["加权"],
                     f"{x['RMSE']:.6f}", f"{x['归一化']:.3f}",
                     f"{x['降幅%']:.0f}%"]
            print("  ".join(pad(c, w) for c, w in zip(cells, widths)) + mark)
        print(line(widths))
    print("  提示：这里扫了多个组合再挑最好的，结果会偏乐观（多重比较）。")


def print_verdict(results):
    """把数字翻译成一句话结论 —— 这才是 8 步里的"解释"。"""
    print(f"\n=== 结论 ===")
    for r in results:
        m = r["main"]
        d = m["降幅%"]
        if d < -1:
            verdict = "用了特征反而更差"
        elif d < 5:
            verdict = "特征基本没用（和基线差不多）"
        elif d < 30:
            verdict = "有用，但提升有限"
        else:
            verdict = "提升明显"
        print(f"  {pad(r['name'], 14)}{verdict}：归一化 RMSE = {m['归一化']:.3f}"
              f"（基线是 {r['base'] / r['sd']:.3f}）")

    if len(results) == 2:
        a, b = results
        ra, rb = a["main"]["归一化"], b["main"]["归一化"]
        if abs(ra - rb) < 0.05:
            print("  -> 两个体系难度相当，按归一化 RMSE 可以直接横向比较。")
        else:
            print(f"  -> 注意：两个体系难度不同（{ra:.3f} vs {rb:.3f}），"
                  f"只能比归一化 RMSE，不能比原始 RMSE。")


def make_plot(results):
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, len(results), figsize=(5.2 * len(results), 4.8))
    if len(results) == 1:
        axes = [axes]

    for ax, r in zip(axes, results):
        y = r["y"]
        pred = loo_predict(r["X"], y, k=min(K_MAIN, r["n"] - 1))
        ax.scatter(y, pred, s=55, alpha=0.85)
        lo, hi = min(y.min(), pred.min()), max(y.max(), pred.max())
        pad_ = (hi - lo) * 0.08
        ax.plot([lo - pad_, hi + pad_], [lo - pad_, hi + pad_],
                "k--", lw=1, label="ideal")
        ax.set_xlabel(f"measured {TARGET}")
        ax.set_ylabel(f"LOO predicted {TARGET}")
        ax.set_title(f"{r['name']}  (k={min(K_MAIN, r['n'] - 1)}, "
                     f"RMSE={r['main']['RMSE']:.5f})")
        ax.legend()

    fig.tight_layout()
    fig.savefig(PLOT_PATH, dpi=130)
    print(f"\n图已保存: {PLOT_PATH}")


# ---------- 4. 主程序 ----------
def main():
    print(f"数据文件: {DATA}")
    print(f"特征    : {FEATURES}")
    print(f"预测目标: {TARGET}")

    data = load_table(DATA)
    print(f"读入行数: {len(data)}")

    results = []
    for enz in ENZYMES:
        sub = data[data["enzyme"] == enz]
        if len(sub) == 0:
            print(f"  [跳过] 找不到体系 '{enz}'，可选的有: "
                  f"{sorted(data['enzyme'].unique())}")
            continue
        results.append(run_one(sub, enz))

    if not results:
        print("没有可分析的体系，检查 CONFIG 里的 ENZYMES。")
        return

    print_main(results)
    print_baseline(results)
    print_scan(results)
    print_verdict(results)

    if PLOT:
        make_plot(results)


if __name__ == "__main__":
    main()
