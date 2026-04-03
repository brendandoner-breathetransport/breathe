FROM python:3.12-slim

WORKDIR /app

COPY breathe_fastapi/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY breathe_fastapi/ breathe_fastapi/
COPY data/ data/
COPY static/ static/

CMD ["sh", "-c", "uvicorn breathe_fastapi.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
