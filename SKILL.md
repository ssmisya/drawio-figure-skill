---
name: drawio-figure
description: Create or edit editable draw.io/diagrams.net figures and editable PPTX slides by visually reconstructing PNG/screenshots into editable layout objects, generating .drawio XML or .pptx OpenXML, searching for and embedding open-source SVG icons when needed, drawing editable text boxes/panels/arrows/tables/color blocks, and reading/updating/uploading Google Drive artifacts through rclone. Use when the user asks for draw.io, drawio, diagrams.net, PowerPoint/PPTX, editable architecture or paper figures, Google Drive drawio links, icon-complete figure reconstruction, or visual reconstruction from a PNG into editable diagram or slide objects.
---

# Draw.io / PPTX Figure Generation

Use this skill when the requested output should be an editable draw.io diagram or editable PowerPoint slide, not only a flat PNG.

## Core Principle

Do not claim a flat PNG has been automatically converted into fully editable layers. The correct approach is visual reconstruction:

- Read or infer the target layout.
- Generate a `.drawio` XML file or `.pptx` OpenXML package programmatically.
- Represent text, boxes, arrows, tables, color bands, and labels as editable objects (`mxCell` for draw.io; PowerPoint shapes/text boxes for PPTX).
- Embed original photos/screenshots only when they are inherently raster content.
- For semantic icons, search/download suitable open-source SVG icons and embed them as movable/scalable image cells or slide images.
- Export PNG/SVG/PDF only as preview artifacts.

Images embedded in draw.io/PPTX remain movable/scalable but their internal pixels are not editable.

## Output Format Selection

- If the user asks for draw.io, diagrams.net, pages, or Google Drive `.drawio` edits, produce or update `.drawio`.
- If the user asks for PPTX, PowerPoint, slides, or "PNG to PPTX", produce `.pptx`.
- If the user asks to upload/sync to Google Drive, generate and validate locally first, upload with `rclone copyto`, then read back or list the target to verify.
- If both `.drawio` and `.pptx` are requested, reuse the same layout analysis and generate separate editable artifacts.

## Image-to-Draw.io Reconstruction Workflow

Use this when the user provides a screenshot/PNG and asks to convert it into editable draw.io.

1. Inspect the reference image and identify layout primitives: canvas size, panels, grid/table geometry, row/column labels, chips/buttons, arrows, separators, colors, shadows, and icons.
2. Rebuild primitives as native draw.io `mxCell` objects. Keep text, chips, boxes, arrows, and table cells editable; avoid flattening them into one background image.
3. For icons such as shields, users, locks, globes, briefcases, scales, hands, flasks, text blocks, robots, brains, databases, documents, and gears, search for real SVG icons from license-clear open-source icon sets. Prefer a single icon family for visual consistency.
4. Embed icons as SVG image cells. They will be movable/scalable in draw.io. Their internal paths are not normally editable unless explicitly recreated as native draw.io shapes.
5. Validate the `.drawio` XML. If a Google Drive file is involved, back up the remote file, replace only the requested page(s), upload, and read back to verify page count and icon count.

Recommended icon sources:

- Tabler Icons: MIT, consistent outline style, good default for paper figures. Raw SVG pattern: `https://raw.githubusercontent.com/tabler/tabler-icons/main/icons/outline/<name>.svg`.
- Lucide: ISC, consistent outline style, useful fallback.
- Bootstrap Icons: MIT, useful fallback.
- Material Symbols / Material Icons: Apache 2.0, useful when a specific concept is missing elsewhere.

Avoid random web icons unless the license is clear for the intended paper/project use.

## Image-to-PPTX Reconstruction Workflow

Use this when the user provides a screenshot/PNG and asks to convert it into editable PPTX/PowerPoint.

1. Inspect the reference image and identify the same primitives used for draw.io: canvas size, panels, grid/table geometry, chips/buttons, arrows, separators, colors, shadows, and icons.
2. Rebuild visible primitives as editable PowerPoint shapes and text boxes. Do not make the whole slide one background image unless the user explicitly accepts a raster-only fallback.
3. Prefer `python-pptx` if available. If not available or it cannot express the required layout, generate the PPTX OpenXML package directly as a zip with `[Content_Types].xml`, relationships, slide XML, media, and theme parts.
4. Use editable rectangles, rounded rectangles, lines, connectors, and grouped-looking layouts. For complex icons, embed SVG/PNG icons as separate image objects; for high-fidelity icon reconstruction, search license-clear SVG sources first.
5. Validate the generated PPTX with `unzip -t file.pptx`. If a renderer is available, export or open a preview for visual spot check; otherwise inspect key slide XML and media references.
6. Be explicit about which parts are editable and which parts are embedded images.

## Preferred Outputs

For paper figures, produce at least:

- `figure.drawio`: editable source when draw.io is requested.
- `figure.pptx`: editable PowerPoint source when PPTX is requested.
- `figure.png` or `figure.svg`: rendered preview when a renderer is available.

