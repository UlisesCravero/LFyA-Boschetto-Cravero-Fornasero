import sys
import ply.lex as lex
import ply.yacc as yacc

reservados = {
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
    'AVG': 'AVG',
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

All_tokens = list(reservados.values()) + [
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
    'numero',
    'Comilla'
    'Cadena'
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
r_Comilla = r'\''
t_Ignorar = ' \t'

def t_string(t):
    r'\w'     #chequear si necesita una expresion regular mas acotada. \w adminte cualquier caracter
    t.type = reservados.get(t.value, 'string'.lower)  #por si viene en mayuscula (CONTROLAR QUE FUNCIONE)
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

def t_Cadena(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'   # revisar expresion regular
    t.type = reservados.get(t.value, 'Cadena')
    return t

# LISTA 
listaColumnas = {} # para identificar las columnas 
listaTablas = {} # para identificar las tablas

def p_Fun_Res(p):
    '''Fun_Res : MAX Parentesis_Izquierdo COLUMNA Parentesis_Derecho
               | MIN Parentesis_Izquierdo COLUMNA Parentesis_Derecho
               | COUNT Parentesis_Izquierdo COLUMNA Parentesis_Derecho
               | COUNT Parentesis_Izquierdo DISTINCT COLUMNA Parentesis_Derecho'''

               # CONTEMPLA EL ASTERISCO? AL PARECER NO HAY QUE HACER AVG
               #| AVG Parentesis_Izquierdo COLUMNA Parentesis_Derecho 

def p_signos(p):
    '''SIGNO: Igual | Desigual | Mayor | Menor | Mayor_Igual | Menor_Igual '''

def p_QUERY(p):
    '''QUERY :  SELECT FROM JOIN WHERE GROUP_BY ORDER_BY'''

def p_SELECT(p):
    '''SELECT | SELECT COLUMNAS
              | SELECT DISTINCT COLUMNAS
              | SELECT Fun_Res AS Comilla Cadena Comilla'''  # VER SI FALTA SELECT *

def p_COLUMNAS(p):
    '''COLUMNAS : COLUMNA
                | COLUMNA Coma COLUMNAS'''

def p_COLUMNA(p):
    '''COLUMNA : Cadena Punto Cadena
               | Cadena Punto Cadena AS Comilla Cadena Comilla'''
    key = p[3]
    if key not in listaColumnas:
        listaColumnas[key].append(key)

def p_TABLAS(p):
    '''TABLAS : Cadena AS Cadena
              | Cadena
              | TABLAS Cadena AS Cadena
              | TABLAS Cadena'''
    if len(p) == 2:
        listaTablas[p[1]] = p[1]
    if len(p) == 3:
        listaTablas[p[2]] = p[2]
    if len(p) == 4:
        listaTablas[p[1]] = p[3]
    if len(p) == 5:
        listaTablas[p[2]] = p[4]

def p_FROM(p):
    '''FROM : FROM TABLAS'''

def p_WHERE(p):
    '''WHERE: WHERE CONDICION'''

def p_CONDICION(p):              # CAMBIAR EL ALGO
    '''CONDICION : COLUMNA signos ALGO  
                 | COLUMNA signos COLUMNA''' 

def p_INNER_JOIN(p):
    ''' '''


query = "SELECT p.nombre , p.edad FROM PERSONA p, CUENTA cu WHERE "

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