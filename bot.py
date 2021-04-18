import logging
import os

from config import *

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.utils import executor
from calendarik import calendar_callback, create_calendar, process_calendar_selection

logging.basicConfig(filename="bot.log", level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
datefmt='%d-%b-%y %H:%M:%S')

bot = Bot(token=TG_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# poll = 30

# starting bot when user sends `/start` command, answering with inline calendar
@dp.message_handler(commands=['select_date'])
async def cmd_start(message: types.Message):
    await message.answer("Please select a date: ", reply_markup=create_calendar())

@dp.callback_query_handler(calendar_callback.filter())  # handler is processing only calendar_callback queries
async def cmd_start(message: types.Message):
    await message.answer("Please select a date: ", reply_markup=create_calendar())

@dp.callback_query_handler(calendar_callback.filter())  # handler is processing only calendar_callback queries
async def process_name(callback_query: CallbackQuery, callback_data: dict):
    selected, date = await process_calendar_selection(callback_query, callback_data)
    if selected:
    	# db.add_user_with_date(callback_query.from_user.first_name, callback_query.from_user.last_name ,date.strftime("%d/%m/%Y"))
        await callback_query.message.answer(
        	'''You,\n{} {}\nid: {}\nselected {}'''.format(
        		callback_query.from_user.first_name, 
        		callback_query.from_user.last_name,
        		callback_query.from_user.id, date.strftime("%d/%m/%Y")
        	), 
        	reply_markup=ReplyKeyboardRemove()
        )

@dp.message_handler(commands=['my_id'])
async def my_id(message: types.Message):
	await message.answer("{}".format(message.from_user.id))

if __name__ == '__main__':
	# loop = asyncio.get_event_loop()
    # loop.create_task(periodic(poll))
    executor.start_polling(dp, skip_updates=True)