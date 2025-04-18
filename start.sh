#!/bin/bash

# Install Python 3 if not available
if ! command -v python3 &> /dev/null; then
    echo "Installing Python 3..."
    apt-get update
    apt-get install -y python3 python3-pip
fi

# Create database directory if it doesn't exist
mkdir -p .data

# Set up environment variables if .env exists
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# Install dependencies
pip3 install --user -r requirements.txt

# Run migrations
python3 migrate.py

# Start the bot
python3 -m tg_news_feed.main 