from compiladorExceptions.blockProgramException import BlockProgramException
from compiladorExceptions.blockVarException import BlockVarException
class Sintatico:
    lineno = 0
    LINE = 0
    COUNT = 0
    BLOCK = ""
    PREV_TOKEN = ""
    RULES_BLOCK_VARS = []
    def __init__(self, token):
        self.token = token        
        
        if(self.token.getTkName() == "PROGRAM"):
            Sintatico.BLOCK = "PROGRAM"
        elif(self.token.getTkName() == "VAR"):
            Sintatico.BLOCK = "VAR"
        elif(self.token.getTkName() == "BEGIN"):
            Sintatico.BLOCK = "BEGIN"

        if(self.token.getTkName() == "NEW_LINE"):
            self.lineno += 1

        if(Sintatico.LINE == 0):
            if(self.token.getTkName() == "PROGRAM"):
                Sintatico.BLOCK = "PROGRAM"
            else:
                if(self.token.getTkName() == "SEMICOLON"):
                    Sintatico.LINE += 1
            self.firstRoule()      
        elif(Sintatico.LINE == 1):
            # Sintatico.BLOCK = ""
            if(self.token.getTkName() == "VAR"):
                Sintatico.BLOCK = "VAR"
            else:
                if(self.token.getTkName() == "BEGIN"):
                    Sintatico.LINE += 1
            self.secondRoule()
            # print("Block VAR!", self.token.getTkName(), Sintatico.BLOCK)
            # Sintatico.LINE += 1         
        else:
            if(self.token.getTkName() == "DOT"):
                 print("Execute with Success!")

    def firstRoule(self):
        tk_name = self.token.getTkName()
        tk_type = self.token.getTkType()

        if(Sintatico.BLOCK == "PROGRAM"):
            if(tk_type == "ID"):
                Sintatico.COUNT+=1
        else:
            raise BlockProgramException("Error Sintatico!", "1")

        if(Sintatico.COUNT > 1):
            Sintatico.COUNT = 0
            raise BlockProgramException("Error Sintatico!", "1")

    def secondRoule(self):
        tk_name = self.token.getTkName()
        tk_type = self.token.getTkType()
        # ruleVars = ()

        if(Sintatico.BLOCK == "VAR"):
            if(tk_name != "VAR" and tk_name != "BEGIN" and tk_name != "SEMICOLON"):
                Sintatico.RULES_BLOCK_VARS.append({tk_name, tk_type})
                if(tk_type == "ID"):
                    Sintatico.PREV_TOKEN = tk_type

                # elif(tk_name == "COMMA"):
                #     Sintatico.RULES_BLOCK_VARS.add(tk_name)
                # elif(tk_name == "COLON"):
                #     Sintatico.RULES_BLOCK_VARS.add(tk_name)
                # elif(tk_name == "INTEGER" or tk_name == "BOOLEAN" or tk_name == "CHAR"):
                #     Sintatico.RULES_BLOCK_VARS.add(tk_name)
                # else:
                #     raise BlockVarException("Error Sintatico!", tk_name)                        
        else:
            raise BlockVarException("Error Sintatico!", tk_name)
        
        # if(len(Sintatico.RULES_BLOCK_VARS)>0):
        #     for j in range(len(Sintatico.RULES_BLOCK_VARS)-1):
        #         print(Sintatico.RULES_BLOCK_VARS[j])
        # print(tk_name)

    def statementRoule(self):
        tk_name = self.token.getTkName()
        tk_type = self.token.getTkType()

        print(tk_type)

    def checkBlockVar(block):
        blockVar = ("ID", "COMMA", "")

    def toString(self):
        print("token Name: "+self.token.getTkName() + " token Type: "+self.token.getTkType())