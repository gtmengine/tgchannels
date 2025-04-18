import asyncio
import logging
import sys
import socket
import uuid
import platform
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from tg_news_feed.config import config
from tg_news_feed.storage.repo import Repository
from tg_news_feed.parser.fetcher import TelegramFetcher
from tg_news_feed.scheduler import UpdateScheduler
from tg_news_feed.bot.handlers import user, admin

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Create web app for health checks
app = web.Application()

async def health_check(request):
    """Health check endpoint for Koyeb."""
    return web.Response(text='OK', status=200)

app.router.add_get('/health', health_check)

async def main():
    """Main function to start the bot."""
    # Generate a unique server ID to track multiple deployments
    server_id = str(uuid.uuid4())[:8]
    hostname = socket.gethostname()
    
    logger.info(f"Starting bot on {hostname} (ID: {server_id}) - Platform: {platform.platform()}")
    
    # Initialize repository and create tables
    repo = Repository()
    repo.create_tables()
    logger.info("Database initialized")
    
    # Initialize Telegram client for parsing
    fetcher = TelegramFetcher(repo)
    await fetcher.start()
    logger.info("Telegram fetcher initialized")
    
    # Initialize scheduler
    scheduler = UpdateScheduler(fetcher)
    scheduler.start()
    logger.info("Scheduler started")
    
    # Initialize bot and dispatcher
    bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    
    # Register handlers
    dp.include_router(user.router)
    dp.include_router(admin.router)
    
    # Register middleware
    async def middleware_handler(handler, event, data):
        data["repo"] = repo
        data["fetcher"] = fetcher
        return await handler(event, data)
    
    dp.message.middleware(middleware_handler)
    dp.callback_query.middleware(middleware_handler)
    
    # Set up webhook handler
    webhook_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_handler.register(app, path='/webhook')
    
    # Start health check endpoint
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    logger.info("Health check endpoint started on port 8080")
    
    # Start polling
    try:
        logger.info(f"Bot started on {hostname} (ID: {server_id})")
        await dp.start_polling(bot)
    finally:
        logger.info(f"Stopping bot on {hostname} (ID: {server_id})")
        await fetcher.stop()
        scheduler.stop()
        await runner.cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped") 