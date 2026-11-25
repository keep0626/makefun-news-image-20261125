#!/usr/bin/env python3
"""Draw the 25 November 2026 world-news front page (1024x1024, deterministic).

Reads stories.json next to this file and writes entry.png next to it.
No randomness, no clock, no network: the same input always gives the
same bytes.
"""

import json
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
MARGIN = 12
CW = W - 2 * MARGIN  # 1000

PAPER = (247, 242, 231)
INK = (20, 20, 20)
RED = (185, 28, 28)
DARKRED = (140, 20, 20)
GREY = (90, 88, 82)
LIGHTGREY = (150, 146, 138)
NAVY = (23, 42, 74)
TEAL = (15, 118, 110)
GOLD = (180, 130, 30)
SEA = (207, 224, 234)
LAND = (232, 220, 192)
RULE = (60, 58, 52)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    for cand in (name, "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(os.path.join(FONT_DIR, cand), size)
        except OSError:
            continue
    return ImageFont.load_default()


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SERIF_I = lambda s: font("DejaVuSerif-Italic.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill=INK, leading=None,
                 max_lines=None, align="left"):
    lines = wrap(draw, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    lh = leading or int(fnt.size * 1.18)
    for ln in lines:
        if align == "center":
            lx = x + (max_w - draw.textlength(ln, font=fnt)) / 2
        else:
            lx = x
        draw.text((lx, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def fit_font(draw, text, path, start, max_w):
    size = start
    while size > 10:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 2
    return font(path, size)


# ---------------------------------------------------------------- pictures

def pic_rocket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    for sx, sy in [(18, 12), (52, 30), (90, 10), (140, 26), (190, 12),
                   (240, 34), (280, 14), (40, 55), (120, 48), (210, 55),
                   (270, 60), (160, 8), (300, 44)]:
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(255, 255, 255))
    # space station ring
    d.ellipse([x + w - 78, y + 8, x + w - 8, y + 34], outline=(255, 255, 255),
              width=3)
    d.rectangle([x + w - 62, y + 18, x + w - 24, y + 24], fill=(255, 255, 255))
    # rocket body
    cx = x + w // 2 - 30
    d.polygon([(cx + 18, y + 22), (cx + 30, y + 40), (cx + 6, y + 40)],
              fill=RED)
    d.rectangle([cx + 6, y + 40, cx + 30, y + 92], fill=(245, 245, 245))
    d.ellipse([cx + 12, y + 52, cx + 24, y + 64], fill=(140, 200, 235))
    d.polygon([(cx + 6, y + 80), (cx - 6, y + 98), (cx + 6, y + 92)],
              fill=RED)
    d.polygon([(cx + 30, y + 80), (cx + 42, y + 98), (cx + 30, y + 92)],
              fill=RED)
    d.polygon([(cx + 12, y + 92), (cx + 24, y + 92), (cx + 18, y + h - 4)],
              fill=(255, 160, 40))
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(90, 110, 60))
    d.text((x + 8, y + h - 24), "SHENZHOU-24", font=SANS_B(11),
           fill=(255, 255, 255))


def pic_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=1)
    for gy in range(4):
        yy = y + 14 + gy * 22
        d.line([x + 34, yy, x + w - 8, yy], fill=(220, 218, 210), width=1)
    d.line([x + 34, y + 12, x + 34, y + h - 16], fill=INK, width=2)
    d.line([x + 34, y + h - 16, x + w - 8, y + h - 16], fill=INK, width=2)
    pts = [(40, 26), (90, 34), (140, 44), (190, 58), (240, 72), (268, 80)]
    pts = [(x + px, y + py) for px, py in pts]
    d.line(pts, fill=RED, width=4)
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED)
    d.text((x + 40, y + h - 14), "KOSPI -5.3%   TAIWAN -5.1%   NIKKEI -2.9%",
           font=SANS_B(10), fill=RED)


