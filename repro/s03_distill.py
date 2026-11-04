"""用 DeepSeek 按论文的规则蒸馏文献文本。

输入：reports/clean2/*.md
输出：reports/distilled/*.md

用法（在仓库根目录）：
    python repro/s03_distill.py --limit 2    # 只跑 2 段，先验证，花几分钱
    python repro/s03_distill.py              # 全跑

API key 从环境变量 DEEPSEEK_API_KEY 读，不写在代码里。
"""

import argparse
import os
import sys
import time
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent))
from prompts import PROMPTS

API_URL = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-chat"

SRC = Path("reports/clean2")
DST = Path("reports/distilled")

CHUNK_CHARS = 3500        # 每段送给模型的字符数
PRICE_IN = 2.0            # 元 / 百万 token（估算）
PRICE_OUT = 8.0


def split_chunks(text, size=CHUNK_CHARS):
    """按空行切段，把相邻段落拼到接近 size 个字符。"""
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks, buf = [], ""
    for p in paras:
        if len(buf) + len(p) + 2 > size and buf:
            chunks.append(buf)
            buf = p
        else:
            buf = f"{buf}\n\n{p}" if buf else p
    if buf:
        chunks.append(buf)
    return chunks


def call_api(key, system, user, retries=3):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.3,
    }
    headers = {"Authorization": f"Bearer {key}"}

    for attempt in range(1, retries + 1):
        try:
            r = requests.post(API_URL, json=payload, headers=headers, timeout=120)
            if r.status_code != 200:
                raise RuntimeError(f"HTTP {r.status_code}: {r.text[:200]}")
            data = r.json()
            return data["choices"][0]["message"]["content"], data.get("usage", {})
        except Exception as e:
            if attempt == retries:
                raise
            print(f"    第 {attempt} 次失败（{e}），5 秒后重试")
            time.sleep(5)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="只跑前 N 段，0 = 全跑")
    ap.add_argument("--field", default="photocatalysis", choices=list(PROMPTS))
    args = ap.parse_args()

    key = os.environ.get("DEEPSEEK_API_KEY")
    if not key:
        print("没读到 DEEPSEEK_API_KEY，先把环境变量设好、并新开一个窗口。")
        return

    files = sorted(SRC.glob("*.md"))
    if not files:
        print(f"{SRC} 里没有 .md 文件")
        return

    DST.mkdir(parents=True, exist_ok=True)
    system = PROMPTS[args.field]
    print(f"模型 {MODEL}   领域 {args.field}   每段 {CHUNK_CHARS} 字符")

    tok_in = tok_out = 0
    done = 0

    for f in files:
        chunks = split_chunks(f.read_text(encoding="utf-8"))
        print(f"\n{f.name}")
        print(f"   共 {len(chunks)} 段，原文 {sum(len(c) for c in chunks):,} 字符")

        outs = []
        for i, ch in enumerate(chunks, 1):
            if args.limit and done >= args.limit:
                break
            out, usage = call_api(key, system, ch)
            tok_in += usage.get("prompt_tokens", 0)
            tok_out += usage.get("completion_tokens", 0)
            done += 1
            outs.append(out.strip())
            print(f"   [{i}/{len(chunks)}] {len(ch):>5,} -> {len(out):>4,} 字符")

        if outs:
            (DST / f.name).write_text("\n\n".join(outs), encoding="utf-8")

    cost = tok_in / 1e6 * PRICE_IN + tok_out / 1e6 * PRICE_OUT
    print(f"\n共 {done} 次调用")
    print(f"输入 {tok_in:,} tok   输出 {tok_out:,} tok")
    print(f"本次花费约 {cost:.4f} 元")
    print(f"输出目录: {DST.resolve()}")


if __name__ == "__main__":
    main()
