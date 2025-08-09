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
- 원본데이터를 규격화 하여 저장
<img width="1145" height="728" alt="스크린샷 2025-08-09 오후 9 05 57" src="https://github.com/user-attachments/assets/ce4de905-299b-48d5-9bce-939c9a96b478" />

## json2vectordb
- Embedding: Qwen/Qwen3-Embedding-0.6B (https://huggingface.co/Qwen/Qwen3-Embedding-0.6B)
- Retriever: Hybrid Search (키워드 벡터 & 의미 벡터 조합하여 유사도 측정) -> 의미 벡터: 코사인 유사도, 키워드 벡터: BM25 유사도

# Vector DB 확인
<img width="1510" height="807" alt="스크린샷 2025-08-09 오후 9 01 52" src="https://github.com/user-attachments/assets/15189920-48df-4cd3-a562-8b6c03492b5e" />
<img width="1510" height="807" alt="스크린샷 2025-08-09 오후 9 02 10" src="https://github.com/user-attachments/assets/97cf25b6-b422-4134-ba57-71b8eeb3bdbc" />
<img width="1510" height="807" alt="스크린샷 2025-08-09 오후 9 02 43" src="https://github.com/user-attachments/assets/320dba35-869f-4e78-9b85-c720cb179b6d" />


