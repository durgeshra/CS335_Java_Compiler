import argparse
import os
import ply.lex as lex
import re
from prettytable import PrettyTable
from lexer_tokens import *

def print_err(s):
    print("-" * 50)
    print(s)
    print("-" * 50)

# def main():
#     #parsing arguments
#     parser = argparse.ArgumentParser(description='Input filename')
#     parser.add_argument('--pretty', action='store_true', help='beautify the output')
#     args, infile = parser.parse_known_args()

#     if len(infile) != 1:
#         print('usage: provide 1 input file')

#     infile = infile[0]

def t_IDENT(t):
    r'[a-zA-Z_$][a-zA-Z_$0-9]*'
    t.type = reserved.get(t.value,'IDENT')    # Check for reserved words
    # DONE check it is not a bool lit or null lit
    if t.value == 'true' or t.value == 'false':
        t.type = 'BOOL_LIT'
    if t.value == 'null':
        t.type = 'NULL_LIT'
    return t


def t_CHAR_LIT(t):
    r'\'([^\\\'\n\r\t]|(\\[btnfr\"\'\\0-7]))\''
    return t

def t_STRING_LIT(t):
    r'\"[^\"\\]*(\\.[^\"\\]*)*\"'
    return t

def t_UNCLOSED_STR(t):
    r'\"'
    print("String not closed at line %d" % t.lexer.lineno)
    t.lexer.skip(1)
    return t

def t_UNCLOSED_CHAR(t):
    r'\''
    print("Unmatched ' in line %d" % t.lexer.lineno)
    t.lexer.skip(0)
    return t

# def t_COMMENT(t):
#     r'(/\*([^*]|\n|(\*+([^*/]|\n)))*\*+/)|(//.*)'
#     t.lexer.lineno += t.value.count('\n');
#     return t

#Todo :: Line not increasing
t_ignore_COMMENT = r'(/\*([^*]|\n|(\*+([^*/]|\n)))*\*+/)|(//.*)'
# Error handling rule
def t_error(t):
    print("Invalid character '" + t.value[0] + "' at line %d" % t.lexer.lineno)
    t.lexer.skip(1)

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

    # Build the lexer
# lexer = lex.lex()
# parser = yacc.yacc()

#     f = open(infile)
#     data = f.read()
#     f.close()

#     # Give the lexer some input
#     lexer.input(data)


#     cnt = {}
#     type = {}

#     def add(tok, t):
#         if tok.value in cnt.keys():
#             cnt[tok.value] += 1
#         else:
#             cnt[tok.value] = 1
#             type[tok.value] = t

#     i=0
#     while True:
#         tok = lexer.token()
#         if not tok:
#             break
#         if tok.type in literals_:
#             add(tok, "Literal")
#         elif tok.type in separators:
#             add(tok, "Separator")
#         elif tok.type == 'IDENT':
#             add(tok, "Identifier")
#         elif tok.type in operators:
#             add(tok, "Operator")
#         elif tok.type in list(reserved.values()):
#             add(tok, "Keyword")
#         else:
#             # Comments or unknown
#             i+=1;
#         # print(tok)

#     t = PrettyTable(['Lexeme', 'Token', 'Count'])
#     for k in cnt.keys():
#         t.add_row([k, type[k], cnt[k]])
#         if not args.pretty:
#             print(k, type[k], cnt[k])

#     t.sortby = "Token"
#     if args.pretty:
#         print(t)

# if __name__ == "__main__":
#     main()
