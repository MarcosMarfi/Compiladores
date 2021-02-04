caracteres = ['i','f',' ', 'e','l','s','e']
resultado = []
for i in range(0,len(caracteres)):
    while(caracteres[i]!= " "):
        caracteres[i] = "".join(caracteres[i])
        resultado.append(caracteres[i])
    
print("resultado: ", resultado)