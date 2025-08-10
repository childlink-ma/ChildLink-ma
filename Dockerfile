FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System deps (FAISS & BLAS)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    libopenblas-dev \
    liblapack-dev \
 && rm -rf /var/lib/apt/lists/*

# Python deps (cache-friendly layer)
COPY requirements.txt .
RUN python -m pip install --upgrade pip \
 && pip install -r requirements.txt

# Copy project (respects .dockerignore)
COPY . .

# Force-copy critical assets (even if someone changes .dockerignore later)
COPY clm_index.index   /app/clm_index.index
COPY clm_metadata.json /app/clm_metadata.json
COPY widget.html       /app/widget.html
COPY app.py            /app/app.py
COPY startup.sh        /app/startup.sh

# Ensure startup is executable
RUN chmod +x /app/startup.sh

EXPOSE 8000

# Robust entrypoint (preflight + gunicorn)
CMD ["/app/startup.sh"]