def pic_port(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(186, 214, 235))
    d.rectangle([x, y + h - 34, x + w, y + h], fill=(28, 80, 130))
    # crane
    d.line([x + 36, y + 12, x + 36, y + h - 34], fill=(40, 40, 40), width=5)
    d.line([x + 36, y + 16, x + w - 60, y + 16], fill=(40, 40, 40), width=4)
    d.line([x + w - 60, y + 16, x + w - 60, y + 44], fill=(40, 40, 40),
           width=3)
    d.rectangle([x + w - 72, y + 44, x + w - 48, y + 60], fill=RED)
    # ship
    d.polygon([(x + 90, y + h - 62), (x + 270, y + h - 62),
               (x + 252, y + h - 34), (x + 108, y + h - 34)], fill=(60, 60, 60))
    for i, col in enumerate([RED, GOLD, TEAL, RED]):
        d.rectangle([x + 108 + i * 34, y + h - 84, x + 138 + i * 34,
                     y + h - 62], fill=col)
    d.rectangle([x + 250, y + h - 92, x + 272, y + h - 62], fill=(240, 240, 240))
    # warning triangle
    d.polygon([(x + w - 44, y + 8), (x + w - 14, y + 52), (x + w - 74, y + 52)],
              fill=(255, 200, 0))
    d.text((x + w - 42, y + 26), "!", font=SANS_B(20), fill=INK)
    d.text((x + 8, y + 6), "JEDDAH · RED SEA", font=SANS_B(11), fill=INK)


def pic_ship(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(186, 214, 235))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(28, 80, 130))
    d.ellipse([x + 30, y + 6, x + 52, y + 22], fill=(255, 255, 255))
    d.ellipse([x + 60, y + 12, x + 76, y + 24], fill=(255, 255, 255))
    d.polygon([(x + 20, y + h - 44), (x + w - 20, y + h - 44),
               (x + w - 44, y + h - 26), (x + 44, y + h - 26)],
              fill=(70, 70, 70))
    d.rectangle([x + 150, y + h - 66, x + 210, y + h - 44], fill=(220, 220, 220))
    d.rectangle([x + 160, y + h - 60, x + 170, y + h - 50], fill=NAVY)
    d.rectangle([x + 180, y + h - 60, x + 190, y + h - 50], fill=NAVY)
    d.line([x + 120, y + 8, x + 120, y + h - 44], fill=INK, width=2)
    d.polygon([(x + 120, y + 8), (x + 148, y + 16), (x + 120, y + 24)],
              fill=RED)


def pic_skyline(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 225, 190))
    d.ellipse([x + w - 52, y + 6, x + w - 12, y + 46], fill=(255, 120, 40))
    base = y + h
    for bx, bw, bh in [(8, 34, 44), (48, 26, 62), (80, 30, 52), (116, 22, 74),
                       (144, 30, 46), (180, 26, 58), (212, 30, 40),
                       (248, 26, 54), (280, 24, 36)]:
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(70, 70, 78))
        for wy in range(base - bh + 6, base - 4, 10):
            for wx in range(x + bx + 5, x + bx + bw - 4, 9):
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 220, 120))
    # Oriental Pearl-style tower
    tx = x + 138
    d.polygon([(tx, y + 4), (tx + 10, y + 4), (tx + 5, base)], fill=RED)
    d.ellipse([tx - 6, y + 26, tx + 16, y + 40], fill=RED)
    d.ellipse([tx - 3, y + 52, tx + 13, y + 64], fill=RED)


