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
    'COUNT':'COUNT',
    'DISTINCT':'DISTINCT',
    'INNER':'INNER',
    'JOIN':'JOIN',
    'LEFT':'LEFT',   
    'AND':'AND',
    'OR':'OR',
    'ON':'ON',
    'IN':'IN',
    'NOT':'NOT',
    'IS':'IS',
    'NULL':'NULL',
    'ASC':'ASC',
    'DESC':'DESC',
}

tokens = list(reservados.values()) + [
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
    'Comilla',
    'Cadena',
    'Columna',
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
t_ignore = ' \t'

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
    r'[a-zA-Z_][a-zA-Z0-9_]*'   
    t.type = reservados.get(t.value, 'Cadena')
    return t

lexer = lex.lex()

# LISTAS
listaColumnas = {} # para identificar las columnas 
listaTablas = {} # para identificar las tablas

def p_S_query(p):
    '''S : _SELECT _FROM _WHERE GROUP_BY ORDER_BY'''

def p__SELECT(p):
    '''_SELECT : SELECT COLUMNAS
               | SELECT DISTINCT COLUMNAS
               | SELECT Fun_Res AS Comilla Cadena Comilla'''

def p_COLUMNAS(p):
    '''COLUMNAS : COLUMNA
                | COLUMNA Coma COLUMNAS'''

def p_COLUMNA(p):
    '''COLUMNA : Cadena Punto Cadena
               | Cadena Punto Cadena AS Comilla Cadena Comilla'''
    key = p[1]
    if key in listaColumnas:
        if p[3] not in listaColumnas[key]:
            listaColumnas[key].append(p[3])
    else:
        listaColumnas[key] = [p[3]]

def p__FROM(p):
    '''_FROM : FROM TABLAS
             | FROM TABLAS INNER_JOIN
             | FROM TABLAS LEFT_JOIN'''

def p_TABLAS(p):
    '''TABLAS : Cadena AS Cadena
              | Cadena
              | TABLAS Cadena AS Cadena
              | TABLAS Cadena'''
    if len(p) == 4:
        listaTablas[p[1]] = p[3]
    if len(p) == 2:
        listaTablas.setdefault(p[2])
    if len(p) == 5:
        listaTablas[p[2]] = p[4]
    if len(p) == 3:
        listaTablas.setdefault(p[2])

def p__WHERE(p):
    '''_WHERE : WHERE CONDICION
              | WHERE CONDICION _IN
              | WHERE CONDICION NOT_IN
              | '''

def p_IN(p):
    '''_IN : IN Parentesis_Izquierdo S Parentesis_Derecho'''

def p_NOT_IN(p):
    '''NOT_IN : NOT IN Parentesis_Izquierdo S Parentesis_Derecho'''

def p_Fun_Res(p):
    '''Fun_Res : MAX Parentesis_Izquierdo COLUMNA Parentesis_Derecho
               | MIN Parentesis_Izquierdo COLUMNA Parentesis_Derecho
               | COUNT Parentesis_Izquierdo COLUMNA Parentesis_Derecho
               | COUNT Parentesis_Izquierdo DISTINCT COLUMNA Parentesis_Derecho'''

def p_SIGNO(p):
    '''SIGNO : Igual 
             | Desigual 
             | Mayor 
             | Menor 
             | Mayor_Igual 
             | Menor_Igual '''

def p_GROUP_BY(p):
    '''GROUP_BY : GROUP BY COLUMNAS
                | GROUP BY COLUMNAS _HAVING
                | '''

def p__HAVING(p):
    '''_HAVING : HAVING CONDICION
               | '''

def p_ORDER_BY(p):
    '''ORDER_BY : ORDER BY Cadena DESC
                | ORDER BY Cadena ASC
                | ORDER BY Cadena
                | '''

def p_CONDICION(p):
    '''CONDICION : COLUMNA SIGNO ALGO  
                 | COLUMNA SIGNO COLUMNA
                 | COLUMNA SIGNO ALGO AND CONDICION
                 | COLUMNA SIGNO COLUMNA AND CONDICION
                 | COLUMNA SIGNO ALGO OR CONDICION
                 | COLUMNA SIGNO COLUMNA OR CONDICION'''

def p_ALGO(p): 
    '''ALGO : numero
            | Comilla Cadena Comilla''' 

def p_INNER_JOIN(p):
    '''INNER_JOIN : INNER JOIN TABLAS ON CONDICION
                  | INNER JOIN TABLAS ON CONDICION INNER JOIN
                  | INNER JOIN TABLAS ON CONDICION WHERE'''

def p_LEFT_JOIN(p):
    '''LEFT_JOIN : LEFT JOIN TABLAS ON CONDICION
                 | LEFT JOIN TABLAS ON CONDICION LEFT JOIN
                 | LEFT JOIN TABLAS ON CONDICION WHERE'''

def parse_select_statement(s):
    listaColumnas.clear()
    listaTablas.clear()
    yacc.yacc()
    yacc.parse(s)
    diccionarioResultado = {}
    for keyT in listaTablas:
        alias = ''
        if listaTablas.get(keyT) != None:
            alias = listaTablas.get(keyT)
        else:
            alias = keyT
        for keyC in listaColumnas:
            if alias == keyC:
                diccionarioResultado[keyT] = sorted(listaColumnas.get(keyC))
    if len(listaColumnas.keys()) > len(listaTablas.keys()):
        raise Exception('Error: se está llamando a una o más tablas tanto por su nombre como por su alias')
    return diccionarioResultado