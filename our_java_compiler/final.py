#!/usr/bin/python
import sys
import os
# sys.path.insert(0, './src/')
import lexRule
from parser import *
import ply.lex as lex
import ply.yacc as yacc
import node_file
import genAssembly as ga
import getopt
import pydot
import node_file
import csv
import getopt
from PIL import Image

def main(argv):
    to_parse = ''
    try:
        opts, args = getopt.getopt(argv,"o:f:h",["opt=","file=","help"])
    except getopt.GetoptError:
        print('Usage : ./bin/final.py [options][-f/-h/-o] [string]')
        sys.exit(2)
    # parse = parser.Parser()
    optjump = 0
    for opt, arg in opts:
        if opt in ("-o", "--opt"):
            if arg == "1":
                optjump = 1
        elif opt in ("-f", "--file"):
            # tree = parse.parse_file((arg))
            tree = parse_file((arg))
            printing()
            print("\nAST in txt format:")
            print(tree)
            f = open('AST.txt', 'w')
            # print >> f, tree
            # f.write(str(tree))
            print(tree, file=f)
            f.close()
            print("\nSymbol Table:")
            # print(ST.SymbolTable)
            img = Image.open('AST.png')
            # #img.show()
            print("\nSymbol Table Dump Written on ST.csv\nAST written in txt format on AST.txt\nAST dot output written on AST.png")
            # with open('ST.csv', 'w') as csv_file:
            #     writer = csv.writer(csv_file)
            #     writer.writerow(["function","variable","modifiers","type","dimension"])
            #     for a in parser.ST.SymbolTableFunction:
            #          for b in parser.ST.SymbolTableFunction[a]['variables']:
            #                  writer.writerow([a , b, parser.ST.SymbolTableFunction[a]['variables'][b]['modifiers'],parser.ST.SymbolTableFunction[a]['variables'][b]['type'],parser.ST.SymbolTableFunction[a]['variables'][b]['dimension']])

            # t = parser.tac.code

            # q = []
            # if optjump == 1:
            #     for x in range(0,len(t)-1):
            #         if t[x][0] == "goto" and t[x+1][3] == t[x][3]:
            #             q.append(x)
            #     for qw in reversed(q):
            #         del t[qw]

            #     parser.tac.code = t
            # # print(t)

            # old_target = sys.stdout
            # ga.generate()

            # sys.stdout = open('output.s', 'w')
            # ga.generate()

            # sys.stdout = old_target


            # print("Run ./a.out for execution")
            # # os.system("nasm -f elf32 inout.s")
            # # os.system("nasm -f elf32 fileio.s")
            # os.system("nasm -f elf32 output.s")
            # # os.system("nasm -f elf32 val1.s")
            # # os.system("nasm -f elf32 next1.s")
            # # os.system("nasm -f elf32 append2.s")
            # os.system("gcc -m32 output.o ./bin/inout.o ./bin/fileio.o ./bin/val1.o ./bin/next1.o ./bin/append2.o")

        elif opt in ("-h", "--help"):
            _file = open("./README.txt")
            content = _file.read()
            print(content)
        else:
            print('Usage : ./bin/final.py [options][-f/-h/-o] [string]')
            sys.exit(2)
    if not opts:
        print('Usage : ./bin/final.py [options][-f/-h/-o] [string]')
        sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])
