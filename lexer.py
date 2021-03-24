import re

from token import Token

class Lexico:
    INDEX = 0
    CURRENT_LINE = 1

    def __init__(self, code, rules, tks_reserved):
        self.code = code
        self.rules = rules
        self.tks_reserved = tks_reserved

    def endCode(self):
        return Lexico.INDEX >= len(self.code)

    def nextToken(self):
        searchToken = None

        if self.endCode():
            return False

        for token in self.rules.keys():
            info = self.rules[token]
            info['compiled'] = re.compile(info['regex'])
            # print(info)
            searchToken = info['compiled'].match(self.code, Lexico.INDEX)

            # if the token is found, stop and move on to the next condition
            if searchToken:
                break
        
        # if token is found
        if searchToken:
            # if new line found, increase CURRENT_LINE
            if "newline" in self.rules[token]:
                Lexico.CURRENT_LINE += 1
            
            # set index where the token found terminate
            Lexico.INDEX += len(searchToken.group())
        else:
            Lexico.INDEX+=1            
        
        return Token(searchToken.group().upper(), token, Lexico.CURRENT_LINE)