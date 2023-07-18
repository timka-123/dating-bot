from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def menu_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text="👤 Профиль"),
        KeyboardButton(text="🚀 Искать"),
    )
    return builder.as_markup(resize_keyboard=True)
