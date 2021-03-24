from lexer import Lexico
from parser import Sintatico

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

TYPE_VALUE = {
  'ID': {
    'regex': r'[a-zA-Z][a-zA-Z0-9]*',
  },
  'NUM': {
    'regex': r'\d+(?:\d+)*(?:[Ee]?\d+)?',
  },
}

code = ''
with open('CodPascalzim.txt', 'r') as myfile:
    code = myfile.read()

try:
    le = Lexico(code, RULES, TOKENS_RESERVED)
    Sintatico(le)
except ParserException as e:
    print(e.getError())
except BlockVarException as e:
    print(e.getError())
except OperatorException as e:
    print(e.getError())
# while True:
#     if le.endCode():
#         break
#     else:
#         print(le.nextToken().getTkName())