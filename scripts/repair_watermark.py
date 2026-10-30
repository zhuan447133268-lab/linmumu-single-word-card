#!/usr/bin/env python3
"""Remove the fixed bottom-right ImageGen watermark ("AI生成 / WORKBUDDX")
by cloning the texture band just above the watermark region, with slight
jitter to hide repetition.

Why not a flat color fill: oil paintings (and any non-uniform background)
show an obvious rectangular block if you fill with an averaged color.
Texture cloning works for oil paintings AND flat illustrations alike.

Usage:
    python repair_watermark.py <image.png> [more.png ...]
    python repair_watermark.py <directory>        # all *.png not ending in _clean

Output: <name>_clean.png next to the source. Deps: numpy, Pillow.
"""
import argparse
import glob
import os

import numpy as np
from PIL import Image

# Watermark bbox as fractions of image size (right-bottom corner).
X0, Y0 = 0.80, 0.90
OFFSET = 0.06  # sample texture this far above the watermark band
JITTER = 5     # ± intensity noise to break visible repetition
SEED = 7


def repair(path: str, out: str | None = None) -> str:
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(np.int16)
    h, w, _ = a.shape
    x0, x1 = int(X0 * w), w
    y0, y1 = int(Y0 * h), h
    off = max(1, int(OFFSET * h))
    rng = np.random.default_rng(SEED)
    for y in range(y0, y1):
        sy = max(0, y - off)
        band = a[sy, x0:x1].astype(np.int16)
        band = band + rng.integers(-JITTER, JITTER + 1, size=band.shape)
        a[y, x0:x1] = band
    out = out or path[:-4] + "_clean.png"
    Image.fromarray(a.clip(0, 255).astype(np.uint8)).save(out)
    print("repaired ->", os.path.basename(out))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("paths", nargs="+", help="png files or a directory")
    args = ap.parse_args()
    n = 0
    for p in args.paths:
        if os.path.isdir(p):
            for f in sorted(glob.glob(os.path.join(p, "*.png"))):
                if not f.endswith("_clean.png"):
                    repair(f)
                    n += 1
        elif p.lower().endswith(".png"):
            repair(p)
            n += 1
        else:
            print("skip (not png):", p)
    print(f"done, {n} file(s) repaired")


if __name__ == "__main__":
    main()
