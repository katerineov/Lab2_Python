import pandas as pd
from aiogram.fsm.state import StatesGroup, State
import asyncio
from bot import Register



async def zanesenie(znach, nomer_st):
    df = pd.read_excel('doctors_schedule.xlsx', sheet_name='Клиенты')
    data = await State.get_data()
    empty_row = df['fullname'].isnull().idxmax()

    if pd.isnull(df.iloc[empty_row, 0]):
        # Если ячейка пустая, заносим данные в эту строку
        df.iloc[empty_row, 0] = znach
    else:
        # Если ячейка занята, заносим данные в следующую строку
        df.loc[empty_row + 1, 'fullname'] = znach

    # Сохраняем изменения обратно в Excel файл
    return df.to_excel('doctors_schedule.xlsx', sheet_name='Клиенты', index=False)

print(zanesenie('да', 1))