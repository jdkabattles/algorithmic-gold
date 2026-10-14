#!/usr/bin/env python3
"""Generate a branded 1200x630 og:image PNG using only stdlib (no PIL)."""
import math
import struct
import zlib

W, H = 1200, 630
BG_TOP = (10, 10, 15)
BG_BOT = (22, 18, 8)
GOLD = (245, 197, 66)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


rows = bytearray()
for y in range(H):
    row = bytearray()
    for x in range(W):
        # diagonal gradient
        t = (x / W * 0.45 + y / H * 0.55)
        px = lerp(BG_TOP, BG_BOT, t)
        # gold radial glow, upper-left
        d = math.hypot(x - 180, y - 120)
        if d < 520:
            glow = (1 - d / 520) ** 2.2
            px = tuple(min(255, int(px[i] + (GOLD[i] - px[i]) * glow * 0.22)) for i in range(3))
        # subtle grid lines
        if x % 60 == 0 or y % 60 == 0:
            px = tuple(min(255, c + 7) for c in px)
        # triangle logo mark (chevron up), centered at (180,150), size ~90
        lx, ly = x - 180, y - 150
        if 0 <= lx <= 120 and 0 <= ly <= 96:
            # inside triangle: |lx-60| <= (ly*0.625) and ly >= (96 - distance from top inverted)
            half = (96 - ly) * 0.625 + 12
            dist = abs(lx - 60)
            edge = 12
            if dist <= half and ly >= 8:
                if half - dist <= edge or ly <= 8 + edge:
                    px = GOLD
        row += bytes(px)
    rows += b"\x00" + row  # filter byte 0


def chunk(tag, data):
    return (struct.pack(">I", len(data)) + tag + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))


png = (b"\x89PNG\r\n\x1a\n"
       + chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))
       + chunk(b"IDAT", zlib.compress(bytes(rows), 9))
       + chunk(b"IEND", b""))

with open("og-image.png", "wb") as f:
    f.write(png)
print("wrote og-image.png", len(png), "bytes")
