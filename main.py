"""Magazine cover: THE WORLD, 22 November 2026.

Cover story: COP31 climate talks collapse in Antalya (no deal).
Drawn with pure Python standard library. Deterministic output.
"""

import os
import struct
import zlib

W = 1024
H = 1024

# ---- colours (r, g, b) -------------------------------------------------
NAVY_TOP = (10, 34, 51)
NAVY_MID = (14, 58, 77)
NAVY_BOT = (8, 26, 40)
WHITE = (255, 255, 255)
GOLD = (212, 175, 55)
RED = (192, 57, 43)
RED_DARK = (150, 40, 30)
YELLOW = (255, 201, 60)
OCEAN = (30, 111, 184)
OCEAN_DARK = (18, 78, 138)
LAND = (47, 168, 79)
LAND_DARK = (34, 130, 60)
ICE = (235, 244, 250)
CRACK = (12, 12, 14)
EMBER = (255, 110, 30)
FLAG_BLUE = (0, 51, 153)
FLAG_RED = (227, 10, 23)
GREY = (180, 190, 196)

# ---- 5x7 bitmap font: each glyph is 7 rows of 5 bits -------------------
FONT = {
    "A": (0x0E, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11),
    "B": (0x1E, 0x11, 0x11, 0x1E, 0x11, 0x11, 0x1E),
    "C": (0x0E, 0x11, 0x10, 0x10, 0x10, 0x11, 0x0E),
    "D": (0x1E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1E),
    "E": (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x1F),
    "F": (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x10),
    "G": (0x0E, 0x11, 0x10, 0x17, 0x11, 0x11, 0x0F),
    "H": (0x11, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11),
    "I": (0x0E, 0x04, 0x04, 0x04, 0x04, 0x04, 0x0E),
    "J": (0x07, 0x02, 0x02, 0x02, 0x02, 0x12, 0x0C),
    "K": (0x11, 0x12, 0x14, 0x18, 0x14, 0x12, 0x11),
    "L": (0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x1F),
    "M": (0x11, 0x1B, 0x15, 0x15, 0x11, 0x11, 0x11),
    "N": (0x11, 0x19, 0x15, 0x13, 0x11, 0x11, 0x11),
    "O": (0x0E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E),
    "P": (0x1E, 0x11, 0x11, 0x1E, 0x10, 0x10, 0x10),
    "Q": (0x0E, 0x11, 0x11, 0x11, 0x15, 0x12, 0x0D),
    "R": (0x1E, 0x11, 0x11, 0x1E, 0x14, 0x12, 0x11),
    "S": (0x0F, 0x10, 0x10, 0x0E, 0x01, 0x01, 0x1E),
    "T": (0x1F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04),
    "U": (0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E),
    "V": (0x11, 0x11, 0x11, 0x11, 0x11, 0x0A, 0x04),
    "W": (0x11, 0x11, 0x11, 0x15, 0x15, 0x1B, 0x11),
    "X": (0x11, 0x11, 0x0A, 0x04, 0x0A, 0x11, 0x11),
    "Y": (0x11, 0x11, 0x0A, 0x04, 0x04, 0x04, 0x04),
    "Z": (0x1F, 0x01, 0x02, 0x04, 0x08, 0x10, 0x1F),
    "0": (0x0E, 0x11, 0x13, 0x15, 0x19, 0x11, 0x0E),
    "1": (0x04, 0x0C, 0x04, 0x04, 0x04, 0x04, 0x0E),
    "2": (0x0E, 0x11, 0x01, 0x06, 0x08, 0x10, 0x1F),
    "3": (0x1F, 0x02, 0x04, 0x02, 0x01, 0x11, 0x0E),
    "4": (0x02, 0x06, 0x0A, 0x12, 0x1F, 0x02, 0x02),
    "5": (0x1F, 0x10, 0x1E, 0x01, 0x01, 0x11, 0x0E),
    "6": (0x06, 0x08, 0x10, 0x1E, 0x11, 0x11, 0x0E),
    "7": (0x1F, 0x01, 0x02, 0x04, 0x08, 0x08, 0x08),
    "8": (0x0E, 0x11, 0x11, 0x0E, 0x11, 0x11, 0x0E),
    "9": (0x0E, 0x11, 0x11, 0x0F, 0x01, 0x02, 0x0C),
    " ": (0, 0, 0, 0, 0, 0, 0),
    "-": (0, 0, 0, 0x0E, 0, 0, 0),
    "'": (0x04, 0x04, 0x08, 0, 0, 0, 0),
    ".": (0, 0, 0, 0, 0, 0x0C, 0x0C),
    ",": (0, 0, 0, 0, 0x0C, 0x04, 0x08),
    ":": (0, 0x0C, 0x0C, 0, 0x0C, 0x0C, 0),
    "!": (0x04, 0x04, 0x04, 0x04, 0x04, 0, 0x04),
    "?": (0x0E, 0x11, 0x01, 0x02, 0x04, 0, 0x04),
    "/": (0x01, 0x02, 0x02, 0x04, 0x08, 0x08, 0x10),
    "(": (0x02, 0x04, 0x08, 0x08, 0x08, 0x04, 0x02),
    ")": (0x08, 0x04, 0x02, 0x02, 0x02, 0x04, 0x08),
    "&": (0x0C, 0x12, 0x14, 0x08, 0x15, 0x12, 0x0D),
    "%": (0x19, 0x1A, 0x02, 0x04, 0x08, 0x0B, 0x13),
    "+": (0, 0x04, 0x04, 0x0E, 0x04, 0x04, 0),
    "=": (0, 0, 0x0E, 0, 0x0E, 0, 0),
    "*": (0, 0x04, 0x15, 0x0E, 0x15, 0x04, 0),
}


