# Compiladores
  (FEV/2021) Implementação dos analisadores léxico, sintático e semântico para a linguagem mini pascal construção em python3
  
# CheckList
#### Analisador Léxico
  
  - [X] Leitura de arquivo
  - [X] Gerando tabela de tokens

#### Analisador Sintático
  
  - [] Leitura de tokens
  - [] Verificação de regras de sintáxi
    
#### Analisador Semântico
  
   - [X] Nada feito.
    
## Analisador Léxico
  tokens
  
      'div','or', 'and','not','if','then','else','of','while','do','begin','end','read','write','print',
      'var','array','function','procedure','program','true','false','char','integer','boolean', 'where'
      
  regras de simbolos
  
      RULES = {  'TIMES': { 'regex': '\*' }, 'MINUS': {'regex': '-'},'PLUS': {'regex': '\+'},'ASSIGN_OP': {'regex': r':='},'GE': {'regex': '>='},'RP': {'regex': '\)'},'GT': {'regex': '>'},'LE': {'regex': '<='},'LP': {'regex': '\('},'DOTDOT': {'regex': '\.\.'},'NE': {'regex': '<>'},'LT': {'regex': '<'},'SEMICOLON': {'regex': ';'},'COMMA': {'regex': ','},'COLON': {'regex': ':'},'DOT': {'regex': '\.'},'LB': {'regex': '\['},'RB': {'regex': '\]'},'EQUAL': {'regex': r'='},'SINGLE_QUOTE': {'regex': r'\''},"DOUBLE_QUOTE": {'regex': r'\"'},'COMMENT': {'regex': r'(\(\*(?:(?:[\n\t]|[ \S])(?!\/\*))*\*\))',},'SINGLE_COMMENT': {'regex': r'{.*}',},'SPACE': {'regex': r'[ ]',},'TAB': {'regex': r'\t',},'NEW_LINE': {'regex': r'\r??\n',}}
      
# Status
    Desenvolvimento...
    
# Download
  ###### Repositorio github 
    Faça o download manual do projeto no link https://github.com/MarcosMarfi/Compiladores.git
  ###### OR copie e cole no seu terminal
    git clone https://github.com/MarcosMarfi/Compiladores.git
    
# Rodar
  ###### Execute
    python3 lexico.py
  ###### OR
    python lexico.py
  
      
      
      
      
      
