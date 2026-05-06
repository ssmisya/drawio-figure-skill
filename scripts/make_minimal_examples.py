#!/usr/bin/env python3
"""Generate minimal editable draw.io and PPTX examples for this skill.

The examples are intentionally simple and dependency-free. They demonstrate the
core promise of the skill: rebuild visible layout primitives as editable objects,
not as one flat screenshot.
"""

from __future__ import annotations

import html
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "examples" / "minimal"


def esc(text: object) -> str:
    return html.escape(str(text), quote=True)


def drawio_cell(cell_id: str, x: int, y: int, w: int, h: int, text: str, style: str) -> str:
    return f"""<mxCell id="{esc(cell_id)}" value="{esc(text)}" style="{style}" vertex="1" parent="1">
  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />
</mxCell>"""


def drawio_line(cell_id: str, x1: int, y1: int, x2: int, y2: int, color: str = "#CBD5E1") -> str:
    return f"""<mxCell id="{esc(cell_id)}" value="" style="endArrow=none;html=1;rounded=0;strokeColor={color};strokeWidth=1;" edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="{x1}" y="{y1}" as="sourcePoint" />
    <mxPoint x="{x2}" y="{y2}" as="targetPoint" />
  </mxGeometry>
</mxCell>"""


def make_drawio() -> None:
    cells = [
        '<mxCell id="0" />',
        '<mxCell id="1" parent="0" />',
        drawio_cell(
            "title",
            40,
            24,
            920,
            44,
            "Scenario x Risk Category Policy Matrix",
            "text;html=1;strokeColor=none;fillColor=none;fontSize=26;fontStyle=1;fontColor=#071B63;align=center;verticalAlign=middle;",
        ),
        drawio_cell(
            "subtitle",
            160,
            66,
            680,
            26,
            "Editable draw.io reconstruction: text, policy chips, grid lines, and legend are native objects.",
            "text;html=1;strokeColor=none;fillColor=none;fontSize=12;fontColor=#475569;align=center;verticalAlign=middle;",
        ),
        drawio_cell(
            "panel",
            40,
            120,
            920,
            440,
            "",
            "rounded=1;arcSize=2;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#94A3B8;strokeWidth=1.4;shadow=1;",
        ),
    ]

    row_h = 80
    col_w = 170
    left_w = 220
    x0, y0 = 40, 120
    headers = ["Mainstream Social", "Protective Child-Safe", "Permissive Legal-Baseline", "Commercial Brand-Safe"]
    rows = [
        ("01", "Nudity, Sexual Content & Fetish", "#4F46E5"),
        ("02", "Violence, Hate & Self-Harm", "#DC2626"),
        ("03", "Regulated Goods & Substances", "#EA580C"),
        ("04", "IP, Copyright & Brand Safety", "#D97706"),
        ("05", "Cultural & Religious Sensitivity", "#16A34A"),
    ]
    chips = [
        ["A. General Safe", "B. Family Safe", "E. Creative Freedom", "D. Lingerie Mode"],
        ["A. Real-world", "B. Zero Tolerance", "E. Legal Compliance", "D. Fiction Only"],
        ["A. Family Friendly", "D. Minor Protection", "B. Regional Permissive", "C. Retail Pharmacy"],
        ["B. Commercial Clean", "-", "A. Parody Friendly", "C. Brand Protection"],
        ["A. Western Liberal", "E. Max Neutrality", "G. Mediterranean", "C. Global Neutrality"],
    ]

    for i in range(6):
        y = y0 + 72 + i * row_h
        cells.append(drawio_line(f"h{i}", x0, y, x0 + left_w + 4 * col_w, y))
    for j in range(6):
        x = x0 + left_w + j * col_w
        cells.append(drawio_line(f"v{j}", x, y0, x, y0 + 72 + 5 * row_h))

    for j, h in enumerate(headers):
        cells.append(
            drawio_cell(
                f"header{j}",
                x0 + left_w + j * col_w + 8,
                y0 + 14,
                col_w - 16,
                44,
                h,
                "rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#CBD5E1;fontSize=13;fontStyle=1;fontColor=#071B63;align=center;verticalAlign=middle;",
            )
        )

    for i, (num, label, color) in enumerate(rows):
        y = y0 + 72 + i * row_h
        cells.append(
            drawio_cell(
                f"row{i}",
                x0 + 16,
                y + 14,
                190,
                52,
                f"{num}  {label}",
                f"text;html=1;strokeColor=none;fillColor=none;fontSize=13;fontStyle=1;fontColor={color};align=left;verticalAlign=middle;whiteSpace=wrap;",
            )
        )
        for j in range(4):
            text = chips[i][j]
            if text == "-":
                style = "text;html=1;strokeColor=none;fillColor=none;fontSize=18;fontStyle=1;fontColor=#071B63;align=center;verticalAlign=middle;"
            else:
                shift = text.startswith(("B. Regional", "A. Parody", "C. Retail", "C. Brand", "D. Fiction"))
                style = (
                    "rounded=1;arcSize=7;whiteSpace=wrap;html=1;fillColor=#F4F0FF;"
                    f"strokeColor={'#EF4444' if shift else '#B8A7E8'};"
                    f"dashed={'1' if shift else '0'};"
                    f"fontColor={'#EF0000' if shift else '#071B63'};fontSize=12;fontStyle=1;align=center;verticalAlign=middle;"
                )
            cells.append(drawio_cell(f"chip{i}_{j}", x0 + left_w + j * col_w + 22, y + 24, col_w - 44, 32, text, style))

    legend = [
        ("Adaptive", "#F4F0FF", "#B8A7E8", "0"),
        ("Shift", "#FFFFFF", "#EF4444", "1"),
    ]
    for i, (name, fill, stroke, dashed) in enumerate(legend):
        lx = 335 + i * 170
        cells.append(
            drawio_cell(
                f"legend_box{i}",
                lx,
                585,
                60,
                28,
                "",
                f"rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};dashed={dashed};strokeWidth=1.5;",
            )
        )
        cells.append(
            drawio_cell(
                f"legend_text{i}",
                lx + 70,
                582,
                100,
                34,
                name,
                "text;html=1;strokeColor=none;fillColor=none;fontSize=14;fontStyle=1;fontColor=#071B63;align=left;verticalAlign=middle;",
            )
        )

    body = "\n".join(cells)
    xml = f"""<mxfile host="app.diagrams.net">
  <diagram name="Policy Matrix">
    <mxGraphModel dx="1000" dy="700" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1000" pageHeight="640" math="0" shadow="0">
      <root>
{body}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""
    (OUT / "policy_matrix.drawio").write_text(xml)


EMU = 914400


def emu(inches: float) -> int:
    return int(inches * EMU)


def ppt_shape(shape_id: int, name: str, x: float, y: float, w: float, h: float, text: str, fill: str, line: str, font: str = "071B63", size: int = 1400, bold: bool = False, dash: bool = False) -> str:
    dash_xml = '<a:prstDash val="dash"/>' if dash else ""
    bold_attr = ' b="1"' if bold else ""
    return f"""
