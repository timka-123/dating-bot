from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def profile_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✏️ Изменить имя", callback_data=f"change_name"),
        InlineKeyboardButton(text="✏️ Изменить возраст", callback_data=f"change_age"),
        InlineKeyboardButton(text="✏️ Изменить город", callback_data=f"change_city"),
        InlineKeyboardButton(text="✏️ Изменить информацию о себе", callback_data=f"change_about"),
        InlineKeyboardButton(text="✏️ Изменить фото", callback_data=f"change_photo"),
    )
    builder.adjust(2)
    return builder.as_markup()
