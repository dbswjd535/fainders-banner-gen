# -*- coding: utf-8 -*-
"""1500x600 노션 스타일 배너 이미지 생성 (Fainders.ai 브랜드 폰트·로고 포함)"""
import os
from PIL import Image, ImageDraw, ImageFont

import config


def _get_font(size: int):
    """Pretendard 폰트 로드. 없으면 기본 폰트 사용."""
    path = config.get_font_path()
    if path:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            pass
    return ImageFont.load_default()


def _load_background(template_index: int) -> Image.Image:
    """선택한 템플릿(1,2,3) 배경을 1500x600으로 로드."""
    idx = max(0, min(template_index, 2))  # 0, 1, 2
    path = config.TEMPLATE_PATHS[idx]
    if os.path.isfile(path):
        img = Image.open(path).convert("RGB")
        return img.resize((config.BANNER_WIDTH, config.BANNER_HEIGHT), Image.Resampling.LANCZOS)
    # 템플릿이 없으면 단색 배경 (개발용)
    colors = [(40, 42, 54), (68, 58, 89), (45, 52, 74)]  # 다크 톤
    img = Image.new("RGB", (config.BANNER_WIDTH, config.BANNER_HEIGHT), colors[idx])
    return img


def _draw_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont):
    """배너 중앙에 문구 그리기 (여백 고려)."""
    # 텍스트 bbox로 중앙 정렬
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = (config.BANNER_WIDTH - tw) // 2
    y = (config.BANNER_HEIGHT - th) // 2
    # 그림자(어두운 테두리) 후 메인 텍스트
    for dx, dy in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
        draw.text((x + dx, y + dy), text, font=font, fill=(0, 0, 0))
    draw.text((x, y), text, font=font, fill=(255, 255, 255))


def _paste_logo(banner: Image.Image) -> None:
    """우측 하단에 Fainders.ai 로고 오버레이."""
    if not os.path.isfile(config.LOGO_PATH):
        return
    try:
        logo = Image.open(config.LOGO_PATH).convert("RGBA")
    except Exception:
        return
    # 로고 최대 높이 120px 비율 유지
    max_h = 120
    r = min(1.0, max_h / logo.height)
    new_w = int(logo.width * r)
    new_h = int(logo.height * r)
    logo = logo.resize((new_w, new_h), Image.Resampling.LANCZOS)
    margin = 24
    x = config.BANNER_WIDTH - logo.width - margin
    y = config.BANNER_HEIGHT - logo.height - margin
    banner.paste(logo, (x, y), logo)


def generate_banner(text: str, template_index: int = 1, output_path: str = None) -> str:
    """
    배너 이미지 생성 후 파일로 저장.
    - text: 배너에 표시할 문구
    - template_index: 1, 2, 3 중 배경 템플릿 번호
    - output_path: 저장 경로 (None이면 임시 파일 생성)
    반환: 저장된 파일 경로
    """
    background = _load_background(template_index - 1)  # 1-based -> 0-based
    banner = background.copy()
    draw = ImageDraw.Draw(banner)

    # 폰트 크기: 문구 길이에 따라 조절 (최대 72, 최소 24)
    length = len(text)
    if length <= 10:
        font_size = 72
    elif length <= 20:
        font_size = 52
    else:
        font_size = max(24, 72 - (length - 20) * 2)
    font = _get_font(font_size)
    _draw_text(draw, text, font)
    _paste_logo(banner)

    if output_path is None:
        import tempfile
        fd, output_path = tempfile.mkstemp(suffix=".png")
        os.close(fd)
    banner.save(output_path, "PNG")
    return output_path
