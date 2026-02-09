FROM python:3.11-slim

WORKDIR /app

# Dependencies
RUN pip install --no-cache-dir nats-py

# Copy CLI scripts
COPY mesh-send.py /app/
COPY mesh-broadcast.py /app/

# Make executable
RUN chmod +x /app/*.py

# Add to PATH
ENV PATH="/app:${PATH}"

CMD ["tail", "-f", "/dev/null"]
