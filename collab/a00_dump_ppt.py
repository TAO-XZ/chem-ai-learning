"""把 PPT 的文字全倒出来（含表格、备注、图片文件名）。

用 DSH 自带 python（有 python-pptx）:
    C:\\Users\\98670\\.dsh\\dsh-runtimes\\dsh-primary-runtime\\dependencies\\python\\python.exe
"""

from pptx import Presentation
from pptx.util import Emu

PATH = r"D:\xwechat_files\wxid_ntna35lpcw9032_e7b8\msg\file\2026-10\酶微环境数据分析与后续计划_2026-10-20.pptx"

prs = Presentation(PATH)


def walk(shapes, indent=0):
    pad = "  " * indent
    for sh in shapes:
        t = sh.shape_type
        name = sh.name
        if sh.has_text_frame:
            txt = "\n".join(p.text for p in sh.text_frame.paragraphs if p.text.strip())
            if txt.strip():
                print(f"{pad}<{name}>")
                for line in txt.split("\n"):
                    print(f"{pad}  {line}")
        if getattr(sh, "has_table", False) and sh.has_table:
            tbl = sh.table
            print(f"{pad}[表格] {len(tbl.rows)} 行 x {len(tbl.columns)} 列")
            for r in tbl.rows:
                cells = []
                for c in r.cells:
                    cells.append(c.text.replace("\n", " / ")[:26])
                print(f"{pad}  | " + " | ".join(cells) + " |")
        if sh.shape_type == 6:  # group
            try:
                walk(sh.shapes, indent + 1)
            except Exception:
                pass


for i, slide in enumerate(prs.slides, 1):
    print("=" * 78)
    print(f"第 {i} 页 / 共 {len(prs.slides)} 页")
    print("=" * 78)
    walk(slide.shapes)
    if slide.has_notes_slide:
        nt = slide.notes_slide.notes_text_frame.text
        if nt.strip():
            print("[备注]")
            for line in nt.split("\n"):
                print("  " + line)
    print()
