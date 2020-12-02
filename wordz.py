import requests
import json

from config import MAX_PLAYERS as _MAX_PLAYERS, WORDS_API_TOKEN, HOST
from util import checkWord, checkWordFirstChar, wordsToStr


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0


class Wordz:
    MAX_PLAYERS = _MAX_PLAYERS
    mode = 'default'

    def __init__(self):
        self.words = {}
        self.playing = False
        self.players = []
        self.currentPlayer = None
        self.previousWord = None


    def addPlayer(self, playerName):
        if len(self.players) < self.MAX_PLAYERS and not self.checkPlayer(playerName):
            self.players.append(Player(playerName))
            self.words[playerName] = []


    def removePlayer(self, playerName):
        player = [p for p in self.players if p.name == playerName][0]
        
        # Changing turns
        if self.currentPlayer.name == player.name:
            next = self.players.index(self.currentPlayer)+1 
            if self.players.index(self.currentPlayer)+1 >= len(self.players):
                next = 0
            self.currentPlayer = self.players[next]

        self.players = [p for p in self.players if p.name != playerName]
        if len(self.players) == 1:
            return self.end()
        return player


    def checkPlayer(self, playerName):
        res = [p.name for p in self.players if p.name == playerName]
        return bool(len(res))


    def start(self):
        self.playing = True
        self.currentPlayer = self.players[0]


    def makeTurn(self, word):
        response = Wordz.requestWord(word)
        try:
            word = response['word']
            definition = response['definition']
            definition = f'{word} - {definition}\n\n🧑‍🎓📃'
        except KeyError: pass
        except TypeError: word = None

        if not word:
            return {'message': 'There is no such word in a dictionary. ❌'}
        
        if len(word) < 3:
            return {'message': 'Word must be at least 3 characters long. ❌'}

        if self.previousWord and not checkWordFirstChar(word, self.previousWord):
            return {'message': 'Nice try, but you\'ve missed the first letter. ❌'}

        if [v for k, v in self.words.items() if word in v]:
            return {'message': 'The word was already used. ❌'}

        self.currentPlayer.score += 1
        self.words[self.currentPlayer.name].append(word)
        self.previousWord = word
        next = self.players.index(self.currentPlayer)+1 
        if self.players.index(self.currentPlayer)+1 >= len(self.players):
            next = 0

        prevName = self.currentPlayer.name
        self.currentPlayer = self.players[next]

        return {'message': (f'Wise choise, @{prevName}! ✅\n'+
                f'@{self.currentPlayer.name}, yours on \'{word[-1].upper()}\'.'
        ),      'definition': definition}


    @staticmethod
    @checkWord
    def requestWord(word):
        word = word.lower()

        url = f'https://wordsapiv1.p.rapidapi.com/words/{word}'
        headers = {
            'x-rapidapi-key': WORDS_API_TOKEN,
            'x-rapidapi-host': HOST
            }
        response = requests.request("GET", url, headers=headers).json()
        try:
            partOfSpeech = response['results'][0]['partOfSpeech']
            if partOfSpeech == 'noun' or partOfSpeech == 'verb':
                word = response['word']
                return {'word': word, 
                        'definition': response['results'][0]['definition']}
        except KeyError: 
            return None


    def end(self):
        self.playing = False
        return {"winner": self.players[0],
                "words": wordsToStr(self.words)}


    def restart(self):
        self.__init__()