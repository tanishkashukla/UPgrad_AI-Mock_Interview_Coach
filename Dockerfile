# InterviewIQ AI — multi-stage Docker build
FROM node:20-alpine AS frontend-build
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install
COPY frontend/ ./
ENV NEXT_PUBLIC_API_URL=http://localhost:8000
RUN npm run build

FROM python:3.12-slim AS backend
WORKDIR /app
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt
COPY backend/ ./backend/
COPY agents/ ./agents/
COPY prompts/ ./prompts/
COPY services/ ./services/
COPY types/ ./types/
COPY utils/ ./utils/
COPY data/ ./data/
ENV PYTHONPATH=/app
ENV MOCK_LLM=true
EXPOSE 8000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
