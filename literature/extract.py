"""从 literature/ 下的 PDF 批量提取「标题 / 摘要 / 关键词」，输出 CSV。

用法（仓库根目录）：
    D:\\conda\\envs\\chem\\python.exe literature\\extract.py

输出：
    reports/文献清单.csv

说明：
    摘要用正则从第 1-2 页抓，抓不到就留空（人工补）。
    标题先试 PDF 元数据，失败再取首页前两行 —— 都不保证准，属于「省 80% 手工」而不是全自动。
"""

import csv
import re
import sys
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[1]
LIT = ROOT / "literature"
OUT = ROOT / "reports" / "文献清单.csv"


def norm(s: str) -> str:
    s = s.replace("\u3000", " ")
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n{2,}", "\n", s)
    return s.strip()


def head_text(doc, pages=2) -> str:
    n = min(pages, doc.page_count)
    return norm("\n".join(doc[i].get_text() for i in range(n)))


def get_title(doc, text: str) -> str:
    """用首页「最大字号」定位标题 —— 比抓第一行可靠得多（第一行常是期刊页眉）。"""
    try:
        d = doc[0].get_text("dict")
        spans = []
        for blk in d.get("blocks", []):
            for line in blk.get("lines", []):
                for sp in line.get("spans", []):
                    s = sp.get("text", "").strip()
                    if len(s) >= 3:
                        spans.append((round(float(sp.get("size", 0)), 1), s))
        if spans:
            mx = max(s for s, _ in spans)
            picked = [t for s, t in spans if s >= mx - 0.6]
            title = " ".join(picked)
            title = re.sub(r"(?<=[\u4e00-\u9fa5]) (?=[\u4e00-\u9fa5])", "", title)
            title = re.sub(r"\s{2,}", " ", title).strip()
            if 8 <= len(title) <= 220:
                return title
    except Exception:
        pass

    t = norm((doc.metadata or {}).get("title", "") or "")
    if 10 <= len(t) <= 200 and not t.lower().endswith(".pdf") and "Microsoft" not in t:
        return t

    lines = [x.strip() for x in text.split("\n") if x.strip()]
    for ln in lines[:12]:
        if 8 <= len(ln) <= 120 and re.search(r"[\u4e00-\u9fa5]{4,}", ln):
            return ln
    return lines[0][:120] if lines else ""


STOP_EN = re.compile(r"(Index Terms|Key\s*words|I\.\s*INTRODUCTION|1\.\s*Introduction|©|Received\s*:)", re.I)
STOP_ZH = re.compile(r"(关\s*键\s*词|中图分类号|文献标志码|Abstract)")


def get_abstract(text: str) -> str:
    """先中文后英文。

    英文库排版坑：Elsevier 把 abstract 排成 `a b s t r a c t`（每个字母之间带空格），
    所以匹配式不能直接写 `Abstract`，要用 `a\\s*b\\s*s\\s*t\\s*r\\s*a\\s*c\\s*t`。
    """
    m = re.search(r"摘\s*要", text)
    if m:
        seg = text[m.end(): m.end() + 1800].lstrip("：: \n")
        cut = STOP_ZH.search(seg)
        if cut:
            seg = seg[:cut.start()]
        seg = norm(seg)
        if len(seg) > 50:
            return seg[:1200]

    m = re.search(r"a\s*b\s*s\s*t\s*r\s*a\s*c\s*t", text, re.I)
    if m:
        seg = text[m.end(): m.end() + 2800]
        seg = re.sub(r"^[\s—\-–:]+", "", seg)
        cut = STOP_EN.search(seg)
        if cut:
            seg = seg[:cut.start()]
        seg = norm(seg)
        if len(seg) > 80:
            return seg[:1500]
    return ""


def get_keywords(text: str) -> str:
    m = re.search(r"关\s*键\s*词[：:\s]*(.{2,200}?)(?:\n|中图分类号|文献标志码|Abstract)", text, re.S)
    if m:
        return norm(m.group(1))[:200]
    m = re.search(r"(?:Index\s*Terms|Key\s*words?)\s*[—\-–:]+\s*(.{3,260})", text, re.I)
    if m:
        return norm(m.group(1).split("\n")[0])[:260]
    return ""


def main():
    rows = []
    pdfs = [p for p in sorted(LIT.rglob("*.pdf")) if p.relative_to(LIT).parts[0] != "其它"]
    if not pdfs:
        print("literature/ 下没有 PDF")
        return
    for p in pdfs:
        rel = p.relative_to(LIT)
        code = p.stem.split("_")[0] if "_" in p.stem else p.stem
        lang = "中文" if rel.parts[0] == "中文" else ("英文" if rel.parts[0] == "英文" else "其它")
        try:
            doc = fitz.open(p)
            text = head_text(doc)
            rows.append({
                "编号": code,
                "语种": lang,
                "简称": "_".join(p.stem.split("_")[1:]) or p.stem,
                "标题": get_title(doc, text),
                "关键词": get_keywords(text),
                "摘要": get_abstract(text),
                "页数": doc.page_count,
                "文件名": p.name,
            })
            doc.close()
        except Exception as e:
            rows.append({"编号": code, "语种": lang, "文件名": p.name,
                         "标题": f"!! 读取失败: {e}", "关键词": "", "摘要": "", "页数": 0, "简称": ""})

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["编号", "语种", "简称", "标题", "关键词", "摘要", "页数", "文件名"])
        w.writeheader()
        w.writerows(rows)

    total = len(rows)
    got_abs = sum(1 for r in rows if len(r["摘要"]) > 50)
    got_kw = sum(1 for r in rows if r["关键词"])
    print(f"共 {total} 篇 → {OUT}")
    print(f"  摘要抓到: {got_abs}/{total}   关键词抓到: {got_kw}/{total}")
    if got_abs < total:
        print("  摘要为空的篇目：")
        for r in rows:
            if len(r["摘要"]) <= 50:
                print(f"    {r['编号']}  {r['文件名'][:60]}")


if __name__ == "__main__":
    main()
