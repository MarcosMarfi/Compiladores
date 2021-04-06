from lexer import Lexico
from Sintatico import Sintatico

from compiladorExceptions.parserException import ParserException
from compiladorExceptions.blockVarException import BlockVarException
from compiladorExceptions.operatorException import OperatorException

RULES = {
    'ASSIGN_OP': {
        'regex': r':='
    },
    'GE': {
        'regex': '>='
    },
    'RP': {
        'regex': '\)'
    },
    'GT': {
        'regex': '>'
    },
    'LE': {
        'regex': '<='
    },
    'LP': {
        'regex': '\('
    },
    'DOTDOT': {
        'regex': '\.\.'
    },
    'NE': {
        'regex': '<>'
    },
    'TIMES': {
        'regex': '\*'
    },
    'LT': {
        'regex': '<'
    },
    'SEMICOLON': {
        'regex': ';'
    },
    'COMMA': {
        'regex': ','
    },
    'MINUS': {
        'regex': '-'
    },
    'COLON': {
        'regex': ':'
    },
    'PLUS': {
        'regex': '\+'
    },
    'DOT': {
        'regex': '\.'
    },
    'LB': {
        'regex': '\['
    },
    'RB': {
        'regex': '\]'
    },
    'EQUAL': {
        'regex': r'='
    },
    'SINGLE_QUOTE': {
        'regex': r'\''
    },
    "DOUBLE_QUOTE": {
        'regex': r'\"'
    },
    'IDENTIFIER': {
        'regex': r'[a-zA-Z][a-zA-Z0-9]*',
    },
    'SINGLE_COMMENT': {
        'regex': r'{.*}',
        'ignore': True,
    },
    'NUM': {
        'regex': r'\d+(?:\d+)*(?:[Ee][+-]?\d+)?',
        'has_attribute': True
    },
    'SPACE': {
        'regex': r'[ ]',
        'ignore': True,
    },
    'TAB': {
        'regex': r'\t',
        'ignore': True,
    },
    'NEW_LINE': {
        'regex': r'\r??\n',
        'ignore': True,
        'newline': True,
    }
}

TOKENS_RESERVED = ['AND','ARRAY','BEGIN','BOOLEAN','CHAR','DIV','DO','ELSE','END','FALSE','FUNCTION','IF','INTEGER','NOT','OF',
    'OR','PROCEDURE','PROGRAM','READ','THEN','TRUE','VAR','WHILE','WRITE','PRINT'
]

def Main():
    code = ''

    while True:
        print("1-Lexico")
        print("2-Sintatico")
        print("3-Ler o Codigo")
        print("0-Sair")

        op = input("DIGITE UMA OPÇÂO: ")
        try:            
            if op == '0':
                break
            elif op == '1':                    
                newLexer = Lexico(code, RULES, TOKENS_RESERVED)
                while True:
                    if newLexer.endCode():
                        break
                    else:
                        print(newLexer.nextToken().toString())       
            elif op == '2':            
                try:
                    if code == '':
                        print('Realize a leitura do arquivo!')
                    else:
                        newLexer = Lexico(code, RULES, TOKENS_RESERVED) 
                        newSintatic = Sintatico(newLexer)
                except ParserException as e:
                    print(e.getError())
                except BlockVarException as e:
                    print(e.getError())
                except OperatorException as e:
                    print(e.getError())
                except Exception as e:
                    print(e)
            elif op == '3':
                with open('CodPascalzim.pas', 'r') as myfile:
                    code = myfile.read()
                print('Leitura Realizada!')
            else:
                print("Digite uma opção valida!")
        except Exception as e:
            print(e)
            continue
        finally:
            Sintatico.currentToken = ""
            Sintatico.branchTree = {
                'PROGRAM': {},
                'BLOCK': {},
                'FUNCTION':{},
                'PROCEDURE': {},
                'VAR': {},
                'STATEMENT': {},
            }

Main()