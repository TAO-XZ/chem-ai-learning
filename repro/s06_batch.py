"""批量：把 papers/ 里的 PDF 一篇篇走完 解析 → 清洗 → 蒸馏 → 建图，
   并记录每一篇给知识图谱带来多少「新增」实体和关系。

输入：papers/*.pdf
输出：
    reports/distilled/*.md          蒸馏后的文本
    reports/kg_growth.csv           每篇的边际增量（画曲线用）
    reports/rag_store/              图谱

用法（在仓库根目录）：
    python repro/s06_batch.py                 # 处理 papers/ 里所有还没处理过的
    python repro/s06_batch.py --reset         # 清空图谱重来
    python repro/s06_batch.py --dry-run       # 只解析+蒸馏，不建图（省钱）

已处理过的文件记在 reports/rag_store/inserted.txt，重跑会自动跳过。
"""

import argparse
import asyncio
import csv
import os
import shutil
import sys
from pathlib import Path

import networkx as nx

sys.path.insert(0, str(Path(__file__).parent))

import s01_strip_images as s01
import s02_clean_rules as s02
import s03_distill as s03
import s04_build_kg as s04

PAPERS = Path("papers")
DISTILLED = Path("reports/distilled")
GROWTH = Path("reports/kg_growth.csv")
DONE_LIST = Path("reports/rag_store/inserted.txt")
GRAPHML = Path("reports/rag_store/graph_chunk_entity_relation.graphml")


def convert_pdf(pdf):
    """docling 把 PDF 转成 Markdown 文本。"""
    from docling.document_converter import DocumentConverter

    print("   解析 PDF（docling）…")
    res = DocumentConverter().convert(str(pdf))
    return res.document.export_to_markdown()


def graph_size():
    if not GRAPHML.exists():
        return 0, 0
    g = nx.read_graphml(GRAPHML)
    return g.number_of_nodes(), g.number_of_edges()


def load_done():
    if DONE_LIST.exists():
        return set(DONE_LIST.read_text(encoding="utf-8").split())
    return set()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reset", action="store_true", help="清空图谱和已处理记录")
    ap.add_argument("--dry-run", action="store_true", help="只到蒸馏，不建图")
    ap.add_argument("--force", action="store_true", help="已有蒸馏结果也重新解析+蒸馏")
    args = ap.parse_args()

    if not os.environ.get("DEEPSEEK_API_KEY"):
        print("没读到 DEEPSEEK_API_KEY。")
        return

    if args.reset:
        if s04.STORE.exists():
            shutil.rmtree(s04.STORE)
        if GROWTH.exists():
            GROWTH.unlink()
        print("已清空图谱")

    PAPERS.mkdir(exist_ok=True)
    DISTILLED.mkdir(parents=True, exist_ok=True)
    pdfs = sorted(PAPERS.glob("*.pdf"))
    if not pdfs:
        print(f"{PAPERS.resolve()} 里没有 PDF。把文献放进去再跑。")
        return

    done = load_done()
    todo = [p for p in pdfs if p.name not in done]
    print(f"共 {len(pdfs)} 篇，未处理 {len(todo)} 篇\n")

    # ---- 1. 解析 + 清洗 + 蒸馏（不依赖图谱）----
    for pdf in todo:
        target = DISTILLED / f"{pdf.stem}.md"
        if target.exists() and target.stat().st_size > 0 and not args.force:
            print(f"[{pdf.name}] 已有蒸馏结果，跳过解析和蒸馏（要重做加 --force）")
            continue
        print(f"[{pdf.name}]")
        md = convert_pdf(pdf)
        text = s02.clean(s01.clean(md))
        chunks = s03.split_chunks(text)
        print(f"   蒸馏 {len(chunks)} 段，{len(text):,} 字符")

        outs = []
        for i, ch in enumerate(chunks, 1):
            out, _ = s03.call_api(os.environ["DEEPSEEK_API_KEY"],
                                  s03.PROMPTS["photocatalysis"], ch)
            if out.strip() != "无":
                outs.append(out.strip())
            print(f"   [{i}/{len(chunks)}] {len(ch):>5,} -> {len(out):>4,}")

        distilled = "\n\n".join(outs)
        (DISTILLED / f"{pdf.stem}.md").write_text(distilled, encoding="utf-8")
        print(f"   蒸馏后 {len(distilled):,} 字符\n")

    if args.dry_run:
        print("--dry-run：到此为止，没有建图。")
        return

    # ---- 2. 一篇篇插进图谱，记录增量 ----
    async def build():
        rag = await s04.build_rag()
        rows = []
        if GROWTH.exists():
            with GROWTH.open(encoding="utf-8") as f:
                rows = list(csv.DictReader(f))

        n0, e0 = graph_size()
        print(f"起始图谱：{n0} 实体 / {e0} 关系")

        for pdf in todo:
            f = DISTILLED / f"{pdf.stem}.md"
            if not f.exists():
                continue
            text = f.read_text(encoding="utf-8")
            if not text.strip():
                print(f"[{pdf.stem}] 蒸馏结果为空，跳过")
                continue

            nb, eb = graph_size()
            await rag.ainsert(text)
            na, ea = graph_size()

            rows.append({
                "file": pdf.stem,
                "new_entities": na - nb,
                "new_relations": ea - eb,
                "total_entities": na,
                "total_relations": ea,
            })
            print(f"   {pdf.stem[:50]:<50}  +{na - nb:>4} 实体  +{ea - eb:>4} 关系"
                  f"   累计 {na} / {ea}")

            with DONE_LIST.open("a", encoding="utf-8") as fh:
                fh.write(pdf.name + "\n")

        with_any = bool(rows)
        if with_any:
            with GROWTH.open("w", encoding="utf-8", newline="") as f:
                w = csv.DictWriter(f, fieldnames=list(rows[0]))
                w.writeheader()
                w.writerows(rows)
            print(f"\n增量表已存: {GROWTH.resolve()}")
        else:
            print("\n没有文档被插入图谱，跳过增量表。")
        print(f"LLM 调用 {s04.STATS['calls']} 次，"
              f"约 {s04.STATS['in'] / 1e6 * 2 + s04.STATS['out'] / 1e6 * 8:.3f} 元")

    asyncio.run(build())


if __name__ == "__main__":
    main()