<p:sp>
  <p:nvSpPr><p:cNvPr id="{shape_id}" name="{esc(name)}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm>
    <a:prstGeom prst="roundRect"><a:avLst/></a:prstGeom>
    <a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>
    <a:ln w="12700"><a:solidFill><a:srgbClr val="{line}"/></a:solidFill>{dash_xml}</a:ln>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="ctr"/><a:lstStyle/>
    <a:p><a:pPr algn="ctr"/><a:r><a:rPr lang="en-US" sz="{size}"{bold_attr}><a:solidFill><a:srgbClr val="{font}"/></a:solidFill></a:rPr><a:t>{esc(text)}</a:t></a:r></a:p>
  </p:txBody>
</p:sp>"""


def ppt_text(shape_id: int, name: str, x: float, y: float, w: float, h: float, text: str, font: str = "071B63", size: int = 1800, bold: bool = False) -> str:
    bold_attr = ' b="1"' if bold else ""
    return f"""
<p:sp>
  <p:nvSpPr><p:cNvPr id="{shape_id}" name="{esc(name)}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
    <a:noFill/><a:ln><a:noFill/></a:ln>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="ctr"/><a:lstStyle/>
    <a:p><a:pPr algn="ctr"/><a:r><a:rPr lang="en-US" sz="{size}"{bold_attr}><a:solidFill><a:srgbClr val="{font}"/></a:solidFill></a:rPr><a:t>{esc(text)}</a:t></a:r></a:p>
  </p:txBody>
