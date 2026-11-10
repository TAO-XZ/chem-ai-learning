"""把知识图谱的统计结果导出成 JSON + Markdown，给报告脚本用。

输入：reports/rag_store/graph_chunk_entity_relation.graphml
      reports/kg_growth.csv
输出：reports/kg_report.json
      reports/kg_report.md
用法：python repro/s07_export.py
"""

import csv
import json
from collections import Counter
from datetime import date
from pathlib import Path

import networkx as nx

GRAPH = Path("reports/rag_store/graph_chunk_entity_relation.graphml")
GROWTH = Path("reports/kg_growth.csv")
OUT_JSON = Path("reports/kg_report.json")
OUT_MD = Path("reports/kg_report.md")

N_TOP = 20
N_TRIPLES = 12


def main():
    g = nx.read_graphml(GRAPH)
    deg = dict(g.degree)
    deg_sorted = sorted(deg.items(), key=lambda x: -x[1])

    # 实体类型分布
    types = Counter(d.get("entity_type", "?") for _, d in g.nodes(data=True))

    # 挑有代表性的三元组：两端都是高度数节点的
    top_set = {n for n, _ in deg_sorted[:40]}
    cand = [(u, v, d) for u, v, d in g.edges(data=True)
            if u in top_set and v in top_set]
    cand.sort(key=lambda e: -(deg[e[0]] + deg[e[1]]))
    triples = []
    for u, v, d in cand[:N_TRIPLES]:
        rel = (d.get("keywords") or "").split(",")[0].strip()
        if not rel:
            rel = (d.get("description") or "")[:40]
        triples.append([u, rel or "related to", v])

    # 每篇文献的增量
    docs = []
    if GROWTH.exists():
        with GROWTH.open(encoding="utf-8") as f:
            docs = list(csv.DictReader(f))

    data = {
        "generated": str(date.today()),
        "n_entities": g.number_of_nodes(),
        "n_relations": g.number_of_edges(),
        "n_communities": len(list(nx.community.greedy_modularity_communities(g))),
        "entity_types": types.most_common(),
        "docs": docs,
        "top_entities": [[n, d] for n, d in deg_sorted[:N_TOP]],
        "triples": triples,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    # 顺手出一份 Markdown
    lines = [
        f"# 知识图谱复现简报（{data['generated']}）",
        "",
        f"- 实体 **{data['n_entities']}** 个，关系 **{data['n_relations']}** 条，"
        f"自动识别 **{data['n_communities']}** 个社区",
        "",
        "## 每篇文献带来的增量",
        "",
        "| 文献 | 新增实体 | 新增关系 | 累计实体 | 累计关系 |",
        "|---|---:|---:|---:|---:|",
    ]
    for d in docs:
        lines.append(f"| {d['file']} | +{d['new_entities']} | +{d['new_relations']} "
                     f"| {d['total_entities']} | {d['total_relations']} |")

    lines += ["", "## 连接最多的实体", "", "| 实体 | 连接数 |", "|---|---:|"]
    for n, d in data["top_entities"]:
        lines.append(f"| {n} | {d} |")

    lines += ["", "## 示例三元组", "", "| 主语 | 关系 | 宾语 |", "|---|---|---|"]
    for s, r, o in triples:
        lines.append(f"| {s} | {r} | {o} |")

    lines += ["", "## 实体类型分布", "", "| 类型 | 数量 |", "|---|---:|"]
    for t, c in data["entity_types"]:
        lines.append(f"| {t} | {c} |")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"实体 {data['n_entities']} / 关系 {data['n_relations']} / "
          f"社区 {data['n_communities']}")
    print(f"已导出: {OUT_JSON.resolve()}")
    print(f"已导出: {OUT_MD.resolve()}")


if __name__ == "__main__":
    main()
