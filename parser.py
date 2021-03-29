from compiladorExceptions.parserException import ParserException
from compiladorExceptions.blockVarException import BlockVarException
from compiladorExceptions.operatorException import OperatorException

class Sintatico:
    currentToken = ""

    tree = []

    tableVar = {}

    currentScope = 0

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

    # consumes token if is valid
    def expectedToken(self, tk):
        rules = self.lexer.rules
        if self.consumesToken(tk):
            # self.tree.append(tk)
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
            if not self.lexer.endCode():
                self.currentToken = self.lexer.nextToken()
                while 'ignore' in rules[self.currentToken.getTkType()] and rules[self.currentToken.getTkType()]['ignore'] == True:
                    self.currentToken = self.lexer.nextToken()
                # self.tree.append(self.currentToken.getTkName())
                return True
            else:
                return True
        return False

    # add variables in cache
    def addVar(self, v):
        if v['id'] in self.tableVar and v['scope'] in self.tableVar:
            # raise BlockVarException("Variable '"+v['id']+"' already declared", str(self.currentToken.getTkLine()))
            return False
        self.tableVar[v['id']] = v

    # search for declarations of varables
    def searchVar(self, v):
        for id, data in self.tableVar.items():
            if data['id'] == v:
                return data
        return None

    # search for ocurrences of the IDENTIFIER
    def checkOcurrences(self, v):
        found = False
        for t in v:
            if self.compare(t, self.currentToken):
                found = True
        
        return found

    # consume TYPES OF VARIABLE CHAR, BOOLEAN, INTEGER
    def simpleType(self):
        if self.consumesToken("CHAR"):
            pass
        elif self.consumesToken("INTEGER"):
            pass
        elif self.consumesToken("BOOLEAN"):
            pass
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
        self.expectedToken("IDENTIFIER")
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
            # valid names of the variables
            if self.checkHead("IDENTIFIER"):
                while self.checkHead("IDENTIFIER"):  # deve gerar erro se nao achar identifier
                    self.variableDeclaration(self.currentScope)
                    self.expectedToken("SEMICOLON")
                # self.currentScope+=1
            else:
                pass
                # raise ParserException("Error IDENTIFIER expected",str(currentToken.getTkLine()))        
        else:
            pass
            # raise ParserException("Not expected "+currentToken.getTkType()+": "+currentToken.getTkName()+", block VAR or function or procedure expected",
            #     str(currentToken.getTkLine()))
   
    # valid declaration of the variables
    def variableDeclaration(self, scope):
        declarations = []
        # search for know if variable is already declareded
        busca = self.searchVar(self.currentToken.getTkName())
        # if variable already generate error
        if busca != None and busca['scope'] == scope: # erro semantico
            raise BlockVarException("Variable '"+self.currentToken.getTkName()+"' already declared",
             str(self.currentToken.getTkLine()))
        #add variable in cache
        self.addVar({
            'id': self.currentToken.getTkName(),
            'scope': scope,
            'type': None,
        })
        declarations.append(self.currentToken.getTkName())
        # consumes declaration of the variable
        self.expectedToken("IDENTIFIER")
        while self.consumesToken("COMMA"): # if COMMA found
            busca = self.searchVar(self.currentToken.getTkName())
            # if variable already generate error
            if busca != None and busca['scope'] == scope: # erro semantico
                raise BlockVarException("Variable '"+self.currentToken.getTkName()+"' already declared",
                 str(self.currentToken.getTkLine()))
            #add variable in cache     
            self.addVar({
                'id': self.currentToken.getTkName(),
                'type': None,
                'scope': scope,
            })
            declarations.append(self.currentToken.getTkName())
            # consumes declaration of the variable
            self.expectedToken("IDENTIFIER")
        # self.currentScope+=1
        # consumes COLON
        self.expectedToken("COLON")
        # for var in declarations:
        #     if self.currentToken.getTkName().lower() == 'INTEGER'.lower():
        #         self.searchVar(var)['type'] = 'integer'
        #     elif self.currentToken.getTkName().lower() == 'BOOLEAN'.lower():
        #         self.searchVar(var)['type'] = 'boolean'
        #     elif self.currentToken.getTkName().lower() == 'CHAR'.lower():
        #         self.searchVar(var)['type'] = 'char'
        #     elif self.currentToken.getTkName().lower() == 'ARRAY'.lower():
        #         self.searchVar(var)['type'] = 'array'
        #     else:
        #         raise BlockVarException("Type of variable "+self.currentToken.getTkName()+" is not recognized", str(self.currentToken.getTkLine()))
        
        #consumes token that representation type of the variables
        self.consumesTypeVars()
    
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
            # valid names of the procedure
            if self.checkHead("IDENTIFIER"):
                self.expectedToken("IDENTIFIER")
                self.expectedToken("SEMICOLON")
                self.block()
            else:
                raise ParserException("Expected IDENTIFIER",str(self.currentToken.getTkLine()))        
        else:
            pass
    
    # valid declaration of functions    
    def functionDeclaration(self):
        while self.consumesToken("FUNCTION"):
            if self.checkHead("IDENTIFIER"):
                self.expectedToken("IDENTIFIER")
                self.expectedToken("LP")
                self.functionParam()
                self.expectedToken("RP")
                self.expectedToken("COLON")
                self.consumesTypeVars()
                self.expectedToken("SEMICOLON")
                self.block()
            else:
                raise ParserException("Expected IDENTIFIER",str(self.currentToken.getTkLine()))  
        else:
            pass

    # consumes parameters passed in the function
    def functionParam(self):
        if self.checkHead("IDENTIFIER"):
            self.variableDeclaration(self.currentScope)
            while self.consumesToken("SEMICOLON"):
                self.variableDeclaration(self.currentScope)
            else:
                pass
        else:
            pass

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
        if self.checkHead("IDENTIFIER"):
            self.assignmentStatement()
        elif self.checkHead("READ"):
            self.readStatement()
        elif self.checkOcurrences(["WRITE","PRINT"]):
            self.writeStatement()
        else:
            pass
            # raise Exception("Error")
        # print("simple structure", self.currentToken.getTkName(), self.currentToken.getTkLine())
        # return
    
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
        # print("simple structure")

    # rule of assignmente of variables
    def assignmentStatement(self):
        self.variable()

    # rule of statement READ
    def readStatement(self):
        # check token READ
        self.expectedToken("READ")
        # check token LP '('
        self.expectedToken("LP")
        # check IDENTIFIER type variable
        self.expectedToken("IDENTIFIER")
        while self.checkHead("COMMA"):  # check MULTIPLE OCURRENCES            
            self.expectedToken("COMMA")
            # check IDENTIFIER type variable
            self.expectedToken("IDENTIFIER")
        # check finally the block with token RP ')'
        self.expectedToken("RP")

    # rule of statement WRITE
    def writeStatement(self):
        # check token WRITE OR PRINT
        if self.checkHead("WRITE"):
            self.expectedToken("WRITE")
        elif self.checkHead("PRINT"):
            self.expectedToken("PRINT")

        # # check token LP '('
        # self.expectedToken("LP")
        # # check IDENTIFIER type variable
        # self.expectedToken("IDENTIFIER")
        self.expression()
        while self.checkHead("COMMA"): # check MULTIPLE OCURRENCES
            self.expectedToken("COMMA")
            # check IDENTIFIER type variable
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
        self.sign()        
        self.term()
        while self.checkOcurrences(["MINUS","PLUS","OR"]):
            # if self.checkHead("MINUS") or self.checkHead("PLUS"):
            #     pass
            # else:
            #     raise OperatorException("Unexpected "+currentToken.getTkName()+" operator", str(currentToken.getTkLine()))
            self.consumeAddingOperator()
            self.term()    

    def term(self):
        self.factor()
        while self.checkOcurrences(["TIMES","DIV","AND"]):
            # if self.checkHead("TIMES") or self.checkHead("DIV"):
            #     pass
            # else:
            #     raise OperatorException("Unexpected "+currentToken.getTkName()+" operator", str(currentToken.getTkLine()))
            self.consumeMultiplyingOperator()
            self.factor()

    def factor(self):
        if self.checkHead("IDENTIFIER"):
            self.expectedToken("IDENTIFIER")
        elif self.checkHead("NUM"):
            self.expectedToken("NUM")
        elif self.checkOcurrences(["SINGLE_QUOTE", "DOUBLE_QUOTE"]):
            self.constant()
        elif self.checkHead("LP"):
            self.expectedToken("LP")
            self.expression()
            self.expectedToken("RP")
        elif self.checkHead("NOT"):
            self.expectedToken("NOT")
        else:
            raise ParserException("Expected IDENTIFIER, NUM, LP or NOT, but found '"+self.currentToken.getTkName()+"'",
             str(self.currentToken.getTkLine()))

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