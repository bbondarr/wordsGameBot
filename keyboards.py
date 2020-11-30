from aiogram.types import InlineKeyboardButton, \
                          InlineKeyboardMarkup, \
                          ReplyKeyboardMarkup, \
                          KeyboardButton

# Keyboard to handle 'join game' functionality
joinGameKb = InlineKeyboardMarkup(inline_keyboard=[
    [ InlineKeyboardButton(text='Join Game', callback_data='joinGame') ]
])

# Basic reply keyboard
newGameBtn = KeyboardButton(text='/newgame')
endGameBtn = KeyboardButton(text='/endgame')
helpBtn = KeyboardButton('/help')
menuKb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
menuKb.add(newGameBtn).add(endGameBtn).add(helpBtn)