from sqlalchemy import create_engine, select, delete, func
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional, Tuple, Dict
from datetime import datetime

from tg_news_feed.config import config
from tg_news_feed.storage.models import Base, Channel, Post, User, SavedPost, Suggestion


class Repository:
    def __init__(self):
        self.engine = create_engine(f"sqlite:///{config.DB_PATH}", echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
    def create_tables(self):
        """Create database tables."""
        Base.metadata.create_all(self.engine)
        
    def get_session(self) -> Session:
        """Get a database session."""
        return self.SessionLocal()
        
    # Channels
    def add_channel(self, username: str, title: Optional[str] = None) -> Channel:
        """Add a new channel to the database."""
        with self.get_session() as session:
            channel = Channel(username=username, title=title, added_at=datetime.now())
            session.add(channel)
            try:
                session.commit()
                session.refresh(channel)
                return channel
            except IntegrityError:
                session.rollback()
                return session.execute(select(Channel).where(Channel.username == username)).scalar_one_or_none()
                
    def get_channels(self, active_only: bool = True) -> List[Channel]:
        """Get all channels."""
        with self.get_session() as session:
            query = select(Channel)
            if active_only:
                query = query.where(Channel.is_active == True)
            return list(session.execute(query).scalars().all())
            
    def get_channel_by_id(self, channel_id: int) -> Optional[Channel]:
        """Get channel by ID."""
        with self.get_session() as session:
            return session.execute(select(Channel).where(Channel.id == channel_id)).scalar_one_or_none()
    
    # Posts
    def add_post(self, channel_id: int, message_id: int, text: str, date: datetime, url: str) -> Optional[Post]:
        """Add a new post to the database."""
        with self.get_session() as session:
            post = Post(
                channel_id=channel_id,
                message_id=message_id,
                text=text,
                date=date,
                url=url
            )
            session.add(post)
            try:
                session.commit()
                session.refresh(post)
                return post
            except IntegrityError:
                session.rollback()
                return None
                
    def get_latest_posts(self, limit: int = 20, offset: int = 0) -> List[Dict]:
        """Get latest posts with channel information."""
        with self.get_session() as session:
            query = select(Post, Channel.username, Channel.title).join(
                Channel, Post.channel_id == Channel.id
            ).order_by(Post.date.desc()).limit(limit).offset(offset)
            
            result = []
            for post, username, title in session.execute(query):
                result.append({
                    "channel_id": post.channel_id,
                    "message_id": post.message_id,
                    "text": post.text,
                    "date": post.date,
                    "url": post.url,
                    "channel_username": username,
                    "channel_title": title
                })
            return result
            
    def get_max_message_id(self, channel_id: int) -> Optional[int]:
        """Get maximum message_id for a channel."""
        with self.get_session() as session:
            result = session.execute(
                select(func.max(Post.message_id)).where(Post.channel_id == channel_id)
            ).scalar_one_or_none()
            return result if result else 0
            
    # Users
    def register_user(self, user_id: int) -> User:
        """Register a new user or get existing."""
        with self.get_session() as session:
            user = session.execute(select(User).where(User.user_id == user_id)).scalar_one_or_none()
            if not user:
                user = User(user_id=user_id)
                session.add(user)
                session.commit()
                session.refresh(user)
            return user
            
    def get_user_count(self) -> int:
        """Get total user count."""
        with self.get_session() as session:
            return session.execute(select(func.count(User.user_id))).scalar_one()
            
    # Saved posts
    def save_post(self, user_id: int, channel_id: int, message_id: int) -> Tuple[bool, str]:
        """Save a post for a user."""
        with self.get_session() as session:
            # Check if post exists
            post = session.execute(
                select(Post).where(
                    Post.channel_id == channel_id,
                    Post.message_id == message_id
                )
            ).scalar_one_or_none()
            
            if not post:
                return False, "Post not found"
                
            # Check if already saved
            saved = session.execute(
                select(SavedPost).where(
                    SavedPost.user_id == user_id,
                    SavedPost.channel_id == channel_id,
                    SavedPost.message_id == message_id
                )
            ).scalar_one_or_none()
            
            if saved:
                return False, "Post already saved"
                
            # Save post
            saved_post = SavedPost(
                user_id=user_id,
                channel_id=channel_id,
                message_id=message_id
            )
            session.add(saved_post)
            session.commit()
            return True, "Post saved"
            
    def get_saved_posts(self, user_id: int, limit: int = 20, offset: int = 0) -> List[Dict]:
        """Get saved posts for a user."""
        with self.get_session() as session:
            query = select(Post, Channel.username, Channel.title, SavedPost.saved_at).join(
                SavedPost, 
                (Post.channel_id == SavedPost.channel_id) & (Post.message_id == SavedPost.message_id)
            ).join(
                Channel, Post.channel_id == Channel.id
            ).where(
                SavedPost.user_id == user_id
            ).order_by(SavedPost.saved_at.desc()).limit(limit).offset(offset)
            
            result = []
            for post, username, title, saved_at in session.execute(query):
                result.append({
                    "channel_id": post.channel_id,
                    "message_id": post.message_id,
                    "text": post.text,
                    "date": post.date,
                    "url": post.url,
                    "channel_username": username,
                    "channel_title": title,
                    "saved_at": saved_at
                })
            return result
            
    def delete_saved_post(self, user_id: int, channel_id: int, message_id: int) -> bool:
        """Delete a saved post."""
        with self.get_session() as session:
            result = session.execute(
                delete(SavedPost).where(
                    SavedPost.user_id == user_id,
                    SavedPost.channel_id == channel_id,
                    SavedPost.message_id == message_id
                )
            )
            session.commit()
            return result.rowcount > 0
            
    # Suggestions
    def add_suggestion(self, user_id: int, channel_username: str, comment: Optional[str] = None) -> Suggestion:
        """Add a new channel suggestion."""
        with self.get_session() as session:
            suggestion = Suggestion(
                user_id=user_id,
                channel_username=channel_username,
                comment=comment
            )
            session.add(suggestion)
            session.commit()
            session.refresh(suggestion)
            return suggestion
            
    def get_suggestions(self) -> List[Suggestion]:
        """Get all channel suggestions."""
        with self.get_session() as session:
            return list(session.execute(select(Suggestion).order_by(Suggestion.created_at.desc())).scalars().all())
            
    # Stats
    def get_stats(self) -> Dict:
        """Get basic stats."""
        with self.get_session() as session:
            user_count = session.execute(select(func.count(User.user_id))).scalar_one()
            post_count = session.execute(select(func.count()).select_from(Post)).scalar_one()
            channel_count = session.execute(select(func.count(Channel.id))).scalar_one()
            saved_count = session.execute(select(func.count()).select_from(SavedPost)).scalar_one()
            
            return {
                "users": user_count,
                "posts": post_count,
                "channels": channel_count,
                "saved_posts": saved_count
            } 