import re
import time
import Sintatico as sint
from analisadorSintatico import Sintatico as parser
from token import Token as tk

from compiladorExceptions.identifierException import IdentifierException
from compiladorExceptions.programException import ProgramException

TOKENS = ['div','or', 'and','not','if','then','else','of','while','do','begin','end','read','write','print',
  'var','array','function','procedure','program','true','false','char','integer','boolean', 'where']

TYPE_VALUE = {
  'ID': {
    'regex': r'[a-zA-Z][a-zA-Z0-9]*',
  },
  'NUM': {
    'regex': r'\d+(?:\d+)*(?:[Ee]?\d+)?',
  },
}

RULES = {
  'TIMES': {
    'regex': '\*'
  },
  'MINUS': {
    'regex': '-'
  },
  'PLUS': {
    'regex': '\+'
  },
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
  'LT': {
    'regex': '<'
  },
  'SEMICOLON': {
    'regex': ';'
  },
  'COMMA': {
    'regex': ','
  },  
  'COLON': {
    'regex': ':'
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
  'COMMENT': {
    'regex': r'(\(\*(?:(?:[\n\t]|[ \S])(?!\/\*))*\*\))',
  },
  'SINGLE_COMMENT': {
    'regex': r'{.*}',
  },
  
  'SPACE': {
    'regex': r'[ ]',
  },
  'TAB': {
    'regex': r'\t',
  },
  'NEW_LINE': {
    'regex': r'\r??\n',
  }
}

def verifyRules(char):
  for sym in RULES.keys():
    res = re.match(RULES[sym]['regex'], char)    
    if(res != None):
      return sym
  return ""

def verifyTypeId(char):
  for sym in TYPE_VALUE.keys():
    res = re.match(TYPE_VALUE[sym]['regex'], char)    
    if(res != None):
      return sym
  return None

def isSimbSpec(char):
  for sym in RULES.keys():
    res = re.match(RULES[sym]['regex'], char)    
    if(res != None):
      return True
  return False

def isTokenReserved(token):
  for i in range(len(TOKENS)):
    if(TOKENS[i].upper() == token.upper()):
      return True
  return False

def verifyLine(line, tokens):
  vet = []
  for i in range(len(line)):
    for j in range(len(tokens)):
      solution = re.search(tokens[j], line[i])      
      if (solution != None):
        vet.append(solution.group())
  return vet

def read_file(name,cod):
  file = open(name, cod)  
  return file.read().splitlines()

def showFileLines(file):
  token_entrada = []
  for j in file:
    token_entrada.append(j)
  return token_entrada

def verifyToken(arr, listToken):
  tokensResevados = []
  for l in arr:
    if(verifyLine([l], listToken) != []):
      tokensResevados.append(verifyLine([l], listToken))
  return tokensResevados

def scanner(lista):
  newToken = object
  current = ""
  symb = ""
  aux = ""
  identifield = ""
  nextEl = ""
  numToken = 0
  table = {}
  for l in lista:
    for j in range(len(l)):    

      if(j < len(l)-2):  #controlador de posições
        current = l[j]
        nextEl = l[j+1]        
      else:
        current = l[j]
        nextEl = ""

      if(isSimbSpec(current) == False):    #concatena se não for simbolo especial
        identifield += current
      else:    #verifica ocorrencia de simbolos
        if(verifyTypeId(identifield) == "ID"):    #adiciona tokens ou identificadores na tabela
          if(isTokenReserved(identifield)):     #se token reservado
            table[numToken] = { identifield.upper() : "" }
            newToken = tk(identifield.upper(), "RESERVED")   
            parser(newToken)
            newToken = object
          else:                                                     #se identificador
            table[numToken] = { verifyTypeId(identifield) : identifield }
            newToken = tk(identifield.upper(), "ID")
            parser(newToken)
            newToken = object
          identifield = ""
          numToken+=1
        elif(identifield != ""):      #adiciona ocorrencias de numeros
          if(identifield.isdigit()):
            table[numToken] = { verifyTypeId(identifield): identifield }
            newToken = tk(identifield.upper(), "NUM")
            parser(newToken)
            newToken = object
            identifield = ""
            numToken+=1
          else:
            raise IdentifierException            
            break
        if((verifyRules(current+nextEl) == "ASSIGN_OP") or (verifyRules(current+nextEl) == "GE") or (verifyRules(current+nextEl) == "NE") or (verifyRules(current+nextEl) == "LE")):
          symb = current+nextEl
          aux = nextEl
          table[numToken] = {verifyRules(symb) : symb}    #adiciona simbolos com ocorrencias duplas
          newToken = tk(verifyRules(symb), "SYMB")
          parser(newToken)
          newToken = object
          symb=""
          numToken+=1
        else:
          if(verifyRules(current) != "SPACE" and current != aux):   #adiciona ocorrencia de simbolos
            aux = ""            
            symb = current
            table[numToken] = {verifyRules(symb) : symb}
            newToken = tk(verifyRules(symb), "SYMB")
            parser(newToken)
            newToken = object
            symb=""
            numToken+=1
  return ""

  
try: 
  file = read_file('CodPascalzim.txt', 'r')
  # file = read_file('C:/Users/madln/Documents/Universidade 2020-2021/2021/COMPILADORES/Compiladores/CodPascalzim.txt', 'r')

  scanner(showFileLines(file))
  # sint.sintatico(scanner(showFileLines(file)))
except IdentifierException:
  print('Error Lexíco, identificador invalido!')
except Exception:
  None