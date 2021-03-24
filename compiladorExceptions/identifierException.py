class IdentifierException(Exception):
    def __init__(self, msg, param):
        self.message = msg
        self.param = param

    def getError(self):
        return "error: { Message: "+self.message+", "+self.param+" }"