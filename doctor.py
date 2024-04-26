import pandas as pd

df = pd.read_excel('doctors_schedule.xlsx')
first_sheet = df[df.columns[0]]