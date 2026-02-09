FROM python:3.11-slim

WORKDIR /app

# Dependencies
RUN pip install --no-cache-dir nats-py requests

# Copy listener script
COPY mesh-listener.py /app/

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD pgrep -f mesh-listener.py || exit 1

CMD ["python3", "-u", "/app/mesh-listener.py"]
