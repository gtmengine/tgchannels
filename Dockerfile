FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for TDLib
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY tg_news_feed ./tg_news_feed

# Create a non-root user and switch to it
RUN useradd -m appuser
USER appuser

# Run the bot
CMD ["python", "-m", "tg_news_feed.main"] 