Keep `.drawio` self-contained by embedding images as base64 unless the user explicitly wants external links. Keep `.pptx` self-contained by embedding required images/icons under `ppt/media/`.

## Draw.io XML Patterns

Generate plain XML that draw.io can open:

```xml
<mxfile host="app.diagrams.net">
  <diagram name="Page-1">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1200" pageHeight="800" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- cells go here -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

Editable rounded text box:

```xml
<mxCell id="box1" value="Policy-conditioned guardrail"
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F1F5FA;strokeColor=#1F4E79;fontSize=12;"
  vertex="1" parent="1">
  <mxGeometry x="468" y="238" width="284" height="44" as="geometry" />
</mxCell>
```

Editable arrow:

```xml
<mxCell id="arrow1" value=""
  style="endArrow=classic;html=1;rounded=0;strokeColor=#666666;strokeWidth=1.6;"
  edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="720" y="306" as="sourcePoint" />
    <mxPoint x="804" y="306" as="targetPoint" />
  </mxGeometry>
</mxCell>
```

Embedded image:

```xml
<mxCell id="img1" value=""
  style="shape=image;html=1;image=data:image/jpeg;base64,..."
  vertex="1" parent="1">
  <mxGeometry x="80" y="120" width="180" height="130" as="geometry" />
</mxCell>
```

## Python Generation Pattern

Use Python for deterministic layout construction. Always escape XML text.

```python
import base64
import html
import io
import re
import urllib.parse
from pathlib import Path
from PIL import Image

def esc(text):
    return html.escape("" if text is None else str(text), quote=True)

def rect(cell_id, x, y, w, h, text, fill="#F1F5FA", stroke="#1F4E79"):
    return f'''<mxCell id="{cell_id}" value="{esc(text)}"
  style="rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};fontSize=12;"
  vertex="1" parent="1">
  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />
</mxCell>'''

def load_svg(path, color="#071B63"):
    svg = Path(path).read_text()
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S).strip()
    svg = svg.replace('stroke="currentColor"', f'stroke="{color}"')
    return svg

def svg_icon_cell(cell_id, svg_path, x, y, w, h, color="#071B63"):
    svg = load_svg(svg_path, color)
    data = urllib.parse.quote(svg, safe=",:/=")
    return f'''<mxCell id="{cell_id}" value=""
  style="shape=image;html=1;imageAspect=1;aspect=fixed;image=data:image/svg+xml,{data};"
  vertex="1" parent="1">
  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />
</mxCell>'''
```

For SVG icons embedded in draw.io style strings, prefer URL-encoded SVG data URIs, not base64. The `;base64` substring can be interpreted as a style-property separator and make the icon render as a broken image.

## Export Preview

If installed:

```bash
drawio --export --format png --scale 2 --output figure.png figure.drawio
drawio --export --format svg --output figure.svg figure.drawio
```

If `drawio` is unavailable, still provide `.drawio`; the user can open it in diagrams.net.

## Google Drive Workflow

Use this when the user gives a Google Drive `.drawio` link or asks to upload/edit a Drive-hosted artifact.

Assumptions:

- `rclone` is installed.
- A Google Drive remote such as `gdrive:` has been configured.
- If your network requires a proxy, set it before running `rclone`.

Safety rules:

- First read and back up the Drive file locally.
- Never overwrite the Drive file until the local artifact has been generated and validated.
- When replacing a draw.io page, preserve all other pages from the downloaded backup and replace only the requested `<diagram>` element.
- If doing a write-permission probe, create a separate probe file; do not modify the target file.
- Write back with `rclone copyto local_artifact gdrive:path/to/target`.
- Read back or list the target after upload to verify.

Draw.io validation:

```bash
python - <<'PY'
from pathlib import Path
import xml.etree.ElementTree as ET
p = Path('figure.drawio')
root = ET.parse(p).getroot()
assert root.tag == 'mxfile'
print('drawio_xml_ok', p, p.stat().st_size, 'pages=', len(root.findall('diagram')))
PY
```

PPTX validation and upload:

```bash
unzip -t figure.pptx
rclone copyto figure.pptx gdrive:figure.pptx
rclone copyto gdrive:figure.pptx /tmp/figure.after.pptx
unzip -t /tmp/figure.after.pptx
```

## Quality Checklist

- Text, boxes, arrows, cards, chips, and table cells are editable objects.
- Raster images are embedded separately and can be moved/scaled.
- SVG icons are searched from license-clear sources and embedded as separate objects.
- Labels do not become part of a bitmap unless unavoidable.
- `.drawio` files open without XML errors.
- `.pptx` files pass `unzip -t` and all referenced media files exist.
- Preview export matches the intended layout when a renderer is available.
- Any raster-only part is explicitly disclosed.
- Google Drive edits/uploads are backup-first and verify-after-write.
