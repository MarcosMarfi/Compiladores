class BlockVarException(Exception):
    def __init__(self, msg, line):
        self.message = msg
        self.line = line

    def getError(self):
        return "error: { Message: "+self.message+", Linha: "+self.line+" }"
