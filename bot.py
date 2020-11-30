import logging
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message, CallbackQuery

from keyboards import menuKb, joinGameKb
from wordz import Wordz

from config import BOT_API_TOKEN, EXPIRATION_VALUE

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot, dispatcher and the game
bot = Bot(token=BOT_API_TOKEN)
dp = Dispatcher(bot)
game = Wordz()


#====================================ROUTES=======================================
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    
    await message.answer('Hello, I\'m a Bot who hosts a simple Words game. Each player should spell a word that starts with the last lesson of the previous word. Type \'/newgame\' to satrt and have fun!', 
                            reply_markup=menuKb)


@dp.message_handler(commands=['newgame'])
async def newGame(message: types.Message):
    game.restart()
    global expiration
    expiration = datetime.now() + timedelta(minutes=EXPIRATION_VALUE)
    await message.answer(f'Waiting 2 minutes for players to join...', 
                            reply_markup=joinGameKb)


@dp.callback_query_handler(text='joinGame')
async def joinGame(call: CallbackQuery):
    # Stop polling criterion
    if (expiration - datetime.now() <= timedelta(0) and
        len(game.players) < 2):
        return await call.message.answer('2 minutes passed, try to start the game again.')
    
    # Add player criterion
    if not game.checkPlayer(call.from_user.username):
        username = (call.from_user.username or
                    call.from_user.first_name or 
                    call.from_user.last_name)

        game.addPlayer(username)
    
        updatedText = (
            call.message.text + f'\n\n@{username} joined!' + f'\n\n{len(game.players)}/4.')
        await call.message.edit_text(text=updatedText)
        await call.message.edit_reply_markup(reply_markup=joinGameKb)
    else:
        await call.answer("You already joined the game!", show_alert=True)

    # Start game criterion
    if (len(game.players) == 4 or 
        expiration - datetime.now() <= timedelta(0) and len(game.players) >= 2):
        await call.message.answer(game.start())



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)