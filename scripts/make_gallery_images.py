#!/usr/bin/env python3
"""Generate README before/after gallery images.

These are lightweight visual previews for the public README. The "before" side
looks like a rough image-model or hand-drawn sketch; the "after" side previews
the kind of polished editable figure the skill asks an agent to reconstruct.
"""

from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "examples" / "gallery"
W, H = 1280, 720


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/dejavu/DejaVuSans.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


F = {
    "title": font(34, True),
    "h1": font(25, True),
    "h2": font(20, True),
    "body": font(16),
    "small": font(13),
    "tiny": font(11),
}


def new_canvas() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (W, H), "#F8FAFC")
    d = ImageDraw.Draw(img)
    for y in range(H):
        tone = int(248 - y * 8 / H)
        d.line([(0, y), (W, y)], fill=(tone, tone + 2, min(255, tone + 7)))
    return img, d


def round_rect(d: ImageDraw.ImageDraw, box, fill, outline="#CBD5E1", width=2, radius=18):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def centered(d: ImageDraw.ImageDraw, box, text, fill="#071B63", ft=None):
    ft = ft or F["body"]
    bbox = d.multiline_textbbox((0, 0), text, font=ft, spacing=4, align="center")
    x = box[0] + (box[2] - box[0] - (bbox[2] - bbox[0])) / 2
    y = box[1] + (box[3] - box[1] - (bbox[3] - bbox[1])) / 2
    d.multiline_text((x, y), text, font=ft, fill=fill, spacing=4, align="center")


def label(d, x, y, text, color="#071B63", ft=None):
    d.text((x, y), text, fill=color, font=ft or F["body"])


def chip(d, x, y, w, h, text, kind="adaptive", size="body"):
    if kind == "adaptive":
        fill, stroke, color, dash = "#F4F0FF", "#B8A7E8", "#071B63", None
    elif kind == "shift":
        fill, stroke, color, dash = "#FFFFFF", "#EF4444", "#EF0000", (8, 6)
    else:
        fill, stroke, color, dash = "#FFFFFF", "#006DFF", "#006DFF", None
    if dash:
        round_rect(d, (x, y, x + w, y + h), fill, "#EF4444", 1, 9)
        for i in range(x + 3, x + w - 3, 16):
            d.line([(i, y), (min(i + 8, x + w), y)], fill=stroke, width=2)
            d.line([(i, y + h), (min(i + 8, x + w), y + h)], fill=stroke, width=2)
        for i in range(y + 3, y + h - 3, 16):
            d.line([(x, i), (x, min(i + 8, y + h))], fill=stroke, width=2)
            d.line([(x + w, i), (x + w, min(i + 8, y + h))], fill=stroke, width=2)
    else:
        round_rect(d, (x, y, x + w, y + h), fill, stroke, 2, 9)
    centered(d, (x, y, x + w, y + h), text, color, F[size])


def rough_common(title: str, subtitle: str) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img, d = new_canvas()
    round_rect(d, (34, 34, W - 34, H - 34), "#FFFFFF", "#CBD5E1", 2, 26)
    label(d, 70, 58, title, "#0F172A", F["title"])
    label(d, 72, 104, subtitle, "#64748B", F["body"])
    d.line((70, 138, W - 70, 138), fill="#E2E8F0", width=2)
    return img, d


def make_policy_before():
    img, d = rough_common("Image-model sketch: policy matrix", "A plausible GPT-image-2 draft: useful composition, but text and boxes are pixels.")
    x0, y0 = 95, 185
    d.rectangle((x0, y0, W - 95, H - 90), outline="#94A3B8", width=3)
    for j in range(6):
        x = x0 + 210 + j * 150
        d.line((x, y0, x, H - 90), fill="#CBD5E1", width=2)
    for i in range(8):
        y = y0 + 54 + i * 58
        d.line((x0, y, W - 95, y), fill="#CBD5E1", width=2)
    for j, t in enumerate(["Social", "Kids", "Legal", "Brand", "Special"]):
        centered(d, (x0 + 220 + j * 150, y0 + 8, x0 + 350 + j * 150, y0 + 46), t, "#0F172A", F["h2"])
    for i in range(7):
        label(d, x0 + 18, y0 + 68 + i * 58, f"0{i+1}", "#2563EB", F["h1"])
        for j in range(5):
            if (i + j) % 3 != 1:
                d.rounded_rectangle((x0 + 230 + j * 150, y0 + 70 + i * 58, x0 + 335 + j * 150, y0 + 100 + i * 58), radius=8, fill="#EDE9FE", outline="#C4B5FD")
                label(d, x0 + 247 + j * 150, y0 + 75 + i * 58, f"{chr(65+(i+j)%6)} policy", "#312E81", F["tiny"])
    img.save(OUT / "01_policy_matrix_before.png", quality=95)