def pic_court(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 236, 226))
    d.polygon([(x + 40, y + 6), (x + w - 40, y + 6), (x + w // 2, y + 24)],
              fill=NAVY)
    d.rectangle([x + 30, y + 24, x + w - 30, y + 30], fill=NAVY)
    for i in range(4):
        cx = x + 44 + i * 64
        d.rectangle([cx, y + 30, cx + 24, y + h - 8], fill=(255, 255, 255),
                    outline=RULE)
        d.rectangle([cx - 3, y + 30, cx + 27, y + 34], fill=(220, 220, 220),
                    outline=RULE)
    d.rectangle([x + 30, y + h - 8, x + w - 30, y + h - 3], fill=NAVY)
    d.ellipse([x + w // 2 - 11, y + 32, x + w // 2 + 11, y + 46],
              outline=GOLD, width=3)


def pic_medal(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(23, 42, 74))
    d.polygon([(x + w // 2 - 46, y + 4), (x + w // 2 - 12, y + 4),
               (x + w // 2 - 8, y + 40), (x + w // 2 - 42, y + 40)],
              fill=RED)
    d.polygon([(x + w // 2 + 12, y + 4), (x + w // 2 + 46, y + 4),
               (x + w // 2 + 42, y + 40), (x + w // 2 + 8, y + 40)],
              fill=(255, 255, 255))
    cx, cy = x + w // 2, y + h - 26
    d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=GOLD,
              outline=(140, 100, 20), width=2)
    d.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], outline=(140, 100, 20),
              width=2)
    d.text((cx - 7, cy - 11), "★", font=SANS_B(20), fill=(140, 100, 20))


def pic_shield(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(220, 228, 235))
    cx = x + w // 2
    d.polygon([(cx - 58, y + 6), (cx + 58, y + 6), (cx + 58, y + 34),
               (cx, y + h - 6), (cx - 58, y + 34)], fill=NAVY)
    d.polygon([(cx - 58, y + 6), (cx + 58, y + 6), (cx + 58, y + 34),
               (cx, y + h - 6), (cx - 58, y + 34)], outline=(255, 255, 255),
              width=2)
    d.line([(cx + 8, y + 14), (cx - 6, y + 34), (cx + 10, y + 50),
            (cx - 4, y + h - 16)], fill=(255, 220, 0), width=3)
    d.text((cx - 26, y + 22), "CIA", font=SANS_B(16), fill=(255, 255, 255))


def pic_fire(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 40, 48))
    d.ellipse([x + 30, y + 6, x + 58, y + 26], fill=(120, 120, 125))
    d.ellipse([x + 70, y + 2, x + 92, y + 18], fill=(140, 140, 145))
    bx, bw = x + 60, 190
    d.rectangle([bx, y + 22, bx + bw, y + h], fill=(90, 88, 84))
    for r in range(2):
        for c in range(8):
            wx, wy = bx + 10 + c * 22, y + 28 + r * 12
            lit = (r == 0 and c in (3, 4)) or (r == 1 and c == 4)
            d.rectangle([wx, wy, wx + 12, wy + 8],
                        fill=(255, 160, 40) if lit else (40, 40, 48))
    # flames stay inside the panel
    for fx, fh in [(150, 18), (168, 20), (186, 16)]:
        d.polygon([(x + fx, y + 22), (x + fx + 8, y + 22 - fh),
                   (x + fx + 16, y + 22)], fill=(255, 120, 20))


ART = {"rocket": pic_rocket, "chart": pic_chart, "port": pic_port,
       "ship": pic_ship, "skyline": pic_skyline, "court": pic_court,
       "medal": pic_medal, "shield": pic_shield, "fire": pic_fire}

# ---------------------------------------------------------------- world map

CONTINENTS = {
    "namerica": [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80),
                 (-85, 70), (-75, 62), (-60, 60), (-55, 47), (-70, 42),
                 (-75, 35), (-80, 26), (-90, 21), (-97, 16), (-105, 20),
                 (-115, 28), (-125, 40), (-125, 49), (-140, 60),
                 (-155, 58), (-165, 60)],
    "samerica": [(-80, 10), (-75, 5), (-60, 0), (-50, -5), (-35, -8),
                 (-40, -20), (-48, -28), (-58, -38), (-65, -45),
                 (-70, -52), (-73, -40), (-70, -20), (-80, -5), (-80, 5)],
    "europe": [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57),
               (18, 56), (21, 55), (28, 60), (30, 70), (40, 68), (45, 60),
               (40, 50), (30, 45), (28, 40), (23, 36), (19, 40), (12, 44),
               (8, 44), (3, 42), (-2, 37)],
    "africa": [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31),
               (35, 28), (43, 12), (51, 10), (48, 0), (40, -10), (35, -20),
               (30, -30), (20, -35), (15, -30), (12, -18), (9, -5), (9, 4),
               (-8, 5), (-15, 10)],
    "asia": [(40, 70), (50, 72), (65, 72), (75, 73), (90, 75), (110, 76),
             (130, 72), (150, 70), (170, 66), (178, 65), (170, 60),
             (160, 55), (145, 45), (140, 40), (130, 35), (122, 30),
             (115, 22), (108, 18), (105, 8), (100, 5), (95, 10), (90, 20),
             (85, 20), (80, 8), (75, 8), (70, 20), (65, 25), (60, 25),
             (55, 28), (50, 30), (45, 40), (40, 55), (40, 65)],
    "oceania": [(113, -22), (114, -30), (120, -34), (130, -32), (140, -38),
                (150, -37), (153, -27), (146, -19), (142, -11), (135, -12),
                (130, -13), (122, -17), (115, -20)],
    "nz": [(167, -45), (174, -41), (178, -38), (174, -35), (167, -38)],
}

PIN_OFFSET = {7: (-9, -7), 8: (9, 7)}


def draw_map(d, x, y, w, h, stories):
    d.rectangle([x, y, x + w, y + h], fill=SEA, outline=RULE, width=1)
    for pts in CONTINENTS.values():
        xy = [(x + (lon + 180) / 360 * w, y + (90 - lat) / 150 * h)
              for lon, lat in pts]
        d.polygon(xy, fill=LAND, outline=(180, 168, 140))
    for s in stories:
        px = x + (s["lon"] + 180) / 360 * w
        py = y + (90 - s["lat"]) / 150 * h
        dx, dy = PIN_OFFSET.get(s["n"], (0, 0))
        px, py = px + dx, py + dy
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                  outline=(255, 255, 255), width=1)
        t = str(s["n"])
        tw = d.textlength(t, font=SANS_B(10))
        d.text((px - tw / 2, py - 7), t, font=SANS_B(10),
               fill=(255, 255, 255))
    d.text((x + 6, y + h - 16), "WHERE THE PICTURED STORIES HAPPENED",
           font=SANS_B(9), fill=INK)


# ---------------------------------------------------------------- page

REGION_COLORS = {"ASIA": (185, 28, 28), "MIDDLE EAST": (194, 65, 12),
                 "EUROPE": (29, 78, 216), "AMERICAS": (15, 118, 110),
                 "AFRICA": (161, 98, 7), "OCEANIA": (109, 40, 217),
                 "GLOBAL": (71, 85, 105)}


def render():
    with open(os.path.join(HERE, "stories.json"), encoding="utf-8") as f:
        data = json.load(f)

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 8

    # kicker
    d.text(((W - d.textlength(data["kicker"], font=SANS_B(14))) / 2, y),
           data["kicker"], font=SANS_B(14), fill=RED)
    y += 22

    # masthead: the date is the biggest element
    f_date = fit_font(d, data["date"], "DejaVuSerif-Bold.ttf", 72, CW)
    tw = d.textlength(data["date"], font=f_date)
    d.text(((W - tw) / 2, y), data["date"], font=f_date, fill=INK)
    y += f_date.size + 8
    wd = data["weekday"] + "  ·  THE WORLD IN ONE PAGE"
    d.text(((W - d.textlength(wd, font=SANS_B(15))) / 2, y), wd,
           font=SANS_B(15), fill=RED)
    y += 24

    # sub-deck
    y = draw_wrapped(d, MARGIN, y, data["subdeck"], SERIF_I(15), CW,
                     fill=DARKRED, leading=18, align="center")
    y += 6
    d.line([MARGIN, y, W - MARGIN, y], fill=RULE, width=2)
    y += 8

    # region bar
    all_stories = data["leads"] + data["cards"] + data["briefs"]
    counts = {}
    for s in all_stories:
        counts[s["region"]] = counts.get(s["region"], 0) + 1
    order = ["ASIA", "MIDDLE EAST", "EUROPE", "AMERICAS", "AFRICA",
             "OCEANIA", "GLOBAL"]
    total = len(all_stories)
    n_regs = sum(1 for reg in order if counts.get(reg, 0))
    rx = MARGIN
    for reg in order:
        n = counts.get(reg, 0)
        if not n:
            continue
        seg = CW / n_regs
        d.rectangle([rx, y, rx + seg, y + 18], fill=REGION_COLORS[reg])
        label = "%s %d" % (reg, n)
        lw = d.textlength(label, font=SANS_B(11))
        d.text((rx + (seg - lw) / 2, y + 3), label, font=SANS_B(11),
               fill=(255, 255, 255))
        rx += seg
    y += 26

    # numbers strip
    nums = data["numbers"]
    cell = CW / len(nums)
    for i, num in enumerate(nums):
        cx = MARGIN + i * cell
        if i:
            d.line([cx, y, cx, y + 44], fill=LIGHTGREY, width=1)
        f_fig = SANS_B(24)
        fw = d.textlength(num["figure"], font=f_fig)
        d.text((cx + (cell - fw) / 2, y), num["figure"], font=f_fig, fill=RED)
        lab = num["label"]
        lw = d.textlength(lab, font=SANS_B(9))
        d.text((cx + (cell - lw) / 2, y + 28), lab, font=SANS_B(9), fill=GREY)
    y += 48
    d.line([MARGIN, y, W - MARGIN, y], fill=RULE, width=2)
    y += 10

    # three leads
    col_w = (CW - 2 * 16) // 3
    lead_top = y
    lead_bottom = lead_top
    for i, s in enumerate(data["leads"]):
        lx = MARGIN + i * (col_w + 16)
        ART[s["art"]](d, lx, lead_top, col_w, 96)
        ly = lead_top + 102
        num = "%d  " % s["n"]
        d.text((lx, ly), num, font=SANS_B(12), fill=RED)
        tw = d.textlength(num, font=SANS_B(12))
        d.text((lx + tw, ly), s["tag"], font=SANS_B(12), fill=INK)
        ly += 17
        ly = draw_wrapped(d, lx, ly, s["headline"], SERIF_B(20), col_w,
                          leading=23, max_lines=2)
        ly += 3
        ly = draw_wrapped(d, lx, ly, s["deck"], SANS(13), col_w, fill=GREY,
                          leading=16, max_lines=3)
        ly += 4
        badge = s["source"]
        bw = d.textlength(badge, font=SANS_B(10)) + 10
        d.rectangle([lx, ly, lx + bw, ly + 15], fill=NAVY)
        d.text((lx + 5, ly + 2), badge, font=SANS_B(10),
               fill=(255, 255, 255))
        lead_bottom = max(lead_bottom, ly + 15)
    y = lead_bottom + 10
    d.line([MARGIN, y, W - MARGIN, y], fill=RULE, width=1)
    y += 10

    # six picture cards, two rows of three
    card_top = y
    for row in range(2):
        for col in range(3):
            s = data["cards"][row * 3 + col]
            cx = MARGIN + col * (col_w + 16)
            cy = card_top + row * 116
            ART[s["art"]](d, cx, cy, col_w, 48)
            ty = cy + 52
            num = "%d  " % s["n"]
            d.text((cx, ty), num, font=SANS_B(11), fill=RED)
            tw = d.textlength(num, font=SANS_B(11))
            d.text((cx + tw, ty), s["tag"], font=SANS_B(11), fill=INK)
            ty += 15
            ty = draw_wrapped(d, cx, ty, s["headline"], SERIF_B(15), col_w,
                              leading=17, max_lines=2)
            ty += 2
            ty = draw_wrapped(d, cx, ty, s["deck"], SANS(11), col_w,
                              fill=GREY, leading=13, max_lines=1)
    y = card_top + 2 * 116 + 4
    d.line([MARGIN, y, W - MARGIN, y], fill=RULE, width=1)
    y += 8

    # briefs header
    hdr = "ALSO ON WEDNESDAY 25 NOVEMBER"
    d.text((MARGIN, y), hdr, font=SANS_B(13), fill=INK)
    d.line([MARGIN + d.textlength(hdr, font=SANS_B(13)) + 8, y + 7,
            W - MARGIN, y + 7], fill=RULE, width=1)
    y += 22

    # map + numbered briefs
    zone_top = y
    map_w, map_h = 296, 156
    draw_map(d, MARGIN, zone_top, map_w, map_h,
             data["leads"] + data["cards"])
    bx = MARGIN + map_w + 16
    bw = W - MARGIN - bx
    half = (len(data["briefs"]) + 1) // 2
    for ci in range(2):
        col_briefs = data["briefs"][ci * half:(ci + 1) * half]
        col_x = bx + ci * (bw / 2 + 8)
        col_wd = bw / 2 - 8
        by = zone_top
        for b in col_briefs:
            num = "%d " % b["n"]
            d.text((col_x, by), num, font=SANS_B(11), fill=RED)
            nw = d.textlength(num, font=SANS_B(11))
            by = draw_wrapped(d, col_x + nw, by, b["text"], SANS(11),
                              col_wd - nw, leading=12, max_lines=1)
            by += 1
    y = zone_top + map_h + 10
    d.line([MARGIN, y, W - MARGIN, y], fill=RULE, width=1)
    y += 8

    # DATE CHECK box
    box_top = y
    inner = draw_wrapped(d, MARGIN + 10, box_top + 18, data["date_check"],
                         SANS(12), CW - 20, leading=15, max_lines=3)
    box_h = (inner - box_top) + 8
    d.rectangle([MARGIN, box_top, W - MARGIN, box_top + box_h],
                outline=RED, width=2)
    d.text((MARGIN + 10, box_top + 3), "DATE CHECK — WHAT WAS LEFT OUT",
           font=SANS_B(11), fill=RED)
    y = box_top + box_h + 8

    # footer: sources + legend
    foot = ("Sources: Reuters, AP, Xinhua, UNAIDS, Bloomberg, NYT · "
            "CONFIRMED = on the record · REPORTED = as reported · "
            "All 32 stories are from 25 November 2026.")
    y = draw_wrapped(d, MARGIN, y, foot, SANS(10), CW, fill=GREY,
                     leading=13, max_lines=2)

    img.save(os.path.join(HERE, "entry.png"), "PNG", optimize=True)


if __name__ == "__main__":
    render()
    print("wrote entry.png")
