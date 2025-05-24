# Use multi-stage build for smaller final image
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy Python requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend/
COPY parsers/ ./parsers/
COPY rag/ ./rag/
COPY setup.py ./

# Copy frontend build from previous stage
COPY --from=frontend-builder /app/frontend/build ./frontend/build

# Environment variables
ENV PORT=8000
ENV HOST=0.0.0.0
ENV WORKERS=4

# Expose port
EXPOSE 8000

# Start the application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]