def make_policy_after():
    img, d = new_canvas()
    label(d, 360, 35, "Scenario x Risk Category Policy Matrix", "#071B63", F["title"])
    label(d, 387, 83, "After reconstruction: editable cells, policy chips, legend, and labels.", "#475569", F["body"])
    chip(d, 425, 122, 78, 28, "", "adaptive")
    label(d, 518, 126, "Adaptive", "#071B63", F["body"])
    chip(d, 610, 122, 78, 28, "", "shift")
    label(d, 703, 126, "Shift", "#071B63", F["body"])
    round_rect(d, (42, 170, W - 42, 650), "#FFFFFF", "#94A3B8", 2, 18)
    x0, y0 = 42, 170
    left, col, row = 245, 190, 62
    for x in [x0 + left + i * col for i in range(6)]:
        d.line((x, y0, x, 650), fill="#CBD5E1", width=2)
    for y in [y0 + 72 + i * row for i in range(8)]:
        d.line((x0, y, W - 42, y), fill="#E2E8F0", width=2)
    headers = ["Mainstream\nSocial", "Protective\nChild-Safe", "Permissive\nLegal-Baseline", "Commercial\nBrand-Safe", "Specialized\nContexts"]
    for j, h in enumerate(headers):
        centered(d, (x0 + left + j * col, y0 + 10, x0 + left + (j + 1) * col, y0 + 64), h, "#071B63", F["h2"])
    rows = [
        ("01", "Nudity & Fetish", "#4F46E5"),
        ("02", "Violence / Hate", "#DC2626"),
        ("03", "Regulated Goods", "#EA580C"),
        ("04", "IP / Brand", "#D97706"),
        ("05", "Culture / Religion", "#16A34A"),
        ("06", "Privacy & PII", "#2563EB"),
        ("07", "Text-in-Image", "#006DFF"),
    ]
    data = [
        [("A. General Safe", "adaptive"), ("B. Family Safe", "adaptive"), ("E. Creative", "adaptive"), ("D. Lingerie", "adaptive"), ("C. Medical", "shift")],
        [("A. Real-world", "adaptive"), ("B. Zero Tol.", "adaptive"), ("E. Legal", "adaptive"), ("D. Fiction", "shift"), ("F. Military", "augment")],
        [("A. Family", "adaptive"), ("D. Minor", "adaptive"), ("B. Regional", "shift"), ("C. Retail", "shift"), ("F. Education", "augment")],
        [("B. Clean", "adaptive"), ("-", "none"), ("A. Parody", "shift"), ("C. Brand", "shift"), ("D. Celebrity", "augment")],
        [("A. Liberal", "adaptive"), ("E. Neutral", "adaptive"), ("G. Med.", "augment"), ("E. Neutral", "adaptive"), ("B. Halal", "shift")],
        [("A. Sharing", "adaptive"), ("B. Privacy", "adaptive"), ("A. Sharing", "adaptive"), ("C. OCR", "shift"), ("D. Listing", "augment")],
        [("A. Basic", "adaptive"), ("D. Kids", "augment"), ("E. News", "augment"), ("B. Anti-Spam", "shift"), ("C. Non-Political", "augment")],
    ]
    for i, (num, name, color) in enumerate(rows):
        y = y0 + 72 + i * row
        label(d, x0 + 30, y + 14, num, color, F["h1"])
        label(d, x0 + 82, y + 19, name, "#071B63", F["body"])
        for j, (text, kind) in enumerate(data[i]):
            if kind == "none":
                centered(d, (x0 + left + j * col, y + 10, x0 + left + (j + 1) * col, y + 44), text, "#071B63", F["h2"])
            else:
                chip(d, x0 + left + j * col + 20, y + 15, col - 40, 32, text, kind, "small")
    img.save(OUT / "01_policy_matrix_after.png", quality=95)


