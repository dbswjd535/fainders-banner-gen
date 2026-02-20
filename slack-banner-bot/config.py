# -*- coding: utf-8 -*-
"""배너 봇 설정 (경로, 폰트, 템플릿)"""
import os

# 프로젝트 루트
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 배너 크기 (노션 배너)
BANNER_WIDTH = 1500
BANNER_HEIGHT = 600

# 배경 템플릿 PNG (3종) — templates 폴더에 template1.png, template2.png, template3.png 배치
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
TEMPLATE_PATHS = [
    os.path.join(TEMPLATES_DIR, "template1.png"),
    os.path.join(TEMPLATES_DIR, "template2.png"),
    os.path.join(TEMPLATES_DIR, "template3.png"),
]

# Fainders.ai 로고 이미지 (PNG 권장, 투명 배경)
LOGO_PATH = os.path.join(BASE_DIR, "assets", "logo.png")

# 폰트: Pretendard (브랜드 폰트로 Pretendard 사용)
# https://github.com/orioncactus/pretendard 에서 다운로드 후 아래 경로에 배치
FONTS_DIR = os.path.join(BASE_DIR, "assets", "fonts")
FONT_PATH = os.path.join(FONTS_DIR, "Pretendard-Regular.otf")
FONT_PATH_TTF = os.path.join(FONTS_DIR, "Pretendard-Regular.ttf")

def get_font_path():
    """설치된 Pretendard 경로 반환 (otf 우선, 없으면 ttf)."""
    if os.path.isfile(FONT_PATH):
        return FONT_PATH
    if os.path.isfile(FONT_PATH_TTF):
        return FONT_PATH_TTF
    return None
