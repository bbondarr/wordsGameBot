import re

def getUsername(user):
    return (user.username or
            user.first_name or 
            user.last_name
    )

def wordsToStr(words):
    str = ''
    for player, vals in words.items():
        str += f'{player} words:\n'
        for words in vals:
            str += f'\t{words}\n'
    return str

def checkWord(func):
    def inner (val):
        val = str(val)
        if re.search(r'[^A-Za-z]+', val) is not None: 
                return None
        return func(val)            

    return inner  

def checkWordFirstChar(currWord, prevWord):
    return currWord.startswith(prevWord[-1])