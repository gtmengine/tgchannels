import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from tg_news_feed.config import config
from tg_news_feed.parser.fetcher import TelegramFetcher
from tg_news_feed.storage.repo import Repository

logger = logging.getLogger(__name__)


class UpdateScheduler:
    def __init__(self, fetcher: TelegramFetcher):
        self.fetcher = fetcher
        self.scheduler = AsyncIOScheduler()
        
    def start(self):
        """Start the scheduler."""
        interval_minutes = config.PARSER_INTERVAL_MINUTES
        
        # Add the job to update channels
        self.scheduler.add_job(
            self.fetcher.update_channels,
            trigger=IntervalTrigger(minutes=interval_minutes),
            id='update_channels',
            replace_existing=True
        )
        
        # Start the scheduler
        self.scheduler.start()
        logger.info(f"Scheduler started with {interval_minutes} minute interval")
        
    def stop(self):
        """Stop the scheduler."""
        self.scheduler.shutdown()
        logger.info("Scheduler stopped") 