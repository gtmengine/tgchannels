# Deploying to PythonAnywhere

This guide provides step-by-step instructions to deploy the Telegram News Aggregator bot on PythonAnywhere.

## Prerequisites

1. A PythonAnywhere account (free tier available)
2. Your Telegram API credentials (API_ID and API_HASH)
3. Your bot token
4. Your Telegram user ID (for ADMIN_IDS)

## Deployment Steps

### 1. Sign Up for PythonAnywhere

1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Create a free account

### 2. Upload Your Code

1. In the PythonAnywhere dashboard, go to "Files"
2. Create a new directory for your project
3. Upload all project files:
   - `tg_news_feed/` directory
   - `requirements.txt`
   - `pythonanywhere_config.py`
   - `pythonanywhere_start.py`

### 3. Set Up Environment Variables

1. Go to "Web" tab in PythonAnywhere dashboard
2. Click "Add a new web app"
3. Choose "Manual configuration" and Python 3.9
4. In the "Virtualenv" section, create a new virtualenv
5. In the "Code" section, set the working directory to your project directory
6. In the "WSGI configuration file", add:
   ```python
   import sys
   path = '/home/yourusername/yourproject'
   if path not in sys.path:
       sys.path.append(path)
   
   from pythonanywhere_start import app as application
   ```

### 4. Configure Environment Variables

1. Go to "Web" tab
2. Click on your web app
3. Go to "Virtualenv" section
4. Click "Enter virtualenv"
5. Run these commands:
   ```bash
   pip install -r requirements.txt
   ```

6. Go to "Web" tab
7. Click on your web app
8. Go to "Environment variables" section
9. Add these variables:
   - `BOT_TOKEN`: Your bot token
   - `API_ID`: Your Telegram API ID
   - `API_HASH`: Your Telegram API hash
   - `ADMIN_IDS`: Your Telegram user ID (comma-separated if multiple)
   - `FEEDBACK_FORM`: URL for feedback form (optional)

### 5. Start the Bot

1. Go to "Web" tab
2. Click on your web app
3. Click "Reload" to start the bot

## Troubleshooting

If your bot doesn't start:

1. Check the error log in the "Web" tab
2. Make sure all environment variables are set correctly
3. Verify that the bot token is valid
4. Check that all required packages are installed

## Notes

- The free tier has some limitations but should be sufficient for this bot
- PythonAnywhere provides a persistent environment
- The bot will stay running as long as your web app is active

If you experience any issues, check the error logs in the PythonAnywhere dashboard. 