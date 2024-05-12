import asyncio, re, logging
from aiogram import Dispatcher, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command
from core.utils.commands import set_commands
from aiogram.fsm.context import FSMContext
from aiogram import Bot
from aiogram.types import Message
from core.keyboards.reply import zapis, vrach, terapevt, pediatr
from core.keyboards.reply import oftalmolog, kardiolog, ginekolog, nevrolog
from core.settings import settings
import pandas as pd
from openpyxl import load_workbook


class Register(StatesGroup):
    fullname = State()
    date_r = State()
    doc = State()
    vremya = State()
    db_upload = State()

async def start_bot(bot: Bot): #определение асинхронной функции start_bot, принимающая объект bot класса Bot
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text='Бот запущен!') #отправка сообщения администратору о запуске бота

async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Бот остановлен!') #отправка сообщения администратору об остановке бота

async def start():
    logging.basicConfig(level=logging.INFO,  #настройка логирования
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                                "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
                        )
    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')  # Объект бота

    dp = Dispatcher()  # Диспетчер
    dp.startup.register(start_bot) #регистрация функции как обработчика события запуска бота
    dp.shutdown.register(stop_bot) #регистрация функции как обработчика события остановки бота
    dp.message.register(get_start, Command(commands=['start', 'run'])) #регистрация функции как обработчика сообщений с командами /start или /run
    dp.message.register(process_vibor_vracha, Register.doc)
    dp.message.register(process_vibor_vremya, Register.vremya)
    dp.message.register(get_name, Register.fullname)
    dp.message.register(get_date, Register.date_r)
    dp.message.register(set_DB, Register.db_upload)

    try:
        await dp.start_polling(bot) #запуск получения обновлений для бота
    finally:
        await bot.session.close() #закрытие сессии бота при завершении работы

async def get_start(message: Message, state: FSMContext, bot: Bot):
    await message.answer(f'Здравствуйте, <b>{message.from_user.first_name}</b>! '
                         f'Я виртуальный помощник, разработанный для помощи в записи на прием к врачу. '
                         f'Я могу предоставить информацию о доступных врачах, свободных местах и помочь '
                         f'вам записаться на прием онлайн.\n')
    await message.answer('Выберите <b>врача</b>, к которому хотите записаться.',
                         reply_markup=vrach)
    await state.set_state(Register.doc)

async def process_vibor_vracha(message: Message, state: FSMContext, bot: Bot):
    sendd = message.text
    await state.update_data(doc=sendd)
    if sendd == 'Терапевт':
        vrachi = terapevt
    elif sendd == 'Педиатр':
        vrachi = pediatr
    elif sendd == 'Офтальмолог':
        vrachi = oftalmolog
    elif sendd == 'Кардиолог':
        vrachi = kardiolog
    elif sendd == 'Гинеколог':
        vrachi = ginekolog
    elif sendd == 'Невролог':
        vrachi = nevrolog

    await message.answer('Выберите <b>дату</b> и <b>время</b>.',
                         reply_markup=vrachi)
    await state.set_state(Register.vremya)


async def process_vibor_vremya(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(vremya=message.text)
    await message.answer("Введите вашу Фамилию, Имя и Отчество (в формате Фамилия Имя Отчество):")
    await state.set_state(Register.fullname)


async def get_name(message: Message, state: FSMContext, bot: Bot):
    sendd = message.text
    if re.match(r"^[А-ЯЁ][а-яё]+\s[А-ЯЁ][а-яё]+\s[А-ЯЁ][а-яё]+$", sendd):
        await state.update_data(fullname=sendd)
        await message.answer("Теперь укажите свою дату рождения в формате ДД.ММ.ГГГГ (например, 01.01.1990):")
        await state.set_state(Register.date_r)
    else:
        await message.answer('Вы ввели некорректные данные. \n'
                             'Перепроверьте свои данные(орфографические ощибки учитывабтся) и  попробуйте снова')


async def get_date(message: Message, state: FSMContext):
    sendd = message.text
    if re.match(r"^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.\d{4}$", sendd):
        await state.update_data(date_r=sendd)
        await message.answer('Все данные получены.', reply_markup=zapis)
        await state.set_state(Register.db_upload)
    else:
        await message.answer('Вы ввели некорректные данные. \n'
                             'Перепроверьте свои данные(орфографические ощибки учитывабтся) и  попробуйте снова')

async def set_DB(message: Message, state: FSMContext):
    data = await state.get_data()

    wb = load_workbook('db_client.xlsx')
    sheet = wb['Клиенты']

    new_row = [data.get('fullname'), data.get('date_r'), data.get('doc'), data.get('vremya')]
    sheet.append(new_row)

    wb.save('db_client.xlsx')

def poshel():
    asyncio.run(start()) #запуск функции