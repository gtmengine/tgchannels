import asyncio
import logging
from datetime import datetime
from typing import List, Dict, Optional

from telethon import TelegramClient
from telethon.errors import FloodWaitError, ChannelPrivateError
from telethon.tl.types import Message

from tg_news_feed.config import config
from tg_news_feed.storage.repo import Repository

logger = logging.getLogger(__name__)


class TelegramFetcher:
    def __init__(self, repo: Repository):
        self.repo = repo
        self.client = TelegramClient(
            'bot_session',
            config.API_ID,
            config.API_HASH
        )
        self.running = False
        
    async def start(self):
        """Start the Telegram client."""
        await self.client.start()
        logger.info("Telegram client started")
        
    async def stop(self):
        """Stop the Telegram client."""
        await self.client.disconnect()
        logger.info("Telegram client stopped")
        
    def _make_post_url(self, channel_username: str, message_id: int) -> str:
        """Create a URL for a Telegram post."""
        return f"https://t.me/{channel_username}/{message_id}"
        
    async def fetch_channel_posts(self, channel: Dict, limit: int = 100) -> int:
        """Fetch recent posts from a channel and store them in the database."""
        channel_id = channel['id']
        username = channel['username']
        
        # Get the latest message_id we have for this channel
        last_message_id = self.repo.get_max_message_id(channel_id)
        new_posts = 0
        
        try:
            # Fetch the latest messages from the channel
            messages = await self.client.get_messages(username, limit=limit)
            
            for message in messages:
                if not isinstance(message, Message) or not message.text:
                    continue
                    
                # Skip if we've already processed this message
                if last_message_id and message.id <= last_message_id:
                    continue
                    
                # Create a URL for the post
                url = self._make_post_url(username, message.id)
                
                # Store the post in the database
                self.repo.add_post(
                    channel_id=channel_id,
                    message_id=message.id,
                    text=message.text[:4096],  # Telegram message limit
                    date=message.date,
                    url=url
                )
                new_posts += 1
                
            logger.info(f"Fetched {new_posts} new posts from {username}")
            return new_posts
            
        except FloodWaitError as e:
            logger.warning(f"FloodWaitError: Need to wait {e.seconds} seconds")
            await asyncio.sleep(e.seconds)
            return 0
        except ChannelPrivateError:
            logger.error(f"Cannot access private channel {username}")
            return 0
        except Exception as e:
            logger.error(f"Error fetching posts from {username}: {e}")
            return 0
            
    async def update_channels(self):
        """Update all active channels."""
        if self.running:
            logger.warning("Update already in progress, skipping")
            return
            
        self.running = True
        
        try:
            channels = self.repo.get_channels(active_only=True)
            total_new_posts = 0
            
            for channel in channels:
                channel_dict = {
                    'id': channel.id,
                    'username': channel.username,
                    'title': channel.title
                }
                new_posts = await self.fetch_channel_posts(channel_dict)
                total_new_posts += new_posts
                
                # Sleep between channels to avoid rate limits
                await asyncio.sleep(2)
                
            logger.info(f"Update complete. Added {total_new_posts} new posts")
        except Exception as e:
            logger.error(f"Error updating channels: {e}")
        finally:
            self.running = False 