def make_pipeline_before():
    img, d = rough_common("Image-model sketch: training pipeline", "Rough blocks capture intent, but everything needs alignment and editable typography.")
    round_rect(d, (85, 180, 660, 570), "#EFF6FF", "#60A5FA", 3, 20)
    round_rect(d, (720, 180, 1185, 570), "#FAF5FF", "#A78BFA", 3, 20)
    label(d, 170, 205, "A. Data Build", "#1D4ED8", F["h1"])
    label(d, 825, 205, "B. Training", "#6D28D9", F["h1"])
    for i, t in enumerate(["images", "VLM vote", "metadata", "rules", "labels"]):
        round_rect(d, (125 + i * 100, 290, 200 + i * 100, 360), "#FFFFFF", "#93C5FD", 2, 14)
        centered(d, (125 + i * 100, 290, 200 + i * 100, 360), t, "#1E3A8A", F["small"])
        if i < 4:
            d.line((205 + i * 100, 325, 220 + i * 100, 325), fill="#111827", width=3)
    for i, t in enumerate(["RP-SFT", "BP-Adapt", "Policy-aware\nmodel"]):
        round_rect(d, (780, 285 + i * 82, 1090, 345 + i * 82), "#FFFFFF", "#C4B5FD", 2, 14)
        centered(d, (780, 285 + i * 82, 1090, 345 + i * 82), t, "#4C1D95", F["h2"])
    img.save(OUT / "02_training_pipeline_before.png", quality=95)


def make_pipeline_after():
    img, d = new_canvas()
    round_rect(d, (42, 42, 730, 595), "#FFFFFF", "#2563EB", 2, 18)
    round_rect(d, (785, 42, 1238, 595), "#FFFFFF", "#7C3AED", 2, 18)
    label(d, 245, 64, "A. Benchmark Construction", "#164E9E", F["title"])
    label(d, 875, 64, "B. Two-Stage Training", "#5B21B6", F["title"])
    steps = ["1 Image\ncollection", "2 VLM\nannotation", "3 Majority\nvote", "4 Rule\nlabeling"]
    for i, t in enumerate(steps):
        x = 85 + i * 155
        d.ellipse((x, 123, x + 42, 165), fill="#2563EB")
        centered(d, (x, 123, x + 42, 165), str(i + 1), "#FFFFFF", F["h2"])
        label(d, x + 50, 132, t[2:], "#0F172A", F["body"])
        if i < 3:
            d.line((x + 130, 145, x + 150, 145), fill="#111827", width=3)
    for i, color in enumerate(["#DBEAFE", "#DCFCE7", "#FFEDD5"]):
        round_rect(d, (105, 230 + i * 86, 285, 292 + i * 86), color, "#94A3B8", 2, 14)
        centered(d, (105, 230 + i * 86, 285, 292 + i * 86), f"VLM-{i+1}\nannotator", "#071B63", F["body"])
    round_rect(d, (365, 245, 565, 482), "#F8FAFC", "#94A3B8", 2, 14)
    for i, t in enumerate(["nudity 2/3", "weapon 0/3", "logo 1/3", "hate text 0/3", "license 2/3"]):
        label(d, 388, 272 + i * 36, t, "#071B63", F["body"])
    round_rect(d, (585, 250, 695, 478), "#ECFDF5", "#22C55E", 2, 14)
    for i, t in enumerate(["01", "02", "03", "04", "05", "06", "07"]):
        chip(d, 606, 270 + i * 27, 66, 20, t, "adaptive", "tiny")
    round_rect(d, (820, 120, 1205, 290), "#FFFFFF", "#A78BFA", 2, 18)
    label(d, 935, 142, "Stage 1: RP-SFT", "#5B21B6", F["h1"])
    chip(d, 855, 205, 56, 28, "01", "adaptive", "small")
    chip(d, 920, 205, 56, 28, "03", "adaptive", "small")
    chip(d, 985, 205, 56, 28, "07", "adaptive", "small")
    d.line((1055, 219, 1110, 219), fill="#111827", width=3)
    round_rect(d, (1120, 180, 1175, 258), "#F5F3FF", "#7C3AED", 2, 15)
    centered(d, (1120, 180, 1175, 258), "VLM", "#4C1D95", F["body"])
    round_rect(d, (820, 330, 1205, 535), "#FFFFFF", "#A78BFA", 2, 18)
    label(d, 915, 352, "Stage 2: BP-Adapt", "#5B21B6", F["h1"])
    round_rect(d, (865, 412, 980, 470), "#F8FAFC", "#CBD5E1", 2, 12)
    centered(d, (865, 412, 980, 470), "Policy A", "#071B63", F["body"])
    round_rect(d, (865, 482, 980, 540), "#F8FAFC", "#CBD5E1", 2, 12)
    centered(d, (865, 482, 980, 540), "Policy B", "#071B63", F["body"])
    d.line((990, 441, 1035, 441), fill="#111827", width=3)
    d.line((990, 511, 1035, 511), fill="#111827", width=3)
    round_rect(d, (1045, 404, 1165, 455), "#ECFDF5", "#22C55E", 2, 12)
    centered(d, (1045, 404, 1165, 455), "SAFE\n(false)", "#15803D", F["h2"])
    round_rect(d, (1045, 477, 1165, 528), "#FEF2F2", "#EF4444", 2, 12)
    centered(d, (1045, 477, 1165, 528), "UNSAFE\n(true | c)", "#DC2626", F["h2"])
    round_rect(d, (70, 625, 1210, 690), "#FFFBEB", "#F59E0B", 2, 14)
    centered(d, (70, 625, 1210, 690), "After reconstruction: aligned panels, editable text, reusable icons/shapes, and publication-ready spacing.", "#071B63", F["body"])
    img.save(OUT / "02_training_pipeline_after.png", quality=95)


