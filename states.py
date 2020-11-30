from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup

class WordzStateGroup(StatesGroup):
    initialState = State()
    pollingState = State()
    gameState    = State()