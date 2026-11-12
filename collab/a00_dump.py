"""把整个 xlsx 拆开看：所有 sheet（含隐藏）、所有列、每列的样子。

用法：
    python collab/a00_dump.py

目的：确认“负载量”到底在不在表里、叫什么名字。
"""

import openpyxl
import pandas as pd

PATH = r"D:\xwechat_files\wxid_ntna35lpcw9032_e7b8\msg\file\2026-10\单组拟合数据(1).xlsx"

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 100)

print("=" * 70)
print("第一部分：工作簿结构（含隐藏 sheet）")
print("=" * 70)

wb = openpyxl.load_workbook(PATH, data_only=True)
for ws in wb.worksheets:
    print(f"  [{ws.sheet_state:>10}] {ws.title!r:30} {ws.max_row} 行 x {ws.max_column} 列")

print()
print("=" * 70)
print("第二部分：每个 sheet 的列和内容")
print("=" * 70)

for ws in wb.worksheets:
    print()
    print("-" * 70)
    print(f"sheet: {ws.title!r}  state={ws.sheet_state}  size={ws.max_row}x{ws.max_column}")
    print("-" * 70)

    # 用 pandas 读，header=None 先看原始布局
    df = pd.read_excel(PATH, sheet_name=ws.title, header=None)
    print(f"原始形状: {df.shape}")
    print()

    # 打印前 6 行原始内容（用来找表头在第几行）
    print("前 6 行原始内容：")
    for i in range(min(6, len(df))):
        cells = ["" if pd.isna(v) else str(v) for v in df.iloc[i].tolist()]
        cells = [c[:18] for c in cells]
        print(f"  行{i}: {cells}")
    print()

    # 猜表头行：第一个非空单元格数量最多的前 3 行里挑
    best_row, best_cnt = 0, 0
    for i in range(min(8, len(df))):
        cnt = df.iloc[i].notna().sum()
        if cnt > best_cnt:
            best_cnt, best_row = cnt, i
    print(f"推测表头在第 {best_row} 行（非空 {best_cnt} 个）")
    print()

    df2 = pd.read_excel(PATH, sheet_name=ws.title, header=best_row)
    print(f"列名 ({len(df2.columns)} 个):")
    for c in df2.columns:
        s = df2[c]
        nn = s.notna().sum()
        try:
            u = s.dropna().unique()
        except Exception:
            u = []
        sample = ", ".join(str(x)[:14] for x in u[:6])
        print(f"    {str(c)[:34]:36} 非空{nn:4}  唯一{len(u):4}  样例: {sample}")
    print()

print("=" * 70)
print("第三部分：全表搜关键词")
print("=" * 70)

KEYS = ["负载", "载量", "loading", "load", "固载", "吸附量", "mg", "浓度", "投料", "比表", "孔径"]
for ws in wb.worksheets:
    df = pd.read_excel(PATH, sheet_name=ws.title, header=None)
    for i in range(len(df)):
        for j in range(len(df.columns)):
            v = df.iat[i, j]
            if isinstance(v, str):
                for k in KEYS:
                    if k.lower() in v.lower():
                        print(f"  [{ws.title}] 行{i} 列{j}: {v[:60]!r}")
                        break
