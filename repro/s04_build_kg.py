"""用 LightRAG 把蒸馏后的文本建成知识图谱。

输入：reports/distilled/*.md
输出：reports/rag_store/   （图谱 + 向量库，本地文件）
      reports/rag_store/graph_chunk_entity_relation.graphml  ← 能用 Gephi 打开

用法：
    python repro/s04_build_kg.py                  # 建图
    python repro/s04_build_kg.py --ask "问题"      # 建完再问一句
    python repro/s04_build_kg.py --ask-only "问题" # 不重建，直接问

需要的环境变量：DEEPSEEK_API_KEY
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path

import numpy as np
import requests
from lightrag import LightRAG, QueryParam
from lightrag.kg.shared_storage import initialize_pipeline_status
from lightrag.utils import EmbeddingFunc
from sentence_transformers import SentenceTransformer

SRC = Path("reports/distilled")
STORE = Path("reports/rag_store")

API_URL = "https://api.deepseek.com/chat/completions"
LLM_MODEL = "deepseek-chat"
EMB_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
EMB_DIM = 384
EMB_MAX_TOKENS = 256


# ---------------- LLM：DeepSeek ----------------
# 累计用量，跑完能算钱
STATS = {"calls": 0, "in": 0, "out": 0}


async def deepseek_complete(prompt, system_prompt=None, history_messages=None, **kwargs):
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    for m in history_messages or []:
        messages.append(m)
    messages.append({"role": "user", "content": prompt})

    payload = {"model": LLM_MODEL, "messages": messages, "temperature": 0.1}
    if kwargs.get("response_format"):
        payload["response_format"] = kwargs["response_format"]

    headers = {"Authorization": f"Bearer {os.environ['DEEPSEEK_API_KEY']}"}
    for attempt in range(3):
        try:
            r = requests.post(API_URL, json=payload, headers=headers, timeout=180)
            if r.status_code != 200:
                raise RuntimeError(f"HTTP {r.status_code}: {r.text[:200]}")
            data = r.json()
            usage = data.get("usage") or {}
            STATS["calls"] += 1
            STATS["in"] += usage.get("prompt_tokens", 0)
            STATS["out"] += usage.get("completion_tokens", 0)
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            if attempt == 2:
                raise
            print(f"   LLM 第 {attempt + 1} 次失败（{e}），重试")
            await asyncio.sleep(5)


# ---------------- 嵌入：本地小模型 ----------------
_model = None


def get_model():
    global _model
    if _model is None:
        print(f"   加载嵌入模型 {EMB_MODEL} …")
        _model = SentenceTransformer(EMB_MODEL)
    return _model


async def embed(texts):
    vecs = get_model().encode(
        texts, convert_to_numpy=True, normalize_embeddings=True, batch_size=16
    )
    return np.asarray(vecs, dtype=np.float32)


async def build_rag():
    STORE.mkdir(parents=True, exist_ok=True)
    rag = LightRAG(
        working_dir=str(STORE),
        llm_model_func=deepseek_complete,
        embedding_func=EmbeddingFunc(
            embedding_dim=EMB_DIM, max_token_size=EMB_MAX_TOKENS, func=embed
        ),
    )
    await rag.initialize_storages()
    await initialize_pipeline_status()
    return rag


def graph_stats():
    """数一下图谱里有多少个实体、多少条关系。"""
    import networkx as nx

    p = STORE / "graph_chunk_entity_relation.graphml"
    if not p.exists():
        print("   还没生成 graphml")
        return
    g = nx.read_graphml(p)
    print(f"\n图谱：{g.number_of_nodes():,} 个实体   {g.number_of_edges():,} 条关系")
    print(f"文件：{p.resolve()}")


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ask", default="", help="建完图后问一个问题")
    ap.add_argument("--ask-only", dest="ask_only", default="", help="不重建，直接问")
    args = ap.parse_args()

    if not os.environ.get("DEEPSEEK_API_KEY"):
        print("没读到 DEEPSEEK_API_KEY，先设环境变量并新开窗口。")
        return

    rag = await build_rag()

    if not args.ask_only:
        files = sorted(SRC.glob("*.md"))
        if not files:
            print(f"{SRC} 里没有 .md 文件")
            return
        for f in files:
            text = f.read_text(encoding="utf-8")
            print(f"\n插入 {f.name}  ({len(text):,} 字符)")
            await rag.ainsert(text)
        graph_stats()

    question = args.ask_only or args.ask
    if question:
        print(f"\n提问：{question}")
        ans = await rag.aquery(question, param=QueryParam(mode="hybrid"))
        print("\n" + "=" * 60)
        print(ans)
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
