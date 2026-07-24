# -*- coding: utf-8 -*-
"""
quant_bot.renderers.sanity_checker — Sanity checker generator class.
"""

import os
import shutil
import subprocess
import tempfile
from typing import Dict
from PIL import Image, ImageDraw, ImageFont


class SanityChecker:
    """Generates contact-sheet verification image for slot validation."""

    def __init__(self, output_png: str):
        self.output_png = output_png

    def generate(self, svgs: Dict[str, str]):
        if shutil.which("rsvg-convert") is None:
            raise RuntimeError(
                "Không tìm thấy 'rsvg-convert'. Cài bằng: "
                "brew install librsvg (macOS) hoặc sudo apt-get install librsvg2-bin (Linux)."
            )

        tmp = tempfile.mkdtemp()
        thumbs = []
        for i, (slot, svg) in enumerate(svgs.items()):
            svg_path = os.path.join(tmp, f"{i:02d}.svg")
            png_path = os.path.join(tmp, f"{i:02d}.png")
            with open(svg_path, "w", encoding="utf-8") as f:
                f.write(svg)
            subprocess.run(["rsvg-convert", "-w", "380", svg_path, "-o", png_path], check=True)

            img = Image.open(png_path).convert("RGB")
            canvas = Image.new("RGB", (img.width, img.height + 24), "white")
            canvas.paste(img, (0, 0))
            draw = ImageDraw.Draw(canvas)
            font = ImageFont.load_default()
            bbox = draw.textbbox((0, 0), slot, font=font)
            tw = bbox[2] - bbox[0]
            draw.text(((canvas.width - tw) // 2, img.height + 5), slot, fill="black", font=font)
            thumbs.append(canvas)

        cols, rows, pad = 3, (len(thumbs) + 2) // 3, 8
        cell_w = max(t.width for t in thumbs) if thumbs else 380
        cell_h = max(t.height for t in thumbs) if thumbs else 200
        sheet = Image.new("RGB", (cols * cell_w + (cols + 1) * pad, rows * cell_h + (rows + 1) * pad), "white")
        for idx, t in enumerate(thumbs):
            r, c = divmod(idx, cols)
            sheet.paste(t, (pad + c * (cell_w + pad), pad + r * (cell_h + pad)))
        sheet.save(self.output_png)
        print(f"       -> Đã xuất ảnh kiểm tra sanity check: {self.output_png}")
