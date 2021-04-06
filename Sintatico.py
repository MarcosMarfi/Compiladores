from semantico import Semantico as SA

from compiladorExceptions.parserException import ParserException
from compiladorExceptions.blockVarException import BlockVarException
from compiladorExceptions.operatorException import OperatorException


class Sintatico:
    currentToken = ""

    typeVariableAssing = ""

    branchTree = {
        'PROGRAM': {},
        'BLOCK': {},
        'FUNCTION':{},
        'PROCEDURE': {},
        'VAR': {},
        'STATEMENT': {},
    }

    cache = []

    tableVar = {}

    currentScope = 0

    Semantic = SA()

    def __init__(self, lexer):
        self.lexer = lexer
        
        self.currentToken = self.lexer.nextToken()
        
        while (self.lexer.endCode() == False):
            if('ignore' in self.lexer.rules[self.currentToken.getTkType()]):
                self.currentToken = self.lexer.nextToken()
            else:
                break

        self.program()
        print("Execute with Success!")

    def createBranchTree(self, token, bloco):
        if bloco == 'PROGRAM':
            if token.getTkLine() in self.branchTree[bloco]: # se linha existe atualiza os itens nela
                self.branchTree[bloco][token.getTkLine()].update({token.getTkType(): token.getTkName()})
            else: # adiciona item com a linha sendo chave
                self.branchTree[bloco].update({token.getTkLine(): {token.getTkType(): token.getTkName()}})
        elif bloco == 'PROCEDURE':
            if token.getTkLine() in self.branchTree[bloco]: # se linha existe atualiza os itens nela
                self.branchTree[bloco][token.getTkLine()].update({token.getTkName(): token.getTkType()})
            else:
                self.branchTree[bloco].update({token.getTkLine(): {token.getTkName(): token.getTkType()}})
        elif bloco == 'FUNCTION':
            if token.getTkLine() in self.branchTree[bloco]: # se linha existe atualiza os itens nela
                self.branchTree[bloco][token.getTkLine()].update({token.getTkName(): token.getTkType()})
            else:
                self.branchTree[bloco].update({token.getTkLine(): {token.getTkName(): token.getTkType()}})
        elif bloco == 'VAR':
            busca = self.branchTree[bloco].get(self.currentScope)

            if busca:
                aux = busca.get(token.getTkLine())
                if aux != None:
                    if token.getTkName() in busca[token.getTkLine()]:
                        raise BlockVarException("Variable '"+token.getTkName()+"' already declared",
                            str(token.getTkLine()))
                    else:
                        if token.getTkName() in ['INTEGER','BOOLEAN','CHAR']:
                            for id,v in self.branchTree[bloco][self.currentScope][token.getTkLine()].items():
                                if len(self.cache)> 0 :
                                    tokenCache = self.cache.pop()
                                self.branchTree[bloco][self.currentScope][token.getTkLine()].update({tokenCache[1]: {token.getTkName()}})
                        else:
                            self.branchTree[bloco][self.currentScope][token.getTkLine()].update({token.getTkName(): {}})
                            self.cache.append((token.getTkLine(),token.getTkName()))
                else:
                    self.branchTree[bloco][self.currentScope].update({token.getTkLine(): {token.getTkName(): {}}})
                    self.cache.append((token.getTkLine(),token.getTkName()))
            else:
                self.branchTree[bloco].update({self.currentScope: {token.getTkLine(): {token.getTkName(): {}}}})           
                self.cache.append((token.getTkLine(),token.getTkName()))
    
    # consumes token if is valid
    def expectedToken(self, tk):
        rules = self.lexer.rules
        if self.consumesToken(tk):
            return True
        else:
            if(tk == "SEMICOLON"):
                raise ParserException(" Expected '"+rules[tk]['regex']+"'", str(self.currentToken.getTkLine()-1))
            else:
                raise ParserException("Not Expected '"+self.currentToken.getTkName()+"'", str(self.currentToken.getTkLine()))
                return False

    # compare if token is valid
    def compare(self, tk, currentToken):
        reserved = currentToken.getTkName() in self.lexer.tks_reserved
        found = False

        if reserved:
            found = currentToken.getTkName() == tk
        else:
            found = currentToken.getTkType() == tk
        
        return found

    # check if header passed is valid
    def checkHead(self, element):
        if self.compare(element, self.currentToken):
            return True
        else:
            return False

    # method for consume of the tokens from lexer
    def consumesToken(self, tk):
        rules = self.lexer.rules        

        if self.compare(tk, self.currentToken):
            # self.createBranchTree(self.currentToken)
            if not self.lexer.endCode():
                self.currentToken = self.lexer.nextToken()
                while 'ignore' in rules[self.currentToken.getTkType()] and rules[self.currentToken.getTkType()]['ignore'] == True:
                    self.currentToken = self.lexer.nextToken()
                # self.tree.append(self.currentToken.getTkName())
                return True
            else:
                return True
        return False   

    # search for ocurrences of the IDENTIFIER
    def checkOcurrences(self, v):
        found = False
        for t in v:
            if self.compare(t, self.currentToken):
                found = True
        
        return found

    # consume TYPES OF VARIABLE CHAR, BOOLEAN, INTEGER
    def simpleType(self):
        if self.checkHead("CHAR"):
            self.createBranchTree(self.currentToken, 'VAR')
            self.consumesToken("CHAR")
        elif self.checkHead("INTEGER"):
            self.createBranchTree(self.currentToken, 'VAR')
            self.consumesToken("INTEGER")
        elif self.checkHead("BOOLEAN"):
            self.createBranchTree(self.currentToken, 'VAR')
            self.consumesToken("BOOLEAN")
        else:
            raise BlockVarException("Type of variable is not recognized", str(self.currentToken.getTkLine()))

    # consumes token types CONSTANT
    def constant(self):
        if self.checkHead("NUM"):
            self.integerConstant()
        elif self.checkOcurrences(["SINGLE_QUOTE","DOUBLE_QUOTE"]):
            self.characterConstant()
        elif self.checkHead("IDENTIFIER"):
            self.expectedToken("IDENTIFIER")

    # variable
    def variable(self):
        self.typeVariableAssing = self.Semantic.type(self.branchTree, self.currentToken, self.currentScope)
        self.expectedToken("IDENTIFIER")
        self.expectedToken("ASSIGN_OP")
        self.expression()

    # rule of characters
    def characterConstant(self):
        if self.checkHead("SINGLE_QUOTE"):
            self.expectedToken("SINGLE_QUOTE")
            while self.checkOcurrences(["IDENTIFIER","NUM"]):
                if self.checkHead("IDENTIFIER"):
                    self.expectedToken("IDENTIFIER")
                else:
                    self.expectedToken("NUM")
            self.expectedToken("SINGLE_QUOTE")
        elif self.checkHead("DOUBLE_QUOTE"):
            self.expectedToken("DOUBLE_QUOTE")
            while self.checkOcurrences(["IDENTIFIER","NUM"]):
                if self.checkHead("IDENTIFIER"):
                    self.expectedToken("IDENTIFIER")
                else:
                    self.expectedToken("NUM")
            self.expectedToken("DOUBLE_QUOTE")

    # rule of integer constant
    def integerConstant(self):
        self.expectedToken("NUM")
        while self.checkHead("NUM"):
            self.expectedToken("NUM")

    # consume TYPES OF VARIABLE ARRAY
    def typeVarArray(self):
        self.expectedToken("ARRAY")
        self.expectedToken("LB")
        self.indexRange()
        self.expectedToken("RB")
        self.expectedToken("OF")
        self.simpleType()        

    # declaration of the variable TYPE ARRAY
    def indexRange(self):
        self.expectedToken("NUM")
        self.expectedToken("DOTDOT")
        self.expectedToken("NUM")

    # consumes TYPES OF VARIABLES declared
    def consumesTypeVars(self):
        if self.checkOcurrences(["INTEGER", "CHAR", "BOOLEAN"]):
            self.simpleType()
        elif self.checkHead("ARRAY"):
            self.typeVarArray()
        else:
            raise BlockVarException("Type of variable is not recognized", str(self.currentToken.getTkLine()))

    # program
    def program(self):
        self.expectedToken("PROGRAM")
        self.createBranchTree(self.currentToken, 'PROGRAM')
        self.expectedToken("IDENTIFIER")
        self.createBranchTree(self.currentToken, 'PROGRAM')
        self.expectedToken("SEMICOLON")
        self.block()
        self.expectedToken("DOT")

    # block
    def block(self):
        self.procedureAndFunctionDeclarationPart()
        self.variableDeclarationPart()
        self.statementPart()
    
    # consumes block of declaration from variables
    def variableDeclarationPart(self):
        # consumes token VAR and enter block of declartion from variables
        if self.consumesToken("VAR"):            
            # self.currentScope+=1
            # valid names of the variables
            if self.checkHead("IDENTIFIER"):
                while self.checkHead("IDENTIFIER"):  # deve gerar erro se nao achar identifier
                    self.variableDeclaration()
                    self.expectedToken("SEMICOLON")
            else:
                pass
                # raise ParserException("Error IDENTIFIER expected",str(currentToken.getTkLine()))        
        else:
            pass
            # raise ParserException("Not expected "+currentToken.getTkType()+": "+currentToken.getTkName()+", block VAR or function or procedure expected",
            #     str(currentToken.getTkLine()))
   
    # valid declaration of the variables
    def variableDeclaration(self):
        # adiciona variavel na tabela       
        self.createBranchTree(self.currentToken, 'VAR')

        # consumes declaration of the variable
        self.expectedToken("IDENTIFIER")
        while self.consumesToken("COMMA"): # if COMMA found            
            # declarations.append(self.currentToken.getTkName())
            self.createBranchTree(self.currentToken, 'VAR')
            # consumes declaration of the variable
            self.expectedToken("IDENTIFIER")

        # consumes COLON
        self.expectedToken("COLON")                
        #consumes token that representation type of the variables
        self.consumesTypeVars()
    
    #check if token exists in the block 
    def checkBlockForToken(self, token, bloco, scope=None):
        if bloco == 'VAR':
            for c,v in self.branchTree[bloco][scope].items():
                if token.getTkName() in v:
                    return True
        else:
            for c,v in self.branchTree[bloco].items():
                if token.getTkName() in v:
                    return True
        return False

    # consumes block of declaration from procedures and functions
    def procedureAndFunctionDeclarationPart(self):
        while self.checkHead("PROCEDURE") or self.checkHead("FUNCTION"):
            if self.checkHead("PROCEDURE"):
                self.procedureDeclaration()
            elif self.checkHead("FUNCTION"):
                self.functionDeclaration()
        else:
            pass

    # valid declaration of the procedures
    def procedureDeclaration(self):
        while self.consumesToken("PROCEDURE"):
            label = self.currentToken
            # valid names of the procedure
            if self.checkHead("IDENTIFIER"):
                if label.getTkName() in self.branchTree['PROCEDURE']:
                    raise ParserException("IDENTIFIER '"+label.getTkName()+"' already exists!",str(label.getTkLine()))
                else:
                    self.createBranchTree(label, 'PROCEDURE')
                self.expectedToken("IDENTIFIER")
                self.createBranchTree(self.currentToken, 'PROCEDURE')
                self.expectedToken("SEMICOLON")
                self.block()
            else:
                raise ParserException("Expected IDENTIFIER",str(label.getTkLine()))
        else:
            pass
    
    # verify call of the procedure
    def callProcedure(self):
        if self.checkHead("IDENTIFIER"):
            self.expectedToken("IDENTIFIER")

    # valid declaration of functions    
    def functionDeclaration(self):
        while self.consumesToken("FUNCTION"):
            if self.checkHead("IDENTIFIER"):
                self.createBranchTree(self.currentToken, 'FUNCTION')
                self.expectedToken("IDENTIFIER")
                self.expectedToken("LP")
                self.functionParam()
                self.expectedToken("RP")
                self.expectedToken("COLON")
                self.returnFunction()
                self.expectedToken("SEMICOLON")
                self.block()
            else:
                raise ParserException("Expected IDENTIFIER",str(self.currentToken.getTkLine()))  
        else:
            pass

    # consumes parameters passed in the function
    def functionParam(self):
        if self.checkHead("IDENTIFIER"):
            self.variableDeclaration()
            while self.consumesToken("SEMICOLON"):
                self.variableDeclaration()            
        else:
            pass

    # verify call of the function
    def callFunction(self):
        if self.checkHead("IDENTIFIER"): # check ID
            self.typeVariableAssing = self.Semantic.typeFunction(self.branchTree, self.currentToken)
            self.expectedToken("IDENTIFIER")
            if self.checkHead("ASSIGN_OP"): #verify if return
                self.expectedToken("ASSIGN_OP")
                self.expression()
                
            elif self.checkHead("LP"): #verify call in other                 
                pass

    def returnFunction(self):
        if self.checkHead("CHAR"):
            self.createBranchTree(self.currentToken, 'FUNCTION')
            self.consumesToken("CHAR")
            pass
        elif self.checkHead("INTEGER"):
            self.createBranchTree(self.currentToken, 'FUNCTION')
            self.consumesToken("INTEGER")
            pass
        elif self.checkHead("BOOLEAN"):
            self.createBranchTree(self.currentToken, 'FUNCTION')
            self.consumesToken("BOOLEAN")
            pass
        else:
            raise BlockVarException("Type of return is not recognized", str(self.currentToken.getTkLine()))

    # consumes block statement of the program
    def statementPart(self):
        self.compoundStatement()

    # valid structure of the statement from application
    def compoundStatement(self):
        self.expectedToken("BEGIN")
        self.statement()
        while self.checkHead("SEMICOLON"):
            self.expectedToken("SEMICOLON")
            self.statement()
        self.currentScope+=1
        self.expectedToken("END")
        
    # check statement block
    def statement(self):
        # verify simple statement
        if self.checkOcurrences(["IDENTIFIER", "READ", "WRITE", "PRINT"]):
            self.simpleStatement()        
        elif self.checkOcurrences(["BEGIN", "IF", "WHILE"]):    # verify if block structured statement
            self.structuredStatement()
        else:
            pass
            # raise ParserException("Expected IDENTIFIER or BEGIN statement!", str(self.currentToken.getTkLine()))
    
    # an simple structure [ASSIGNMENT OF VARIABLE, READ OR WRITE]
    def simpleStatement(self):
        if self.checkHead("READ"):
            self.readStatement()
        elif self.checkOcurrences(["WRITE","PRINT"]):
            self.writeStatement()
        elif self.checkHead("IDENTIFIER"):
            if  self.checkBlockForToken(self.currentToken, 'VAR', self.currentScope):
                self.assignmentStatement()
            elif self.checkBlockForToken(self.currentToken, 'FUNCTION'):
                self.callFunction()
            elif self.checkBlockForToken(self.currentToken, 'PROCEDURE'):
                self.callProcedure()
            else:
                self.Semantic.checkVariableDeclaredID(self.branchTree, self.currentToken, self.currentScope)
        else:
            pass            
    
    # an block structure [BEGIN, IF OR WHILE]
    def structuredStatement(self):     
        if self.checkHead("BEGIN"): # verify if exists new block STATEMENTE
            self.compoundStatement()
        elif self.checkHead("IF"): # verify if exists block statement IF
            self.ifStatement()
        elif self.checkHead("WHILE"): # verify if exists block statement WHILE
            self.whileStatement()
        else:
            raise ParserException("Error expected block BEGIN or IF or WHILE", self.currentToken.getTkLine())

    # rule of assignmente of variables
    def assignmentStatement(self):
        self.variable()

    # rule of statement READ
    def readStatement(self):
        # check token READ
        self.expectedToken("READ")
        # check token LP '('
        # self.expectedToken("LP")
        # check IDENTIFIER type variable
        self.expression()
        while self.checkHead("COMMA"):  # check MULTIPLE OCURRENCES            
            self.expectedToken("COMMA")
            # check IDENTIFIER type variable
            self.expression()
        # check finally the block with token RP ')'
        # self.expectedToken("RP")

    # rule of statement WRITE
    def writeStatement(self):
        # check token WRITE OR PRINT
        if self.checkHead("WRITE"):
            self.expectedToken("WRITE")
        elif self.checkHead("PRINT"):
            self.expectedToken("PRINT")

        self.expression()
        while self.checkHead("COMMA"): # check MULTIPLE OCURRENCES
            self.expectedToken("COMMA")            
            # self.expectedToken("IDENTIFIER")
            self.expression()
        # check finally the block with token RP ')'
        # self.expectedToken("RP")

    # rule of statement IF
    def ifStatement(self):
        # Expected token IF
        self.expectedToken("IF")
        # Expected Expression
        self.expression()
        # Expected token THEN
        self.expectedToken("THEN")
        # verify if exists news structures
        self.statement()
        if self.checkHead("ELSE"):    # Verify if exists token ELSE
            # Expected Token ELSE
            self.expectedToken("ELSE")
            # verify is exists news structures
            self.statement()
        else:
            pass

    # rule of statement WHILE
    def whileStatement(self):
        # check token WHILE
        self.expectedToken("WHILE")
        # verify expression
        self.expression()
        # check token DO
        self.expectedToken("DO")
        # verify STATEMENT
        self.statement()

    # rule of EXPRESSION
    def expression(self):
        self.simpleExpression()
        if self.checkOcurrences(["EQUAL", "NE", "LT", "GT", "LE", "GE"]):
            self.relationalOperator()
            self.simpleExpression()

    # rule simple expression
    def simpleExpression(self):
        termo1 = ""
        termo2 = ""
        type   = ""
        self.sign()        
        termo1 = self.term()
        while self.checkOcurrences(["MINUS","PLUS","OR"]):
            if self.checkHead("MINUS"):
                type = 'INTEGER'
            elif self.checkHead("PLUS"):
                type = 'INTEGER'

            self.consumeAddingOperator()            
            termo2 = self.term()

            self.Semantic.compareType(termo1,termo2,type, self.currentToken)

    def term(self):
        termo1 = ""
        termo2 = ""
        type   = ""
        termo1 = self.factor()
        while self.checkOcurrences(["TIMES","DIV","AND"]):
            if self.checkHead("TIMES"):
                type = 'INTEGER'
            elif self.checkHead("DIV"):
                type = 'INTEGER'

            self.consumeMultiplyingOperator()
            termo2 = self.factor()                

            self.Semantic.compareType(termo1, termo2, type, self.currentToken)
        return termo1
        

    def factor(self):
        type = ""
        if self.checkHead("IDENTIFIER"):
            #check if variable is declareded in actual scope
            # print(self.currentScope)            
            self.Semantic.checkVariableDeclaredID(self.branchTree, self.currentToken, self.currentScope)
            self.Semantic.checkTypeVariable(self.branchTree, self.typeVariableAssing, self.currentToken, self.currentScope)
            type = self.Semantic.type(self.branchTree, self.currentToken, self.currentScope)
            self.expectedToken("IDENTIFIER")
        elif self.checkHead("NUM"):
            type = 'INTEGER'
            self.expectedToken("NUM")
        elif self.checkOcurrences(["SINGLE_QUOTE", "DOUBLE_QUOTE"]):
            type = 'INTEGER'
            self.constant()
        elif self.checkHead("LP"):
            self.expectedToken("LP")
            self.expression()
            self.expectedToken("RP")
        elif self.checkHead("NOT"):
            self.expectedToken("NOT")
        else:
            pass
            # raise ParserException("Expected IDENTIFIER, NUM, LP or NOT, but found '"+self.currentToken.getTkName()+"'",
            #  str(self.currentToken.getTkLine()))

        return type

    # consumes MINUS OR PLUS
    def sign(self):
        if self.consumesToken("PLUS"):
            pass
        elif self.consumesToken("MINUS"):
            pass

    # consumes OPERATOR RELATIONAL
    def relationalOperator(self):        
        if self.consumesToken("EQUAL"):
            pass
        elif self.consumesToken("NE"):
            pass
        elif self.consumesToken("LT"):
            pass
        elif self.consumesToken("GT"):
            pass
        elif self.consumesToken("LE"):
            pass
        elif self.consumesToken("GE"):
            pass
        else:
            raise OperatorException("Expected OPERATOR RELATIONAL", str(self.currentToken.getTkLine()))
    
    # consumes OPERATOR MINUS, PLUS or OR
    def consumeAddingOperator(self):
        if self.consumesToken("MINUS"):
            pass
        elif self.consumesToken("PLUS"):
            pass
        elif self.consumesToken("OR"):
            pass
        else:
            raise OperatorException("Expected OPERATOR MINUS, PLUS or OR", str(self.currentToken.getTkLine()))

    # consumes OPERATOR TIMES, DIV or AND
    def consumeMultiplyingOperator(self):
        if self.consumesToken("TIMES"):
            pass
        elif self.consumesToken("DIV"):
            pass
        elif self.consumesToken("AND"):
            pass
        else:
            raise OperatorException("Expected OPERATOR TIMES, DIV or AND", str(self.currentToken.getTkLine()))