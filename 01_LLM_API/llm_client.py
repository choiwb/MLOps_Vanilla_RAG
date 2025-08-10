# pip install openai>=1.40
import os
from openai import OpenAI

BASE_URL = os.getenv("VLLM_BASE_URL", "http://vllm.poc-kanana-rag.svc.cluster.local:8082/v1")
API_KEY  = os.getenv("LLM_API_KEY", "EMPTY")  # vLLM에선 ANY/EMPTY 허용

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

rag_context = ["""배포 및 DNS 설정
 Heroku 배포 자동화, 일부 구버전 API 사용 문제는 문서 링크로 해결
 GoDaddy 도메인 연결도 버튼 누를 위치와 값까지 알려줘 손쉽게 설정 완료
 AI 도구로서의 Windsurf 사용 경험""",
 """WinDBG(CDB)를 파이썬으로 제어하며, 이를 AI가 사용할 수 있도록 MCP 프로토콜 서버로 래핑함
 MCP는 Anthropic이 개발한 AI와 외부 도구 간의 통신 표준으로, 툴을 AI의 손처럼 사용할 수 있게 해줌
 MCP의 장점:
 모든 AI 모델에서 사용 가능
 VS Code 외 환경에서도 독립 실행 가능
 비플랫폼 종속적
 빠른 기능 확장성 확보""",
 """Playwright MCP - LLM을 위한 웹 브라우저 자동화용 MCP 서버""",
 """Model Context Protocol (MCP) 지원 예정
 MCP는 LLM이 툴에 접근하는 새로운 표준 프로토콜로 급부상
 지난 8일 내에 OpenAI, Anthropic, Mistral 등 대형 벤더 API에도 빠르게 도입되고 있음
 향후 LLM을 MCP 클라이언트로 만들어 다양한 MCP 서버에 쉽게 연동 계획""",
 """Claude Code는 시스템을 변경할 수 있는 작업(파일 쓰기, bash 명령어 실행, MCP 도구 사용 등)에 대해 기본적으로 사용자 승인 요청을 함
이는 보안을 위한 보수적 설계이며, 사용자가 안전하다고 판단되는 도구는 허용 목록(allowlist) 을 통해 사전 승인 가능함
 허용 도구 설정 방법"""]

ctx_text = "\n\n".join(f"[{i+1}] {doc}" for i, doc in enumerate(rag_context))

query = "model context protocol 에 대해서 설명해줘"


# 1) Chat Completions (non-stream)
resp = client.chat.completions.create(
    model="kakaocorp/kanana-nano-2.1b-instruct",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user",   "content": f"CONTEXT: {ctx_text}\n\nQUESTION: {query}"}
    ],
    temperature=0.5,
    max_tokens=4096,
)
print(resp.choices[0].message.content)
