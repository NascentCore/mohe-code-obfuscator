FROM reg.dev.mahanova.com/registry/public/library/python:3.12-slim-bookworm AS build
ENV PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
WORKDIR /app
COPY requirements.txt .
RUN python -m pip install -U pip \
    && pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
CMD ["python", "-m", "src", "api"]
EXPOSE 9001