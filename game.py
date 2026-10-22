# game.py - the non-AI part: loading pictures, messing them up, making a round
import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

IMG_SIZE = 160
EXTS = {".jpg", ".jpeg", ".png", ".webp"}


def list_images(folder):
    folder = Path(folder)
    if not folder.exists():
        return []
    return sorted(p for p in folder.iterdir() if p.suffix.lower() in EXTS)


def load_square(path, size=IMG_SIZE):
    """open an image, crop the centre square, resize so the grid looks neat"""
    img = Image.open(path).convert("RGB")
    w, h = img.size
    s = min(w, h)
    left, top = (w - s) // 2, (h - s) // 2
    img = img.crop((left, top, left + s, top + s))
    return img.resize((size, size))


def augment(img, level):
    """
    Randomly distort an image. level goes 1 (barely changed) to 5 (really nasty).
    Same idea as the augmentation we did in module 4, just done by hand with PIL.
    """
    out = img.copy()

    # flip (always possible, any level)
    if random.random() < 0.5:
        out = out.transpose(Image.FLIP_LEFT_RIGHT)

    # rotation gets bigger with level
    angle = random.uniform(-15 * level, 15 * level)
    out = out.rotate(angle, resample=Image.BICUBIC, fillcolor=(128, 128, 128))

    # colour changes
    amount = 0.12 * level
    out = ImageEnhance.Brightness(out).enhance(1 + random.uniform(-amount, amount))
    out = ImageEnhance.Contrast(out).enhance(1 + random.uniform(-amount, amount))
    out = ImageEnhance.Color(out).enhance(1 + random.uniform(-amount, amount))

    # random zoom-in crop from level 3
    if level >= 3:
        keep = 1 - 0.08 * (level - 2)  # 0.92, 0.84, 0.76
        w, h = out.size
        cw, ch = int(w * keep), int(h * keep)
        x = random.randint(0, w - cw)
        y = random.randint(0, h - ch)
        out = out.crop((x, y, x + cw, y + ch)).resize((w, h))

    # blur from level 4
    if level >= 4:
        out = out.filter(ImageFilter.GaussianBlur(radius=(level - 3) * 1.2))

    # noise on top at the highest levels
    if level >= 2:
        arr = np.array(out).astype(np.float32)
        arr += np.random.normal(0, 4 * level, arr.shape)
        out = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

    return out


def make_round(paths, n_choices, level):
    """pick n_choices different pictures, one of them is the answer"""
    chosen = random.sample(paths, n_choices)
    answer = random.randrange(n_choices)
    originals = [load_square(p) for p in chosen]
    target = augment(originals[answer], level)
    return {
        "choices": originals,
        "answer": answer,
        "target": target,
        "level": level,
    }
