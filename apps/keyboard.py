from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from config import directions

main  = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Поиск предприятий')],
],
                            resize_keyboard=True,
                            input_field_placeholder='Выберите пункт меню')


async def inline_items():
    keyboard = ReplyKeyboardBuilder()
    for key, value in directions.items():
        keyboard.add(KeyboardButton(text=str(key) + ' ' + str(value)))
    return keyboard.adjust(1).as_markup()


async def next_organization():
    buttons = [
        KeyboardButton(text="Следующая организация"),
        KeyboardButton(text="Выйти в главное меню")
    ]
    markup = ReplyKeyboardMarkup(keyboard=[buttons], resize_keyboard=True)
    return markup



