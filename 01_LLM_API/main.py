

import os
import argparse
import subprocess
from dotenv import load_dotenv
load_dotenv()
HF_HOME = os.getenv("HF_HOME")
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
from huggingface_hub import login
login(token=HUGGINGFACEHUB_API_TOKEN)

# import torch
# from vllm import SamplingParams, LLM



# nohup python src/vllm_serving.py --host 0.0.0.0 --port 8082
# ─── 2) 명령행 인자 파싱 ───────────────────────────────────────────────────
parser = argparse.ArgumentParser(
    description="Serve kakaocorp/kanana-nano-2.1b-instruct via vLLM OpenAI-compatible API"
)
parser.add_argument("--host", default="0.0.0.0", help="서버 호스트 (기본값: 0.0.0.0)")
parser.add_argument("--port", type=int, default=8082, help="서버 포트 (기본값: 8082)")
args = parser.parse_args()


# ─── 4) vLLM 서버 실행 커맨드 구성 ─────────────────────────────────────────
model_id = "kakaocorp/kanana-nano-2.1b-instruct"
cmd = [
    "python", "-m", "vllm.entrypoints.openai.api_server",
    "--model", model_id,
    "--trust-remote-code",
    "--dtype", "bfloat16",
    "--gpu-memory-utilization", "0.15",
    "--tensor-parallel-size", "1",
    "--host", args.host,
    "--port", str(args.port),
    "--api-key", "EMPTY"  # vLLM에서는 기본값을 EMPTY로 사용
]

# ─── 5) 서버 시작 ─────────────────────────────────────────────────────────
print(f"Starting vLLM server for {model_id} on {args.host}:{args.port}...")
subprocess.run(cmd, check=True)
