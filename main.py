import os
import csv
from aiogram import Bot, Dispatcher, executor, types
from fetch_data import fetch_data
from datetime import datetime

API_TOKEN = open('.bot_token.txt').read()[:-1]  # get bot token from your file
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# command for devs
@dp.message_handler(commands=['klenin'])
async def dev(message: types.Message):
    log(message)
    await message.answer('Семь бед — один ответ: Костыль и велосипед!')


@dp.message_handler(commands=['info'])
async def dev(message: types.Message):
    log(message)
    await message.answer(open('info.md').read(), parse_mode='MarkdownV2')


@dp.message_handler(commands=['cities'])
async def dev(message: types.Message):
    log(message)
    await message.answer(open('cities.txt').read())


@dp.message_handler(commands=['showtimes'])
async def showtimes(message: types.Message):
    log(message)
    request = message.text.split()
    city = 'vladivostok'
    ext = 'xlsx'
    cities = ['vladivostok', 'artem', 'arsenyev', 'ussuriysk', 'nakhodka', 'spassk', 'vrangel', 'dalnegorsk',
              'partizansk', 'chernigovka', 'preobrazhenie']
    if len(request) > 1:
        if not (0 <= int(request[1]) <= 10):
            await message.answer('Указан неверный номер города.')
            return
        city = cities[int(request[1])]
        print(city)
    if len(request) > 2:
        ext = request[2]
    t_date = datetime.now().strftime('%d_%m_%Y')
    if not os.path.isfile(f'data/data_{city}_{t_date}.json'):  # check whether file exists
        try:
            await message.answer('Это первый запрос за день, придётся подождать...')
            fetch_data(city)
        except:
            await message.answer('Что-то пошло не так :/')
            return

    if not os.path.isfile(f'data/data_{city}_{t_date}.{ext}'):
        await message.answer('Указан неверный формат файла')
    else:
        await message.answer_document(types.InputFile(f'data/data_{city}_{t_date}.{ext}'))


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    log(message)
    await message.answer(open('greet.md').read(), parse_mode='MarkdownV2')


def log(message: types.Message):
    with open('log.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow(
            [message.date.date(), message.date.time(), message.from_user.id, message.from_user.username,
                message.from_user.first_name, message.from_user.last_name, message.text]
        )


@dp.message_handler()
async def log_messages(message: types.Message):
    log(message)


if __name__ == '__main__':
    if not os.path.isfile('log.csv'):  # create a log file if needed
        with open('log.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow(
                ['Date', 'Time', 'ID', 'Username', 'First name', 'Last name', 'Message']
            )
    executor.start_polling(dp, skip_updates=True)  # start bot
