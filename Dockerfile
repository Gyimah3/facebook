FROM python:3.12-slim-bullseye AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 

FROM python:3.12-slim-bullseye

WORKDIR /app

# Copy dependencies from builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

RUN groupadd -r appuser && useradd -r -g appuser appuser \
    && mkdir -p logs \
    && chown -R appuser:appuser logs \
    && chmod 755 logs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
    
# Copy application code
COPY . /app/

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8061

USER appuser

EXPOSE ${PORT}

CMD ["python", "-m", "uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8061"]