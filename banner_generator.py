"""
Fainders.ai 사내 배너 생성기 - Pillow 기반 이미지 생성 모듈
제목/부제목, 템플릿 배경, Pretendard 폰트 지원
"""
from PIL import Image, ImageDraw, ImageFont
import io
import os

BANNER_WIDTH = 1500
BANNER_HEIGHT = 600

# 부제목 컬러 옵션
SUB_TITLE_COLORS = {
    "#5BE444": (91, 228, 68),
    "#17CF81": (23, 207, 129),
    "#4A9DF7": (74, 157, 247),
}


def _find_pretendard_path(weight: str = "regular") -> str | None:
    """시스템에 설치된 Pretendard 폰트 경로 탐색 (Bold / Medium / Regular)"""
    weight_map = {
        "bold": ["Pretendard-Bold.otf", "Pretendard-Bold.ttf", "PretendardBold.otf", "PretendardBold.ttf"],
        "medium": ["Pretendard-Medium.otf", "Pretendard-Medium.ttf", "PretendardMedium.otf", "PretendardMedium.ttf"],
        "regular": ["Pretendard-Regular.otf", "Pretendard-Regular.ttf", "Pretendard.otf", "Pretendard.ttf"],
    }
    names = weight_map.get(weight.lower(), weight_map["regular"])
    search_dirs = [
        os.path.expanduser("~/Library/Fonts"),
        "/Library/Fonts",
        "/System/Library/Fonts",
        "/System/Library/Fonts/Supplemental",
    ]
    for d in search_dirs:
        if not os.path.isdir(d):
            continue
        for name in names:
            path = os.path.join(d, name)
            if os.path.isfile(path):
                return path
        for f in os.listdir(d):
            if "retendard" in f.lower() and (".otf" in f or ".ttf" in f):
                if weight == "bold" and ("bold" in f.lower() or "Bold" in f):
                    return os.path.join(d, f)
                if weight == "medium" and ("medium" in f.lower() or "Medium" in f):
                    return os.path.join(d, f)
                if weight == "regular" and ("regular" in f.lower() or "Regular" in f or ("bold" not in f.lower() and "Bold" not in f and "medium" not in f.lower() and "Medium" not in f)):
                    return os.path.join(d, f)
    return None


def get_font(size: int, weight: str = "regular") -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Pretendard 우선, 없으면 한글 지원 시스템 폰트로 로드
    weight: 'bold', 'medium', 'regular'
    """
    path = _find_pretendard_path(weight=weight)
    if path:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            pass
    fallback = [
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",
        "/System/Library/Fonts/Supplemental/AppleGothic.ttf",
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "C:\\Windows\\Fonts\\malgun.ttf",
    ]
    for p in fallback:
        if os.path.isfile(p):
            try:
                return ImageFont.truetype(p, size)
            except OSError:
                continue
    return ImageFont.load_default()


def _load_template(template_name: str, templates_dir: str = ".") -> Image.Image:
    """템플릿 이미지 로드. 없으면 그레이 배경 생성"""
    path = os.path.join(templates_dir, template_name)
    if os.path.isfile(path):
        img = Image.open(path).convert("RGBA")
        if img.size != (BANNER_WIDTH, BANNER_HEIGHT):
            img = img.resize((BANNER_WIDTH, BANNER_HEIGHT), Image.Resampling.LANCZOS)
        return img
    # 템플릿 없을 때: 깔끔한 그레이 배경
    base = Image.new("RGBA", (BANNER_WIDTH, BANNER_HEIGHT), (245, 245, 247, 255))
    return base


def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """#RRGGBB -> (r,g,b)"""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def create_banner(
    main_title: str,
    sub_title: str,
    sub_title_color: str,
    template_name: str,
    templates_dir: str = ".",
) -> bytes:
    """
    제목/부제목과 템플릿으로 1500x600 배너 이미지를 생성해 PNG 바이트를 반환합니다.
    - 제목: 중앙 정렬, 110pt, Pretendard Bold
    - 부제목: 제목 위로 70px, 67px, Pretendard Medium, 선택 컬러
    - 배경: 지정 템플릿 (temp1.png, temp2.png, temp3.png) 또는 기본 배경
    """
    bg = _load_template(template_name, templates_dir)
    if bg.mode != "RGBA":
        bg = bg.convert("RGBA")
    base = Image.new("RGBA", (BANNER_WIDTH, BANNER_HEIGHT), (255, 255, 255, 0))
    base.paste(bg, (0, 0))
    draw = ImageDraw.Draw(base)

    # 제목: 중앙 정렬, 110pt, Pretendard Bold
    title_font_size = 110
    title_font = get_font(title_font_size, weight="bold")
    title_color = (40, 40, 42, 255)

    # 부제목: 67px, Pretendard Medium
    sub_font_size = 67
    sub_font = get_font(sub_font_size, weight="medium")
    sub_rgb = SUB_TITLE_COLORS.get(sub_title_color, SUB_TITLE_COLORS["#5BE444"])
    sub_color = (*sub_rgb, 255)

    # 제목을 중앙에 배치 (세로 중앙 기준)
    center_y = BANNER_HEIGHT // 2

    # 제목 먼저 그리기 (/) 기준으로 줄바꿈)
    if main_title.strip():
        title_text = main_title.strip()
        # (/) 기준으로 줄 나누기, "/" 문자는 표시하지 않음
        lines = [line.strip() for line in title_text.split("/") if line.strip()]
        if not lines:
            lines = [title_text]
        
        # 각 줄의 높이 계산
        line_height = 0
        line_widths = []
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=title_font)
            line_height = max(line_height, bbox[3] - bbox[1])
            line_widths.append(bbox[2] - bbox[0])
        
        # 전체 제목 높이 (줄 간격 포함)
        line_spacing = 10
        total_height = line_height * len(lines) + line_spacing * (len(lines) - 1)
        
        # 제목을 세로 중앙에 배치 (텍스트 상단 기준)
        y_title_draw = center_y - total_height // 2
        
        # 각 줄 그리기
        for idx, line in enumerate(lines):
            x_title = (BANNER_WIDTH - line_widths[idx]) // 2
            y_line = y_title_draw + idx * (line_height + line_spacing)
            draw.text((x_title, y_line), line, fill=title_color, font=title_font)
        
        title_top = y_title_draw  # 제목의 상단 위치
        th = total_height
    else:
        th = 0
        title_top = center_y

    # 부제목: 제목 위로 70px (제목 상단에서 70px 위에 부제목 하단 배치)
    if sub_title.strip():
        bbox_sub = draw.textbbox((0, 0), sub_title, font=sub_font)
        sw = bbox_sub[2] - bbox_sub[0]
        sh = bbox_sub[3] - bbox_sub[1]
        x_sub = (BANNER_WIDTH - sw) // 2
        # 제목 상단에서 70px 위에 부제목의 하단이 위치하도록
        y_sub = title_top - 70 - sh
        draw.text((x_sub, y_sub), sub_title, fill=sub_color, font=sub_font)

    # RGB로 저장 (투명 배경이면 흰색으로 합성)
    out = Image.new("RGB", (BANNER_WIDTH, BANNER_HEIGHT), (255, 255, 255))
    out.paste(base, (0, 0), base)

    buf = io.BytesIO()
    out.save(buf, format="PNG")
    buf.seek(0)
    return buf.getvalue()
