FROM python:3.14.7-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
PYTHONUNBUFFERED=1 

#sets workdir within container
WORKDIR /app 

RUN apt-get update && apt-get install -y curl

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY dj_blog/requirements.txt .
RUN uv pip install -r requirements.txt --system

COPY dj_blog/ .

#exposes port 8000 within container to outside
EXPOSE 8000 

CMD ["./entrypoint.sh"]