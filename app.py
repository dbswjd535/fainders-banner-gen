"""
Fainders.ai 사내 배너 생성기 - Streamlit 대시보드
왼쪽 사이드바: 배너 설정 | 메인: 실시간 미리보기 및 다운로드
"""
import streamlit as st
from banner_generator import create_banner

st.set_page_config(
    page_title="Fainders.ai 배너 생성기",
    page_icon="🟢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 커스텀 스타일: 화이트/그레이 톤, 세련된 UI
st.markdown(
    """
    <style>
    /* 메인 영역 배경 */
    .stApp { background-color: #f8f9fa; }
    /* 사이드바 배경 */
    [data-testid="stSidebar"] { background-color: #ffffff; }
    [data-testid="stSidebar"] .stMarkdown { color: #374151; }
    /* primary 버튼: 브랜드 컬러 #5BE444 */
    .stButton > button[kind="primary"] {
        background-color: #5BE444;
        color: #111827;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #4dd13a;
        color: #111827;
    }
    /* 미리보기 카드 영역 */
    div[data-testid="stImage"] { border-radius: 8px; }
    /* Notice 카드 */
    .notice-card {
        background-color: #F9F9F9;
        border-radius: 12px;
        padding: 1.5rem 1.75rem;
        margin-top: 1rem;
        border: 1px solid #eee;
    }
    .notice-card h3 { margin-top: 0; color: #374151; font-size: 1.1rem; }
    .notice-card p { margin: 0.5rem 0; color: #4b5563; line-height: 1.6; }
    .notice-card ul { margin: 0.5rem 0; padding-left: 1.25rem; color: #4b5563; line-height: 1.7; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----- 사이드바: 배너 설정 -----
with st.sidebar:
    st.markdown("### 파인더스 에이아이 사내 배너 생성기")
    st.markdown("---")

    main_title = st.text_input(
        "**제목 (Main Title)**",
        placeholder="예: 2025 신년 워크숍",
        max_chars=80,
    )
    st.markdown(
        '<p style="font-size:0.75rem; color:#878D97; margin-top:-0.5rem;">제목 입력 시, 줄바꿈 영역에 <strong>슬래시(/)</strong>를 입력해 주세요</p>',
        unsafe_allow_html=True,
    )

    sub_title = st.text_input(
        "**부제목 (Sub Title)**",
        placeholder="공지사항",
        max_chars=80,
    )

    color_names = {
        "#5BE444": "FAIGreen",
        "#17CF81": "FAI Mint",
        "#4A9DF7": "FAI Blue",
    }
    sub_title_color = st.radio(
        "**부제목 컬러**",
        options=["#5BE444", "#17CF81", "#4A9DF7"],
        format_func=lambda x: color_names[x],
        horizontal=False,
    )

    template_options = {
        "temp1.png": "FAIGreen",
        "temp2.png": "FAI Blue",
        "temp3.png": "FAI Mint",
    }
    template_choice = st.selectbox(
        "**배경 템플릿**",
        options=list(template_options.keys()),
        format_func=lambda x: template_options[x],
    )

    st.markdown("---")
    st.caption("설정 변경 시 미리보기가 자동으로 갱신됩니다.")

# ----- 메인 영역: 실시간 미리보기 및 다운로드 -----
st.markdown("## 배너 미리보기")
st.caption("1500 × 600 px · 생성된 배너를 확인한 뒤 다운로드하세요.")

try:
    png_bytes = create_banner(
        main_title=main_title or " ",
        sub_title=sub_title or " ",
        sub_title_color=sub_title_color,
        template_name=template_choice,
        templates_dir=".",
    )
except Exception as e:
    png_bytes = None
    st.error(f"배너 생성 중 오류: {e}")

if png_bytes:
    col_preview, col_dl = st.columns([3, 1])
    with col_preview:
        st.image(png_bytes, width=750)
    with col_dl:
        st.download_button(
            label="📥 배너_다운로드.png",
            data=png_bytes,
            file_name="배너_다운로드.png",
            mime="image/png",
            type="primary",
        )

# ----- Notice 섹션 -----
st.markdown("---")
st.markdown(
    """
    <div class="notice-card">
        <h2 style="margin:0 0 1rem 0; font-size:1.25rem; color:#374151;">📢 Fainders.ai 사내 배너 생성기 활용 가이드</h2>
        <p>Fainders.ai 구성원 여러분, 안녕하세요. 디자인팀입니다.</p>
        <p>팀원분들이 브랜드 가이드를 준수하면서도 간편하게 배너를 제작하실 수 있도록 '사내 배너 생성기'를 배포합니다.</p>
        <ul>
            <li>본 배너의 제작 사이즈(1500x600px)는 노션 커버 이미지와 완벽하게 호환되도록 설계되었습니다.</li>
            <li>노션 외에도 슬랙 공지, GWS(구글 워크스페이스) 등 다양한 사내 협업 툴에서 자유롭게 사용이 가능합니다.</li>
            <li>Fainders.ai의 브랜드 가이드 규정에 맞춰 주기적으로 템플릿과 기능을 업데이트할 예정입니다.</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)
