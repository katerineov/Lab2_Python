import logging
from aiogram import Bot, Dispatcher, F, types #, executor
from aiogram.fsm.state import StatesGroup, State
import asyncio
from aiogram.filters import Command
from core.settings import settings
from core.utils.commands import set_commands
from aiogram.fsm.context import FSMContext
from aiogram import Bot
from aiogram.types import Message
from core.keyboards.reply import zapis, vrach, terapevt, pediatr
from core.keyboards.reply import oftalmolog, kardiolog, ginekolog, nevrolog
import pandas as pd

class Register(StatesGroup):
    fullname = State()
    date_r = State()
    doc = State()
    vremya = State()

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
    dp.message.register(process_vibor_vracha, F.text == 'Записаться на приём')
    dp.message.register(process_vibor_terapevt, F.text == 'Терапевт')
    dp.message.register(process_vibor_pediatr, F.text == 'Педиатр')
    dp.message.register(process_vibor_oftalmolog, F.text == 'Офтальмолог')
    dp.message.register(process_vibor_kardiolog, F.text == 'Кардиолог')
    dp.message.register(process_vibor_ginekolog, F.text == 'Гинеколог')
    dp.message.register(process_vibor_nevrolog, F.text == 'Невролог')
    dp.message.register(get_name, Register.fullname)
    dp.message.register(get_date, Register.date_r)

    try:
        await dp.start_polling(bot) #запуск получения обновлений для бота
    finally:
        await bot.session.close() #закрытие сессии бота при завершении работы

async def get_start(message: Message, state: FSMContext, bot: Bot):
    await message.answer(f'Здравствуйте, <b>{message.from_user.first_name}</b>! '
                         f'Я виртуальный помощник, разработанный для помощи в записи на прием к врачу. '
                         f'Я могу предоставить информацию о доступных врачах, свободных местах и помочь '
                         f'вам записаться на прием онлайн.',
                         reply_markup=zapis)
    await state.set_state(Register.doc)

async def process_vibor_vracha(message: Message, state: FSMContext, bot: Bot):
    await message.answer('Выберите <b>врача</b>, к которому хотите записаться.',
                             reply_markup=vrach)
    await state.update_data(doc=message.text)
    await state.set_state(Register.vremya)

async def process_vibor_terapevt(message: Message, state: FSMContext, bot: Bot):
    await message.answer('Выберите <b>дату</b> и <b>время</b>.',
                         reply_markup=terapevt)
    await state.update_data(vreamya=message.text)
    await state.set_state(Register.fullname)

async def process_vibor_pediatr(message: Message, state: FSMContext, bot: Bot):
    await message.answer('Выберите <b>дату</b> и <b>время</b>.',
                         reply_markup=pediatr)
    await state.update_data(vreamya=message.text)
    await state.set_state(Register.fullname)

async def process_vibor_oftalmolog(message: Message, state: FSMContext, bot: Bot):
    await message.answer('Выберите <b>дату</b> и <b>время</b>.',
                         reply_markup=oftalmolog)
    await state.update_data(vreamya=message.text)
    await state.set_state(Register.fullname)

async def process_vibor_kardiolog(message: Message, state: FSMContext, bot: Bot):
    await message.answer('Выберите <b>дату</b> и <b>время</b>.',
                         reply_markup=kardiolog)
    await state.update_data(vreamya=message.text)
    await state.set_state(Register.fullname)

async def process_vibor_ginekolog(message: Message, state: FSMContext, bot: Bot):
    await message.answer('Выберите <b>дату</b> и <b>время</b>.',
                         reply_markup=ginekolog)
    await state.update_data(vreamya=message.text)
    await state.set_state(Register.fullname)

async def process_vibor_nevrolog(message: Message, bot: Bot, state: FSMContext):
    await message.answer('Выберите <b>дату</b> и <b>время</b>.',
                         reply_markup=nevrolog)
    await state.update_data(vreamya=message.text)
    await state.set_state(Register.fullname)

async def get_name(message: Message, state: FSMContext, bot: Bot):
    await message.answer("Введите вашу Фамилию, Имя и Отчество (в формате Фамилия Имя Отчество):")
    await state.update_data(fullname=message.text)
    await state.set_state(Register.date_r)

async def get_date(message: Message, state: FSMContext):
    await message.answer("Теперь укажите свою дату рождения в формате ДД.ММ.ГГГГ (например, 01.01.1990):")
    await state.update_data(date_r=message.text)
    await state.clear()
def poshel():
    asyncio.run(start()) #запуск функции