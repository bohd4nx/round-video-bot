FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# ffmpeg is required for video processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.13.0 /uv /usr/local/bin/uv

WORKDIR /srv/round-video-bot

# Dependencies first, so code changes don't invalidate this layer
COPY pyproject.toml .
RUN uv pip install --system --no-cache -r pyproject.toml

COPY main.py .
COPY bot ./bot
COPY locales ./locales
COPY files ./files

# Run unprivileged; code stays read-only, ensure it's readable regardless of host file modes
RUN chmod -R a+rX . && useradd --system --no-create-home bot
USER bot

CMD ["python", "main.py"]
