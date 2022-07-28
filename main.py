import logging
import sqlite3 as sq
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from buttons import kurs_btn_Ru, kurs_btn_Uz, can, lang_btn, courseTime

token = "your api token here"


logging.basicConfig(level=logging.INFO)

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

sendMessageUz = ["Ism-familia:", "tugulgan yilingiz:", "telefon raqam:", "kurs vaqtini kiriting:",
                 "🥳🥳🥳 Tabriklaymiz!!! 🥳🥳🥳\nSiz ro'yxatdan o'ttingiz, batafsil ma'lumot uchun +998953001199 nomeriga qo'ng'iroq qiling!n", 'Manzil:\nhttps://goo.gl/maps/WM1ftxkGZ7hgqLmh9']


# create database table
def sql_start():
    global base
    global cur
    base = sq.connect("users.db")
    cur = base.cursor()
    if base:
        print('data base connect OK!')
    cur.execute('create table if not exists menu(Course TEXT, fullname TEXT, year TEXT , PhoneNumber TEXT, date TEXT);')
    base.commit()


# data save
async def sql_add_command(state):
    async with state.proxy() as data:
        dataStorage = []
        for i in data.values():
            dataStorage.append(i)
        cur.execute('insert into menu values(?, ?, ?, ?, ?)', tuple(dataStorage))
        base.commit()


# create state action
class FSMAdmin(StatesGroup):
    til = State()
    getKurs = State()  # kurslar buttoni uchun
    fullname = State()
    year = State()
    phoneNumber = State()
    date = State()


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    await state.finish()
    await message.reply('Cancelled', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands='members')
async def send_welcome(message: types.Message):
    conn = sq.connect('users.db')
    data = conn.execute('select * from menu;')
    await message.reply(f'{data.fetchall()}')
    conn.commit()


@dp.message_handler(commands='delete')
async def deleteCommand(message: types.Message):
    conn = sq.connect('users.db')
    conn.execute('Delete from menu;')
    conn.commit()
    await message.reply('Baza tozalandi!')


# start handler
@dp.message_handler(commands=['start'])
async def cm_start(message: types.Message):

    await message.reply(
        f"Assalomu alaykum {message.from_user.full_name}!")
    await message.reply(
        "Batafsil ma'lumot uchun +998953001199 telefon raqamiga murojaat qilishingiz mumkin...\nMaqsadlar sari olg'a!!!",
        reply_markup=lang_btn)
    await FSMAdmin.til.set()


@dp.message_handler(state=FSMAdmin.til)
async def load_fullname(message: types.Message):
    if message.text == "UZ":
        await message.reply('Assalomu aleykum Kursga yozilish uchun yonalishlardan birini tanlang!',
                            reply_markup=kurs_btn_Uz)
    elif message.text == "RUS":
        await message.reply('Assalomu aleykum Kursga yozilish uchun yonalishlardan birini tanlang!',
                            reply_markup=kurs_btn_Ru)
    await FSMAdmin.next()


# register handler
@dp.message_handler(state=FSMAdmin.getKurs)
async def cm_register(message: types.Message, state: FSMContext, nametxt=sendMessageUz[0]):
    markup = types.ReplyKeyboardRemove()
    async with state.proxy() as data:
        data['Course'] = message.text
    await FSMAdmin.next()
    await message.reply(nametxt, reply_markup=markup)


# get user fullname
@dp.message_handler(state=FSMAdmin.fullname)
async def load_fullname(message: types.Message, state: FSMContext, yeartxt=sendMessageUz[1]):
    async with state.proxy() as data:
        data['fullname'] = message.text
    await FSMAdmin.next()
    await message.reply(yeartxt)


# get user year
@dp.message_handler(state=FSMAdmin.year)
async def load_year(message: types.Message, state: FSMContext, phonetxt=sendMessageUz[2]):
    async with state.proxy() as data:
        data['year'] = message.text
    await FSMAdmin.next()
    await message.reply(phonetxt)


# get user phone Number
@dp.message_handler(state=FSMAdmin.phoneNumber)
async def load_phoneNumber(message: types.Message, state: FSMContext, datetxt=sendMessageUz[3]):
    async with state.proxy() as data:
        data['PhoneNumber'] = message.text
    await FSMAdmin.next()
    await message.reply(datetxt, reply_markup=courseTime)


# cource date
@dp.message_handler(state=FSMAdmin.date)
async def load_date(message: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardRemove()
    async with state.proxy() as data:
        data['date'] = message.text
    await sql_add_command(state)
    await state.finish()
    await message.reply(sendMessageUz[4], reply_markup=markup)
    await message.reply(sendMessageUz[5])


if __name__ == '__main__':
    sql_start()
    executor.start_polling(dp, skip_updates=True)
