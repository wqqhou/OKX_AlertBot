# Logging module
import logging

# Aiogram imports
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode, ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

# Local modules to work with Database and Ton network
import config
import info
import db

# Now all the info about bot work will be printed out to console
logging.basicConfig(level=logging.INFO)

# Initialize the bot and dispatcher
bot = Bot(token=config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=['start', 'help'])
async def welcome_handler(message: types.Message):
    # Function that sends the welcome message with main keyboard to user
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(KeyboardButton('Register'), KeyboardButton('Unregister'))


    # Send welcome text and include the keyboard
    await message.answer('Current watch list: TON',
                         reply_markup=keyboard,
                         parse_mode=ParseMode.MARKDOWN)
    
@dp.message_handler(commands='Register')
@dp.message_handler(Text(equals='Register', ignore_case=True))
async def deposit_handler(message: types.Message):

    uid = message.from_user.id
    if db.check_subscriber(uid):
        await message.answer('You are already registered')
    else:
        db.add_subscriber(uid)
        await message.answer('You are successfully registered')
    
@dp.message_handler(commands='Unregister')
@dp.message_handler(Text(equals='Unregister', ignore_case=True))
async def deposit_handler(message: types.Message):

    uid = message.from_user.id
    if db.check_subscriber(uid):
        if db.remove_subscriber(uid):
            await message.answer('You are successfully unregistered')
        else:
            await message.answer('Something went wrong')
    else:
        await message.answer('You are not registered')

if __name__ == '__main__':
    # Create Aiogram executor for our bot
    ex = executor.Executor(dp)

    # Launch the deposit waiter with our executor
    ex.loop.create_task(info.start())

    # Launch the bot
    ex.start_polling()