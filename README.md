# Cluster 환경에서 Pod 배치

| 노드풀 이름        | 노드 개수 | NodeSelector 라벨                                                           | 배포되는 파드(Pod)                                                                               | 주요 서비스/포트                                                                                                      | 비고                                                                  |
| ------------- | ----- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| **cpu1**      | 1     | `nodepool-name=cpu1`                                                      | **RAG Controller**                                                                         | `rag-controller` (ClusterIP, 8080)                                                                             | LLM, Milvus, Embedding 서비스 호출 및 전체 오케스트레이션 담당                       |
| **gpu1**      | 1     | - **Embedding**: `nodepool-name=gpu1`<br>- **Milvus(Helm)**: `system=vdb` | **Embedding 서비스** (8085)<br>**Milvus** (19530 gRPC)<br>**MinIO** (9000)<br>**etcd** (2379) | Milvus는 Helm chart로 배포되며 MinIO, etcd를 함께 구성. gpu1 노드가 두 라벨(`nodepool-name=gpu1`, `system=vdb`) 모두 있어야 동일 노드 배치 |                                                                     |
| **gpu2** (사용) | 1     | `nodepool-name=gpu2`, `gpu2-slot=llm`                                     | **LLM (vLLM)**                                                                             | `vllm` (ClusterIP, 8082 HTTP API)                                                                              | OpenAI 호환 API 제공, ConfigMap의 `LLM_OPENAI_BASE`로 RAG Controller에서 호출 |
| **gpu2** (비움) | 1     | `nodepool-name=gpu2` (추가 라벨 없음)                                           | 없음                                                                                         | 없음                                                                                                             | 확장 시 신규 LLM/Embedding 배치 가능                                         |


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
<img width="1512" height="759" alt="스크린샷 2025-08-10 오전 12 37 42" src="https://github.com/user-attachments/assets/300b3457-e10e-4835-85fe-5e43bafa5352" />

<img width="1512" height="759" alt="스크린샷 2025-08-10 오전 12 37 57" src="https://github.com/user-attachments/assets/5caca83c-0225-4b24-9f73-5e3579752f00" />

<img width="1512" height="759" alt="스크린샷 2025-08-10 오전 12 40 01" src="https://github.com/user-attachments/assets/15191290-441a-4c40-88fa-3ac36ddf0029" />


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


