"""用 reports/kg_report.json + 图谱图，生成一份给导师看的 Word 简报。

需要 python-docx（用 DSH 自带 Python 跑）：
    "C:\\Users\\98670\\.dsh\\dsh-runtimes\\dsh-primary-runtime\\dependencies\\python\\python.exe" repro/build_report_docx.py

输入：reports/kg_report.json、reports/figures/kg_graph.png
输出：reports/知识图谱复现简报_<日期>.docx
"""

import json
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

DATA = Path("reports/kg_report.json")
FIG = Path("reports/figures/kg_graph.png")
OUT_DIR = Path("reports")

COST_YUAN = 2.61          # 本次建图实测花费（s06 输出）
COST_PER_PAPER = 0.87
CALLS = 233

# 文件名太长，表格里换短名字
SHORT_NAMES = {
    "MXene_cocatalyst_2017": "MXene/CdS（2017）",
    "Pt_clusters_on_COF_2022": "Pt 团簇/COF（2022）",
    "Pt_single_sites_ZnIn2S4_2022": "Pt 单原子/ZnIn2S4（2022）",
}


def set_font(run, name="宋体", size=10.5, bold=False, color=None):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    if color:
        run.font.color.rgb = color
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)


def para(doc, text, size=10.5, bold=False, name="宋体", space_after=3,
         align=None, color=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if align is not None:
        p.alignment = align
    set_font(p.add_run(text), name=name, size=size, bold=bold, color=color)
    return p


def heading(doc, text, level=1):
    size = 14 if level == 1 else 12
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True     # 标题别和下面的表分家
    set_font(p.add_run(text), name="黑体", size=size, bold=True)


def table(doc, header, rows, widths=None):
    t = doc.add_table(rows=1, cols=len(header))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(header):
        cell = t.rows[0].cells[i]
        cell.text = ""
        set_font(cell.paragraphs[0].add_run(h), size=9.5, bold=True)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    for row in rows:
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].text = ""
            set_font(cells[i].paragraphs[0].add_run(str(v)), size=9.5)
    if widths:
        from docx.oxml import OxmlElement
        t.autofit = False
        layout = OxmlElement("w:tblLayout")
        layout.set(qn("w:type"), "fixed")
        t._tbl.tblPr.append(layout)
        for i, w in enumerate(widths):
            t.columns[i].width = Cm(w)
            for cell in t.columns[i].cells:
                cell.width = Cm(w)
    return t


def main():
    d = json.loads(DATA.read_text(encoding="utf-8"))

    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
    sec.left_margin = sec.right_margin = Cm(2.2)
    sec.top_margin = sec.bottom_margin = Cm(2.0)

    # 标题
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(2)
    set_font(p.add_run("知识图谱复现简报"), name="黑体", size=18, bold=True)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(2)
    set_font(p.add_run("从文献 PDF 到可问答的领域知识图谱"), size=10.5,
             color=RGBColor(0x55, 0x55, 0x55))
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(8)
    set_font(p.add_run(d["generated"]), size=9,
             color=RGBColor(0x88, 0x88, 0x88))

    # 一、结论
    heading(doc, "一、结论")
    para(doc, f"用 4 篇光催化产氢文献跑通了「PDF → 文本 → LLM 蒸馏 → 知识图谱 → 跨文献问答」"
              f"全流程，建成 {d['n_entities']} 个实体、{d['n_relations']} 条关系的知识图谱，"
              f"能够跨文献综合回答专业问题。")
    para(doc, f"全流程成本 {COST_YUAN} 元（{CALLS} 次模型调用），"
              f"折合约 {COST_PER_PAPER} 元/篇；按 100 篇计，预算约 90 元。")
    para(doc, "主要瓶颈不在算力，而在「实体归一化」：同一化学物种会以多种写法进入图谱"
              "（如 Pt / Pt NPs / Pt Single Atoms 未合并），这是后续需要重点处理的问题。")

    # 二、数据规模
    heading(doc, "二、数据规模与逐篇增量")
    rows = []
    for x in d["docs"]:
        rows.append([SHORT_NAMES.get(x["file"], x["file"]),
                     f"+{x['new_entities']}", f"+{x['new_relations']}",
                     x["total_entities"], x["total_relations"]])
    table(doc, ["文献", "新增实体", "新增关系", "累计实体", "累计关系"], rows,
          widths=[6.4, 2.4, 2.4, 2.4, 2.4])
    para(doc, "注：第一篇（JACS 2026, MOF 微环境）为方法来源文献，其统计为建图起点。",
         size=9, color=RGBColor(0x66, 0x66, 0x66))

    # 三、图谱
    heading(doc, "三、知识图谱")
    if FIG.exists():
        doc.add_picture(str(FIG), width=Cm(14.2))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    para(doc, f"节点大小正比于连接数，颜色为自动识别的社区（全图共 {d['n_communities']} 个）。"
              f"图中可见不同材料体系各自成团，而 Pt、H2 等节点位于各团之间起连接作用。",
         size=9, color=RGBColor(0x66, 0x66, 0x66))

    # 四、核心实体
    heading(doc, "四、连接最多的实体")
    rows = [[n, c] for n, c in d["top_entities"][:10]]
    table(doc, ["实体", "连接数"], rows, widths=[10.6, 3.0])

    # 五、三元组
    heading(doc, "五、抽取到的三元组（示例）")
    rows = [[s, r, o] for s, r, o in d["triples"][:8]]
    table(doc, ["主语", "关系", "宾语"], rows, widths=[5.0, 4.5, 5.0])

    # 六、方法
    heading(doc, "六、方法与工具链")
    para(doc, "1. 解析：docling 将 PDF 转 Markdown。单篇 10 页约 40 秒；"
              "图片以 base64 内嵌，占全文体积 96.6%，须先剥离。")
    para(doc, "2. 蒸馏：按领域 system prompt 调用 deepseek-chat，只保留机理相关陈述，"
              "并规范化学实体写法；文本由 6.6 万字符压缩至 1.4 万。")
    para(doc, "3. 建图：LightRAG 抽取实体与关系，写入 GraphML；"
              "向量检索使用本地嵌入模型 paraphrase-multilingual-MiniLM-L12-v2。")
    para(doc, "4. 问答：图谱检索 + LLM 生成，答案附来源文档。")

    # 七、已知问题
    heading(doc, "七、已知问题与下一步")
    para(doc, "① 实体归一化不足。Pt 相关实体分裂为 5 种写法，稀释了检索命中率；"
              "需在蒸馏提示或后处理中加入同义词归并。")
    para(doc, "② 嵌入截断。当前嵌入模型上限 256 token，而实体摘要可达 2000 字符，"
              "超出部分被截断；建议更换支持长文本的模型（如 bge-m3）。")
    para(doc, "③ 规模尚小。4 篇文献不足以观察「多篇合并的边际递减」，"
              "需 100 篇同方向文献验证。")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"知识图谱复现简报_{d['generated']}.docx"
    doc.save(out)
    print(f"已生成: {out.resolve()}")

    # 回读校验
    chk = Document(out)
    print(f"段落 {len(chk.paragraphs)} 个，表格 {len(chk.tables)} 个，"
          f"图片 {len(chk.inline_shapes)} 张")
    bad = [p.text for p in chk.paragraphs if "**" in p.text]
    print(f"残留 Markdown 粗体标记: {len(bad)} 处")


if __name__ == "__main__":
    main()
