from aiogram.types import InlineKeyboardButton, \
                          InlineKeyboardMarkup, \
                          ReplyKeyboardMarkup, \
                          KeyboardButton

# Keyboard to handle 'join game' functionality
joinGameKb = InlineKeyboardMarkup(inline_keyboard=[
    [ InlineKeyboardButton(text='Join Game', callback_data='joinGame') ],
    [ InlineKeyboardButton(text='Force Start', callback_data='forceStart') ]
])

# Basic reply keyboard
newGameBtn = KeyboardButton(text='New game')
helpBtn = KeyboardButton('Help')
menuKb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
menuKb.add(newGameBtn).add(helpBtn)

# Game State keyboard
rulesBtn = KeyboardButton(text='Rules') 
surrenderBtn = KeyboardButton(text='Surrender')
gameKb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
gameKb.add(surrenderBtn).add(rulesBtn)