"""Render Power BI canvas backgrounds (1280x720 layout, exported at 2x for sharpness).

Usage:
    python make_backgrounds.py
    python make_backgrounds.py --urban-photo city.jpg --ganga-photo ganga.jpg
"""
import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

S = 2
W, H = 1280, 720
OUT = Path(__file__).parent
FONTS = Path("C:/Windows/Fonts")

PAGE_BG = "#EDF1F6"
CARD = "#FFFFFF"
TEXT = "#1B2A41"
MUTED = "#5B6B7F"
DIVIDER = "#DCE3EC"
SAFFRON, WHITE, GREEN = "#FF9933", "#FFFFFF", "#138808"

PANEL = (12, 80, 200, 628)
KPIS = [(224 + i * 211, 80, 199, 90) for i in range(5)]
CHARTS = [
    (224, 182, 516, 258), (752, 182, 516, 258),
    (224, 452, 340, 256), (576, 452, 340, 256), (928, 452, 340, 256),
]

PAGES = {
    "urban": {
        "file": "urban_cleanliness_background.png",
        "header": ("#0B2545", "#1D4E89"),
        "accent": "#E07A1F",
        "title": "Swachh Bharat: Urban Cleanliness Performance",
        "subtitle": "Swachh Survekshan 2024  |  135 cities with population above 3 lakh  |  22 States/UTs",
        "tag": "DECISION DASHBOARD  |  URBAN CLEANLINESS",
        "kpi_accents": ["#1D4E89", "#138808", "#E07A1F", "#0F7C8C", "#B3261E"],
        "legend_title": "PERFORMANCE BANDS",
        "legend": [
            ("#138808", "Excellent", "≥ 10,000"),
            ("#1D4E89", "Good", "8,000 – 9,999"),
            ("#E07A1F", "Average", "6,000 – 7,999"),
            ("#B3261E", "Critical", "< 6,000"),
        ],
        "source": "Source: Swachh Survekshan, Ministry of Housing & Urban Affairs (MoHUA). Total score combines survey, GFC and ODF certification marks.",
    },
    "ganga": {
        "file": "ganga_water_quality_background.png",
        "header": ("#06324A", "#0E6E8C"),
        "accent": "#2BB3C0",
        "title": "Ganga River Water Quality Assessment",
        "subtitle": "CPCB monitoring  |  66 stations from Gangotri to Diamond Harbour  |  4 States",
        "tag": "DECISION DASHBOARD  |  RIVER HEALTH",
        "kpi_accents": ["#0E6E8C", "#1A936F", "#D97706", "#B3261E", "#13315C"],
        "legend_title": "CPCB BATHING LIMITS (CLASS B)",
        "legend": [
            ("#1A936F", "Dissolved O₂", "≥ 5 mg/L"),
            ("#D97706", "BOD", "≤ 3 mg/L"),
            ("#0E6E8C", "pH", "6.5 – 8.5"),
            ("#B3261E", "Fecal Coliform", "≤ 2,500 /100mL"),
        ],
        "source": "Source: Central Pollution Control Board (CPCB), River Ganga water quality, 2012. Values are annual station means.",
    },
}


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), int(size * S))


def box(x, y, w, h):
    return [x * S, y * S, (x + w) * S, (y + h) * S]


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def horizontal_gradient(w, h, c1, c2):
    a, b = hex_rgb(c1), hex_rgb(c2)
    strip = Image.new("RGB", (w, 1))
    for x in range(w):
        t = x / max(w - 1, 1)
        strip.putpixel((x, 0), tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3)))
    return strip.resize((w, h))


def shadowed_card(canvas, rect, radius=10):
    x, y, w, h = rect
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle(box(x, y + 2, w, h), radius * S, fill=(15, 35, 70, 38))
    shadow = shadow.filter(ImageFilter.GaussianBlur(6 * S))
    canvas.alpha_composite(shadow)
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle(box(x, y, w, h), radius * S, fill=CARD, outline=DIVIDER, width=S)


