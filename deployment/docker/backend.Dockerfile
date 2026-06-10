# Stage 1: Build dependencies
FROM python:3.11-slim as builder

WORKDIR /app

# Install compilation tools needed for C extensions (e.g. FAISS, if compiled)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Final minimal runner image
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for FAISS/OpenBLAS
RUN apt-get update && apt-get install -y --no-install-recommends \
    libopenblas-dev \
    libomp-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy local dependencies from build step
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy codebase
COPY src/ /app/src/
COPY models/ /app/models/
COPY data/ /app/data/

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
