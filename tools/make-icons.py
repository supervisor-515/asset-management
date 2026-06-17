#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
자산관리 PWA 아이콘 생성 스크립트.

산출물(저장소 루트):
  - icon-192.png          : 일반 아이콘 192x192
  - icon-512.png          : 일반 아이콘 512x512
  - icon-maskable-512.png : 안드로이드 어댑티브(maskable) 아이콘 512x512

안드로이드 어댑티브 아이콘은 원/스쿼클로 마스킹되므로 maskable 아이콘은
심볼을 가운데 안전영역(중앙 80%) 안에 배치하고 가장자리 여백을 충분히 둔다.

재생성:
    pip install pillow
    python3 tools/make-icons.py
"""

import os
from PIL import Image, ImageDraw, ImageFont

# 디자인 토큰 (앱 테마와 일치)
INK = (58, 74, 63)        # #3A4A3F  올리브 잉크 (theme_color / maskable 배경)
PAPER = (251, 247, 239)   # #FBF7EF  페이퍼 (일반 아이콘 배경)
GOLD = (193, 154, 76)     # #C19A4C  포인트 골드
IVORY = (245, 238, 224)   # #F5EEE0  아이보리

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def find_font(size):
    """₩ 글리프를 가진 폰트를 찾는다. 없으면 도형 폴백을 쓴다."""
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return None


def glyph_has_won(font):
    """폰트에 원화 기호(₩)가 있는지 대략 확인."""
    if font is None:
        return False
    try:
        mask = font.getmask("₩")
        return mask.getbbox() is not None
    except Exception:
        return False


def draw_won_symbol(draw, cx, cy, scale, color):
    """폰트에 ₩가 없을 때 막대그래프형 폴백 심볼을 그린다."""
    bar_w = int(38 * scale)
    gap = int(26 * scale)
    base_y = cy + int(70 * scale)
    heights = [int(70 * scale), int(120 * scale), int(170 * scale)]
    total_w = 3 * bar_w + 2 * gap
    x0 = cx - total_w // 2
    for i, h in enumerate(heights):
        x = x0 + i * (bar_w + gap)
        draw.rounded_rectangle(
            [x, base_y - h, x + bar_w, base_y],
            radius=int(8 * scale),
            fill=color,
        )


def make_icon(size, bg, fg, symbol_ratio, rounded=True, maskable=False):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    if maskable:
        # 마스킹돼도 배경이 꽉 차도록 정사각형 배경
        draw.rectangle([0, 0, size, size], fill=bg)
    elif rounded:
        radius = int(size * 0.22)
        draw.rounded_rectangle([0, 0, size, size], radius=radius, fill=bg)
    else:
        draw.rectangle([0, 0, size, size], fill=bg)

    cx, cy = size // 2, size // 2
    font_size = int(size * symbol_ratio)
    font = find_font(font_size)

    if glyph_has_won(font):
        text = "₩"  # ₩
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        tx = cx - tw // 2 - bbox[0]
        ty = cy - th // 2 - bbox[1]
        draw.text((tx, ty), text, font=font, fill=fg)
    else:
        scale = size / 512.0
        draw_won_symbol(draw, cx, cy, scale, fg)

    return img


def main():
    # 일반 아이콘: 페이퍼 배경 + 골드 심볼, 둥근 사각형
    make_icon(192, INK, GOLD, 0.62, rounded=True).save(
        os.path.join(ROOT, "icon-192.png"))
    make_icon(512, INK, GOLD, 0.62, rounded=True).save(
        os.path.join(ROOT, "icon-512.png"))

    # maskable: 잉크 배경 꽉 채우고 심볼을 중앙 안전영역(작게)에 배치
    make_icon(512, INK, GOLD, 0.46, rounded=False, maskable=True).save(
        os.path.join(ROOT, "icon-maskable-512.png"))

    print("생성 완료:")
    for name in ("icon-192.png", "icon-512.png", "icon-maskable-512.png"):
        print("  -", os.path.join(ROOT, name))


if __name__ == "__main__":
    main()
