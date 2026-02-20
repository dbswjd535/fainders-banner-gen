# -*- coding: utf-8 -*-
"""
배경 템플릿 PNG 3종 생성 (1500x600).
실행 후 templates/ 폴더의 template1~3.png를 원하는 디자인으로 교체해 사용할 수 있습니다.
"""
import os
from PIL import Image, ImageDraw

# 프로젝트 루트 기준
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
os.makedirs(TEMPLATES_DIR, exist_ok=True)

W, H = 1500, 600

# 템플릿 1: 다크 그레이 + 그라데이션 느낌
def make_template1():
    img = Image.new("RGB", (W, H), (30, 32, 44))
    draw = ImageDraw.Draw(img)
    for i in range(H):
        r = int(30 + (50 - 30) * i / H)
        g = int(32 + (38 - 32) * i / H)
        b = int(44 + (60 - 44) * i / H)
        draw.line([(0, i), (W, i)], fill=(r, g, b))
    return img

# 템플릿 2: 네이비/퍼플 톤
def make_template2():
    img = Image.new("RGB", (W, H), (45, 42, 74))
    draw = ImageDraw.Draw(img)
    for i in range(H):
        r = int(45 + (60 - 45) * i / H)
        g = int(42 + (45 - 42) * i / H)
        b = int(74 + (95 - 74) * i / H)
        draw.line([(0, i), (W, i)], fill=(r, g, b))
    return img

# 템플릿 3: 차콜 + 블루 톤
def make_template3():
    img = Image.new("RGB", (W, H), (40, 48, 70))
    draw = ImageDraw.Draw(img)
    for i in range(H):
        r = int(40 + (55 - 40) * i / H)
        g = int(48 + (58 - 48) * i / H)
        b = int(70 + (90 - 70) * i / H)
        draw.line([(0, i), (W, i)], fill=(r, g, b))
    return img

def main():
    make_template1().save(os.path.join(TEMPLATES_DIR, "template1.png"))
    make_template2().save(os.path.join(TEMPLATES_DIR, "template2.png"))
    make_template3().save(os.path.join(TEMPLATES_DIR, "template3.png"))
    print(f"템플릿 3개 생성 완료: {TEMPLATES_DIR}")

if __name__ == "__main__":
    main()
