"""Build the production asset set for karakas-law-firm.

Source files (kept in the repo, never shipped to the browser):
  assets/KARAKAS_HUKUK_LOGO_SEFFAF_4K.png   4096x2731 stacked lockup

Output goes to assets/ as WebP, plus favicons and an Open Graph card.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFilter

REPO = sys.argv[1] if len(sys.argv) > 1 else "."
ASSETS = os.path.join(REPO, "assets")

INK = (10, 15, 26, 255)
GOLD = (201, 169, 106, 255)

LOGO_SRC = "KARAKAS_HUKUK_LOGO_SEFFAF_4K.png"


def p(*parts):
    return os.path.join(ASSETS, *parts)


def trimmed(name, threshold=16):
    im = Image.open(p(name)).convert("RGBA")
    mask = im.getchannel("A").point(lambda v: 255 if v > threshold else 0)
    return im.crop(mask.getbbox())


def save_webp(im, name, width, quality=88):
    h = max(1, round(im.height * width / im.width))
    out = im.resize((width, h), Image.LANCZOS)
    path = p(name)
    out.save(path, "WEBP", quality=quality, method=6)
    return path, out.size, os.path.getsize(path)


results = []


def record(path, size, nbytes):
    results.append((os.path.basename(path), f"{size[0]}x{size[1]}", nbytes))


def for_dark(im, floor=(232, 224, 206)):
    """The supplied lockup sets 'HUKUK BÜROSU' in near-black, which dies on the
    navy ground. Lift only the dark ink toward warm cream; the gold gradient is
    already bright and passes through untouched."""
    out = im.copy()
    px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
            if lum >= 140:
                continue
            # 0 at the threshold, 1 for pure black -> full lift.
            t = (140 - lum) / 140
            px[x, y] = (
                round(r + (floor[0] - r) * t),
                round(g + (floor[1] - g) * t),
                round(b + (floor[2] - b) * t),
                a,
            )
    return out


# ---------------------------------------------------------------- lockup ----
lockup = trimmed(LOGO_SRC)
for w in (420, 840):
    record(*save_webp(lockup, f"logo-lockup-{w}.webp", w))

lockup_dark = for_dark(lockup)
for w in (260, 420, 840):
    record(*save_webp(lockup_dark, f"logo-lockup-ondark-{w}.webp", w))

# --------------------------------------------------------------- monogram ---
# Band analysis: monogram occupies the top 64% of the trimmed lockup,
# horizontally inset to roughly x 583-1317 of 1772.
L, T = 583, 0
R, B = 1318, 914
mono = lockup.crop((L, T, R, B))
mono_mask = mono.getchannel("A").point(lambda v: 255 if v > 16 else 0)
mono = mono.crop(mono_mask.getbbox())
for w in (120, 240):
    record(*save_webp(mono, f"mark-{w}.webp", w))

# Hero watermark. It sits at ~6% opacity, where only the silhouette reads, so
# it is softened and heavily compressed — the alpha channel is what costs, and
# a crisp version would triple the page weight for no visible gain.
ghost = mono.filter(ImageFilter.GaussianBlur(1.6))
record(*save_webp(ghost, "mark-ghost.webp", 400, quality=32))

# Portre üretimi kaldırıldı: Av. Pınar Karakaş fotoğrafının yayınlanmasını
# istemedi; kaynak dosya da depodan silindi.

# --------------------------------------------------------------- favicons ---
def favicon(size):
    canvas = Image.new("RGBA", (size, size), INK)
    inner = int(size * 0.66)
    m = mono.copy()
    ratio = min(inner / m.width, inner / m.height)
    m = m.resize((max(1, round(m.width * ratio)), max(1, round(m.height * ratio))), Image.LANCZOS)
    canvas.alpha_composite(m, ((size - m.width) // 2, (size - m.height) // 2))
    return canvas


for size, name in ((32, "favicon-32.png"), (180, "apple-touch-icon.png"), (512, "icon-512.png")):
    ico = favicon(size)
    ico.save(p(name), optimize=True)
    record(p(name), ico.size, os.path.getsize(p(name)))

ico32 = favicon(32)
ico32.save(p("favicon.ico"), sizes=[(16, 16), (32, 32)])
record(p("favicon.ico"), (32, 32), os.path.getsize(p("favicon.ico")))

# ------------------------------------------------------------ open graph ----
OG_W, OG_H = 1200, 630
og = Image.new("RGBA", (OG_W, OG_H), INK)
draw = ImageDraw.Draw(og)
# Hairline frame, the same detail the site uses on panels.
draw.rectangle([40, 40, OG_W - 41, OG_H - 41], outline=(255, 255, 255, 38), width=1)
draw.rectangle([0, OG_H - 5, OG_W, OG_H], fill=GOLD)

lock = lockup_dark.copy()
target_w = 560
lock = lock.resize((target_w, round(lock.height * target_w / lock.width)), Image.LANCZOS)
og.alpha_composite(lock, ((OG_W - lock.width) // 2, (OG_H - lock.height) // 2 - 10))

og.convert("RGB").save(p("og-image.jpg"), "JPEG", quality=90, optimize=True, progressive=True)
record(p("og-image.jpg"), (OG_W, OG_H), os.path.getsize(p("og-image.jpg")))

# ------------------------------------------------------------------ report --
print(f"{'file':<32}{'size':<14}{'weight':>10}")
print("-" * 56)
total = 0
for name, size, nbytes in results:
    total += nbytes
    print(f"{name:<32}{size:<14}{nbytes/1024:>8.1f} KB")
print("-" * 56)
print(f"{'TOTAL (all variants)':<46}{total/1024:>8.1f} KB")

src = os.path.getsize(p(LOGO_SRC))
print(f"{'source PNG (kept, not shipped)':<46}{src/1024:>8.1f} KB")
