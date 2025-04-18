# Deploying to Koyeb

This guide provides step-by-step instructions to deploy the Telegram News Aggregator bot on Koyeb.

## Why Koyeb?

- Free tier includes 2 nano instances
- Simple GitHub deployment
- Automatic HTTPS
- Persistent storage
- Easy environment variable management

## Prerequisites

1. A Koyeb account (free tier available)
2. Your Telegram bot token (already configured)
3. Your Telegram API credentials (API_ID and API_HASH)
4. Your Telegram user ID (for ADMIN_IDS)

## Deployment Steps

### 1. Sign Up for Koyeb

1. Go to [koyeb.com](https://www.koyeb.com)
2. Create a free account
3. Install the Koyeb CLI (optional but recommended)

### 2. Connect Your GitHub Repository

1. In the Koyeb dashboard, go to "Settings" → "Connected Services"
2. Click "Connect GitHub"
3. Select your repository (gtmengine/tgchannels)

### 3. Create a New App

1. Click "Create App"
2. Choose "GitHub"
3. Select your repository and branch (main)
4. Choose "Docker" as the build method
5. Set the following:
   - Name: tg-channels-bot
   - Region: Frankfurt (or closest to you)
   - Instance Type: Nano (free tier)

### 4. Configure Environment Variables

In the app settings, add these environment variables:
- `BOT_TOKEN`: Already configured in koyeb.yaml
- `API_ID`: Your Telegram API ID
- `API_HASH`: Your Telegram API hash
- `ADMIN_IDS`: Your Telegram user ID
- `FEEDBACK_FORM`: Optional, can be empty
- `PARSER_INTERVAL_MINUTES`: 5 (default)
- `DB_PATH`: /data/db.sqlite

### 5. Configure Persistent Storage

The app is configured to use a 1GB persistent volume mounted at `/data`.
This is already set up in the `koyeb.yaml` file.

### 6. Deploy

1. Click "Deploy"
2. Wait for the build and deployment to complete
3. Check the logs for any issues

## Monitoring

1. Go to the "Apps" section
2. Click on your app name
3. Check:
   - Logs
   - Metrics
   - Instance status

## Troubleshooting

If your bot doesn't start:

1. Check the deployment logs
2. Verify environment variables
3. Ensure API credentials are correct
4. Check instance status

## Notes

- Free tier includes 2 nano instances
- Each instance has:
  - Shared CPU
  - 512MB RAM
  - 5GB storage
- Deployment is automatic on git push
- Logs are available in real-time

For more help, visit [Koyeb Documentation](https://www.koyeb.com/docs) 