</p:sp>"""


def make_pptx() -> None:
    shapes = []
    sid = 2
    shapes.append(ppt_text(sid, "title", 0.8, 0.28, 11.7, 0.45, "Editable Policy Matrix", size=2600, bold=True)); sid += 1
    shapes.append(ppt_text(sid, "subtitle", 2.1, 0.72, 9.0, 0.28, "A minimal PPTX reconstruction with editable shapes and text.", font="475569", size=1200)); sid += 1
    shapes.append(ppt_shape(sid, "panel", 0.55, 1.2, 12.2, 5.7, "", "FFFFFF", "94A3B8", size=1000)); sid += 1

    headers = ["Mainstream", "Protective", "Permissive", "Commercial"]
    rows = ["01 Nudity", "02 Violence", "03 Goods", "04 Brand", "05 Culture"]
    chips = [
        ["A. General Safe", "B. Family Safe", "E. Creative", "D. Lingerie"],
        ["A. Real-world", "B. Zero Tolerance", "E. Legal", "D. Fiction"],
        ["A. Family Friendly", "D. Minor Protect", "B. Regional", "C. Retail"],
        ["B. Clean", "-", "A. Parody", "C. Brand"],
        ["A. Liberal", "E. Neutrality", "G. Mediterranean", "C. Global"],
    ]

    x0, y0 = 0.9, 1.55
    left_w, col_w, row_h = 2.3, 2.25, 0.78
    for j, header in enumerate(headers):
        shapes.append(ppt_shape(sid, f"header {j}", x0 + left_w + j * col_w, y0, 2.0, 0.45, header, "F8FAFC", "CBD5E1", size=1300, bold=True)); sid += 1

    for i, row in enumerate(rows):
        y = y0 + 0.72 + i * row_h
        shapes.append(ppt_text(sid, f"row {i}", x0, y + 0.1, left_w - 0.2, 0.35, row, font="0F4C81", size=1300, bold=True)); sid += 1
        for j, chip in enumerate(chips[i]):
            shift = chip.startswith(("B. Regional", "A. Parody", "C. Retail", "C. Brand", "D. Fiction"))
            if chip == "-":
                shapes.append(ppt_text(sid, f"dash {i} {j}", x0 + left_w + j * col_w, y + 0.1, 2.0, 0.35, "-", size=1700, bold=True)); sid += 1
            else:
                shapes.append(
                    ppt_shape(
                        sid,
                        f"chip {i} {j}",
                        x0 + left_w + j * col_w,
                        y,
                        2.0,
                        0.42,
                        chip,
                        "F4F0FF" if not shift else "FFFFFF",
                        "B8A7E8" if not shift else "EF4444",
                        font="071B63" if not shift else "EF0000",
                        size=1150,
                        bold=True,
                        dash=shift,
                    )
                )
                sid += 1

    shapes.append(ppt_shape(sid, "legend adaptive", 4.3, 6.95, 0.55, 0.22, "", "F4F0FF", "B8A7E8")); sid += 1
    shapes.append(ppt_text(sid, "legend adaptive text", 4.9, 6.89, 1.25, 0.35, "Adaptive", size=1200, bold=True)); sid += 1
    shapes.append(ppt_shape(sid, "legend shift", 6.35, 6.95, 0.55, 0.22, "", "FFFFFF", "EF4444", dash=True)); sid += 1
    shapes.append(ppt_text(sid, "legend shift text", 6.95, 6.89, 1.0, 0.35, "Shift", size=1200, bold=True)); sid += 1

    slide_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
      {''.join(shapes)}
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sld>"""

    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
  <Override PartName="/ppt/slides/slide1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
</Types>"""
    root_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
</Relationships>"""
    presentation = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:sldIdLst><p:sldId id="256" r:id="rId1"/></p:sldIdLst>
  <p:sldSz cx="12192000" cy="6858000" type="wide"/>
  <p:notesSz cx="6858000" cy="9144000"/>
</p:presentation>"""
    presentation_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide1.xml"/>
</Relationships>"""

    out = OUT / "policy_matrix.pptx"
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", root_rels)
        zf.writestr("ppt/presentation.xml", presentation)
        zf.writestr("ppt/_rels/presentation.xml.rels", presentation_rels)
        zf.writestr("ppt/slides/slide1.xml", slide_xml)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    make_drawio()
    make_pptx()
    print(f"wrote {OUT / 'policy_matrix.drawio'}")
    print(f"wrote {OUT / 'policy_matrix.pptx'}")


if __name__ == "__main__":
    main()
