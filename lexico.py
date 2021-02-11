import re
import time

tokens = ['uses','div','or', 'and','not','if','then','else','of','while','do',
  'begin','end','read','write','var','array','function','procedure','program',
  'true','false','char','integer','boolean']

alfabeto = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p',
  'q','r','s','t','u','v','x','y','z','w']

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
  tokensValidos = []
  for l in arr:
    if(verifyLine([l], listToken) != []):
      tokensValidos.append(verifyLine([l], listToken))
  
  return tokensValidos

teste = read_file('C:/Trabalhos_GitHub/Compiladores/CodPascalzim.txt', 'r')

# print(verifyLine(['else if write es'], token))
print(verifyToken(teste, tokens))