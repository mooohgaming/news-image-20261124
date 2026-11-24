#!/usr/bin/env python3
"""Draw one newspaper page summing up Tuesday 24 November 2026.

Writes a 1024x1024 PNG to /output/entry.png (or $MAKEFUN_OUTPUT_DIR).
Python standard library only. No network, no clock, no randomness:
two runs produce byte-identical output.
"""

import math
import os
import struct
import zlib

W, H = 1024, 1024

PAPER = (247, 243, 234)
INK = (20, 20, 20)
GREY = (90, 90, 90)
DARKGREY = (58, 58, 58)
RED = (179, 32, 44)
WHITE = (255, 255, 255)
NAVY = (27, 58, 92)
TEAL = (15, 91, 91)
GREEN_D = (30, 77, 43)
GREEN_B = (20, 38, 26)
GOLD = (212, 175, 55)
ORANGE = (232, 116, 30)
YELLOW = (244, 196, 48)
PITCH = (46, 125, 50)
SKY = (120, 160, 200)


# ---------------------------------------------------------------- font
# A 5x7 bitmap font, drawn fresh for this page. '#' is an inked pixel.
FONT = {
    'A': (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    'B': ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    'C': (".####", "#....", "#....", "#....", "#....", "#....", ".####"),
    'D': ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    'E': ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    'F': ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    'G': (".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."),
    'H': ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    'I': ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"),
    'J': ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    'K': ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    'L': ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    'M': ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    'N': ("#...#", "##..#", "##..#", "#.#.#", "#..##", "#..##", "#...#"),
    'O': (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    'P': ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    'Q': (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    'R': ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    'S': (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    'T': ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    'U': ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    'V': ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    'W': ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    'X': ("#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"),
    'Y': ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    'Z': ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    '0': (".###.", "#..##", "#.#.#", "##..#", "#...#", "#...#", ".###."),
    '1': ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
    '2': (".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"),
    '3': ("####.", "....#", "....#", ".###.", "....#", "....#", "####."),
    '4': ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    '5': ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    '6': (".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."),
    '7': ("#####", "....#", "...#.", "...#.", "..#..", "..#..", "..#.."),
    '8': (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    '9': (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
    ' ': (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    '.': (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    ',': (".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."),
    "'": ("..#..", "..#..", "..#..", ".....", ".....", ".....", "....."),
    ':': (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    ';': (".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."),
    '!': ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    '?': (".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."),
    '-': (".....", ".....", ".....", ".###.", ".....", ".....", "....."),
    '(': ("...#.", "..#..", ".#...", ".#...", ".#...", "..#..", "...#."),
    ')': (".#...", "..#..", "...#.", "...#.", "...#.", "..#..", ".#..."),
    '/': ("....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."),
    '&': (".##..", "#..#.", "#..#.", ".#...", "#.#.#", "#..#.", ".##.#"),
    '%': ("##..#", "##.#.", "...#.", "..#..", ".#...", "#.##.", "#..##"),
    '$': ("..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."),
    '+': (".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."),
    '=': (".....", ".....", "#####", ".....", "#####", ".....", "....."),
    '"': (".#.#.", ".#.#.", ".#.#.", ".....", ".....", ".....", "....."),
    '*': (".....", ".#.#.", ".###.", "#####", ".###.", ".#.#.", "....."),
}


def text_width(s, scale, gap=None):
    if gap is None:
        gap = max(1, scale // 3)
    if not s:
        return 0
    return len(s) * (5 * scale + gap) - gap


def wrap_text(s, max_chars):
    """Word-wrap a string into lines of at most max_chars characters."""
    words = s.split(' ')
    lines, cur = [], ''
    for word in words:
        trial = word if not cur else cur + ' ' + word
        if len(trial) <= max_chars:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg * (w * h))

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = c

    def fill_rect(self, x, y, w, h, c):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        for yy in range(y0, y1):
            i = (yy * self.w + x0) * 3
            row = bytes(c) * (x1 - x0)
            self.px[i:i + (x1 - x0) * 3] = row

    def rect(self, x, y, w, h, c, t=1):
        self.fill_rect(x, y, w, t, c)
        self.fill_rect(x, y + h - t, w, t, c)
        self.fill_rect(x, y, t, h, c)
        self.fill_rect(x + w - t, y, t, h, c)

    def line(self, x0, y0, x1, y1, c, t=1):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            for a in range(t):
                for b in range(t):
                    self.set(x0 + a, y0 + b, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, c):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.set(xx, yy, c)

    def triangle(self, pts, c):
        (x0, y0), (x1, y1), (x2, y2) = pts
        ymin, ymax = min(y0, y1, y2), max(y0, y1, y2)
        for yy in range(ymin, ymax + 1):
            xs = []
            for (ax, ay), (bx, by) in (((x0, y0), (x1, y1)),
                                       ((x1, y1), (x2, y2)),
                                       ((x2, y2), (x0, y0))):
                if ay == by:
                    continue
                if min(ay, by) <= yy < max(ay, by) or yy == ymax and yy == max(ay, by):
                    xs.append(ax + (yy - ay) * (bx - ax) / (by - ay))
            if len(xs) >= 2:
                xa, xb = int(min(xs)), int(max(xs))
                for xx in range(xa, xb + 1):
                    self.set(xx, yy, c)

    def text(self, s, x, y, scale, c, align='left'):
        s = s.upper()
        gap = max(1, scale // 3)
        w = text_width(s, scale, gap)
        if align == 'center':
            x -= w // 2
        elif align == 'right':
            x -= w
        cx = x
        for ch in s:
            glyph = FONT.get(ch, FONT[' '])
            for row in range(7):
                bits = glyph[row]
                for col in range(5):
                    if bits[col] == '#':
                        self.fill_rect(cx + col * scale, y + row * scale,
                                       scale, scale, c)
            cx += 5 * scale + gap
        return w


def png_bytes(cv):
    raw = bytearray()
    stride = cv.w * 3
    for y in range(cv.h):
        raw.append(0)
        raw += cv.px[y * stride:(y + 1) * stride]

    def chunk(tag, data):
        out = struct.pack('>I', len(data)) + tag + data
        out += struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)
        return out

    ihdr = struct.pack('>IIBBBBB', cv.w, cv.h, 8, 2, 0, 0, 0)
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr)
            + chunk(b'IDAT', zlib.compress(bytes(raw), 9))
            + chunk(b'IEND', b''))


# ---------------------------------------------------------------- pictures
def pic_strike(cv, x, y, w, h):
    """Zaporizhzhia: night skyline, an explosion burst, smoke."""
    cv.fill_rect(x, y, w, h, NAVY)
    cv.fill_rect(x, y + h - 18, w, 18, (12, 26, 44))
    for bx, bw, bh in ((8, 34, 34), (52, 26, 48), (88, 40, 30),
                       (140, 24, 56), (176, 30, 40), (218, 36, 26),
                       (268, 28, 52), (310, 34, 36), (356, 26, 44),
                       (396, 30, 30), (430, 22, 38)):
        cv.fill_rect(x + bx, y + h - 18 - bh, bw, bh, (10, 22, 40))
        for wy in range(4):
            cv.fill_rect(x + bx + 6, y + h - 18 - bh + 6 + wy * 10, 5, 5,
                         (244, 196, 48))
    cx, cy = x + 330, y + 34
    for r, c in ((26, ORANGE), (18, YELLOW), (10, WHITE)):
        cv.circle(cx, cy, r, c)
    for ang in range(0, 360, 30):
        rad = math.radians(ang)
        cv.line(cx, cy, cx + int(40 * math.cos(rad)),
                cy + int(40 * math.sin(rad)), ORANGE, 3)
    cv.circle(x + 300, y + 18, 12, (120, 120, 120))
    cv.circle(x + 316, y + 10, 9, (150, 150, 150))
    cv.circle(x + 360, y + 14, 10, (120, 120, 120))


def pic_jets(cv, x, y, w, h):
    """Korea: jets over the sea near an island, warning triangle."""
    cv.fill_rect(x, y, w, h, TEAL)
    cv.fill_rect(x, y + h - 26, w, 26, (8, 60, 60))
    for wy in (0, 8, 16):
        for wx in range(0, w, 44):
            cv.line(x + wx, y + h - 22 + wy, x + wx + 22,
                    y + h - 22 + wy, (140, 200, 200), 2)
    cv.triangle([(x + 380, y + h - 26), (x + 420, y + h - 62),
                 (x + 460, y + h - 26)], (24, 80, 40))
    cv.fill_rect(x + 396, y + h - 34, 30, 8, (24, 80, 40))
    for jx, jy, s in ((150, 30, 1.0), (230, 52, 0.7), (300, 22, 0.55)):
        sw, sh = int(46 * s), int(14 * s)
        cv.triangle([(x + jx, y + jy), (x + jx + sw, y + jy + sh // 2),
                     (x + jx, y + jy + sh)], WHITE)
        cv.triangle([(x + jx + sw // 2, y + jy + 2),
                     (x + jx + sw // 2 + 12, y + jy - 8),
                     (x + jx + sw // 2 + 20, y + jy + 4)], WHITE)
    cv.triangle([(x + 60, y + 66), (x + 86, y + 22), (x + 112, y + 66)],
                YELLOW)
    cv.fill_rect(x + 82, y + 66, 8, 4, YELLOW)
    cv.text('!', x + 80, y + 26, 3, INK)


def pic_gaza(cv, x, y, w, h):
    """Gaza: damaged buildings, a smoke plume, dusk sky."""
    cv.fill_rect(x, y, w, h, (96, 84, 78))
    cv.fill_rect(x, y + h - 14, w, 14, (52, 44, 40))
    cv.fill_rect(x + 20, y + 30, 70, h - 44, (70, 62, 56))
    cv.fill_rect(x + 110, y + 48, 60, h - 62, (80, 70, 64))
    cv.line(x + 214, y + 26, x + 238, y + h - 14, (62, 54, 48), 16)
    cv.fill_rect(x + 250, y + 40, 64, h - 54, (70, 62, 56))
    cv.fill_rect(x + 330, y + 56, 56, h - 70, (80, 70, 64))
    cv.fill_rect(x + 404, y + 36, 44, h - 50, (70, 62, 56))
    for wx, wy in ((38, 44), (58, 62), (128, 60), (268, 54), (348, 68),
                   (418, 50)):
        cv.fill_rect(x + wx, y + wy, 10, 8, YELLOW)
    cv.circle(x + 330, y + 26, 16, (150, 140, 132))
    cv.circle(x + 352, y + 14, 12, (170, 160, 150))
    cv.circle(x + 372, y + 26, 10, (150, 140, 132))
    cv.circle(x + 300, y + 12, 9, (170, 160, 150))


def pic_bank(cv, x, y, w, h):
    """Iran: a bank front, a dollar sign crossed out in red."""
    cv.fill_rect(x, y, w, h, GREEN_D)
    cv.fill_rect(x + 150, y + 58, 170, 8, GOLD)
    cv.triangle([(x + 140, y + 58), (x + 235, y + 18),
                 (x + 330, y + 58)], GOLD)
    for cx in (165, 205, 245, 285):
        cv.fill_rect(x + cx, y + 66, 12, h - 66 - 8, GOLD)
    cv.fill_rect(x + 150, y + h - 8, 170, 8, GOLD)
    cx, cy = x + 400, y + 46
    cv.text('$', cx - 14, cy - 21, 6, GOLD)
    cv.circle(cx, cy, 34, RED)
    cv.circle(cx, cy, 28, GREEN_D)
    cv.text('$', cx - 14, cy - 21, 6, GOLD)
    cv.line(cx - 26, cy + 24, cx + 26, cy - 24, RED, 7)


def pic_chip(cv, x, y, w, h):
    """Nvidia: a green chip and a rising chart line."""
    cv.fill_rect(x, y, w, h, GREEN_B)
    for px in range(0, w, 24):
        cv.fill_rect(x + px + 8, y + 4, 6, 4, (120, 185, 0))
        cv.fill_rect(x + px + 8, y + h - 8, 6, 4, (120, 185, 0))
    cv.line(x + 30, y + 78, x + 150, y + 62, (120, 185, 0), 4)
    cv.line(x + 150, y + 62, x + 260, y + 66, (120, 185, 0), 4)
    cv.line(x + 260, y + 66, x + 360, y + 30, (120, 185, 0), 4)
    cv.line(x + 360, y + 30, x + 430, y + 14, (120, 185, 0), 4)
    cv.triangle([(x + 430, y + 6), (x + 430, y + 26), (x + 448, y + 14)],
                (120, 185, 0))
    cx, cy = x + 96, y + 40
    cv.fill_rect(cx - 26, cy - 26, 52, 52, (118, 185, 0))
    cv.fill_rect(cx - 18, cy - 18, 36, 36, (30, 90, 10))
    cv.text('AI', cx - 15, cy - 11, 3, (118, 185, 0))
    for px in range(cx - 22, cx + 23, 10):
        cv.fill_rect(px, cy - 34, 4, 8, (118, 185, 0))
        cv.fill_rect(px, cy + 26, 4, 8, (118, 185, 0))
    for py in range(cy - 22, cy + 23, 10):
        cv.fill_rect(cx - 34, py, 8, 4, (118, 185, 0))
        cv.fill_rect(cx + 26, py, 8, 4, (118, 185, 0))


def pic_cricket(cv, x, y, w, h):
    """Cricket: stumps, bat and ball on a green pitch."""
    cv.fill_rect(x, y, w, h, PITCH)
    cv.fill_rect(x, y + 34, w, h - 68, (150, 190, 120))
    cv.fill_rect(x + 30, y + 30, 10, h - 60, (210, 210, 210))
    cv.fill_rect(x + 44, y + 30, 10, h - 60, (210, 210, 210))
    cv.fill_rect(x + 58, y + 30, 10, h - 60, (210, 210, 210))
    cv.fill_rect(x + 30, y + 24, 14, 5, (210, 210, 210))
    cv.fill_rect(x + 48, y + 24, 14, 5, (210, 210, 210))
    cv.fill_rect(x + 400, y + 30, 10, h - 60, (210, 210, 210))
    cv.fill_rect(x + 414, y + 30, 10, h - 60, (210, 210, 210))
    cv.fill_rect(x + 428, y + 30, 10, h - 60, (210, 210, 210))
    cv.fill_rect(x + 400, y + 24, 14, 5, (210, 210, 210))
    cv.fill_rect(x + 418, y + 24, 14, 5, (210, 210, 210))
    cv.line(x + 220, y + 70, x + 260, y + 22, (190, 140, 80), 12)
    cv.line(x + 252, y + 34, x + 268, y + 12, (190, 140, 80), 8)
    cv.circle(x + 320, y + 60, 9, (178, 34, 34))
    cv.circle(x + 318, y + 58, 3, (255, 255, 255))


# ---------------------------------------------------------------- stories
# Headlines are two short lines each, decks two wrapped lines.
# Sources name the outlet that reported the story on 24 November 2026.
STORIES = [
    dict(kicker='UKRAINE', kick=NAVY, pic=pic_strike,
         head=['RUSSIA STRIKES', 'ZAPORIZHZHIA'],
         deck="2 killed, 22 hurt overnight; a drone entered Poland.",
         source='REUTERS'),
    dict(kicker='KOREA', kick=TEAL, pic=pic_jets,
         head=['KOREA SCRAMBLES', 'JETS'],
         deck="Jets near Ulleung Island; a 5-minute shelter alert.",
         source='REUTERS'),
    dict(kicker='GAZA', kick=DARKGREY, pic=pic_gaza,
         head=['AIRSTRIKE KILLS', '3 IN GAZA'],
         deck="Strike near a police post in Khan Younis; 5 more hurt.",
         source='REUTERS'),
    dict(kicker='IRAN', kick=GREEN_D, pic=pic_bank,
         head=["US HITS IRAN'S", 'SHADOW BANKS'],
         deck="US sanctions 24 Iran exchange houses and front firms.",
         source='US TREASURY'),
    dict(kicker='TECH', kick=GREEN_B, pic=pic_chip,
         head=['HUANG IS BACK', 'AT NVIDIA'],
         deck="Board brings back the AI chip boss; shares jump a third.",
         source='REUTERS'),
    dict(kicker='CRICKET', kick=PITCH, pic=pic_cricket,
         head=['KIWIS BAT OUT', 'DRAW WITH INDIA'],
         deck="Mitchell, Phillips hold on at Wellington; India stay 4th.",
         source='ICC'),
]


def draw_card(cv, x, y, st):
    w, h = 496, 268
    cv.fill_rect(x, y, w, h, WHITE)
    cv.rect(x, y, w, h, INK, 2)
    # picture band
    st['pic'](cv, x + 2, y + 2, w - 4, 92)
    # kicker chip
    kw = text_width(st['kicker'], 2) + 16
    cv.fill_rect(x + 10, y + 10, kw, 22, st['kick'])
    cv.rect(x + 10, y + 10, kw, 22, WHITE, 1)
    cv.text(st['kicker'], x + 18, y + 14, 2, WHITE)
    # headline, two lines
    for i, line in enumerate(st['head']):
        cv.text(line, x + 14, y + 106 + i * 40, 5, INK)
    # deck, wrapped to two lines
    for i, line in enumerate(wrap_text(st['deck'], 29)[:2]):
        cv.text(line, x + 14, y + 196 + i * 22, 3, (51, 51, 51))
    # source line
    cv.text(st['source'], x + 14, y + 244, 2, GREY)


def build():
    cv = Canvas(W, H, PAPER)
    # masthead
    cv.text('THE WORLD IN ONE PAGE', 512, 22, 7, INK, align='center')
    cv.fill_rect(16, 86, 992, 48, RED)
    cv.text('TUESDAY 24 NOVEMBER 2026', 512, 92, 6, WHITE, align='center')
    cv.text('SIX STORIES THAT DEFINED THE DAY', 512, 146, 2, INK,
            align='center')
    cv.line(16, 166, 1008, 166, INK, 2)
    # six cards, two columns by three rows
    for i, st in enumerate(STORIES):
        col, row = i % 2, i // 2
        draw_card(cv, 16 + col * (496 + 16), 176 + row * (268 + 14), st)
    return cv


def main():
    outdir = os.environ.get('MAKEFUN_OUTPUT_DIR', '/output')
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, 'entry.png')
    data = png_bytes(build())
    with open(path, 'wb') as f:
        f.write(data)
    print('wrote', path, len(data), 'bytes')


if __name__ == '__main__':
    main()
