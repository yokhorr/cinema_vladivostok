import os
from aiogram import Bot, Dispatcher, executor, types
from fetch_data import fetch_data
from datetime import datetime

API_TOKEN = open('.bot_token.txt').read()[:-1]  # get bot token from your file
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# command for devs
@dp.message_handler(commands=['klenin'])
async def dev(message: types.Message):
    await message.answer('Семь бед — один ответ: Костыль и велосипед!')


@dp.message_handler(commands=['showtimes'])
async def lev(message: types.Message):
    t_date = datetime.now().strftime('%d_%m_%Y')
    if not os.path.isfile(f'data_{t_date}.csv'):  # check whether file exists
        fetch_data()
    await message.answer_document(types.InputFile(f'data_{t_date}.csv'))


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer('Привет! Введи команду /showtimes, чтобы получить актуальное расписание сеансов на ближайшие '
                         'дни.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)  # start bot
