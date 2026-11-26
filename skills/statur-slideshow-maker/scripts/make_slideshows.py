#!/usr/bin/env python3
"""Render photo-mode slideshows (TikTok, Instagram) and PDF carousels (LinkedIn)
from a CSV spec. One row per slide. Zero network, one dependency (Pillow).

Usage:
  python3 make_slideshows.py spec.csv --out out/ [--size 1080x1920] [--style outline]
         [--font /path/to/font.ttf] [--pdf] [--sheet]

CSV columns (header required):
  post_id   id of the slideshow (one folder per post), e.g. hook-a-01
  slide     slide number (1, 2, 3...)
  text      text shown on the slide (use \\n for a forced line break)
  image     optional path to a background image (relative to the CSV file)
  bg        optional background color when there is no image, e.g. #0E0E0C
  position  optional: top, center or bottom (default from --position)

Output per post: slide-01.jpg... (or .png/.webp with --format), contact-sheet.jpg (with --sheet),
<post_id>.pdf (with --pdf).
Output for the run: manifest.csv with one row per slide, the font size used and a fit check.
"""
import argparse
import csv
import os
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("Pillow is missing. Install it with: pip install Pillow")

FONT_CANDIDATES = [
    # Linux
    "/usr/share/fonts/opentype/inter/Inter-Bold.otf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    # macOS
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    # Windows
    "C:/Windows/Fonts/arialbd.ttf",
    "C:/Windows/Fonts/segoeuib.ttf",
]


def find_font(user_font):
    if user_font:
        if not os.path.exists(user_font):
            sys.exit(f"Font not found: {user_font}")
        return user_font
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            return path
    sys.exit("No bold font found. Pass one with --font /path/to/font.ttf")


def parse_size(value):
    try:
        w, h = value.lower().split("x")
        return int(w), int(h)
    except ValueError:
        sys.exit(f"Bad --size {value}. Use WIDTHxHEIGHT, e.g. 1080x1920")


def hex_to_rgb(value, default=(14, 14, 12)):
    value = (value or "").strip().lstrip("#")
    if len(value) != 6:
        return default
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def cover(img, size):
    """Crop and resize an image so it fills size without distortion."""
    tw, th = size
    iw, ih = img.size
    scale = max(tw / iw, th / ih)
    nw, nh = int(iw * scale + 0.5), int(ih * scale + 0.5)
    img = img.resize((nw, nh), Image.LANCZOS)
    left, top = (nw - tw) // 2, (nh - th) // 2
    return img.crop((left, top, left + tw, top + th))


def wrap(draw, text, font, max_width):
    """Greedy word wrap by pixel width. Keeps forced line breaks."""
    lines = []
    for paragraph in text.replace("\\n", "\n").split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            trial = current + " " + word
            if draw.textlength(trial, font=font) <= max_width:
                current = trial
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def fit_text(draw, text, font_path, box_w, box_h, max_size, min_size, spacing):
    """Largest font size where the wrapped text fits the box. Returns (font, lines, size, fits)."""
    size = max_size
    while size >= min_size:
        font = ImageFont.truetype(font_path, size)
        lines = wrap(draw, text, font, box_w)
        widest = max((draw.textlength(l, font=font) for l in lines), default=0)
        line_h = int(size * spacing)
        if widest <= box_w and line_h * len(lines) <= box_h:
            return font, lines, size, True
        size -= 2
    font = ImageFont.truetype(font_path, min_size)
    return font, wrap(draw, text, font, box_w), min_size, False


