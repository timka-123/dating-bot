from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def user_actions(user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="👍", callback_data=f"like_{user_id}"),
        InlineKeyboardButton(text="👎", callback_data=f"dislike_{user_id}"),
        InlineKeyboardButton(text="⏹️", callback_data=f"stop"),
    )
    return builder.as_markup()
