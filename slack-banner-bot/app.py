# -*- coding: utf-8 -*-
"""
슬랙 배너 봇: /banner [문구] 입력 시 1500x600 배너 생성 후 슬랙에 업로드.
Socket Mode 사용 (별도 공개 URL 없이 동작).
"""
import os
from dotenv import load_dotenv
load_dotenv()

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

import config
from banner_generator import generate_banner


# 환경 변수에서 토큰 로드 (README 참고)
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


def parse_banner_command(text: str):
    """
    '/banner [문구]' 또는 '/banner [문구] [템플릿번호]' 파싱.
    템플릿 번호 생략 시 1 사용.
    반환: (문구, 템플릿번호 1|2|3)
    """
    text = (text or "").strip()
    # 마지막 토큰이 숫자 1,2,3이면 템플릿 번호로 간주
    parts = text.split()
    template = 1
    if len(parts) >= 2 and parts[-1] in ("1", "2", "3"):
        template = int(parts[-1])
        phrase = " ".join(parts[:-1])
    else:
        phrase = text
    return phrase, template


@app.command("/banner")
def handle_banner(ack, command, client):
    ack()  # 3초 이내 응답 필수
    text = (command.get("text") or "").strip()
    channel_id = command["channel_id"]
    user_id = command["user_id"]

    if not text:
        client.chat_postEphemeral(
            channel=channel_id,
            user=user_id,
            text="사용법: `/banner [배너에 넣을 문구]` 또는 `/banner [문구] [1|2|3]` (1~3: 배경 템플릿 선택)",
        )
        return

    phrase, template_index = parse_banner_command(text)
    if not phrase:
        client.chat_postEphemeral(
            channel=channel_id,
            user=user_id,
            text="배너에 표시할 문구를 입력해 주세요. 예: `/banner 우리 팀 소개`",
        )
        return

    try:
        path = generate_banner(phrase, template_index=template_index)
        try:
            client.files_upload_v2(
                channel=channel_id,
                file=path,
                filename="banner.png",
                title=f"배너: {phrase[:50]}",
            )
        finally:
            if path and os.path.isfile(path) and path.startswith("/tmp") or "tmp" in path:
                try:
                    os.unlink(path)
                except Exception:
                    pass
    except Exception as e:
        client.chat_postEphemeral(
            channel=channel_id,
            user=user_id,
            text=f"배너 생성 중 오류가 났어요: {str(e)}",
        )


def main():
    # SLACK_APP_TOKEN (Socket Mode) 필요
    app_token = os.environ.get("SLACK_APP_TOKEN")
    if not app_token:
        print("환경 변수 SLACK_APP_TOKEN 이 필요합니다. README.md 설정 가이드를 확인하세요.")
        return
    if not os.environ.get("SLACK_BOT_TOKEN"):
        print("환경 변수 SLACK_BOT_TOKEN 이 필요합니다. README.md 설정 가이드를 확인하세요.")
        return
    handler = SocketModeHandler(app, app_token)
    handler.start()


if __name__ == "__main__":
    main()
