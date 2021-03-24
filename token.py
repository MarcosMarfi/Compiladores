class Token:
    def __init__(self, tk_name, tk_type, line):
        self.token = tk_name
        self.type = tk_type
        self.line = line
    
    def getTkName(self):
        return self.token

    def setTkName(self, tk_name):
        self.type = tk_name
    
    def getTkType(self):
        return self.type
    
    def setTkType(self, tk_type):
        self.type = tk_type
    
    def getTkLine(self):
        return self.line
    
    def toString():
        return "Token Name: "+self.token.getTkName()+" Token Type: "+self.token.getTkType()