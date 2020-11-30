import random
import requests

from config import MAX_PLAYERS, WORDS_API_TOKEN, HOST

url = "https://wordsapiv1.p.rapidapi.com/words/hatchback"

headers = {
    'x-rapidapi-key': WORDS_API_TOKEN,
    'x-rapidapi-host': HOST
    }

response = requests.request("GET", url, headers=headers)

print(response.text)

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

class Wordz:
    MAX_PLAYERS = 4

    def __init__(self):
        self.playing = False
        self.players = []
        self.currentPlayer = None

    def addPlayer(self, playerName):
        if len(self.players) < self.MAX_PLAYERS and not self.checkPlayer(playerName):
            self.players.append(Player(playerName))

    def checkPlayer(self, playerName):
        res = [p.name for p in self.players if p.name == playerName]
        return bool(len(res))

    def start(self):
        self.playing = True
        self.currentPlayer = self.players[0]
        return 'startGamePlaceholder'

    def makeTurn(self, word):
        
        if word:
            self.currentPlayer.score += 1
            next = self.players.index(self.currentPlayer)+1 
            if self.players.index(self.currentPlayer)+1 >= len(self.players):
                next = 0

            self.currentPlayer = self.players[next]

    def restart(self):
        self.__init__()