def make_case_before():
    img, d = rough_common("Image-model sketch: qualitative policy flip", "Sketch asks for one image, two policies, and model outputs; editable version makes the contrast precise.")
    round_rect(d, (90, 180, 500, 545), "#E0F2FE", "#38BDF8", 3, 18)
    centered(d, (90, 180, 500, 545), "image\nplaceholder", "#0369A1", F["h1"])
    for i, color in enumerate(["#DCFCE7", "#FEE2E2"]):
        x = 560 + i * 310
        round_rect(d, (x, 190, x + 260, 375), color, "#94A3B8", 3, 18)
        centered(d, (x, 200, x + 260, 290), f"Policy {chr(65+i)}\ntext text text", "#071B63", F["h2"])
        centered(d, (x, 305, x + 260, 365), "model: true/false", "#111827", F["body"])
    d.line((500, 360, 560, 280), fill="#111827", width=4)
    d.line((500, 360, 870, 280), fill="#111827", width=4)
    img.save(OUT / "03_qualitative_case_before.png", quality=95)


def make_case_after():
    img, d = new_canvas()
    label(d, 310, 40, "Qualitative Policy Flip: Same Image, Different Policy", "#071B63", F["title"])
    label(d, 390, 88, "After reconstruction: policy cards and prediction table are editable objects.", "#475569", F["body"])
    round_rect(d, (65, 135, 485, 570), "#FFFFFF", "#CBD5E1", 2, 22)
    round_rect(d, (105, 180, 445, 455), "#DBEAFE", "#60A5FA", 2, 18)
    d.ellipse((215, 250, 335, 370), fill="#93C5FD", outline="#2563EB", width=3)
    centered(d, (105, 180, 445, 455), "Reference\nimage", "#1D4ED8", F["h1"])
    label(d, 135, 492, "One image can be acceptable or blocked\nunder different deployment policies.", "#334155", F["body"])
    cards = [
        ("Policy A: General Safe", "ALLOWED", "#ECFDF5", "#22C55E", "false"),
        ("Policy E: Legal Baseline", "NOT ALLOWED", "#FEF2F2", "#EF4444", "true | 01"),
    ]
    for i, (title, badge, fill, stroke, output) in enumerate(cards):
        x = 535 + i * 350
        round_rect(d, (x, 145, x + 315, 400), "#FFFFFF", stroke, 2, 18)
        label(d, x + 24, 170, title, "#071B63", F["h2"])
        round_rect(d, (x + 24, 215, x + 291, 300), fill, stroke, 2, 12)
        centered(d, (x + 24, 215, x + 291, 300), badge, "#15803D" if output == "false" else "#DC2626", F["h1"])
        label(d, x + 26, 322, "Policy text is editable and can be\nexpanded, shortened, or replaced.", "#475569", F["small"])
        round_rect(d, (x, 435, x + 315, 570), "#F8FAFC", "#CBD5E1", 2, 16)
        label(d, x + 24, 458, "Model output", "#071B63", F["h2"])
        chip(d, x + 24, 502, 160, 40, output, "augment" if output == "false" else "shift", "body")
    d.line((485, 350, 535, 270), fill="#22C55E", width=4)
    d.line((485, 350, 885, 270), fill="#EF4444", width=4)
    round_rect(d, (1050, 190, 1215, 535), "#FFFFFF", "#94A3B8", 2, 18)
    label(d, 1085, 225, "Other models", "#071B63", F["h2"])
    for i, t in enumerate(["miss flip", "over-block", "invalid"]):
        round_rect(d, (1082, 285 + i * 70, 1185, 330 + i * 70), "#F1F5F9", "#CBD5E1", 2, 9)
        centered(d, (1082, 285 + i * 70, 1185, 330 + i * 70), t, "#64748B", F["small"])
    img.save(OUT / "03_qualitative_case_after.png", quality=95)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    make_policy_before()
    make_policy_after()
    make_pipeline_before()
    make_pipeline_after()
    make_case_before()
    make_case_after()
    print(f"wrote gallery images to {OUT}")


if __name__ == "__main__":
    main()
