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
newGameBtn = KeyboardButton('New game 🎮')
settingsBtn = KeyboardButton('Settings ⚙️')
helpBtn = KeyboardButton('Rules 📖')
menuKb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
menuKb.add(newGameBtn).add(settingsBtn).add(helpBtn)

# Game State keyboard
rulesBtn = KeyboardButton('Rules 📙') 
surrenderBtn = KeyboardButton('Surrender 👋')
gameKb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
gameKb.add(surrenderBtn).add(rulesBtn)

# Settings keyboard
setMaxPlayersBtn = KeyboardButton('Change Max. Players 👫')
goBackBtn = KeyboardButton('Back ◁')
settingsKb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
settingsKb.add(setMaxPlayersBtn).add(goBackBtn)

# Settings inner keyboard
choiseKb = InlineKeyboardMarkup(inline_keyboard=[
    [ InlineKeyboardButton(text='+', callback_data='inc') ],
    [ InlineKeyboardButton(text='-', callback_data='dec') ]    
])