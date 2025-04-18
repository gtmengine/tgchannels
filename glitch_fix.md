# Glitch Deployment Instructions

Since Glitch uses an older version of Python and has limitations on what packages can be installed, you'll need to make these changes:

## 1. Create .env File in Glitch

In the Glitch project, go to `.env` (not visible in the file list) and add:
```
BOT_TOKEN=7964681343:AAEzlbYON6QBszXQQSOZQHpJKkV9-mjKyRE
API_ID=123456  # Replace with your API ID
API_HASH=your_api_hash_here  # Replace with your API hash
ADMIN_IDS=your_telegram_id  # Replace with your Telegram user ID
FEEDBACK_FORM=https://forms.gle/example
DB_PATH=.data/db.sqlite
PARSER_INTERVAL_MINUTES=5
```

## 2. Adjust Python Code for aiogram 2.x

Since we had to downgrade from aiogram 3.x to 2.x, you'll need to modify these files:

### tg_news_feed/main.py
Change the dispatcher initialization and middleware setup to match aiogram 2.x:
```python
# Initialize bot and dispatcher
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Register handlers
dp.include_router(user.router)  # Change to: register_handlers_user(dp)
dp.include_router(admin.router)  # Change to: register_handlers_admin(dp)

# Register middleware
dp.middleware.setup(CustomMiddleware(repo=repo, fetcher=fetcher))
```

### tg_news_feed/bot/handlers/user.py & admin.py
Change router setup to function-based registration:
```python
# Replace:
# router = Router()
# @router.message(...)

# With:
def register_handlers_user(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=["start"])
    dp.register_message_handler(cmd_help, commands=["help"])
    # etc.
```

### Update callback registration
```python
# Replace:
# @router.callback_query(F.data.startswith("save:"))

# With:
@dp.callback_query_handler(lambda c: c.data.startswith("save:"))
```

## 3. Refresh the Project

After making these changes:
1. In Glitch, click "Terminal" and run: `refresh`
2. This will restart your project with the new configuration

## 4. Alternative: Use a Different Platform

If these changes are too complex, consider:
- Render.com (has free tier)
- Railway.app (has free tier)
- PythonAnywhere (has free tier)

These platforms better support Python 3.11 and modern dependencies. 