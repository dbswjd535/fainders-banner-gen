# 파인더스 에이아이 사내 배너 생성기

Streamlit과 Pillow로 만든 사내 배너 이미지 생성 웹 앱입니다.

## 주요 기능

- **크기:** 1500 × 600 px (노션 커버 이미지 호환)
- **제목/부제목:** 제목은 Pretendard Bold 110pt, 부제목은 Pretendard Medium 67px
- **줄바꿈:** 제목 입력 시 `/`로 줄바꿈 가능
- **배경 템플릿:** FAIGreen, FAI Blue, FAI Mint 중 선택
- **부제목 컬러:** FAIGreen, FAI Mint, FAI Blue 중 선택

## 로컬 실행

```bash
# 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt

# 앱 실행
streamlit run app.py
```

브라우저에서 `http://localhost:8501` 로 접속합니다.

## 배포하기 (Streamlit Cloud)

### 1. GitHub에 코드 업로드

```bash
# Git 저장소 초기화 (아직 안 했다면)
git init
git add .
git commit -m "Initial commit: 배너 생성기"

# GitHub에 새 저장소 생성 후
git remote add origin https://github.com/사용자명/저장소명.git
git branch -M main
git push -u origin main
```

### 2. Streamlit Cloud에 배포

1. [Streamlit Cloud](https://share.streamlit.io/) 접속
2. "Sign in with GitHub" 클릭하여 GitHub 계정으로 로그인
3. "New app" 클릭
4. 다음 정보 입력:
   - **Repository**: 방금 올린 GitHub 저장소 선택
   - **Branch**: `main` (또는 `master`)
   - **Main file path**: `app.py`
5. "Deploy!" 클릭

### 3. 배포 완료!

배포가 완료되면 `https://사용자명-저장소명.streamlit.app` 형태의 URL이 생성됩니다.

이 URL을 팀원들과 공유하면 바로 사용할 수 있습니다! 🎉

## 템플릿 파일

프로젝트 폴더에 다음 템플릿 파일을 추가하세요:
- `temp1.png` → FAIGreen 배경
- `temp2.png` → FAI Blue 배경  
- `temp3.png` → FAI Mint 배경

각 파일은 1500×600px 크기로 준비하세요. 없어도 앱은 동작하며, 이 경우 기본 회색 배경이 사용됩니다.

## 프로젝트 구조

```
├── app.py                  # Streamlit 대시보드
├── banner_generator.py      # Pillow 배너 생성 로직
├── requirements.txt        # Python 패키지 의존성
├── .streamlit/
│   └── config.toml         # Streamlit 설정
├── temp1.png              # (직접 추가) FAIGreen 템플릿
├── temp2.png              # (직접 추가) FAI Blue 템플릿
├── temp3.png              # (직접 추가) FAI Mint 템플릿
└── README.md
```
