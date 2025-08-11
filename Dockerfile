FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install Python deps
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Environment file (optional)
ENV PYTHONUNBUFFERED=1

# Entrypoint for daemon run (overrideable)
ENTRYPOINT ["python", "gmail_poll.py", "--daemon"]
