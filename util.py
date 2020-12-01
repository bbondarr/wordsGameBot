import re


def getUsername(user):
    return (user.username or
            user.first_name or 
            user.last_name
    )


def wordsToStr(word):
    str = ''
    for player, words in word.items():
        str += f'@{player} words ({len(words)}):\n'
        for word in words:
            str += f'\t\t{word}\n'
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