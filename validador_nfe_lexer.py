import ply.lex as lex

# Definindo os estados do lexer
states = (
   ('tag', 'exclusive'),
)

# Tokens
tokens = (
    'TAG_ABERTURA_COM_NOME',  # Ex: <infNFe
    'TAG_FECHAMENTO',         # Ex: </ide>
    'MAIOR_QUE',              # >
    'IDENTIFICADOR',          # Nome de atributo, ex: versao
    'IGUAL',                  # =
    'VALOR_ATRIBUTO',         # "4.00"
    'CONTEUDO',               # Conteúdo entre tags
)

# Regras do estado inicial (INITIAL)
def t_TAG_ABERTURA_COM_NOME(t):
    r'<[a-zA-Z_][a-zA-Z0-9_]*'
    t.lexer.begin('tag')
    return t

def t_TAG_FECHAMENTO(t):
    r'</[a-zA-Z0-9_]+>'
    return t

def t_CONTEUDO(t):
    r'[^<>]+'
    t.value = t.value.strip()
    if t.value:
        return t

# Regras do estado 'tag'
def t_tag_MAIOR_QUE(t):
    r'>'
    t.type = 'MAIOR_QUE'
    t.lexer.begin('INITIAL')
    return t

def t_tag_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = 'IDENTIFICADOR'
    return t

def t_tag_IGUAL(t):
    r'='
    t.type = 'IGUAL'
    return t

def t_tag_VALOR_ATRIBUTO(t):
    r'\"[^"]*\"'
    t.type = 'VALOR_ATRIBUTO'
    t.value = t.value[1:-1]  # Remove as aspas
    return t

# Regra para ignorar espaços e tabs dentro da tag
t_tag_ignore = ' \t'

# Regra de erro para o estado 'tag'
def t_tag_error(t):
    print(f"Caractere ilegal '{t.value[0]}' dentro de uma tag na linha {t.lineno}")
    t.lexer.skip(1)

# Regras globais (para todos os estados)
t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}' na linha {t.lineno}")
    t.lexer.skip(1)
lexer = lex.lex()