def render_slide(row, base_dir, args, font_path, size):
    w, h = size
    k = h / 1920.0  # safe zones are defined for 1920 px height, scaled for other sizes
    top, right, bottom, left = [int(v * k) for v in args.safe]
    if args.safe_auto and h < 1900:
        # 4:5 and square formats have no TikTok UI over the image edges in feed: smaller margins
        top, bottom = int(90 * k), int(140 * k)

    image_path = (row.get("image") or "").strip()
    if image_path:
        full = image_path if os.path.isabs(image_path) else os.path.join(base_dir, image_path)
        if not os.path.exists(full):
            sys.exit(f"Image not found for {row['post_id']} slide {row['slide']}: {full}")
        canvas = cover(Image.open(full).convert("RGB"), size)
        if args.darken > 0:
            shade = Image.new("RGB", size, (0, 0, 0))
            canvas = Image.blend(canvas, shade, args.darken)
    else:
        canvas = Image.new("RGB", size, hex_to_rgb(row.get("bg"), hex_to_rgb(args.bg)))

    draw = ImageDraw.Draw(canvas, "RGBA")
    box_w = w - left - right
    box_h = int((h - top - bottom) * args.text_area)
    font, lines, font_size, fits = fit_text(
        draw, (row.get("text") or "").strip(), font_path, box_w, box_h,
        int(args.max_font * k), int(args.min_font * k), args.spacing)

    line_h = int(font_size * args.spacing)
    block_h = line_h * len(lines)
    position = (row.get("position") or args.position).strip().lower()
    if position == "top":
        y0 = top
    elif position == "bottom":
        y0 = h - bottom - block_h
    else:
        y0 = top + ((h - top - bottom) - block_h) // 2

    fill = hex_to_rgb(args.color, (255, 255, 255))
    stroke_fill = hex_to_rgb(args.stroke_color, (0, 0, 0))
    stroke_w = max(2, font_size // 14) if args.style == "outline" else 0

    if args.style == "band" and lines:
        pad = int(font_size * 0.45)
        widest = max(draw.textlength(l, font=font) for l in lines)
        x_band = (w - widest) / 2 - pad if args.align == "center" else left - pad
        draw.rectangle([x_band, y0 - pad, x_band + widest + 2 * pad, y0 + block_h + pad // 2],
                       fill=stroke_fill + (int(255 * 0.62),))

    for i, line in enumerate(lines):
        lw = draw.textlength(line, font=font)
        x = (w - lw) / 2 if args.align == "center" else left
        draw.text((x, y0 + i * line_h), line, font=font, fill=fill,
                  stroke_width=stroke_w, stroke_fill=stroke_fill)

    words = len((row.get("text") or "").split())
    return canvas, {"font_size": font_size, "lines": len(lines), "fits": fits, "words": words}


def save_image(img, path, args):
    if args.format == "jpg":
        img.save(path, "JPEG", quality=args.quality, optimize=True, progressive=True)
    elif args.format == "webp":
        img.save(path, "WEBP", quality=args.quality, method=6)
    else:
        img.save(path, "PNG", optimize=True)


def contact_sheet(images, out_path, thumb_h=480, gap=12):
    thumbs = [im.resize((int(im.width * thumb_h / im.height), thumb_h)) for im in images]
    width = sum(t.width for t in thumbs) + gap * (len(thumbs) + 1)
    sheet = Image.new("RGB", (width, thumb_h + 2 * gap), (40, 40, 40))
    x = gap
    for t in thumbs:
        sheet.paste(t, (x, gap))
        x += t.width + gap
    sheet.save(out_path, "JPEG", quality=85)


def main():
    p = argparse.ArgumentParser(description="Render slideshows and carousels from a CSV spec.")
    p.add_argument("spec", help="CSV file: post_id, slide, text, image, bg, position")
    p.add_argument("--out", default="slideshows", help="output folder")
    p.add_argument("--size", default="1080x1920", help="1080x1920 (9:16), 1080x1350 (4:5) or 1080x1080")
    p.add_argument("--font", default=None, help="path to a bold .ttf or .otf font")
    p.add_argument("--style", choices=["outline", "band", "plain"], default="outline")
    p.add_argument("--align", choices=["center", "left"], default="center")
    p.add_argument("--position", choices=["top", "center", "bottom"], default="center")
    p.add_argument("--color", default="#FFFFFF", help="text color")
    p.add_argument("--stroke-color", default="#000000", help="outline or band color")
    p.add_argument("--bg", default="#0E0E0C", help="default background color without image")
    p.add_argument("--darken", type=float, default=0.15, help="0 to 0.6, darkens photos for contrast")
    p.add_argument("--max-font", type=int, default=92, help="max font size at 1920 px height")
    p.add_argument("--min-font", type=int, default=40, help="min font size at 1920 px height")
    p.add_argument("--spacing", type=float, default=1.18, help="line height as a multiple of font size")
    p.add_argument("--text-area", type=float, default=0.62, help="share of the safe area the text may fill")
    p.add_argument("--safe", default="220,130,420,90",
                   help="margins top,right,bottom,left in px for a 1920 px tall slide (scaled otherwise)")
    p.add_argument("--no-safe-auto", dest="safe_auto", action="store_false",
                   help="keep the 9:16 margins on 4:5 and square sizes")
    p.add_argument("--max-words", type=int, default=30, help="warn above this many words on a slide")
    p.add_argument("--format", choices=["jpg", "png", "webp"], default="jpg",
                   help="image format of the slides (jpg is accepted everywhere)")
    p.add_argument("--quality", type=int, default=92, help="jpg or webp quality, 1 to 100")
    p.add_argument("--pdf", action="store_true", help="also save one PDF per post (LinkedIn carousel)")
    p.add_argument("--sheet", action="store_true", help="also save a contact sheet per post")
    args = p.parse_args()
    args.safe = [int(v) for v in args.safe.split(",")]
    if len(args.safe) != 4:
        sys.exit("--safe needs four numbers: top,right,bottom,left")

    size = parse_size(args.size)
    font_path = find_font(args.font)
    base_dir = os.path.dirname(os.path.abspath(args.spec))

    with open(args.spec, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    missing = {"post_id", "slide", "text"} - set(rows[0].keys() if rows else [])
    if missing:
        sys.exit(f"CSV header is missing: {', '.join(sorted(missing))}")

    posts = {}
    for row in rows:
        posts.setdefault(row["post_id"].strip(), []).append(row)

    os.makedirs(args.out, exist_ok=True)
    manifest = []
    warnings = 0
    for post_id, slides in posts.items():
        slides.sort(key=lambda r: int(r["slide"]))
        folder = os.path.join(args.out, post_id)
        os.makedirs(folder, exist_ok=True)
        images = []
        for row in slides:
            img, info = render_slide(row, base_dir, args, font_path, size)
            name = f"slide-{int(row['slide']):02d}.{args.format}"
            save_image(img, os.path.join(folder, name), args)
            images.append(img)
            flag = []
            if not info["fits"]:
                flag.append("text does not fit at min font size: shorten it")
            if info["words"] > args.max_words:
                flag.append(f"{info['words']} words: above {args.max_words}")
            warnings += len(flag)
            manifest.append({"post_id": post_id, "slide": row["slide"], "file": os.path.join(post_id, name),
                             "words": info["words"], "font_size": info["font_size"], "lines": info["lines"],
                             "fits": info["fits"], "warning": "; ".join(flag)})
        if args.sheet:
            contact_sheet(images, os.path.join(folder, "contact-sheet.jpg"))
        if args.pdf:
            images[0].save(os.path.join(folder, f"{post_id}.pdf"), save_all=True,
                           append_images=images[1:], resolution=150)

    with open(os.path.join(args.out, "manifest.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(manifest[0].keys()))
        writer.writeheader()
        writer.writerows(manifest)

    print(f"{len(posts)} posts, {len(manifest)} slides, {warnings} warnings, font: {os.path.basename(font_path)}")
    print(f"Output: {os.path.abspath(args.out)}")
    return 0 if warnings == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
