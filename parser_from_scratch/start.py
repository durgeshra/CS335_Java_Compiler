import os 
import argparse 
parser = argparse.ArgumentParser(description = "A text file manager!") 

# defining arguments for parser object 
requiredNamed = parser.add_argument_group('required named arguments')
requiredNamed.add_argument("-i", "--input", type = str, nargs = 1, 
                    metavar = "file_name", required = True,
                    help = "Input file for parsing") 
    
parser.add_argument("-o", "--output", type = str, nargs = 1, 
                    metavar = "file_name", default = "graph", 
                    help = "Enter output file name without extension. Creates DOT(.dot) file and PDF(.pdf) file with same name") 

parser.add_argument("-v", "--verbose", type = bool, nargs = 1, 
                    metavar = "verbose", default = False, 
                    help = "Takes boolean value.") 

args = parser.parse_args() 
    
# calling functions depending on type of argument 
# if args.read != None: 
#     read(args) 
# elif args.show != None: 
#     show(args) 
# elif args.delete !=None: 
#     delete(args) 
# elif args.copy != None: 
#     copy(args) 
# elif args.rename != None: 
#     rename(args) 