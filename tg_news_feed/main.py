import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

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


async def main():
    """Main function to start the bot."""
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
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")
    )
    dp = Dispatcher(storage=MemoryStorage())
    
    # Register handlers
    dp.include_router(user.router)
    dp.include_router(admin.router)
    
    # Register middleware
    # We'll use DI for providing repository and fetcher
    dp.message.middleware(lambda handler, event, data: {
        **data, "repo": repo, "fetcher": fetcher
    })
    dp.callback_query.middleware(lambda handler, event, data: {
        **data, "repo": repo, "fetcher": fetcher
    })
    
    # Start polling
    try:
        logger.info("Starting bot")
        await dp.start_polling(bot)
    finally:
        logger.info("Stopping bot")
        await fetcher.stop()
        scheduler.stop()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped") 