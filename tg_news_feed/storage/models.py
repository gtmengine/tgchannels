from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, UniqueConstraint, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Channel(Base):
    __tablename__ = 'channels'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    title = Column(String)
    added_at = Column(DateTime, default=func.current_timestamp())
    is_active = Column(Boolean, default=True)


class Post(Base):
    __tablename__ = 'posts'
    
    channel_id = Column(Integer, ForeignKey('channels.id'), primary_key=True)
    message_id = Column(Integer, primary_key=True)
    text = Column(Text)
    date = Column(DateTime)
    url = Column(String)


class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True)
    first_seen = Column(DateTime, default=func.current_timestamp())


class SavedPost(Base):
    __tablename__ = 'saved_posts'
    
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    channel_id = Column(Integer, primary_key=True)
    message_id = Column(Integer, primary_key=True)
    saved_at = Column(DateTime, default=func.current_timestamp())
    
    __table_args__ = (
        ForeignKey('posts.channel_id', 'posts.message_id'),
    )


class Suggestion(Base):
    __tablename__ = 'suggestions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    channel_username = Column(String)
    comment = Column(Text)
    created_at = Column(DateTime, default=func.current_timestamp()) 