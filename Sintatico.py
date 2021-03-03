import re as regex
import time as t
import string

alfabeto = list(string.ascii_lowercase)
#      TRECHO DE CAPTURA DA TABELA DO LÉXICO
def sintatico(tabela_lex):
    #print("Recebi no Sintático: ",tabela_lex)
#-------------------------------------------------
    pascalzim = open('C:/Users/madln/Documents/Universidade 2020-2021/2021/COMPILADORES/Compiladores/CodPascalzim.txt', 'r')
    linha = [] # salve arquivo em linhas sem espaços
    linhaComEspacos = [] # salva arquivo em linhas com espaços
    for percorreArq in pascalzim:
        temporario = percorreArq.splitlines()
        linha.append(temporario)
     
    def Regras(tabela_do_Lexico):
    #------------------------------------------------------------Verificando o PROGRAM como início do programa------------------------------------------------------------#
        tableLex = dict(tabela_do_Lexico)
        
        for lin in linha: #PERCORRE A LINHA DO ARQUIVO
            resultre = regex.search("program",lin[0])
            LinhaConsultadaAtual = list(lin[0])
            string = "program"
            
            for l in tableLex: #PERCORRE A TABELA
                
                TamDiciTable = len(tabela_lex[l].keys())
                if (TamDiciTable == 0): #significa que está vazio
                    None
                else:
                    TempKey = tableLex[l].popitem() #retorna uma TUPLA
                
                    for op in range(0,2): #PERCORRE A TUPLA
                        resultOP = TempKey[op]
                        
                        if TempKey:
                            if ((resultre != None and resultre.group() == string) and (resultOP == resultre.group() or (resultOP == resultre.group().upper()))): # 1° REGRA: Identificar o.
                    
                                inicio, fim = resultre.span()
                                for perc in range(0, int(inicio)):
                                    if LinhaConsultadaAtual[perc] != " ":
                                        print("Erro Sintático 1")
                                        break
                                concatenando = ""
                                ConcatenadoComEsp = ""
                                for per in range(fim+1, len(LinhaConsultadaAtual)):
                                    char = LinhaConsultadaAtual[per]
                                    ConcatenadoComEsp += char
                                    if char != " ":
                                    #print("char: ", char)
                                        concatenando += char
                             
# significa que ele encontrou o token esperado no arquivo e na tabela de tokens na "sequência ideal de leitura do código fonte"
                                
                                try:
                                    I,F = regex.search(";",concatenando).span()
                                    #print("virg:", virg)
                                    #print(type(virg[0]))
                                    print("Ini: ",I, "FIM: ", F, "TamConc: ", len(concatenando))
                                    for posVirg in range(I, len(concatenando)):
                                        
                                        if concatenando[posVirg] == ";" or concatenando[posVirg] : 
                                            concat = concatenando[posVirg]
                                            posVirg = posVirg + 1
                                            for virgPosterior in range(posVirg, len(concatenando)):
                                                if concatenando[posVirg] != " ":
                                                    None # Se tiver algo após a vírgula mostra erro sintático
                                                    #print()
                                                    return print("ERRO SINTÁTICO: {",concatenando[posVirg],"}")
                                                else:
                                                    None #se for vazio está ok
                                        else:
                                            None
                                except:
                                    print("ERRO SINTÁTICO: { ; }")

                                   
                                for opsaum in range(0,2): #PERCORRE A TUPLA
                                    resultOPC = TempKey[opsaum] #AQUI SÃO INFORMAÇÕES DA TABELA(LÉXICO)
                                    vetConc = list(concatenando)
                                    
                                for ver in range(0,len(vetConc)): #verifica se o NOME DO PROGRAMA inicia com número
                                    for alf in range(0, len(alfabeto)): # iniciando em 1 para não contabilizar UM ESPAÇO do código fonte(deve ser corrigido!!!)
                                        if (vetConc[ver] == " " or vetConc[ver] == ""): #if ((vetConc[ver] != " " or vetConc[ver] != "") and (vetConc[ver] != alfabeto[alf])):
                                            alf = alf + 1
                                        else:
                                            try:
                                                consultaRegraNum = int(vetConc[ver])
                                                vetGamb = list(concatenando)
                                                vetGamb.remove(";")

                                                vetGambESP = list(ConcatenadoComEsp)
                                                if (vetGamb[0].isidentifier() == True):
                                                    #print("Passei", vetGamb)
                                                    None
                                                else:
                                                    print("Erro Sintático: Iniciando com número!: ",consultaRegraNum)
                                                    break
                
                                                for espaco in range(0, len(ConcatenadoComEsp)):
                                                    if ConcatenadoComEsp[espaco] != " " and espaco <= ConcatenadoComEsp.index(";"):
                                                        None   
                                                    
                                            except:
                                                None
                        else:
                            print("Vazio")
    Regras(tabela_lex)