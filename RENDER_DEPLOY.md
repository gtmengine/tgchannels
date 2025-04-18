# Deploying to Render.com

This guide provides step-by-step instructions to deploy the Telegram News Aggregator bot on Render.com.

## Why Render?

- Free tier with 750 hours/month (enough for continuous operation)
- Persistent disk for database storage
- Simple and straightforward deployment from GitHub
- Built-in environment variables management
- HTTPS enabled

## Deployment Steps

### 1. Sign Up for Render

Visit [render.com](https://render.com) and sign up for an account.

### 2. Configure the Service

**Option 1: One-Click Deploy**

1. Click the "Deploy to Render" button in the repository (if available)
2. Fill in the required environment variables

**Option 2: Manual Setup**

1. From the Render dashboard, click "New +"
2. Select "Blueprint" (to use the render.yaml configuration)
3. Connect your GitHub account if you haven't already
4. Select the repository "gtmengine/tg-news-feed"
5. Give your service a name
6. Provide the required environment variables:
   - `BOT_TOKEN`: Your Telegram bot token (7964681343:AAEzlbYON6QBszXQQSOZQHpJKkV9-mjKyRE)
   - `API_ID`: Your Telegram API ID (numeric)
   - `API_HASH`: Your Telegram API hash
   - `ADMIN_IDS`: Your Telegram user ID (comma-separated if multiple)
   - `FEEDBACK_FORM`: URL for the feedback form (can be empty)

7. Click "Create Blueprint"

### 3. Monitor Deployment

1. Render will automatically build and deploy your application
2. You can view build and runtime logs from the dashboard
3. Once deployed, your bot should start working immediately

### 4. Administration

- Use admin commands like `/stats` and `/server` to check status
- Use `/addchannel @username` to add channels to your aggregator

## Troubleshooting

If your bot doesn't start:

1. Check the logs in the Render dashboard
2. Make sure all environment variables are set correctly
3. Verify that the bot token is valid
4. Check database permissions (the bot needs write access to the disk mount)

## Notes

- The free tier has some CPU and memory limitations, but should be sufficient for this bot
- Render's free tier includes a persistent disk which is perfect for the SQLite database
- The bot will stay running continuously without sleep periods (unlike Glitch)

If you experience any issues, contact support or create an issue in the GitHub repository. 