def wrap(draw, text, fnt, max_w):
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w * S:
            line = trial
        else:
            lines.append(line)
            line = word
    return lines + [line]


def blend_photo(header, photo_path):
    w, h = header.size
    photo = ImageOps.fit(Image.open(photo_path).convert("RGB"), (w, h), Image.LANCZOS)
    photo = ImageOps.grayscale(photo).convert("RGB")
    mask = Image.linear_gradient("L").rotate(90).resize((w, h))
    mask = mask.point(lambda v: int(v * 0.38))
    return Image.composite(photo, header, mask)


def render(key, photo=None):
    cfg = PAGES[key]
    canvas = Image.new("RGBA", (W * S, H * S), PAGE_BG)
    d = ImageDraw.Draw(canvas)

    header = horizontal_gradient(W * S, 68 * S, *cfg["header"])
    if photo:
        header = blend_photo(header, photo)
    canvas.paste(header, (0, 0))
    for i, c in enumerate((SAFFRON, WHITE, GREEN)):
        d.rectangle([i * W * S // 3, 0, (i + 1) * W * S // 3, 4 * S], fill=c)

    d.text((24 * S, 13 * S), cfg["title"], font=font("seguisb.ttf", 22), fill="#FFFFFF")
    d.text((24 * S, 44 * S), cfg["subtitle"], font=font("segoeui.ttf", 11), fill="#C9D6E8")
    tag_font = font("seguisb.ttf", 9)
    tw = d.textlength(cfg["tag"], font=tag_font) / S
    d.rounded_rectangle(box(W - 24 - tw - 20, 24, tw + 20, 22), 11 * S, outline=cfg["accent"], width=S)
    d.text(((W - 24 - tw - 10) * S, 28 * S), cfg["tag"], font=tag_font, fill="#FFFFFF")

    shadowed_card(canvas, PANEL)
    d = ImageDraw.Draw(canvas)
    px, py, pw, ph = PANEL
    d.rectangle(box(px + 16, py + 16, 3, 14), fill=cfg["accent"])
    d.text(((px + 24) * S, (py + 13) * S), "FILTERS", font=font("seguisb.ttf", 11), fill=TEXT)
    d.line(box(px + 16, py + 38, pw - 32, 0), fill=DIVIDER, width=S)

    ly = 492
    d.line(box(px + 16, ly, pw - 32, 0), fill=DIVIDER, width=S)
    d.text(((px + 16) * S, (ly + 10) * S), cfg["legend_title"], font=font("seguisb.ttf", 8.5), fill=MUTED)
    for i, (color, label, value) in enumerate(cfg["legend"]):
        y = ly + 32 + i * 22
        d.ellipse(box(px + 18, y + 3, 9, 9), fill=color)
        d.text(((px + 34) * S, y * S), label, font=font("seguisb.ttf", 9), fill=TEXT)
        d.text(((px + 112) * S, y * S), value, font=font("segoeui.ttf", 9), fill=MUTED)

    src_font = font("segoeui.ttf", 7.5)
    sy = py + ph - 52
    d.line(box(px + 16, sy - 6, pw - 32, 0), fill=DIVIDER, width=S)
    for i, line in enumerate(wrap(d, cfg["source"], src_font, pw - 32)[:4]):
        d.text(((px + 16) * S, (sy + i * 11) * S), line, font=src_font, fill=MUTED)

    for rect, accent in zip(KPIS, cfg["kpi_accents"]):
        shadowed_card(canvas, rect)
        x, y, w, h = rect
        ImageDraw.Draw(canvas).rounded_rectangle(box(x, y, 5, h), 3 * S, fill=accent)

    for rect in CHARTS:
        shadowed_card(canvas, rect)

    out = OUT / cfg["file"]
    canvas.convert("RGB").save(out, optimize=True)
    print(f"saved {out}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--urban-photo")
    ap.add_argument("--ganga-photo")
    args = ap.parse_args()
    render("urban", args.urban_photo)
    render("ganga", args.ganga_photo)
