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


# RAG 확인
- LLM: kakaocorp/kanana-nano-2.1b-instruct (https://huggingface.co/kakaocorp/kanana-nano-2.1b-instruct)
  - Temperature: 0.5
  - max_tokens: 4096    

- Q. mcp 에 대해서 알려줘
- Retriever.

| 파일명     | chunk |
|------------|-----------|
| **20109.md** | **배포 및 DNS 설정**<br>- Heroku 배포 자동화 진행, 일부 구버전 API 사용 문제는 문서 링크로 해결<br>- GoDaddy 도메인 연결 과정(버튼 위치, 입력 값)까지 상세 안내하여 손쉽게 설정 완료<br>- AI 도구로서의 Windsurf 사용 경험 공유 |
| **20721.md** | **WinDBG(CDB) 파이썬 제어 및 MCP 프로토콜 서버 래핑**<br>- WinDBG(CDB)를 파이썬으로 제어하고, AI가 활용할 수 있도록 MCP 서버로 래핑<br>- MCP는 Anthropic이 개발한 AI-외부 도구 통신 표준<br>- **MCP 장점**:<br>  • 모든 AI 모델에서 사용 가능<br>  • VS Code 외 환경에서도 독립 실행 가능<br>  • 비플랫폼 종속적<br>  • 빠른 기능 확장성 확보 |
| **19987.md** | **Playwright MCP**<br>- LLM을 위한 웹 브라우저 자동화 MCP 서버 구현 |
| **21155.md** | **Model Context Protocol(MCP) 지원 예정**<br>- LLM이 툴에 접근하는 새로운 표준 프로토콜로 급부상<br>- 최근 8일 내 OpenAI, Anthropic, Mistral 등 대형 벤더 API에 빠르게 도입<br>- 향후 LLM을 MCP 클라이언트로 만들어 다양한 MCP 서버에 쉽게 연동 계획 |
| **20430.md** | **Claude Code 보안 설계**<br>- 파일 쓰기, bash 실행, MCP 도구 사용 등 시스템 변경 작업 시 기본적으로 사용자 승인 요청<br>- 보안 강화를 위한 보수적 설계<br>- 안전하다고 판단되는 도구는 허용 목록(allowlist)에 사전 등록 가능<br>- 허용 도구 설정 방법 포함 |
- A. **Model Context Protocol (MCP)**은 인공지능(AI) 모델과 외부 도구 간의 상호작용을 표준화하고 효율적으로 관리하기 위해 개발된 프로토콜입니다. 이 프로토콜은 AI 모델이 다양한 외부 도구를 사용할 수 있도록 하여, AI 시스템의 기능을 확장하고, 사용자 경험을 개선하며, 보안을 강화하는 것을 목표로 합니다. MCP는 AI와 도구 간의 통신을 단순화하고, 다양한 환경에서 일관된 방식으로 작동하도록 설계되었습니다. 다음은 MCP의 주요 특징과 장점입니다.

### 주요 특징

1. **표준화된 통신 방식**:
   - MCP는 AI 모델과 도구 간의 통신을 표준화하여 다양한 환경과 플랫폼에서 일관된 방식으로 동작합니다. 이를 통해 호환성을 높이고, 개발 및 유지보수를 용이하게 합니다.

2. **모든 AI 모델 지원**:
   - MCP는 모든 AI 모델에서 사용할 수 있도록 설계되었습니다. 이는 OpenAI의 GPT, Anthropic의 Alpaca, Mistral 등 다양한 AI 모델과 호환됩니다.

3. **VS Code 외 환경 독립 실행 가능**:
   - MCP는 VS Code 외의 다양한 개발 환경에서도 독립적으로 작동할 수 있습니다. 이는 사용자가 특정 IDE에 종속되지 않고, 다양한 환경에서 AI 도구를 사용할 수 있게 합니다.

4. **비플랫폼 종속적**:
   - MCP는 특정 플랫폼이나 IDE에 종속되지 않습니다. 이는 다양한 운영 체제와 개발 환경에서 동일한 기능을 제공할 수 있음을 의미합니다.

5. **빠른 기능 확장성 확보**:
   - MCP는 새로운 도구와 기능을 쉽게 추가할 수 있는 확장성을 제공합니다. 이는 AI 시스템의 기능을 지속적으로 확장하고, 새로운 요구사항에 대응할 수 있게 합니다.

### 장점

1. **통합성**:
   - AI 모델과 다양한 도구를 쉽게 통합할 수 있어, 개발자가 더 빠르게 새로운 기능을 구현할 수 있습니다.

2. **보안**:
   - 기본적으로 사용자 승인 요청을 통해 보안을 강화합니다. 안전하다고 판단된 도구는 허용 목록(allowlist)을 통해 사전 승인할 수 있습니다.

3. **유연성**:
   - 다양한 맥락과 상황에서 유연하게 도구를 사용할 수 있습니다. 이는 특히 AI가 다양한 작업을 수행할 때 유용합니다.

4. **일관성**:
   - 표준화된 프로토콜을 통해 통신 방식이 일관되게 유지되어, 개발자와 사용자가 예측 가능하게 동작하는 시스템을 경험할 수 있습니다.

### 예시 사용 사례

- **AI 기반 자동화**:
  - Playwright MCP를 통해 LLM이 웹 브라우저를 자동화할 수 있습니다. 이를 통해 다양한 웹 페이지를 쉽게 탐색하고, 데이터를 수집하며, 자동화된 작업을 수행할 수 있습니다.
  
- **AI 도구 통합**:
  - MCP를 통해 AI 모델이 WinDBG(CDB)와 같은 외부 도구를 제어할 수 있습니다. 이를 통해 보다 정교한 디버깅과 테스트가 가능해집니다.

- **보안**:
  - AI 모델이 시스템을 안전하게 변경할 수 있도록 허용 목록(allowlist)을 통해 승인된 도구만 사용할 수 있게 보안을 강화합니다.

### 결론

MCP는 AI와 도구 간의 상호작용을 표준화하고, 다양한 환경에서 일관된 방식으로 동작할 수 있도록 설계된 프로토콜입니다. 이는 AI 시스템의 기능 확장성, 보안, 그리고 유연성을 크게 향상시키며, 다양한 도구와의 통합을 쉽게 만듭니다. 앞으로도 MCP는 AI와 도구 간의 상호작용을 더욱 효율적이고 안전하게 만들어 줄 것으로 기대됩니다.


