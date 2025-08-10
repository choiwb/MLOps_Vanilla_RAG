
FROM python:3.11.11-slim AS builder

# 한국 시간대 설정
ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y gcc python3-dev build-essential

WORKDIR /app

# src 및 하위 폴더 복사
COPY ./src ./src

# Cython 빌드 (src/setup.py 기준)
RUN pip install --upgrade pip && pip install cython==3.1.2
RUN python src/setup.py build_ext --inplace

# ----- 런타임 스테이지 -----
FROM python:3.11.11-slim AS runner

WORKDIR /app

ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# builder 에서 .c , .so 파일만 복사
COPY --from=builder /app/src /app/src

RUN mkdir -p ./logs
COPY ./conf ./conf

RUN mkdir -p ./models

# 패키징 위한 불필요 .py 제거
RUN find src -type f -name '*.py' \
  ! -path 'src/main.py' \
  -delete

# Cython 빌드 후 생성된 .c 파일 제거 제거
RUN find src -type f -name '*.c' -delete

CMD ["python", "src/main.py"]
