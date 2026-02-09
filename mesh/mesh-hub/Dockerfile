FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY hub.py .
COPY config.json .

# Expose port
EXPOSE 7100

# Run
CMD ["python", "hub.py"]
