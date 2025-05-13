FROM python:3.10-slim AS python-base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Python application
COPY . .

FROM golang:1.21-alpine AS go-builder

WORKDIR /app

# Copy Go application
COPY --from=python-base /app/chatbot /app/chatbot
COPY --from=python-base /app/go.mod /app/go.sum* /app/

# Download Go dependencies
RUN go mod download

# Build Go application
WORKDIR /app/chatbot
RUN go build -o /app/chatbot/chatbot-server server.go

FROM python:3.10-slim AS final

WORKDIR /app

# Copy from Python base
COPY --from=python-base /app /app
# Copy Go binary
COPY --from=go-builder /app/chatbot/chatbot-server /app/chatbot/

# Set environment variables
ENV PORT=8000 \
    CHATBOT_PORT=8080

# Expose ports
EXPOSE $PORT $CHATBOT_PORT

# Create startup script
RUN echo '#!/bin/bash\n\
python server.py & \
cd chatbot && ./chatbot-server\n\
wait\n' > /app/start.sh && \
chmod +x /app/start.sh

# Run the startup script
CMD ["/app/start.sh"] 