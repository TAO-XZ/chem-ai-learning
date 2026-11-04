"""规则清洗：在送进 LLM 蒸馏之前，先用几条死规则去掉明显垃圾。

输入：reports/clean/*.md   （s01 去掉图片后的结果）
输出：reports/clean2/*.md

只做四件事，不做“聪明”的事：
  1. HTML 实体还原（&amp; -> &）
  2. 删掉超长的 base64 串（出版商的版权加密块）
  3. 删掉纯网址行 / 纯导航词行
  4. 删掉投稿日期行

用法：python repro/s02_clean_rules.py
"""

import html
import re
from pathlib import Path

SRC = Path("reports/clean")
DST = Path("reports/clean2")

# 一整行都是超长无空格的字母数字（版权加密串的特征）
LONG_TOKEN = re.compile(r"^[A-Za-z0-9_\\\-]{120,}$")
# 一整行只有一个网址
URL_ONLY = re.compile(r"^(https?://\S+|[\w.-]+\.(com|org|net|edu|gov)\S*)$")
# 投稿流程行
DATE_LINE = re.compile(r"^(Received|Revised|Accepted|Published)[:]", re.I)
# 版式导航词（ACS 版式固定出现的几个）
NAV_WORDS = {"SOVT", "Article", "Read Online", "ACCESS", "Metrics & More"}


def clean(text):
    text = html.unescape(text)

    kept = []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            kept.append("")           # 空行是段落分界，必须留着
            continue
        if s in NAV_WORDS or URL_ONLY.match(s) or DATE_LINE.match(s) or LONG_TOKEN.match(s):
            continue
        kept.append(line.rstrip())

    return re.sub(r"\n{3,}", "\n\n", "\n".join(kept)).strip()


def main():
    DST.mkdir(parents=True, exist_ok=True)
    files = sorted(SRC.glob("*.md"))
    if not files:
        print(f"{SRC} 里没有 .md 文件")
        return

    total_in = total_out = 0
    for f in files:
        raw = f.read_text(encoding="utf-8")
        out = clean(raw)
        (DST / f.name).write_text(out, encoding="utf-8")
        total_in += len(raw)
        total_out += len(out)
        print(f"{f.name}")
        print(f"   {len(raw):>9,} -> {len(out):>9,} 字符"
              f"   (再压缩 {100 * (1 - len(out) / len(raw)):.1f}%)")

    print(f"\n合计 {total_in:,} -> {total_out:,} 字符")
    print(f"输出目录: {DST.resolve()}")


if __name__ == "__main__":
    main()
