# 슬랙 배너 봇 (Fainders.ai)

팀원이 `/banner [문구]`를 입력하면 **1500×600** 노션 스타일 배너 이미지를 생성해 슬랙 채널에 업로드하는 봇입니다.  
Fainders.ai 브랜드 폰트(Pretendard)와 로고가 포함됩니다.

---

## 1. Slack API 설정 (단계별)

### 1단계: Slack 앱 만들기

1. [Slack API 앱 페이지](https://api.slack.com/apps) 접속 후 **Create New App** 클릭  
2. **From scratch** 선택  
3. **App Name**: 예) `배너 봇`  
4. **Workspace**: 사용할 슬랙 워크스페이스 선택 후 **Create App** 클릭  

### 2단계: Socket Mode 켜기

1. 왼쪽 메뉴에서 **Socket Mode** 클릭  
2. **Enable Socket Mode**를 **On**으로 변경  
3. **App-Level Token** 생성:
   - **Generate Token and Scopes** 클릭  
   - **Token Name**: 예) `banner-bot`  
   - **Scope**에 **`connections:write`** 추가 후 **Generate**  
   - 표시되는 **xapp-...** 토큰을 복사해 두기 → 이게 **SLACK_APP_TOKEN** 입니다  

### 3단계: Bot Token Scopes 추가

1. 왼쪽 메뉴 **OAuth & Permissions** 이동  
2. **Scopes** → **Bot Token Scopes**에서 **Add an OAuth Scope** 클릭 후 아래 추가:
   - **`chat:write`** — 채널에 메시지/파일 전송  
   - **`files:write`** — 파일 업로드  
   - **`commands`** — 슬래시 커맨드 사용  
   - **`chat:write.public`** — (선택) 봇이 초대되지 않은 채널에도 메시지 전송 시  

### 4단계: 워크스페이스에 앱 설치

1. **OAuth & Permissions** 페이지 상단에서 **Install to Workspace** 클릭  
2. 권한 확인 후 **Allow**  
3. **Bot User OAuth Token** (xoxb-로 시작) 복사 → 이게 **SLACK_BOT_TOKEN** 입니다  

### 5단계: 슬래시 커맨드 등록

1. 왼쪽 메뉴 **Slash Commands** 클릭  
2. **Create New Command**  
3. 입력:
   - **Command**: `/banner`  
   - **Short Description**: 예) `노션 스타일 배너 이미지 생성`  
   - **Usage Hint**: 예) `[배너 문구] [1|2|3]`  
4. **Save**  

### 6단계: 토큰 정리

| 환경 변수 | 값 | 설명 |
|-----------|-----|------|
| **SLACK_APP_TOKEN** | `xapp-...` | Socket Mode용 App-Level Token (1단계에서 생성) |
| **SLACK_BOT_TOKEN** | `xoxb-...` | Bot User OAuth Token (워크스페이스 설치 후 발급) |

---

## 2. 로컬 환경 설정

### 의존성 설치

```bash
cd slack-banner-bot
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 환경 변수 설정

**방법 A: 터미널에서 직접**

```bash
export SLACK_APP_TOKEN="xapp-1-..."
export SLACK_BOT_TOKEN="xoxb-..."
python app.py
```

**방법 B: `.env` 파일 사용 (권장)**

1. 프로젝트 루트에 `.env` 파일 생성:

```env
SLACK_APP_TOKEN=xapp-1-XXXX-...
SLACK_BOT_TOKEN=xoxb-XXXX-...
```

2. `python-dotenv`를 쓰고 싶다면 `pip install python-dotenv` 후 `app.py` 상단에 다음 추가:

```python
from dotenv import load_dotenv
load_dotenv()
```

---

## 3. 폰트·로고·템플릿 준비

### Pretendard 폰트 (필수)

1. [Pretendard 릴리스](https://github.com/orioncactus/pretendard/releases)에서 **Variable** 또는 **Static** OTF/TTF 다운로드  
2. `assets/fonts/` 폴더에 다음 중 하나로 저장:
   - `Pretendard-Regular.otf`  
   - 또는 `Pretendard-Regular.ttf`  

### Fainders.ai 로고 (선택)

- `assets/logo.png`에 투명 배경 PNG 로고를 넣으면 배너 **우측 하단**에 자동으로 붙습니다.  
- 없어도 배너는 생성됩니다.

### 배경 템플릿 3종 (선택)

- 기본으로 **스크립트로 생성한 단색 배경**을 쓰거나,  
- 원하는 PNG를 직접 사용하려면:

```bash
python scripts/create_templates.py
```

위 명령으로 `templates/template1.png`, `template2.png`, `template3.png`를 생성한 뒤,  
원하는 디자인 PNG(1500×600 권장)로 교체하면 됩니다.

---

## 4. 사용법

### 봇 실행

```bash
python app.py
```

콘솔에 `Bolt app is running!` 이 보이면 준비 완료입니다.

### 슬랙에서 사용

- **기본**: `/banner 우리 팀을 소개합니다`  
  → 문구가 배너 중앙에 들어가고, 배경은 템플릿 1번이 사용됩니다.  

- **템플릿 선택**: `/banner 새 프로젝트 오픈 2`  
  → 문구는 "새 프로젝트 오픈", 배경은 2번 템플릿.  

- **템플릿 3번**: `/banner Fainders.ai 3`  

생성된 **1500×600** 배너 이미지가 해당 채널에 파일로 업로드됩니다.

---

## 5. 프로젝트 구조

```
slack-banner-bot/
├── app.py              # 슬랙 봇 진입점 (/banner 처리, 파일 업로드)
├── config.py           # 배너 크기, 템플릿/로고/폰트 경로
├── banner_generator.py # 1500x600 배너 이미지 생성 (PIL)
├── requirements.txt
├── README.md
├── assets/
│   ├── logo.png        # Fainders.ai 로고 (선택)
│   └── fonts/
│       └── Pretendard-Regular.otf  # 또는 .ttf
├── templates/
│   ├── template1.png  # 배경 1
│   ├── template2.png  # 배경 2
│   └── template3.png  # 배경 3
└── scripts/
    └── create_templates.py  # 기본 템플릿 PNG 생성
```

---

## 6. 트러블슈팅

- **"missing_scope"**  
  → **OAuth & Permissions**에서 봇에 `files:write`, `chat:write`, `commands` 스코프가 추가되었는지 확인 후, **Reinstall to Workspace** 한 번 더 실행  

- **슬래시 커맨드가 안 보임**  
  → **Slash Commands**에서 `/banner`가 등록되었는지, 해당 채널에 앱이 초대되었는지 확인  

- **한글이 깨짐**  
  → `assets/fonts/`에 Pretendard가 제대로 설치되었는지 확인 (파일명: `Pretendard-Regular.otf` 또는 `.ttf`)  

- **Socket Mode 연결 실패**  
  → `SLACK_APP_TOKEN`이 `xapp-`로 시작하는 App-Level Token인지, Socket Mode가 **On**인지 확인  

---

이 설정을 마치면 팀원은 슬랙에서 `/banner [문구]`만 입력해 1500×600 노션 스타일 배너를 바로 받을 수 있습니다.
