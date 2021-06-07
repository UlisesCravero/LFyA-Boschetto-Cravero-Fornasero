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



