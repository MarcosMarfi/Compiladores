import re

from token import Token

class Lexico:
    index = 0
    currentLine = 1

    def __init__(self, code, rules, tks_reserved):
        self.code = code
        self.rules = rules
        self.tks_reserved = tks_reserved

    def endCode(self):
        return self.index >= len(self.code)

    def nextToken(self):
        searchToken = None

        if self.endCode():
            self.index = 0
            self.currentLine = 1
            return False

        for token in self.rules.keys():
            info = self.rules[token]
            info['compiled'] = re.compile(info['regex'])
            # print(info)
            searchToken = info['compiled'].match(self.code, self.index)

            # if the token is found, stop and move on to the next condition
            if searchToken:
                break
        
        # if token is found
        if searchToken:
            # if new line found, increase currentLine
            if "newline" in self.rules[token]:
                self.currentLine += 1
            
            # set index where the token found terminate
            self.index += len(searchToken.group())
        else:
            self.index+=1            
        
        return Token(searchToken.group().upper(), token, self.currentLine)