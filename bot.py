import logging
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text

from keyboards import menuKb, joinGameKb, gameKb
from wordz import Wordz
from util import getUsername
from rules import rulesStr

from config import BOT_API_TOKEN, MIN_PLAYERS, MAX_PLAYERS, EXPIRATION_VALUE, START_KW

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot, dispatcher and the game
bot = Bot(token=BOT_API_TOKEN)
dp = Dispatcher(bot)
game = Wordz()


#============================================RULES ROUTE============================================
@dp.message_handler(text=START_KW)
async def ohHiMark(message: types.Message):
    await message.answer('Hello, I\'m a Bot who hosts a simple Words game. Each player should spell a word that starts with the last lesson of the previous word. Type \'/newgame\' to satrt and have fun!', 
                            reply_markup=menuKb)


#=========================================INIT STAGE ROUTES=========================================
@dp.message_handler(text='Rules 📖')
async def rulesI(message: types.Message):
    await message.answer(rulesStr, reply_markup=menuKb)


@dp.message_handler(text='New game 🎮')
async def newGame(message: types.Message):
    game.restart()
    global expiration
    expiration = datetime.now() + timedelta(minutes=EXPIRATION_VALUE)
    await message.answer(
        f'Waiting 2 minutes for players to join...', reply_markup=joinGameKb
    )


#====================================PLAYER POLLING STAGE ROUTES===================================
async def startGame(call: CallbackQuery):
    if not game.playing:
        game.start()
        await call.message.answer(
            ('Alright, the game begins!'+
            f'@{game.currentPlayer.name}, you can start with any word.'),
            reply_markup=gameKb)


@dp.callback_query_handler(text='joinGame')
async def joinGame(call: CallbackQuery):
    # Stop polling criterion
    if (expiration - datetime.now() <= timedelta(0) and
        len(game.players) < MIN_PLAYERS):
        return await call.message.answer(
            f'{EXPIRATION_VALUE} minutes passed, try to start the game again.'
        )

    # Add player criterion
    if not (game.checkPlayer(call.from_user.username) or game.playing):
        username = getUsername(call.from_user)
        game.addPlayer(username)
    
        updatedText = (
            call.message.text + f'\n\n@{username} joined!' + f'\n\n{len(game.players)}/{MAX_PLAYERS}.')
        await call.message.edit_text(text=updatedText)
        await call.message.edit_reply_markup(reply_markup=joinGameKb)
    else:
        await call.answer("You already joined the game!", show_alert=True)

    # Start game criterion
    if len(game.players) == MAX_PLAYERS:
        await startGame(call)


@dp.callback_query_handler(text='forceStart')
async def forceStart(call: CallbackQuery):
    if len(game.players) >= MIN_PLAYERS:
        await startGame(call)

    else: 
        await call.answer(
            'Not enough players to begin or game is already going.', show_alert=True
        )


#=========================================GAME STAGE ROUTES=========================================
@dp.message_handler(text='Rules 📙')
async def rulesG(message: types.Message):
    await message.answer(rulesStr, reply_markup=gameKb)


@dp.message_handler(text='Surrender 👋')
async def surrender(message: types.Message):
    if not game.playing: return

    username = getUsername(message.from_user)
    player = game.removePlayer(username)
    if game.playing:
        await message.answer(
            f'Player @{player.name} surrendered. His score - {player.score}'
        )
    else: 
        await message.answer((
            f'Game ended!\n\nCongratulations to @{player["winner"].name}, '+
            f'he won with the score {player["winner"].score} 🥳🎉.'
        ), reply_markup=menuKb)
        await message.answer(
            'All the words that were played:\n\n'+player["words"]
        )


@dp.message_handler(regexp='[A-Za-z ]+')
async def pollWord(message: types.Message):
    if not game.playing: return

    username = getUsername(message.from_user)
    if username == game.currentPlayer.name:
        msg = game.makeTurn(message.text)
        await message.answer(msg)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)