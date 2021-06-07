import sys
import ply.lex as lex
import ply.yacc as yacc

reserved = {
    'SELECT':'SELECT',
    'FROM':'FROM',
    'WHERE':'WHERE',
    'GROUP':'GROUP',
    'BY':'BY',
    'HAVING':'HAVING',
    'ORDER':'ORDER',
    'AS':'AS',
    'MIN':'MIN',
    'MAX':'MAX',
    'COUNT':'COUNT',
    'DISTINCT':'DISTINCT',
    'INNER':'INNER',
    'JOIN':'JOIN',
    'ON':'ON',
    'LEFT':'LEFT',   
    'AND':'AND',
    'OR':'OR',
    'IN':'IN',
    'NOT':'NOT',
    'IS':'IS',
    'NULL':'NULL',
    'ASC':'ASC',
    'DESC':'DESC',
}

All_tokens = list(reserved.values()) + [
    'Igual', 
    'Desigual',
    'Mayor',
    'Mayor_Igual',
    'Menor',
    'Menor_Igual',
    'Parentesis_Izquierdo',
    'Parentesis_Derecho',
    'Corchete_Izquierdo',
    'Corchete_Derecho',
    'Coma',
    'Punto',
    'string',
    'numero'
    # Faltan declarar algunos de la expresion regular Por ejemplo (cadena, tabla)
]

t_Igual = r'\='
t_Desigual = r'\<>'
t_Mayor = r'\>'
t_Mayor_Igual = r'\>='
t_Menor = r'\<'
t_Menor_Igual = r'\<='
t_Parentesis_Izquierdo = r'\('
t_Parentesis_Derecho = r'\)'
t_Corchete_Izquierdo = r'\['
t_Corchete_Derecho = r'\]'
t_Coma = r'\,'
t_Punto = r'\.'

t_Ignorar = ' \t'

def t_string(t):
    r'\w'     #chequear si necesita una expresion regular mas acotada. \w adminte cualquier caracter
    t.type = reserved.get(t.value, 'string'.lower)  #por si viene en mayuscula (CONTROLAR QUE FUNCIONE)
    return t

def t_numero(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Lex error. Character '%s' is not valid" % t.value[0])
    t.lexer.skip(1)

query = "INTRODUCIR QUERY A EVALUAR"

lexer = lex.lex()
lexer.input(query)


# mostrar tokens
while True:
    tok = lexer.token()
    if not tok:
        break 
    print(tok)


# chequea si la query tiene validez sintactica
parser = yacc.yacc()