import re
import time

TOKENS = ['div','or', 'and','not','if','then','else','of','while','do','begin','end','read','write','print',
  'var','array','function','procedure','program','true','false','char','integer','boolean', 'where']

TYPE_VALUE = {
  'ID': {
    'regex': r'[a-zA-Z][a-zA-Z0-9]*',
    # 'has_attribute': id_has_attribute
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
    # 'ignore': True,
    # 'newline': comment_newlines
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


def isChar(char):
  if(re.match("[a-zA-Z]", char) == None):
    return False
  else:
    return True

def isNumber(char):
  if(re.search(r"\d+", char) == None):
    return False
  else:
    return True

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

def createTable(lista):
  current = ""
  symb = ""
  aux = ""
  identifield = ""
  valueAtrib = ""
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
        if(verifyTypeId(identifield) != "ID"):  #retira qualquer parte numerica antes de identificaroes ou tokens
          valueAtrib+=identifield
          identifield=""
      elif(isSimbSpec(current)):    #verifica ocorrencia de simbolos
        if(isTokenReserved(identifield) or verifyTypeId(identifield) == "ID"):  #adiciona tokens ou identificadores na tabela
          if(isTokenReserved(identifield)):     #se token reservado
            table[numToken] = { identifield.upper() : "" }
          else:                                                     #se identificador
            table[numToken] = { verifyTypeId(identifield) : identifield }
          identifield = ""
          numToken+=1
        if((verifyRules(current+nextEl) == "ASSIGN_OP") or (verifyRules(current+nextEl) == "GE") or (verifyRules(current+nextEl) == "NE") or (verifyRules(current+nextEl) == "LE")):
          symb = current+nextEl
          aux = nextEl
          table[numToken] = {verifyRules(symb) : symb}    #adiciona simbolos com ocorrencias duplas
          symb=""
          numToken+=1
        else:
          if(verifyTypeId(valueAtrib) == "NUM"):      #adiciona ocorrencias de numeros
            table[numToken] = { verifyTypeId(valueAtrib): valueAtrib }
            valueAtrib = ""
            numToken+=1
          if(verifyRules(current) != "SPACE" and current != aux):   #adiciona ocorrencia de simbolos
            aux = ""            
            symb = current
            table[numToken] = {verifyRules(symb) : symb}
            symb=""
            numToken+=1
  return table

  
file = read_file('CodPascalzim.txt', 'r')

print(createTable(showFileLines(file)))