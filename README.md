# Cluster 환경에서 Pod 배치

| 노드풀      | 노드 개수  | 배치되는 Pod                                                          |
| -------- | ------ | ----------------------------------------------------------------- |
| **cpu1** | 1      | rag-controller                                                    |
| **gpu1** | 1      | **Embedding** Pod + **Milvus**(Helm chart로 배포, nodeSelector=gpu1) |
| **gpu2** | 1 (사용) | LLM(vLLM) Pod                                                     |
| **gpu2** | 1 (비움) | 없음 (empty)       

# Vector DB 구성
- Milvus

## md2json
- chunk 길이: 200
- chunk overlap 길이: 20
- 분할자: "\n\n"
---
- 원본데이터를 규격화 하여 저장
<img width="1145" height="728" alt="스크린샷 2025-08-09 오후 9 05 57" src="https://github.com/user-attachments/assets/ce4de905-299b-48d5-9bce-939c9a96b478" />

## json2vectordb
- Embedding: Qwen/Qwen3-Embedding-0.6B (https://huggingface.co/Qwen/Qwen3-Embedding-0.6B)
- Retriever: Hybrid Search  
  - Sparse Vector (키워드 벡터) & Dense Vector (의미 벡터) 조합하여 유사도 측정  
    - Sparse Vector: Cosine 유사도 (Milvus IP + L2 정규화)
      - chunk 컬럼을 통해 Vector DB Insert 시, 연산
    - Dense Vector: BM25 유사도 (TF-IDF 와 유사)

# Vector DB 확인
<img width="1510" height="807" alt="스크린샷 2025-08-09 오후 9 01 52" src="https://github.com/user-attachments/assets/15189920-48df-4cd3-a562-8b6c03492b5e" />
<img width="1510" height="807" alt="스크린샷 2025-08-09 오후 9 02 10" src="https://github.com/user-attachments/assets/97cf25b6-b422-4134-ba57-71b8eeb3bdbc" />
<img width="1510" height="807" alt="스크린샷 2025-08-09 오후 9 02 43" src="https://github.com/user-attachments/assets/320dba35-869f-4e78-9b85-c720cb179b6d" />


# Vector DB 검색 결과 확인
- Q. mcp 에 대해서 알려줘
- Retriever.

| 파일명     | chunk |
|------------|-----------|
| **20109.md** | **배포 및 DNS 설정**<br>- Heroku 배포 자동화 진행, 일부 구버전 API 사용 문제는 문서 링크로 해결<br>- GoDaddy 도메인 연결 과정(버튼 위치, 입력 값)까지 상세 안내하여 손쉽게 설정 완료<br>- AI 도구로서의 Windsurf 사용 경험 공유 |
| **20721.md** | **WinDBG(CDB) 파이썬 제어 및 MCP 프로토콜 서버 래핑**<br>- WinDBG(CDB)를 파이썬으로 제어하고, AI가 활용할 수 있도록 MCP 서버로 래핑<br>- MCP는 Anthropic이 개발한 AI-외부 도구 통신 표준<br>- **MCP 장점**:<br>  • 모든 AI 모델에서 사용 가능<br>  • VS Code 외 환경에서도 독립 실행 가능<br>  • 비플랫폼 종속적<br>  • 빠른 기능 확장성 확보 |
| **19987.md** | **Playwright MCP**<br>- LLM을 위한 웹 브라우저 자동화 MCP 서버 구현 |
| **21155.md** | **Model Context Protocol(MCP) 지원 예정**<br>- LLM이 툴에 접근하는 새로운 표준 프로토콜로 급부상<br>- 최근 8일 내 OpenAI, Anthropic, Mistral 등 대형 벤더 API에 빠르게 도입<br>- 향후 LLM을 MCP 클라이언트로 만들어 다양한 MCP 서버에 쉽게 연동 계획 |
| **20430.md** | **Claude Code 보안 설계**<br>- 파일 쓰기, bash 실행, MCP 도구 사용 등 시스템 변경 작업 시 기본적으로 사용자 승인 요청<br>- 보안 강화를 위한 보수적 설계<br>- 안전하다고 판단되는 도구는 허용 목록(allowlist)에 사전 등록 가능<br>- 허용 도구 설정 방법 포함 |


