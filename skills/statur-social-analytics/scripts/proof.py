#!/usr/bin/env python3
"""Blur parts of an analytics screenshot so the numbers can be shown without naming the account.

  python3 proof.py IN.png OUT.png --box x0,y0,x1,y1 [--box ...] [--radius 14]

Boxes are in pixels of the input image (caption, thumbnail, avatar, handle). Needs Pillow: pip install pillow.
Keep the raw screenshot in proof/ and write the blurred copy to proof_anon/.
"""
import sys

try:
    from PIL import Image, ImageFilter
except ImportError:
    sys.exit('Pillow is missing: pip install pillow')


def main(argv):
    if len(argv) < 5 or '--box' not in argv:
        print(__doc__)
        return 1
    src, dst = argv[1], argv[2]
    boxes, radius = [], 14
    for i, a in enumerate(argv):
        if a == '--box':
            boxes.append(tuple(int(v) for v in argv[i + 1].split(',')))
        if a == '--radius':
            radius = int(argv[i + 1])
    im = Image.open(src).convert('RGB')
    for box in boxes:
        im.paste(im.crop(box).filter(ImageFilter.GaussianBlur(radius)), box)
    im.save(dst)
    print(f'wrote {dst} ({len(boxes)} zones blurred)')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
