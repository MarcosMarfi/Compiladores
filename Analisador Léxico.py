#ANALISADOR LÉXICO - DISCIPLINA: COMPILADORES
import re
import time


Pascalzim = open('c:/Users/madln/Documents/Universidade 2020-2021/2021/COMPILADORES/CodPascalzim.txt','r')

EntradaUsuario = str(input("Usuário Informa: "))
palavrasCadastradas = [] #Cadastradas
PalavrasFormadas = []
EntradaUser = []
#LENDO


alfabeto = ['a','b','c','d','e','f',
            'g','h','i','j','k','l',
            'm','n','o','p','q','r',
            's','t','u','v','x','y',
            'z','w']

for Arquivo in Pascalzim:
    TamanhoDoArquivo = len(Arquivo)
    #print("\nPalavras Cadastradas: \n",Arquivo)
    #print("QTD Caracteres: ",TamanhoDoArquivo)

for i in range(0,len(Arquivo)):
    palavrasCadastradas.append(Arquivo[i])
print("\n----------------------------------------------")
print("QTD Caracteres: ",TamanhoDoArquivo)
print("Palavras Cadastradas: ", palavrasCadastradas)
print("\n----------------------------------------------")
vetTemp = []
inicio = 0
def FormandoPalavras(inicio):
    for j in range(inicio, len(palavrasCadastradas)):
        if palavrasCadastradas[j] == " ":
            resultado = "".join(str(palavrasCadastradas[j]))
            vetTemp.append(resultado)
        else:
            FormandoPalavras(j+1)
        #print("VetTempUnido","".join(vetTemp))
        

FormandoPalavras(inicio)
print("vetTemp: ",vetTemp)
print("Palavras Formadas: ",PalavrasFormadas)