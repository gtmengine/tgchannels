#!/bin/bash

# Create data directory if it doesn't exist
mkdir -p /data

# Initialize database
python -m alembic upgrade head

# Start the bot
exec python -m tg_news_feed.main 