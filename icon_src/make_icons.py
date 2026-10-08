# Generates FocusDeck app icons (matches the sidebar logo: indigo gradient tile with a white clock).
from PIL import Image, ImageDraw
import os, sys
OUT = sys.argv[1] if len(sys.argv) > 1 else 'site/icons'
os.makedirs(OUT, exist_ok=True)
S = 1024
A, B = (0x4F, 0x5B, 0xF0), (0x7C, 0x5C, 0xFF)

def gradient(size):
    g = Image.new('RGB', (size, size))
    px = g.load()
    for y in range(size):
        for x in range(size):
            t = (x + y) / (2 * (size - 1))
            px[x, y] = tuple(round(A[i] + (B[i] - A[i]) * t) for i in range(3))
    return g

def clock(draw, cx, cy, r, w):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline='white', width=w)
    # hands: 12 o'clock to center, center to ~4 o'clock (like the SVG polyline 12,6 -> 12,12 -> 16,14)
    hx, hy = cx, cy - r * 0.6
    mx, my = cx + r * 0.4, cy + r * 0.2
    draw.line([hx, hy, cx, cy], fill='white', width=w)
    draw.line([cx, cy, mx, my], fill='white', width=w)
    for (x, y) in [(hx, hy), (cx, cy), (mx, my)]:
        draw.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill='white')

grad = gradient(256).resize((S, S), Image.BICUBIC)

# "any" icon: rounded tile on transparent background
anyimg = Image.new('RGBA', (S, S), (0, 0, 0, 0))
mask = Image.new('L', (S, S), 0)
ImageDraw.Draw(mask).rounded_rectangle([40, 40, S - 40, S - 40], radius=220, fill=255)
anyimg.paste(grad, (0, 0), mask)
clock(ImageDraw.Draw(anyimg), S / 2, S / 2, 270, 64)

# "maskable" icon: full-bleed background, clock inside the 80% safe zone
mk = grad.convert('RGBA')
clock(ImageDraw.Draw(mk), S / 2, S / 2, 230, 56)

for size in (192, 512):
    anyimg.resize((size, size), Image.LANCZOS).save(f'{OUT}/icon-{size}.png', optimize=True)
mk.resize((512, 512), Image.LANCZOS).save(f'{OUT}/icon-maskable-512.png', optimize=True)
mk.convert('RGB').resize((180, 180), Image.LANCZOS).save(f'{OUT}/apple-touch-icon.png', optimize=True)
anyimg.resize((32, 32), Image.LANCZOS).save(f'{OUT}/favicon-32.png', optimize=True)
print('icons written to', OUT)
