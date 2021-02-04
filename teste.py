import re
linha = ["if eu fizer isso else aquilo"]
tokens = ["write","else","if"]
def verifica(linha, tokens):
    for i in range(len(linha)):
        for j in range(len(tokens)):
            if linha[i] != None:
                resultado = re.search(tokens[j],linha[i])
                print (resultado)

    print ("Span",resultado.span())
verifica(linha,tokens)