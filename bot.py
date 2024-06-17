import asyncio
from io import BytesIO
from os import getenv
from aiogram import Bot, Dispatcher
from aiogram.filters import Filter, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
import sqlite3
from aiogram import F
from aiogram.fsm.state import StatesGroup, State




from keyboards import keyboard_selection_record
from media_records import set_record, get_record

connection = sqlite3.connect('db_user.db', check_same_thread=False)
cursor = connection.cursor()


def search_user_by_tg_id(id):
    cursor.execute('SELECT tg_id FROM Users WHERE tg_id = ? ', (id,))
    return cursor.fetchone()


def create_new_user_in_db(id, name, telephone=None):
    cursor.execute('''INSERT INTO Users (tg_id, username, telephone) VALUES ( ?, ?, ?)''', (id, name, telephone))
    connection.commit()


TOKEN = getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()


class Record(StatesGroup):
    text = State()
    media = State()



@dp.callback_query(F.data == 'text')
async def text(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Record.text)
    await callback.answer()
    await callback.message.edit_text("Введите текст")


@dp.callback_query(F.data == 'media')
async def media(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Record.media)
    await callback.answer()
    await callback.message.edit_text("Пришлите картинку или документ")


@dp.message(Record.text)
async def record_text(message: Message, state: FSMContext):
    set_record(message.chat.id, message.text, None)
    await message.answer("Ваш текст сохранён")
    await state.clear()

@dp.message(Record.media)
async def record_media(message: Message, state: FSMContext):
    name = message.photo[-1].file_id + ".jpg"
    await message.bot.download(file=message.photo[-1].file_id, destination=name)
    set_record(message.chat.id, None, name)
    await message.answer("Объект сохранён")
    await state.clear()


@dp.message(Command('save'))
async def save(message: Message) -> None:
    await message.answer("Что бы Вы хотели сохранить?", reply_markup=keyboard_selection_record())


@dp.message(Command('get'))
async def get(message: Message) -> None:
    records = ''
    for i in get_record(message.chat.id):
        records += f'\n type:  {i["type"]}; name: {i["content"]}'

    await message.answer("Ваши файлы: " + records)


@dp.message()
async def start_message(message: Message) -> None:
    if (search_user_by_tg_id(message.chat.id) == None):
        print(f"Пользователесь с id: {message.chat.id} не найден в бд")
        create_new_user_in_db(message.chat.id, message.from_user.full_name, "0000")
        await message.answer(f"Здравствуйте, {message.from_user.full_name}. Я могу сохранять Ваши записи.")

    await message.answer("Что бы Вы хотели сохранить?", reply_markup=keyboard_selection_record())


async def main():
    await dp.start_polling(bot)


asyncio.run(main())
