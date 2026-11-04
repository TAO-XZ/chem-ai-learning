"""把 docling 输出的 Markdown 清干净：去图片、去链接、压空行。

输入：reports/docling_out/*.md
输出：reports/clean/*.md
用法：python repro/s01_strip_images.py
"""

import re
from pathlib import Path

SRC = Path("reports/docling_out")
DST = Path("reports/clean")

IMG = re.compile(r"!\[[^\]]*\]\(data:image/[^)]*\)")   # base64 图片块
LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")             # [文字](网址) -> 文字


def clean(text):
    text = IMG.sub("", text)          # 图片整个删掉
    text = LINK.sub(r"\1", text)      # 只留链接文字
    lines = [ln.rstrip() for ln in text.splitlines()]
    text = "\n".join(lines)
    # 空行要留着 —— 它是段落分界线，s03 靠它切段
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def main():
    DST.mkdir(parents=True, exist_ok=True)
    files = sorted(SRC.glob("*.md"))
    if not files:
        print(f"{SRC} 里没有 .md 文件")
        return

    for f in files:
        raw = f.read_text(encoding="utf-8")
        out = clean(raw)
        (DST / f.name).write_text(out, encoding="utf-8")
        print(f"{f.name}")
        print(f"   {len(raw):>10,} -> {len(out):>9,} 字符"
              f"   (压缩 {100 * (1 - len(out) / len(raw)):.1f}%)")

    print(f"\n输出目录: {DST.resolve()}")


if __name__ == "__main__":
    main()
