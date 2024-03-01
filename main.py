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


@dp.message_handler(commands=['showtimes'])
async def showtimes(message: types.Message):
    log(message)
    request = message.text.split()
    t_date = datetime.now().strftime('%d_%m_%Y')
    if not os.path.isfile(f'data/data_{t_date}.csv'):  # check whether file exists
        try:
            await message.answer('Это первый запрос за день, придётся подождать...')
            fetch_data()
        except:
            await message.answer('Что-то пошло не так :/')
            return
    ext = ''
    if len(request) == 1:  # if only `/showtimes` command
        ext = 'xlsx'
    else:
        ext = request[1]

    if not os.path.isfile(f'data/data_{t_date}.{ext}'):
        await message.answer('Wrong file format requested')
    else:
        await message.answer_document(types.InputFile(f'data/data_{t_date}.{ext}'))


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
