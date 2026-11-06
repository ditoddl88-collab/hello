# Image 2.6 for Codex Cloud

Python 3.10+ 표준 라이브러리만 사용합니다. 추가 패키지 설치는 필요 없습니다.

## 실행

실행 환경의 보안 자격 증명 설정에서 `OPENAI_API_KEY`를 제공하세요.
키를 채팅, 소스 코드, GitHub 저장소 또는 로그에 붙여 넣지 마세요.
이 도구는 .env 파일을 자동으로 읽지 않습니다.

```bash
python tools/image26.py --prompt "따뜻한 수채화 스타일의 서울 풍경" --output outputs/seoul.png
python tools/image26.py --model gpt-image-2.6-flare --prompt "앱 배경용 푸른 파도" --output outputs/waves.png
python tools/image26.py --prompt-file prompt.txt --output outputs/custom.png
```

기본 모델은 `gpt-image-2.6-sunburst`입니다. API 사용에는 별도 요금과 해당 모델 접근 권한이 필요합니다.
기존 출력 파일은 덮어쓰지 않습니다. 이 도구는 새 PNG 생성용이며 이미지 편집은 포함하지 않습니다.

요금 없이 요청 내용만 확인:
```bash
python tools/image26.py --prompt "테스트 이미지" --dry-run
```

## Codex Cloud

1. 이 저장소를 Cloud 환경에 연결하고 최신 main 브랜치를 사용합니다.
2. 실행 단계에서 `OPENAI_API_KEY`를 사용할 수 있도록 환경의 자격 증명 기능을 설정합니다.
3. 실행 단계에서 `api.openai.com`으로 HTTPS 접속을 허용합니다.
4. 채팅에서 “tools/image26.py로 Image 2.6 이미지를 생성하고 outputs에 저장해줘”라고 요청합니다.

Legacy Codex Cloud의 Secrets는 setup 단계에만 제공되며 에이전트 실행 전 제거됩니다.
그 경우 Secrets에 키를 넣는 것만으로는 이 도구를 에이전트 단계에서 실행할 수 없습니다.
실행 시 자격 증명을 안전하게 제공할 수 있는 Cloud 환경 또는 로컬 환경에서 사용하세요.
키를 파일에 복사해서 이 제한을 우회하지 마세요.

저장소 추가만으로 계정의 Cloud 네트워크나 자격 증명 설정이 바뀌지는 않습니다.
Codex 내장 이미지 생성 모델을 변경하지도 않습니다.

## 공식 문서

- https://developers.openai.com/api/docs/models/gpt-image-2.6-sunburst
- https://developers.openai.com/api/reference/resources/images/methods/generate
- https://learn.chatgpt.com/docs/environments/cloud-environment
