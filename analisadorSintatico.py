from compiladorExceptions.programException import ProgramException
class Sintatico:
    LINE = 0
    TK_RESERVED = ""
    def __init__(self, token):
        self.token = token
        while(True):
            try:
                if(self.token.getTkName() == "DOT"):
                    return print("success!")
                    break

                if(self.token.getTkName() == "SEMICOLON"):
                    Sintatico.LINE += 1

                if(Sintatico.LINE == 0):
                    if(self.token.getTkName() == "PROGRAM"):
                        Sintatico.TK_RESERVED = "PROGRAM"                    
                    self.firstRoule(Sintatico.TK_RESERVED)                    
                    break
                else:
                    None
                    break
            except ProgramException:
                print('Erro Sintatico!')
                break

    def firstRoule(self, tk_aux):
        tk_name = self.token.getTkName()
        tk_type = self.token.getTkType()

        if(tk_aux == "PROGRAM"):
            if(tk_type == "ID" or tk_name == "SEMICOLON"):
                None
        else:    
            raise ProgramException

    def secondRoule(self):
        tk_name = self.token.getTkName()
        tk_type = self.token.getTkType()

        print(tk_name)

    def statementRoule(self):
        tk_name = self.token.getTkName()
        tk_type = self.token.getTkType()

        print(tk_type)

    def toString(self):
        print("token Name: "+self.token.getTkName() + " token Type: "+self.token.getTkType())