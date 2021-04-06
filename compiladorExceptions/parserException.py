class ParserException(Exception):
    def __init__(self, msg, line):
        self.message = msg
        self.line = line

    def getError(self):
        return "error Sintatico: { Message: "+self.message+", Linha: "+self.line+" }"
