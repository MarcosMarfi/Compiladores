class Semantico:

    # check if token is declared in scope
    def checkToken(self, dic, token):
        if dic:
            for c,v in dic.items():
                if token.getTkName() in v:
                    return True
        
        return False

    # verify if variable is declared in scope actual
    def checkVariableDeclaredID(self, tableSimb, token, scope):
        busca = tableSimb['VAR'].get(scope)
        if busca:
            if self.checkToken(busca, token):
                return True                                  
            else:
                raise Exception("Erro Semantico: { Message: IDENTIFIER '"+token.getTkName()+"' undeclared, linha "+str(token.getTkLine())+" }")
        else:
            raise Exception("Erro Semantico: { Message: IDENTIFIER '"+token.getTkName()+"' undeclared, linha "+str(token.getTkLine())+" }")

        return False

    def checkTypeVariable(self, tableSimb, variableAssign, token, scope):
        busca = tableSimb['VAR'].get(scope)
        if self.checkVariableDeclaredID(tableSimb, token, scope) and variableAssign:
            if self.type(tableSimb, token, scope) == variableAssign:
                return True
            else:
                raise Exception("Erro Semantico: { Message: IDENTIFIER '"+token.getTkName()+"' type is not valid"+
                " for assignment, linha "+str(token.getTkLine())+" }")        
        return False

    # return type the variable declared
    def type(self, tableSimb, token, scope):
        busca = tableSimb['VAR'].get(scope)
        if busca:
            for c,v in busca.items():
                if token.getTkName() in busca[c]:
                    return list(busca[c][token.getTkName()])[0]
        
        return ""

    # return type the return the function
    def typeFunction(self, tableSimb, token):
        busca = tableSimb.get('FUNCTION')
        if busca:
            for c,v in busca.items():
                if token.getTkName() in v:                    
                    return list(v)[1]
        
        return ""

    # check if function is declared
    def checkFunctionID(self, tableSimb, token, scope):
        busca = tableSimb['FUNCTION']
        if busca:
            for c,v in busca.items():
                if token.getTkName() in v:
                    return True                                  
            raise Exception("Erro Semantico: { Message: IDENTIFIER '"+token.getTkName()+"' not declared in scope actual, linha "+str(token.getTkLine())+" }")

    # compare type of the variables
    def compareType(self, termo1, termo2, type, token):
        if termo1 != type or termo2 != type:
            raise Exception("Erro Semantico: { Message: Operation with different data types, linha "+str(token.getTkLine())+" }")
            return True
        else:
            return False
        
