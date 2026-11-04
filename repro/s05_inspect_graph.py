"""看一眼建出来的知识图谱：抽几条三元组、数一数谁最重要、画一张图。

输入：reports/rag_store/graph_chunk_entity_relation.graphml
输出：reports/figures/kg_graph.png
用法：python repro/s05_inspect_graph.py
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx

GRAPH = Path("reports/rag_store/graph_chunk_entity_relation.graphml")
FIG = Path("reports/figures/kg_graph.png")

TOPN_NODES = 70      # 图里画多少个节点
TOPN_LABELS = 16     # 标多少个名字


def main():
    g = nx.read_graphml(GRAPH)
    print(f"实体 {g.number_of_nodes():,}   关系 {g.number_of_edges():,}\n")

    # ---- 1. 抽 12 条三元组看看 ----
    print("=== 随便抽 12 条三元组 ===")
    for i, (u, v, d) in enumerate(g.edges(data=True)):
        if i >= 12:
            break
        rel = d.get("keywords") or d.get("description", "")[:40] or "?"
        print(f"  {u}  --[{rel}]-->  {v}")

    # ---- 2. 谁的连接最多 ----
    deg = sorted(g.degree, key=lambda x: -x[1])
    print("\n=== 连接最多的 20 个实体 ===")
    for name, d in deg[:20]:
        print(f"  {d:>3} 条   {name}")

    # ---- 3. 画图 ----
    top = [n for n, _ in deg[:TOPN_NODES]]
    sub = g.subgraph(top)

    # 按"抱团"分成几组：同一组的节点颜色一样
    comms = nx.community.greedy_modularity_communities(sub)
    color_of = {}
    for ci, com in enumerate(comms):
        for n in com:
            color_of[n] = ci
    palette = ["#d64545", "#2f7ed8", "#2e9e5b", "#e0a020", "#8e5cc4",
               "#12a3a3", "#c25b9a", "#7d8b2f"]
    node_colors = [palette[color_of[n] % len(palette)] for n in sub.nodes]

    pos = nx.kamada_kawai_layout(sub)

    fig, ax = plt.subplots(figsize=(16, 12))
    sizes = [120 + 55 * sub.degree(n) for n in sub.nodes]
    nx.draw_networkx_edges(sub, pos, ax=ax, alpha=0.18, width=1.1, edge_color="#666666")
    nx.draw_networkx_nodes(sub, pos, ax=ax, node_size=sizes, node_color=node_colors,
                           linewidths=0.8, edgecolors="white")
    labels = {n: n for n, _ in deg[:TOPN_LABELS]}
    nx.draw_networkx_labels(sub, pos, labels=labels, ax=ax, font_size=9)

    ax.set_title(f"Knowledge graph built from 1 paper — {g.number_of_nodes()} entities, "
                 f"{g.number_of_edges()} relations\n"
                 f"(top {TOPN_NODES} by degree, colour = {len(comms)} communities)",
                 fontsize=13)
    ax.axis("off")
    fig.tight_layout()
    FIG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG, dpi=140, bbox_inches="tight")
    print(f"\n图已保存: {FIG.resolve()}")


if __name__ == "__main__":
    main()
