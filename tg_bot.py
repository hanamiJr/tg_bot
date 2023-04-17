import logging
import asyncio
from datetime import datetime, time, timedelta
from aiogram import Bot, Dispatcher, executor, types

TOKEN = ''
MSG = 'Time to work!'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

bot_active = True

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} {user_full_name=} {datetime.now()}')
    await message.reply(f'Привет, {user_name}!')

    # Определяем время первой отправки сообщения
    now = datetime.now()
    start_time = datetime.combine(now.date(), time(hour=21, minute=20))

    # Если текущее время уже больше указанного времени, то первая отправка сообщения будет завтра
    if now > start_time:
        start_time += timedelta(days=1)

    # Рассчитываем интервал между отправками сообщений (1 день)
    interval = timedelta(days=1)

    # Отправляем сообщения с интервалом в 1 день до тех пор, пока флаг bot_active равен True
    while bot_active:
        await bot.send_message(user_id, MSG.format(user_name))
        logging.info(f'{user_id=} {user_full_name=} {datetime.now()}')
        start_time += interval
        time_to_sleep = (start_time - datetime.now()).total_seconds()
        if time_to_sleep > 0:
            await asyncio.sleep(time_to_sleep)

@dp.message_handler(commands=['stop'])
async def stop_handler(message: types.Message):
    global bot_active
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} {user_full_name=} {datetime.now()}')
    await message.reply('Остановка бота')
    bot_active = False

if __name__ == '__main__':
    executor.start_polling(dp)
