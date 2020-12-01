from datetime import datetime, timedelta

from aiogram.types import Message, CallbackQuery

from loader import bot, dp, game
from util import getUsername
from messages import helloStr, rulesStr
from keyboards import menuKb, joinGameKb, gameKb, settingsKb, choiseKb
from config import START_KW, MIN_PLAYERS, MAX_PLAYERS, EXPIRATION_VALUE


#============================================MENU ROUTE============================================
@dp.message_handler(text=[*START_KW, 'Back ◁'])
async def ohHiMark(message: Message):
    await message.answer(helloStr, reply_markup=menuKb)


#=========================================INIT STAGE ROUTES=========================================
@dp.message_handler(text='Rules 📖')
async def rulesI(message: Message):
    await message.answer(rulesStr, reply_markup=menuKb)


@dp.message_handler(text='New game 🎮')
async def newGame(message: Message):
    game.restart()
    global expiration
    expiration = datetime.now() + timedelta(minutes=EXPIRATION_VALUE)
    await message.answer(
        f'Waiting 2 minutes for players to join...\n' + '🧑‍💻' * MAX_PLAYERS, 
        reply_markup=joinGameKb
    )


#==========================================SETTINGS ROUTES==========================================
@dp.message_handler(text='Settings ⚙️')
async def settings(message: Message):
    await message.answer(
        f'Choose what you wanna change:', reply_markup=settingsKb
    )


@dp.message_handler(text='Change Max. Players 👫')
async def setMaxPlayers(message: Message):
    # await message.answer(
    #     f'Set up maximal amount of players.\n\nCurrent - {MAX_PLAYERS}', 
    #     reply_markup=choiseKb
    # )
    await message.answer(
        'Gonna be implemented soon... 🔨', reply_markup=settingsKb
    )


@dp.callback_query_handler(text='inc')
async def incrementPlayers(call: CallbackQuery, max=MAX_PLAYERS):
    # max += 1
    # updatedText = call.message.text.replace(f'{max-1}', str(max))
    # await call.message.edit_text(updatedText, reply_markup=choiseKb)
    # MAX_PLAYERS = max
    await call.message.edit_text('Gonna be implemented soon...')


@dp.callback_query_handler(text='dec')
async def decrementPlayers(call: CallbackQuery, max=MAX_PLAYERS):
    # max -= 1
    # updatedText = call.message.text.replace(f'{max+1}', str(max))
    # await call.message.edit_text(updatedText, reply_markup=choiseKb)
    # MAX_PLAYERS = max
    await call.message.edit_text('Gonna be implemented soon...')


#====================================PLAYER POLLING STAGE ROUTES===================================
async def startGame(call: CallbackQuery):
    if not game.playing:
        game.start()
        await call.message.answer(
            ('Alright, the game begins! '+
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
            call.message.text + f'\n\n@{username} joined!' + 
            f'\n\n{len(game.players)}/{MAX_PLAYERS}.'
        ).replace('🧑‍💻', '🙋', 1)
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
async def rulesG(message: Message):
    await message.answer(rulesStr, reply_markup=gameKb)


@dp.message_handler(text='Surrender 👋')
async def surrender(message: Message):
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


@dp.message_handler(regexp='[A-Za-z]+')
async def pollWord(message: Message):
    if not game.playing: return

    username = getUsername(message.from_user)
    if username == game.currentPlayer.name:
        msg = game.makeTurn(message.text)
        await message.answer(msg)