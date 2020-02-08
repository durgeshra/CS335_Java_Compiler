import ply.yacc as yacc
import sys
import argparse
import lexer
from graphviz import Digraph
import os

tokens = lexer.tokens


def p_empty(p):
    '''epsilon : '''
    p[0] = "epsilon"


# Add rules here
def p_type(t):
    


parser = yacc.yacc()

f = open("test1.java","r")
data = f.read()
output = parser.parse(data)

print(output)
f.close()
