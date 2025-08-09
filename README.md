| 노드풀      | 노드 개수  | 배치되는 Pod                                                          |
| -------- | ------ | ----------------------------------------------------------------- |
| **cpu1** | 1      | rag-controller                                                    |
| **gpu1** | 1      | **Embedding** Pod + **Milvus**(Helm chart로 배포, nodeSelector=gpu1) |
| **gpu2** | 1 (사용) | LLM(vLLM) Pod                                                     |
| **gpu2** | 1 (비움) | 없음 (empty)       
