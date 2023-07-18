from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def name_kb(user_name: str) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text=user_name)
    )
    return builder.as_markup(resize_keyboard=True, one_time=True)


def city_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="Отправить геолокацию", request_location=True)
    )
    return builder.as_markup(resize_keyboard=True, one_time=True)