class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(w * h * 3)
        for i in range(w * h):
            self.px[i * 3] = bg[0]
            self.px[i * 3 + 1] = bg[1]
            self.px[i * 3 + 2] = bg[2]

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i] = c[0]
            self.px[i + 1] = c[1]
            self.px[i + 2] = c[2]

    def rect(self, x0, y0, x1, y1, c):
        for y in range(max(0, y0), min(self.h, y1)):
            for x in range(max(0, x0), min(self.w, x1)):
                self.set(x, y, c)

    def disc(self, cx, cy, r, c):
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                if (x - cx) * (x - cx) + (y - cy) * (y - cy) <= r * r:
                    self.set(x, y, c)

    def ring(self, cx, cy, r, thick, c):
        for y in range(cy - r - thick, cy + r + thick + 1):
            for x in range(cx - r - thick, cx + r + thick + 1):
                d2 = (x - cx) * (x - cx) + (y - cy) * (y - cy)
                if (r - thick) * (r - thick) <= d2 <= (r + thick) * (r + thick):
                    self.set(x, y, c)

    def line(self, x0, y0, x1, y1, c, thick=1):
        dx = x1 - x0
        dy = y1 - y0
        steps = max(abs(dx), abs(dy), 1)
        for i in range(steps + 1):
            x = x0 + dx * i // steps
            y = y0 + dy * i // steps
            self.disc(x, y, thick, c)

    def text(self, x, y, s, scale, c):
        cx = x
        for ch in s:
            rows = FONT.get(ch, FONT[" "])
            for r in range(7):
                bits = rows[r]
                for col in range(5):
                    if bits & (1 << (4 - col)):
                        self.rect(
                            cx + col * scale,
                            y + r * scale,
                            cx + (col + 1) * scale,
                            y + (r + 1) * scale,
                            c,
                        )
            cx += 6 * scale

    def text_w(self, s, scale):
        return len(s) * 6 * scale - scale

    def text_c(self, y, s, scale, c):
        self.text((self.w - self.text_w(s, scale)) // 2, y, s, scale, c)


def lerp(a, b, t):
    return a + (b - a) * t // 100


def draw():
    cv = Canvas(W, H, NAVY_TOP)
    # vertical gradient background
    for y in range(H):
        if y < H // 2:
            t = y * 100 // (H // 2)
            c = (lerp(NAVY_TOP[0], NAVY_MID[0], t),
                 lerp(NAVY_TOP[1], NAVY_MID[1], t),
                 lerp(NAVY_TOP[2], NAVY_MID[2], t))
        else:
            t = (y - H // 2) * 100 // (H // 2)
            c = (lerp(NAVY_MID[0], NAVY_BOT[0], t),
                 lerp(NAVY_MID[1], NAVY_BOT[1], t),
                 lerp(NAVY_MID[2], NAVY_BOT[2], t))
        for x in range(W):
            cv.set(x, y, c)

    # gold frame
    cv.rect(16, 16, W - 16, 24, GOLD)
    cv.rect(16, H - 24, W - 16, H - 16, GOLD)
    cv.rect(16, 16, 24, H - 16, GOLD)
    cv.rect(W - 24, 16, W - 16, H - 16, GOLD)

    # masthead
    cv.text_c(38, "THE WORLD", 13, WHITE)
    cv.rect(120, 142, W - 120, 147, GOLD)

    # date banner
    cv.rect(48, 158, W - 48, 224, RED)
    cv.rect(48, 158, W - 48, 164, RED_DARK)
    cv.text_c(164, "22 NOVEMBER 2026", 9, WHITE)

    # ---- cracked globe illustration ----
    gx, gy, gr = 512, 425, 155
    # ocean + shading
    cv.disc(gx, gy, gr, OCEAN)
    cv.disc(gx - 42, gy - 48, 96, OCEAN_DARK)
    cv.disc(gx - 42, gy - 48, 96, OCEAN)
    # continents (land blobs clipped to the globe)
    blobs = [
        (452, 372, 38), (486, 352, 26), (548, 388, 32), (585, 420, 22),
        (520, 452, 30), (470, 478, 24), (600, 470, 20), (430, 430, 18),
        (560, 505, 24), (500, 512, 16),
    ]
    for y in range(gy - gr, gy + gr + 1):
        for x in range(gx - gr, gx + gr + 1):
            d2 = (x - gx) * (x - gx) + (y - gy) * (y - gy)
            if d2 > gr * gr:
                continue
            for bx, by, br in blobs:
                if (x - bx) * (x - bx) + (y - by) * (y - by) <= br * br:
                    cv.set(x, y, LAND if (x + y) % 3 else LAND_DARK)
                    break
    # polar ice cap
    for y in range(gy - gr, gy - gr + 46):
        for x in range(gx - gr, gx + gr + 1):
            if (x - gx) * (x - gx) + (y - gy) * (y - gy) <= gr * gr:
                cv.set(x, y, ICE)
    # jagged crack down the globe
    crack_pts = [
        (505, 272), (522, 300), (498, 330), (528, 362), (500, 395),
        (530, 428), (506, 462), (534, 496), (508, 530), (526, 560),
        (512, 578),
    ]
    for i in range(len(crack_pts) - 1):
        x0, y0 = crack_pts[i]
        x1, y1 = crack_pts[i + 1]
        cv.line(x0, y0, x1, y1, CRACK, 5)
    # ember glow along the crack
    for i in range(0, len(crack_pts) - 1, 2):
        x0, y0 = crack_pts[i]
        x1, y1 = crack_pts[i + 1]
        cv.line(x0 + 7, y0, x1 + 7, y1, EMBER, 2)
    # crack branches
    cv.line(500, 395, 462, 418, CRACK, 3)
    cv.line(530, 428, 566, 452, CRACK, 3)
    cv.line(508, 530, 478, 556, CRACK, 3)
    # globe outline
    cv.ring(gx, gy, gr, 3, WHITE)

    # small flags flanking the globe (empty chairs: no deal)
    # left flag pole + red flag
    cv.rect(296, 330, 301, 470, GREY)
    cv.rect(301, 330, 361, 372, FLAG_RED)
    cv.disc(326, 351, 9, WHITE)
    cv.disc(330, 351, 7, FLAG_RED)
    # right flag pole + blue flag
    cv.rect(723, 330, 728, 470, GREY)
    cv.rect(663, 330, 723, 372, FLAG_BLUE)
    for dx in (-14, 14):
        for dy in (-10, 10):
            cv.disc(693 + dx, 351 + dy, 3, YELLOW)
    cv.disc(693, 351, 3, YELLOW)

    # ---- cover story headline ----
    cv.text_c(600, "COP31 COLLAPSES", 10, YELLOW)
    cv.text_c(682, "CLIMATE TALKS END WITH NO DEAL", 5, WHITE)
    cv.text_c(726, "ANTALYA - LONGEST COP ON RECORD", 4, GOLD)

    # divider
    cv.rect(120, 772, W - 120, 777, GOLD)

    # ---- cover lines ----
    lines = [
        ("DEMOCRATS WIN BIGGEST HOUSE MAJORITY", RED),
        ("TANKERS ABLAZE AT HORMUZ", EMBER),
        ("RUSSIAN WARSHIP HIT OFF LIBYA", YELLOW),
        ("SUDAN DRONES STRIKE UN BUILDING", WHITE),
        ("EL CHAPO ISIDRO CAPTURED IN MEXICO", GOLD),
    ]
    y = 796
    for text, bullet_c in lines:
        cv.rect(64, y + 6, 88, y + 22, bullet_c)
        cv.text(104, y, text, 4, WHITE)
        y += 38

    return cv


def write_png(cv, path):
    raw = bytearray()
    for y in range(cv.h):
        raw.append(0)
        raw.extend(cv.px[y * cv.w * 3:(y + 1) * cv.w * 3])
    comp = zlib.compress(bytes(raw), 6)

    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        out += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", ihdr)
    png += chunk(b"IDAT", comp)
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    cv = draw()
    write_png(cv, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
