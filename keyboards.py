from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def keyboard_selection_record():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="Загрузить текст", callback_data='text'),
            types.InlineKeyboardButton(text="Загрузить медиа", callback_data='media')
        ],
    ])
    return kb
    # return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Выберите тип записи")
