import datetime
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from datetime import datetime
import doctor
import pandas as pd

df = pd.read_excel('doctors_schedule.xlsx')
first_sheet = df[df.columns[0]]
time_string = datetime.strftime(df.iloc[0, 1], '%Y-%m-%d %H:%M:%S')

zapis = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Записаться на приём')]],
                            resize_keyboard=True,
                            input_field_placeholder='Запишитесь')

ok = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='OK'), ]],
                         resize_keyboard=True,
                         input_field_placeholder='Чтобы продолжить нажмите OK')

vrach = ReplyKeyboardMarkup(keyboard=[
    [
    KeyboardButton(text=first_sheet[0]),
    KeyboardButton(text=first_sheet[1]),
    KeyboardButton(text=first_sheet[2])
    ],
    [
    KeyboardButton(text=first_sheet[3]),
    KeyboardButton(text=first_sheet[4]),
    KeyboardButton(text=first_sheet[5])
    ]
], resize_keyboard=True, input_field_placeholder='Выберите доктора')

terapevt = ReplyKeyboardMarkup(keyboard=[
    [
    KeyboardButton(text=datetime.strftime(df.iloc[0, 1], '%Y-%m-%d %H:%M:%S')),
    KeyboardButton(text=datetime.strftime(df.iloc[0, 2], '%Y-%m-%d %H:%M:%S')),
    KeyboardButton(text=datetime.strftime(df.iloc[0, 3], '%Y-%m-%d %H:%M:%S'))
    ]
], resize_keyboard=True)

pediatr = ReplyKeyboardMarkup(keyboard=[
    [
    KeyboardButton(text=datetime.strftime(df.iloc[1, 1], '%Y-%m-%d %H:%M:%S')),
    KeyboardButton(text=datetime.strftime(df.iloc[1, 2], '%Y-%m-%d %H:%M:%S')),
    KeyboardButton(text=datetime.strftime(df.iloc[1, 3], '%Y-%m-%d %H:%M:%S'))
    ]
], resize_keyboard=True)

oftalmolog = ReplyKeyboardMarkup(keyboard=[
    [
    KeyboardButton(text=datetime.strftime(df.iloc[2, 1], '%Y-%m-%d %H:%M:%S')),
    KeyboardButton(text=datetime.strftime(df.iloc[2, 2], '%Y-%m-%d %H:%M:%S')),
    KeyboardButton(text=datetime.strftime(df.iloc[2, 3], '%Y-%m-%d %H:%M:%S'))
    ]
], resize_keyboard=True)

kardiolog = ReplyKeyboardMarkup(keyboard=[
    [
    KeyboardButton(text=datetime.strftime(df.iloc[3, 1], '%Y-%m-%d %H:%M:%S')),
    KeyboardButton(text=datetime.strftime(df.iloc[3, 2], '%Y-%m-%d %H:%M:%S')),
    KeyboardButton(text=datetime.strftime(df.iloc[3, 3], '%Y-%m-%d %H:%M:%S'))
    ]
], resize_keyboard=True)

ginekolog = ReplyKeyboardMarkup(keyboard=[
    [
    KeyboardButton(text=datetime.strftime(df.iloc[4, 1], '%Y-%m-%d %H:%M:%S')),
    KeyboardButton(text=datetime.strftime(df.iloc[4, 2], '%Y-%m-%d %H:%M:%S')),
    KeyboardButton(text=datetime.strftime(df.iloc[4, 3], '%Y-%m-%d %H:%M:%S'))
    ]
], resize_keyboard=True)

nevrolog = ReplyKeyboardMarkup(keyboard=[
    [
    KeyboardButton(text=datetime.strftime(df.iloc[5, 1], '%Y-%m-%d %H:%M:%S')),
    KeyboardButton(text=datetime.strftime(df.iloc[5, 2], '%Y-%m-%d %H:%M:%S')),
    KeyboardButton(text=datetime.strftime(df.iloc[5, 3], '%Y-%m-%d %H:%M:%S'))
    ]
], resize_keyboard=True)




# def get_reply_keyboard():
#     keyboard_builder = ReplyKeyboardBuilder()
#
#     keyboard_builder.button(text='Кнопка 1')
#     keyboard_builder.button(text='Кнопка 2')
#     keyboard_builder.button(text='Кнопка 3')
#     keyboard_builder.button(text='Отправить свой контакт', request_contact=True)
#     keyboard_builder.adjust(2, 2)
#
#     return keyboard_builder.as_markup(resize_keyboard=True, input_field_placeholder='Выбери кнопку',
#                                       one_time_keyboard=True)

# reply_keyboard = ReplyKeyboardMarkup(keyboard=[
#     [
#         KeyboardButton(text='Ряд 1. Кнопка 1'),
#         KeyboardButton(text='Ряд 1. Кнопка 2'),
#         KeyboardButton(
#             text='Ряд 1. Кнопка 3'
#         )
#     ],
#     [
#         KeyboardButton(
#             text='Отправить свой контакт',
#             request_contact=True
#         ),
#         KeyboardButton(
#             text='Ряд 2. Кнопка 2'
#         ),
#         KeyboardButton(
#             text='Ряд 2. Кнопка 3'
#         ) ,
#         KeyboardButton(
#             text='Ряд 2. Кнопка 4'
#         )
#     ]
# ], resize_keyboard=True, input_field_placeholder='Выбери кнопку') #one_time_keyboard=True
