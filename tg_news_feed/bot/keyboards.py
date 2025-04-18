from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from typing import Optional


def main_keyboard() -> ReplyKeyboardMarkup:
    """Create the main keyboard with primary commands."""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(
        KeyboardButton("Лента"), 
        KeyboardButton("Сохранённые")
    )
    keyboard.row(
        KeyboardButton("Предложить канал"),
        KeyboardButton("Помощь")
    )
    return keyboard


def post_keyboard(channel_id: int, message_id: int) -> InlineKeyboardMarkup:
    """Create inline keyboard for a post."""
    keyboard = InlineKeyboardMarkup(row_width=2)
    save_callback = f"save:{channel_id}:{message_id}"
    
    keyboard.add(
        InlineKeyboardButton("❤️ Сохранить", callback_data=save_callback),
        InlineKeyboardButton("🔗 Перейти", url=f"https://t.me/c/{channel_id}/{message_id}")
    )
    
    return keyboard


def saved_post_keyboard(channel_id: int, message_id: int) -> InlineKeyboardMarkup:
    """Create inline keyboard for a saved post."""
    keyboard = InlineKeyboardMarkup(row_width=2)
    delete_callback = f"delete:{channel_id}:{message_id}"
    
    keyboard.add(
        InlineKeyboardButton("❌ Удалить", callback_data=delete_callback),
        InlineKeyboardButton("🔗 Перейти", url=f"https://t.me/c/{channel_id}/{message_id}")
    )
    
    return keyboard


def pagination_keyboard(
    current_page: int, 
    total_pages: int, 
    page_type: str = "feed"
) -> Optional[InlineKeyboardMarkup]:
    """Create pagination keyboard for feeds or saved posts."""
    if total_pages <= 1:
        return None
        
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = []
    
    if current_page > 1:
        buttons.append(
            InlineKeyboardButton(
                "⬅️ Назад", 
                callback_data=f"page:{page_type}:{current_page-1}"
            )
        )
    
    if current_page < total_pages:
        buttons.append(
            InlineKeyboardButton(
                "➡️ Вперёд", 
                callback_data=f"page:{page_type}:{current_page+1}"
            )
        )
    
    keyboard.add(*buttons)
    return keyboard 