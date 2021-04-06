# Compiladores
  (FEV/2021) Implementação dos analisadores léxico, sintático e semântico para a linguagem mini pascal construção em python3
  
# CheckList
#### Analisador Léxico
  
  - [X] Leitura de arquivo
  - [X] Gerando tabela de tokens

#### Analisador Sintático
  
  - [X] Leitura de tokens
  - [X] Verificação de regras de sintáxi
    
#### Analisador Semântico
  
   - [X] Feito.
    
## Analisador Léxico
  tokens
  
      'div','or', 'and','not','if','then','else','of','while','do','begin','end','read','write','print',
      'var','array','function','procedure','program','true','false','char','integer','boolean', 'where'
      
  regras de simbolos
  
      RULES = {  'TIMES': { 'regex': '\*' }, 'MINUS': {'regex': '-'},'PLUS': {'regex': '\+'},'ASSIGN_OP': {'regex': r':='},'GE': {'regex': '>='},'RP': {'regex': '\)'},'GT': {'regex': '>'},'LE': {'regex': '<='},'LP': {'regex': '\('},'DOTDOT': {'regex': '\.\.'},'NE': {'regex': '<>'},'LT': {'regex': '<'},'SEMICOLON': {'regex': ';'},'COMMA': {'regex': ','},'COLON': {'regex': ':'},'DOT': {'regex': '\.'},'LB': {'regex': '\['},'RB': {'regex': '\]'},'EQUAL': {'regex': r'='},'SINGLE_QUOTE': {'regex': r'\''},"DOUBLE_QUOTE": {'regex': r'\"'},'COMMENT': {'regex': r'(\(\*(?:(?:[\n\t]|[ \S])(?!\/\*))*\*\))',},'SINGLE_COMMENT': {'regex': r'{.*}',},'SPACE': {'regex': r'[ ]',},'TAB': {'regex': r'\t',},'NEW_LINE': {'regex': r'\r??\n',}}
      
# Status
    Concluido!
    
# Download
  ###### Repositorio github 
    Faça o download manual do projeto no link https://github.com/MarcosMarfi/Compiladores.git
  ###### OR copie e cole no seu terminal
    git clone https://github.com/MarcosMarfi/Compiladores.git
    
# Rodar
  ###### Execute

    Para executar basta dar dois click´s no arquivo alfos.exe, o mesmo ira mostrar um menu.
      
      Menu 
        op 1 - Mostra os Tokens Lidos no Léxico
        op 2 - Executa a validação de regras Sintática
        op 3 - Realiza a leitura do Arquivo CodPascalzim.pas
        op 0 - Sair
      
    para cada execução deve-se realizar a leitura do arquivo, quando houver alguma modificação
    no arquivo CodPascalzim.pas, salvar o arquivo e em seguida realizar novamente a leitura.
  ###### OR
    python lexico.py
  
      
      
      
      
      
