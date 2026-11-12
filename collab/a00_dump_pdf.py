"""把两份 PDF 的文字全倒出来，并定位“负载量”出现的位置。

用 chem python（有 pymupdf）:
    D:\\conda\\envs\\chem\\python.exe
"""

import re
import fitz

PDFS = [
    (r"D:\xwechat_files\wxid_ntna35lpcw9032_e7b8\msg\file\2026-10\酶微环境分析报告_2026-10-20.pdf", "报告"),
    (r"D:\xwechat_files\wxid_ntna35lpcw9032_e7b8\msg\file\2026-10\课题介绍.pdf", "课题介绍"),
]

KEYS = ["负载", "载量", "loading", "固载", "吸附", "投料", "mg/", "mg·g", "比表", "孔径", "mmol"]

for path, tag in PDFS:
    doc = fitz.open(path)
    print("=" * 78)
    print(f"{tag}：{doc.page_count} 页  {path.split(chr(92))[-1]}")
    print("=" * 78)
    for pno, page in enumerate(doc, 1):
        txt = page.get_text()
        print(f"\n---------- 第 {pno} 页 ----------")
        print(txt.rstrip())
    print()

    print("#" * 78)
    print(f"# 关键词命中（{tag}）")
    print("#" * 78)
    for pno, page in enumerate(doc, 1):
        txt = page.get_text()
        for k in KEYS:
            for m in re.finditer(re.escape(k), txt):
                s = max(0, m.start() - 60)
                e = min(len(txt), m.end() + 60)
                snippet = txt[s:e].replace("\n", " ")
                print(f"  p{pno} [{k}] ...{snippet}...")
    print()
    doc.close()
