"""按组把关键帧拼成带标签的接触表，用于全片画风一致性实看。

用法：python make_style_sheets.py [groups.json]
groups.json 结构：{"<输出名>": {"cols": 3, "items": [["标签", "路径"], ...]}}
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
CELL_W = 620
PAD = 8
LABEL_H = 26


def load_font(size=18):
    for name in ("msyh.ttc", "segoeui.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def build(name, spec, font):
    items = spec["items"]
    cols = spec.get("cols", 3)
    cells = []
    for label, path in items:
        p = Path(path)
        if not p.exists():
            print(f"  ! 缺图 {label}: {p}")
            continue
        im = Image.open(p).convert("RGB")
        h = round(im.height * CELL_W / im.width)
        cells.append((label, im.resize((CELL_W, h), Image.LANCZOS)))

    if not cells:
        return None
    cell_h = max(c[1].height for c in cells) + LABEL_H
    rows = (len(cells) + cols - 1) // cols
    sheet = Image.new(
        "RGB",
        (cols * (CELL_W + PAD) + PAD, rows * (cell_h + PAD) + PAD),
        (24, 24, 28),
    )
    d = ImageDraw.Draw(sheet)
    for i, (label, im) in enumerate(cells):
        r, c = divmod(i, cols)
        x = PAD + c * (CELL_W + PAD)
        y = PAD + r * (cell_h + PAD)
        d.text((x + 2, y + 4), label, fill=(255, 214, 120), font=font)
        sheet.paste(im, (x, y + LABEL_H))
    out = HERE / f"{name}.png"
    sheet.save(out, quality=92)
    print(f"  -> {out.name}  ({len(cells)} 张, {sheet.width}x{sheet.height})")
    return out


def main():
    cfg = json.loads(Path(sys.argv[1] if len(sys.argv) > 1 else HERE / "groups.json").read_text(encoding="utf-8"))
    font = load_font()
    for name, spec in cfg.items():
        build(name, spec, font)


if __name__ == "__main__":
    main()
