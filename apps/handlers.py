import aiogram
from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from apps import keyboard as kb
from config import options_list
import aiosqlite
import re

router = Router()
rePattern = r'\d+\.\d+\.\d+'

template = """
<b>🏢 Название компании:</b> {compname}
<b>📞 Контакты:</b> {contacts}
<b>📘 Направление подготовки:</b> {direction}
<b>👥 Количество мест на практику:</b> {people}
<b>💬 Комментарий:</b> {comment}
<b>📝 Есть ли контракт:</b> {ifcontract}
<b>🏛️ Форма собственности предприятия:</b> {ownership_form}
"""

rows = None 
cursor = None
current_organization_index = 0

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply('Здравствуйте! Я бот ВВГУ для получения практики.',
                        reply_markup=kb.main)


@router.message(F.text == 'Выйти в главное меню')
async def return_to_main_menu(message: Message):
    await message.reply('Главное меню',
                        reply_markup=kb.main)


@router.message(F.text == 'Поиск предприятий')
async def found_comp_func(message: Message):
    global current_organization_index
    current_organization_index = 0
    await message.reply('Выберите направление подготовки:',
                        reply_markup=await kb.inline_items())


@router.message(F.text == "Следующая организация")
async def next_organization(message: Message):
    global rows, cursor

    if rows is None or cursor is None:
        await message.reply("Ошибка: данные не загружены. Пожалуйста, попробуйте позже.")
        return

    global current_organization_index

    try:
        if current_organization_index < len(rows) - 1:
            current_organization_index += 1
            row = rows[current_organization_index]
            row_dict = {cursor.description[i][0]: value for i, value in enumerate(row)}
            row_dict.pop('direction_code', None)
            formatted_row = template.format(**row_dict)
            await message.reply(formatted_row, parse_mode='html', reply_markup=await kb.next_organization())
        else:
            await message.reply("Это последняя организация в списке.", reply_markup=kb.main)
    except aiogram.exceptions.TelegramBadRequest:
        await message.reply("Ошибка: невозможно разобрать разметку сообщения. Перехожу к следующей организации.")
        # Переходим к следующей организации
        if current_organization_index < len(rows) - 1:
            current_organization_index += 1
            row = rows[current_organization_index]
            row_dict = {cursor.description[i][0]: value for i, value in enumerate(row)}
            row_dict.pop('direction_code', None)
            formatted_row = template.format(**row_dict)
            await message.reply(formatted_row, parse_mode='html', reply_markup=await kb.next_organization())
        else:
            await message.reply("Это последняя организация в списке.", reply_markup=kb.main)
for dir in options_list:
    if dir != F.text:
        async def dirNotEquals(message: Message):
            await message.reply("Выбранного направления подготовки нет.", reply_markup=kb.main)

for dir in options_list:
    if dir == F.text:
        @router.message(F.text == dir)
        async def all_organizations(message: Message):
            global rows, cursor

            async with aiosqlite.connect("practice_matrix.db") as db:
                matches = re.findall(rePattern, message.text)
                for match in matches:
                    cursor = await db.execute('SELECT * FROM practice_matrix WHERE direction_code LIKE ?', (f'%{match}%',))
                rows = await cursor.fetchall()
                await cursor.close()

                if not rows:
                    await message.reply('На выбранное направление практики организации отсутствуют.', reply_markup=kb.main)
                elif len(rows) == 1:
                    row = rows[0]
                    row_dict = {cursor.description[i][0]: value for i, value in enumerate(row)}
                    row_dict.pop('direction_code', None)
                    formatted_row = template.format(**row_dict)
                    await message.reply(formatted_row, parse_mode='html', reply_markup=kb.main)
                else:
                    current_organization_index = 0
                    row = rows[current_organization_index]
                    row_dict = {cursor.description[i][0]: value for i, value in enumerate(row)}
                    row_dict.pop('direction_code', None)
                    formatted_row = template.format(**row_dict)
                    await message.reply(formatted_row, parse_mode='html', reply_markup=await kb.next_organization())