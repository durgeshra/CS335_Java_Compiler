import os
from graphviz import Digraph
import sys
import lexRule
from  custom_classes import SymbolTable, MethodObj, ClassObj, Node
import ply.lex as lex
import ply.yacc as yacc
tokens = lexRule.tokens



#####################################################
# Milestone 2
#####################################################

#-------------------GLOBAL DATA-STRUCTURES-----------------------------

# Elements of the list represent size, index, parent-index in the "widening DAG" (see figure 6.25 in the Aho book), depth
# TODO: anay - add precedences
type_dict = {'boolean': {'size': 1, 'pid': -1, 'lvl': 0}, \
             'byte': {'size': 1, 'pid': 'short', 'lvl': 6}, \
             'short': {'size': 2, 'pid': 'int', 'lvl': 5}, \
             'char': {'size': 2, 'pid': 'int', 'lvl': 5}, \
             'int': {'size': 4, 'pid': 'long', 'lvl': 4}, \
             'long': {'size': 8, 'pid': 'float', 'lvl': 3}, \
             'float': {'size': 4, 'pid': 'double', 'lvl': 2}, \
             'double': {'size': 8, 'pid': -1, 'lvl': 1}, \
             'identifier': {'size': -1, 'pid': -1, 'lvl': -1}}  # dummy type in place of unknown identifier types

def higher(a, b):
    if a not in type_dict.keys() or b not in type_dict.keys():
        raise NameError("Unknown types " +  a + " or " + b + ".")

    if a == b:
        return a

    if a == 'boolean' or b == 'boolean':
        return -1
        # raise NameError("Type " +  a + " and " + b + " are incompatible.")

    while True:
        if type_dict[a]['lvl'] < type_dict[b]['lvl']:
            a = type_dict[a]['pid']
        elif type_dict[a]['lvl'] > type_dict[b]['lvl']:
            b = type_dict[b]['pid']
        else:
            break

    while a != b and type_dict[a]['pid'] != -1 and type_dict[b]['pid'] != -1:
        a = type_dict[a]['pid']
        b = type_dict[b]['pid']

    if a==b:
        return a
    else:
        return -1
        # raise NameError("Type " +  a + " and " + b + " are incompatible.")


#TODO (Anay): implement this for 3AC see Fig 6.26 of Aho book
def widen():
    return



#-------------------SYMBOL TABLE STUFF-----------------------------
scope_stack = [SymbolTable()]

# Removed stuff from PyGo
# scopes_ctr = 0    #TODO (anay): I don't think we need this, it is basically equal to len(scope_stack).
# current_scope = 0  #TODO (anay): I don't think we need this, it is basically scope_stack.top()
# scope_stack_old = [0]   #TODO (Durgesh): to remove
                          #TODO (anay): I agree, we don't need this.
# root_node = None  #TODO (Anay): I don't think we need this.
#-------------------TEMPORARY VARIABLE STUFF-----------------------------
temp_ctr = 0
label_ctr = 0
label_dict = dict()
# Use type_dict instead of sizeof
# sizeof = dict()
# sizeof["uint8"] = 4; sizeof["uint16"] = 2; sizeof["uint32"] = 4; sizeof["uint"] = 4; sizeof["uint64"] = 4;
# sizeof["int8"] = 4; sizeof["int16"] = 2; sizeof["int32"] = 4; sizeof["int"] = 4; sizeof["int64"] = 4;
# sizeof["float32"] = 4; sizeof["float64"] = 4;
# sizeof["byte"] = 4; sizeof["bool"] = 4; sizeof["string"] = 4; sizeof["file"] = 4

temp_array = [] #used to store the temporary varibles used to define an array   #TODO (Durgesh): Change variable type names


#####################################################
###############   Helper functions  #################
#####################################################

def is_number(s):
    if s == True or s == False:
        return False
    try:
        float(s) # for int, long, float
    except ValueError:
        return False
    return True

def new_temp():
    global temp_ctr
    temp_ctr += 1
    return "temp" + str(temp_ctr)

def new_label():
    global label_ctr
    label_ctr += 1
    return "label" + str(label_ctr)

def in_scope(ident, scope = None):
    global scope_stack
    if scope != None:
        if scope_stack[scope].look_up(ident):
            return True
        return False
    stack_size = len(scope_stack)
    for scope in range(stack_size-1,-1,-1):
        if scope_stack[scope].look_up(ident):
            return True
    return False

# Updated (anay)
def add_scope(p = None):
    global scope_stack
    scope_stack += [SymbolTable()]
    scope_stack[-1].set_parent(len(scope_stack)-2) # -1 means there is no parent


    # scopes_ctr += 1
    # previous_scope = current_scope
    # current_scope = scopes_ctr
    # scope_stack += [current_scope]

    # if p is not None:
        # if p[-1] == "for":
        #     p[0] = Node()
        #     for_label = "_for_" + new_label()
        #     end_for_label = "_end_" + for_label
        #     scopes[current_scope].insert(for_label, "label")
        #     scopes[current_scope].insert("__BeginFor", for_label, "value")
        #     scopes[current_scope].insert("__MidFor", for_label, "value")
        #     scopes[current_scope].insert("__EndFor", end_for_label, "value")
        #     p[0].code += [["label", for_label]]

        # elif p[-2] == "func":
        #     if in_scope(p[-1]):
        #         raise NameError(str(p.lexer.lineno) + ": Function " + p[-1] + " already defined")
        #     p[0] = Node()
        #     func_label = "_func_" + p[-1]
        #     end_func_label = "_end_" + func_label
        #     scopes[0].insert(p[-1], "function")
        #     scopes[0].update(p[-1], func_label, "label")
        #     scopes[current_scope].insert("__FuncName", p[-1], "value")
        #     scopes[current_scope].insert("__EndFuncLabel", end_func_label, "value")
        #     p[0].code += [["label", func_label], ["func_begin", p[-1]]]

        # elif p[-1] == "else":
        #     p[0] = Node()
        #     temp_label = new_label()
        #     p[0].extra["ElseLabel"] = temp_label
        #     p[0].code += [["label", temp_label]]

        # elif p[-2] == "if":
        #     p[0] = Node()
        #     temp_label = new_label()
        #     end_if_label = "_end_if_" + temp_label
        #     scopes[current_scope].insert("__EndIf", end_if_label, "value")
        #     p[0].extra["IfLabel"] = temp_label
        #     p[0].extra["EndIfLabel"] = end_if_label
        #     p[0].code += [["label", temp_label]]

        # elif p[-2] == "switch":
        #     temp_label = new_label()
        #     end_switch_label = "_end_switch_" + temp_label
        #     scopes[current_scope].insert("__Switch", temp_label, "value")
        #     scopes[current_scope].insert("__EndSwitch", end_switch_label, "value")
        #     scopes[current_scope].add_extra(1, "label_ctr")
        #     if not p[-1].place_list == []:
        #         scopes[current_scope].add_extra(p[-1].type_list[0], "switch_expr_type")
        #         scopes[current_scope].add_extra(p[-1].place_list[0], "switch_expr_var")

        # # taken from p_add_scope
        # TODO (Durgesh): Add support for while
    return

# Updated (anay)
def end_scope(p = None):
    global scope_stack
    # if p is not None:
    #     if p[-3] == "for" or p[-4] == "for":
    #         p[0] = Node()
    #         for_label = find_info("__BeginFor", p.lexer.lineno, current_scope)["value"]
    #         end_for_label = "_end_" + for_label
    #         p[0].code += [["goto", for_label]]
    #         p[0].code += [["label", end_for_label]]

    #     elif p[-4] == "func":
    #         p[0] = Node()
    #         end_func_label = find_info("__EndFuncLabel", p.lexer.lineno, current_scope)["value"]
    #         p[0].code += [["func_end", end_func_label]]

    #     elif p[-4] == "if":
    #         p[0] = Node()
    #         end_if_label = find_info("__EndIf", p.lexer.lineno, current_scope)["value"]
    #         p[0].code += [["goto", end_if_label]]

    #     elif p[-6] == "switch":
    #         p[0] = Node()
    #         end_switch_label = find_info("__EndSwitch", p.lexer.lineno, current_scope)["value"]
    #         p[0].code += [["label", end_switch_label]]

    # # taken from p_end_scope
    # TODO (Durgesh): Add support for while
    scope_stack.pop()

# Updated (anay)
def find_scope(ident, line):
    global scope_stack
    stack_size = len(scope_stack)
    for scope in range(stack_size-1,-1,-1):
        if scope_stack[scope].look_up(ident):
            return scope
    raise NameError(str(line) + ": Identifier " + ident + " is not in any scope")

# Updated (anay)
def find_info(ident, line, scope = None):
    global scope_stack
    if scope != None:
        temp = scope_stack[scope].get_info(ident)
        if temp != None:
            return temp
        raise NameError(str(line) + ": Identifier " + ident + " is not in this scope")

    stack_size = len(scope_stack)
    for scope in range(stack_size-1,-1,-1):
        if scope_stack[scope].look_up(ident):
            return scope_stack[scope].get_info(ident)
    raise NameError(str(line) + ": Identifier " + ident + " is not in any scope")


#####################################################
################  /Helper functions  ################
#####################################################



#<editor-fold> SACRED #########################
#
# # Description of p: It is a node object
#
#
# def p_add_scope_with_lbrace(p):
#     '''add_scope_with_lbrace    : LBRACE'''
#     add_scope()
#
# def p_end_scope_with_rbrace(p):
#     '''end_scope_with_rbrace    : RBRACE'''
#     end_scope()
#
# def p_semicolon_opt(p):
#     '''semicolon_opt    : SEMICOLON
#                         | epsilon'''
#
# def p_type_token(p):
#     '''type_token   : UINT8
#                     | UINT16
#                     | UINT32
#                     | UINT64
#                     | INT8
#                     | INT16
#                     | INT32
#                     | INT64
#                     | FLOAT32
#                     | FLOAT64
#                     | BYTE
#                     | BOOL
#                     | UINT
#                     | INT
#                     | UINTPTR
#                     | STRING'''
#     global sizeof
#     p[0] = Node()
#     if p[1] == "string":
#         p[0].type_list += [[p[1], None]]
#     else:
#         p[0].type_list += [p[1]]
#     p[0].extra["size"] = sizeof[p[1]]
#
# def p_type(p):
#     '''type : type_token
#             | type_lit
#             | TYPE IDENT'''
#     # check_shivansh
#     # Arpit LPAREN type RPAREN removed from RHS
#     # we shoudl check wether this type is available
#     if len(p) == 3:
#         p[0] = Node()
#         p[0].type_list += ["type " + p[2]]
#         info = find_info("type " + p[2], p.lineno(1), 0)
#         p[0].extra["methods"] = info.get("methods")
#         p[0].extra["fields"] = info.get("fields")
#         p[0].extra["fields_type"] = info.get("fields_type")
#         p[0].extra["fields_size"] = info.get("fields_size")
#         p[0].extra["size"] = info.get("size")
#     else:
#         p[0] = p[1]
#
# def p_operand_name(p):
#     '''operand_name : IDENT
#                     | NIL'''
#     p[0] = Node()
#     if p[1] != "nil":
#         p[0].id_list = [p[1]]
#         p[0].type_list = ["identifier"]
#     else:
#         p[0].type_list = [["pointer", None, 0]]
#         p[0].place_list = [0]
#         p[0].extra["size"] = 4
# def p_type_name(p):
#     '''type_name    : TYPE IDENT'''
#     # check_shivansh
#     #Hritvik remove qualified_ident from type_name
#     p[0] = Node()
#     p[0].type_list = ["type " + p[1]]
#
# def p_type_lit(p):
#     '''type_lit : array_type
#                 | struct_type
#                 | pointer_type
#                 | interface_type
#                 | slice_type'''
#     #Hritvik removed function_type
#     p[0] = p[1]
#
# def p_array_type(p):
#     '''array_type   : LBRACK array_length RBRACK element_type'''
#     global scopes
#     if type(p[2].code[-1][-1]) != int:
#         raise TypeError(str(p.lineno(2)) + ": Array length should be integer")
#     p[0] = Node()
#     temp_v = p[4].extra["size"]
#     p[0].type_list = [["array", p[4].type_list[0], temp_v]]
#     p[0].extra["size"] = p[2].code[-1][-1]*temp_v
#     p[0].code = p[4].code
#
# def p_array_length(p):
#     '''array_length : expression'''
#     p[0] = p[1]
#
# def p_element_type(p):
#     '''element_type : type'''
#     p[0] = p[1]
#
# def p_slice_type(p):
#     '''slice_type   : LBRACK RBRACK element_type'''
#     p[0] = Node()
#     temp_v = p[3].extra["size"]
#     p[0].type_list = [["slice", p[3].type_list[0], temp_v]]
#     p[0].code = p[3].code
#
# def p_struct_type(p):
#     '''struct_type  : STRUCT LBRACE field_decl_rep RBRACE'''
#     # ADD "fields" and "methods" and "fields_type" and "field_size"
#     if len(p[3].id_list) != len(set(p[3].id_list)):
#         raise NameError(str(p.lineno(2)) + " - " + str(p.lineno(4)) + ": Multiple fields with same name in struct")
#     p[0] = Node()
#     p[0].extra["fields"] = p[3].id_list
#     p[0].extra["fields_type"] = p[3].type_list
#     p[0].extra["fields_size"] = p[3].extra["element_size"]
#     p[0].type_list = ["struct"]
#     p[0].extra["size"] = sum(p[3].extra["element_size"])
#     p[0].code = p[3].code
#
# def p_field_decl_rep(p):
#     '''field_decl_rep   : field_decl_rep field_decl semicolon_opt
#                         | epsilon'''
#     p[0] = p[1]
#     if len(p) == 4:
#         p[0].id_list += p[2].id_list
#         p[0].type_list += p[2].type_list
#         p[0].extra["element_size"] += p[2].extra["element_size"]
#         p[0].code += p[2].code
#     else:
#         p[0].extra["element_size"] = []
#
# def p_field_decl(p):
#     '''field_decl   : identifier_list type'''
#     p[0] = Node()
#     p[0].id_list = p[1].id_list
#     p[0].type_list = [p[2].type_list[0]]*len(p[1].id_list)
#     if "type" in p[2].type_list[0]:
#         info = find_info(p[2].type_list[0], p.lineno(2), 0)
#         p[0].extra["element_size"] = [info["size"]]*len(p[1].id_list)
#     else:
#         p[0].extra["element_size"] = [p[2].extra["size"]]*len(p[1].id_list)
#     p[0].code = p[2].code
#
# def p_pointer_type(p):
#     '''pointer_type : MUL base_type'''
#     p[0] = Node()
#     p[0].type_list = [["pointer", p[2].type_list[0], p[2].extra["size"]]]
#     p[0].extra["size"] = 4
#
# def p_base_type(p):
#     '''base_type    : type'''
#     p[0] = p[1]
#
# # def p_function_type(p):
# #     '''function_type    : FUNC signature'''
# #     p[0] = Node()
# #     p[0].type_list += ["func"] + p[1].type_list #TODO: Need to fix this
#
# def p_signature(p):
#     '''signature    : parameters result'''
#     global scopes, current_scope, temp_array
#     p[0] = Node()
#     p[0].id_list = p[1].id_list
#     p[0].type_list = p[1].type_list
#     p[0].extra["parameter_size"] = p[1].extra["size"]
#     p[0].extra["parameter_temp"] = []
#     p[0].extra["scope"] = current_scope
#     if len(p[2].type_list) == 0:
#         p[0].extra["return_type"] = ["void"]
#         p[0].extra["return_id"] = [None]
#         p[0].extra["return_size"] = [0]
#         p[0].extra["return_temp"] = []
#     else:
#         p[0].extra["return_type"] = p[2].type_list
#         p[0].extra["return_id"] = p[2].id_list
#         p[0].extra["return_temp"] = []
#         if type(p[2].extra["size"]) == list:
#             p[0].extra["return_size"] = p[2].extra["size"]
#         else:
#             p[0].extra["return_size"] = [p[2].extra["size"]]
#     if p[-3] == "func":
#         id_list = p[0].id_list
#         if len(id_list) != len(set(id_list)):
#             raise NameError(str(p.lineno(1)) + ": Variable already declared")
#         for i in range(len(id_list)):
#             temp_v = new_temp()
#             temp_array += [temp_v]
#             p[0].extra["parameter_temp"] += [temp_v]
#             scopes[current_scope].insert(id_list[i], p[0].type_list[i])
#             scopes[current_scope].update(id_list[i], p[0].extra["parameter_size"][i], "size")
#             scopes[current_scope].update(id_list[i], temp_v, "temp")
#             scopes[current_scope].update(id_list[i], True, "is_var")
#             scopes[current_scope].update(id_list[i], True, "is_param")
#
#         id_list = p[0].extra["return_id"]
#         for i in range(len(id_list)):
#             if id_list[i] == None:
#                 p[0].extra["return_temp"] += [None]
#                 continue
#             if id_list[i] in p[0].extra["parameter_temp"] or id_list[i] in p[0].extra["return_temp"]:
#                 raise NameError(str(p.lexer.lineno) + ": Variable " + str(id_list[i]) + " already declared")
#             temp_v = new_temp()
#             temp_array += [temp_v]
#             p[0].extra["return_temp"] += [temp_v]
#             scopes[current_scope].insert(id_list[i], p[0].extra["return_type"][i])
#             scopes[current_scope].update(id_list[i], p[0].extra["return_size"][i], "size")
#             scopes[current_scope].update(id_list[i], temp_v, "temp")
#             scopes[current_scope].update(id_list[i], True, "is_var")
#
#         scopes[0].update(p[-2], p[0].type_list , "parameter_type")
#         scopes[0].update(p[-2], p[0].id_list , "parameter_id")
#         scopes[0].update(p[-2], p[0].extra["parameter_size"] , "parameter_size")
#         scopes[0].update(p[-2], p[0].extra["return_type"] , "return_type")
#         scopes[0].update(p[-2], p[0].extra["return_id"] , "return_id")
#         scopes[0].update(p[-2], p[0].extra["return_size"] , "return_size")
#
# def p_result(p):
#     '''result   : parameters
#                 | type_list
#                 | type
#                 | epsilon'''
#     p[0] = p[1]
#     if len(p[0].type_list) != len(p[0].id_list):
#         p[0].id_list = [None]*(len(p[0].type_list))
#
# def p_type_list(p):
#     '''type_list    : LPAREN type type_rep comma_opt RPAREN'''
#     p[0] = p[2]
#     p[0].type_list += p[3].type_list
#     p[0].extra["size"] = [p[0].extra["size"]] + p[3].extra["size"]
#     p[0].id_list = [None]*(len(p[0].type_list))
#
# def p_type_rep(p):
#     '''type_rep : type_rep COMMA type
#                 | epsilon'''
#     p[0] = p[1]
#     if len(p) == 4:
#         p[0].type_list += p[3].type_list
#         p[0].extra["size"] += [p[3].extra["size"]]
#     else:
#         p[0].extra = []
#
# def p_parameters(p):
#     '''parameters   : LPAREN RPAREN
#                     | LPAREN parameter_list comma_opt RPAREN'''
#     if len(p) == 3:
#         p[0] = Node()
#         p[0].extra["size"] = []
#     else:
#         p[0] = p[2]
#
# def p_parameter_list(p):
#     '''parameter_list   : parameter_decl parameter_decl_rep '''
#     p[0] = p[1]
#     p[0].id_list += p[2].id_list
#     p[0].type_list += p[2].type_list
#     p[0].extra["size"] += p[2].extra["size"]
#
# def p_parameter_decl_rep(p):
#     '''parameter_decl_rep   : parameter_decl_rep COMMA parameter_decl
#                             | epsilon'''
#     p[0] = p[1]
#     if len(p) == 4:
#         p[0].id_list += p[3].id_list
#         p[0].type_list += p[3].type_list
#         p[0].extra["size"] += p[3].extra["size"]
#     else:
#         p[0].extra["size"] = []
# def p_parameter_decl(p):
#     '''parameter_decl   : identifier_list_opt type '''
#     p[0] = Node()
#     if len(p[1].id_list) == 0:
#         p[0].type_list = [p[2].type_list[0]]
#         p[0].id_list = [None]
#         p[0].extra["size"] = [p[2].extra["size"]]
#     else:
#         p[0].id_list = p[1].id_list
#         p[0].type_list = [p[2].type_list[0]]*(len(p[1].id_list))
#         p[0].extra["size"] = [p[2].extra["size"]]*(len(p[1].id_list))
#
# def p_identifier_list_opt(p):
#     '''identifier_list_opt  : identifier_list
#                             | epsilon'''
#     p[0] = p[1]
#
# def p_interface_type(p):
#     '''interface_type   : INTERFACE LBRACE method_spec_rep RBRACE '''
#     # p[0] = mytuple(["interface_type"] + p[1:])
#
# def p_method_spec_rep(p):
#     '''method_spec_rep  : method_spec_rep method_spec semicolon_opt
#                         | epsilon'''
#     # p[0] = mytuple(["method_spec_rep"] + p[1:])
#
# def p_method_spec(p):
#     '''method_spec  : method_name signature
#                     | interface_type_name'''
#     # p[0] = mytuple(["method_spec"] + p[1:])
#
# def p_method_name(p):
#     '''method_name  : IDENT'''
#     p[0] = p[1]
#
# def p_interface_type_name(p):
#     '''interface_type_name  : type_name'''
#     p[0] = p[1]
#
# #def p_key_type(p):
# #    '''key_type : type'''
# #    p[0] = p[1]
#
# def p_declaration(p):
#     '''declaration  : const_decl
#                     | type_decl
#                     | var_decl'''
#     p[0] = p[1]
#
# def p_top_level_decl(p):
#     '''top_level_decl   : declaration
#                         | function_decl
#                         | method_decl'''
#     p[0] = p[1]
#
# def p_const_decl(p):
#     '''const_decl   : CONST const_spec
#                     | CONST LPAREN const_spec_rep RPAREN'''
#     # p[0] = mytuple(["const_decl"] + p[1:])
#
# def p_const_spec_rep(p):
#     '''const_spec_rep   : const_spec_rep const_spec semicolon_opt
#                         | epsilon'''
#     # p[0] = mytuple(["const_spec_rep"] + p[1:])
#
# def p_const_spec(p):
#     '''const_spec   : identifier_list
#                     | identifier_list type_opt ASSIGN expression_list'''
#     # p[0] = mytuple(["const_spec"] + p[1:])
#
# def p_type_opt(p):
#     '''type_opt : type
#                 | epsilon'''
#     p[0] = p[1]
#
# def p_type_decl(p):
#     '''type_decl    : TYPE type_spec
#                     | TYPE LPAREN type_spec_rep RPAREN'''
#     p[0] = Node()
#
# def p_type_spec_rep(p):
#     '''type_spec_rep    : type_spec_rep type_spec semicolon_opt
#                         | epsilon'''
#     p[0] = Node()
#
# def p_type_spec(p):
#     '''type_spec    : type_def'''
#     #TODO: Hritvik removed alias type add that it is pretty easy
#     p[0] = p[1]
#
# def p_add_type(p):
#     '''add_type   :'''
#     p[0] = Node()
#     scopes[current_scope].insert("type " + p[-1], "struct")
#
# def p_type_def(p):
#     '''type_def : IDENT add_type struct_type'''
#     #TODO: Hritvik changed this to struct type
#     p[0] = Node()
#     global scopes, current_scope
#     for i, j in enumerate(p[3].extra["fields_type"]):
#         if j == ["pointer", "type " + p[1], None]:
#             p[3].extra["fields_type"][i] = ["pointer", "type " + p[1], p[3].extra["size"]]
#     scopes[current_scope].update("type " + p[1], [], "methods")
#     scopes[current_scope].update("type " + p[1], p[3].extra["fields"], "fields")
#     scopes[current_scope].update("type " + p[1], p[3].extra["fields_type"], "fields_type")
#     scopes[current_scope].update("type " + p[1], p[3].extra["fields_size"], "fields_size")
#     scopes[current_scope].update("type " + p[1], p[3].extra["size"], "size")
#
# def p_var_decl(p):
#     '''var_decl : VAR var_spec
#                 | VAR LPAREN var_spec_rep RPAREN'''
#     if len(p) == 3:
#         p[0] = p[2]
#     else:
#         p[0] = p[3]
#
# def p_var_spec_rep(p):
#     '''var_spec_rep : var_spec_rep var_spec semicolon_opt
#                     | epsilon'''
#     p[0] = p[1]
#     if len(p) != 2:
#         p[0].id_list += p[2].id_list
#         p[0].type_list += p[2].type_list
#         p[0].code += p[2].code
#
# def p_var_spec(p):
#     '''var_spec : identifier_list type expr_list_assign_opt
#                 | identifier_list ASSIGN expression_list'''
#     global scopes, current_scope, temp_array
#     p[0] = p[1]
#     if p[2] == "=":
#         if len(p[1].id_list) != len(p[3].place_list):
#             raise ArithmeticError(str(p.lineno(3)) + ": Different Number of identifiers and Expression")
#         p[0].place_list = p[3].place_list
#         id_list = p[1].id_list
#         expr_type_list = p[3].type_list
#         for i in range(len(p[1].id_list)):
#             if scopes[current_scope].look_up(id_list[i]):
#                 raise NameError(str(p.lineno(1)) + ": Variable " + str(id_list[i]) + " already declared")
#             if expr_type_list[i] == "void":
#                 raise TypeError(str(p.lineno(3)) + ": Cannot assign type void")
#             if p[3].place_list[i] in temp_array:
#                 temp_v = new_temp()
#                 p[0].code += [["decl", temp_v]] + p[3].code[i] + [["=", temp_v, p[3].place_list[i]]]
#             else:
#                 temp_v = p[3].place_list[i]
#                 p[0].code += [["decl", temp_v]] + p[3].code[i]
#             temp_array += [temp_v]
#             scopes[current_scope].insert(id_list[i], expr_type_list[i])
#             scopes[current_scope].update(id_list[i], p[3].extra["size"][i], "size")
#             scopes[current_scope].update(id_list[i], temp_v, "temp")
#             scopes[current_scope].update(id_list[i], True, "is_var")
#     else:
#         assert (len(p[2].code) == 0), "Type should not have any code"
#         if len(p[3].place_list) == 0:
#             # not initialised with expressions
#             id_list = p[1].id_list
#             for i in range(len(id_list)):
#                 if scopes[current_scope].look_up(id_list[i]):
#                     raise NameError(str(p.lineno(1)) + ": Variable " + str(id_list[i]) + " already declared")
#                 temp_v = new_temp()
#                 temp_array += [temp_v]
#                 scopes[current_scope].insert(id_list[i], p[2].type_list[0])
#                 scopes[current_scope].update(id_list[i], p[2].extra["size"], "size")
#                 scopes[current_scope].update(id_list[i], temp_v, "temp")
#                 scopes[current_scope].update(id_list[i], True, "is_var")
#                 p[0].code += [["decl", temp_v]]
#         else:
#             if len(p[1].id_list) != len(p[3].place_list):
#                 raise ArithmeticError(str(p.lineno(3)) + ": Different Number of identifiers and Expressions")
#             p[0].place_list = p[3].place_list
#             id_list = p[1].id_list
#             expr_type_list = p[3].type_list
#             for i in range(len(id_list)):
#                 if scopes[current_scope].look_up(id_list[i]):
#                     raise NameError(str(p.lineno(1)) + ": Variable " + str(id_list[i]) + " already declared")
#                 if expr_type_list[i] == "void":
#                     raise TypeError(str(p.lineno(3)) + ": Cannot assign type void")
#                 # typecast = ("float" in p[2].type_list[0] and "int" in expr_type_list[i])
#                 # typecast = typecast or (p[2].type_list[0].startswith("int") and "int" in expr_type_list[i])
#                 # typecast = typecast or ("uint" in p[2].type_list[0] and "int" in expr_type_list[i])
#                 if "string" in p[2].type_list[0] and "string" in expr_type_list[i]:#TODO: should make this condition a bit strong ["array", ["string"]]
#                     p[2].type_list[0] = expr_type_list[i]
#
#                 if ["pointer", None, None] == expr_type_list[i] and "pointer" in p[2].type_list[0]:
#                     expr_type_list[i] = p[2].type_list[0]
#                 if p[2].type_list[0] == expr_type_list[i]:
#                     if p[3].place_list[i] in temp_array:
#                         temp_v = new_temp()
#                         p[0].code += [["decl", temp_v]] + p[3].code[i] + [["=", temp_v, p[3].place_list[i]]]
#                     else:
#                         temp_v = p[3].place_list[i]
#                         p[0].code += [["decl", temp_v]] + p[3].code[i]
#                     temp_array += [temp_v]
#                     scopes[current_scope].insert(p[1].id_list[i], p[2].type_list[0])
#                     scopes[current_scope].update(id_list[i], p[2].extra["size"], "size")
#                     scopes[current_scope].update(id_list[i], temp_v, "temp")
#                     scopes[current_scope].update(id_list[i], True, "is_var")
#                 else:
#                     raise TypeError(str(p.lineno(1)) + ": Type mismatch for identifier: " + str(id_list[i]))
# def p_expr_list_assign_opt(p):
#     '''expr_list_assign_opt : ASSIGN expression_list
#                             | epsilon'''
#     if len(p) == 2:
#         p[0] = p[1]
#     else:
#         p[0] = p[2]
#
# def p_short_val_decl(p):
#     '''short_val_decl   : IDENT DEFINE expression'''
#     # '''short_val_decl   : identifier_list DEFINE expression_list'''
#     # Arpit: mutiple identifiers can be defined
#     global scopes, current_scope, temp_array
#     p[0] = p[3]
#     p[0].id_list += [p[1]]
#     if scopes[current_scope].look_up(p[1]):
#         raise NameError(str(p.lineno(1)) + ": Variable " + str(p[1]) + " already declared")
#     if p[0].type_list[0] == "void":
#         raise TypeError(str(p.lineno(3)) + ": Cannot assign type void")
#     if p[3].place_list[0] in temp_array:
#         temp_v = new_temp()
#         p[0].code = [["decl", temp_v], ["=", temp_v, p[3].place_list[0]]] + p[0].code
#     else:
#         temp_v = p[3].place_list[0]
#         p[0].code = [["decl", temp_v]] + p[0].code
#     temp_array += [temp_v]
#     scopes[current_scope].insert(p[1], p[3].type_list[0])
#     scopes[current_scope].update(p[1], p[3].extra["size"], "size")
#     scopes[current_scope].update(p[1], temp_v, "temp")
#     scopes[current_scope].update(p[1], True, "is_var")
#
# def p_function_decl(p):
#     '''function_decl    : FUNC function_name add_scope function end_scope
#                         | FUNC function_name add_scope signature end_scope semicolon_opt'''
#     #TODO: verify whether we need to add scope at the time of signature declaration
#     #In this function current scope is actually global
#     global scopes, current_scope, scopes_ctr, temp_ctr, temp_array
#     if len(p) == 6:
#         p[0] = p[4]
#         p[0].code = p[3].code + p[0].code + p[5].code
#     else:
#         if in_scope("signature_" + p[2]):
#             raise NameError(str(p.lineno(4)) + ": Signature " + p[2] + " already defined")
#         else:
#             scopes[0].delete(p[2])
#             scopes_ctr -= 1
#             temp_ctr -= len(p[4].extra["parameter_temp"]) + sum([i!=None for i in p[4].extra["return_temp"]])
#             temp_array = [x for x in temp_array if x not in p[4].extra["parameter_temp"]]
#             temp_array = [x for x in temp_array if x not in p[4].extra["return_temp"]]
#             del scopes[p[4].extra["scope"]]
#             scopes[0].insert("signature_" + p[2], "signature")
#             scopes[0].update("signature_" + p[2], "_func_" + p[2], "label")
#             p[0] = p[4]
#             scopes[0].update("signature_" + p[2], p[0].type_list , "parameter_type")
#             scopes[0].update("signature_" + p[2], p[0].id_list , "parameter_id")
#             scopes[0].update("signature_" + p[2], p[0].extra["parameter_size"] , "parameter_size")
#             scopes[0].update("signature_" + p[2], p[0].extra["return_type"] , "return_type")
#             scopes[0].update("signature_" + p[2], p[0].extra["return_id"] , "return_id")
#             scopes[0].update("signature_" + p[2], p[0].extra["return_size"] , "return_size")
#
# def p_function_name(p):
#     '''function_name    : IDENT'''
#     p[0] = p[1]
#
# def p_function(p):
#     '''function : signature function_body'''
#     global scopes, current_scope
#     if in_scope("signature_" + p[-2]):
#         info = scopes[0].get_info("signature_" + p[-2])
#         if info["parameter_type"] != p[1].type_list:
#             raise TypeError(str(p.lineno(1)) + ": Prototype and Function parameter type don't match ", info["parameter_type"], p[1].type_list)
#         elif info["return_type"] != p[1].extra["return_type"]:
#             raise TypeError(str(p.lineno(1)) + ": Prototype and Function return type don't match ", info["parameter_type"], p[1].extra["return_type"])
#
#     info = scopes[0].get_info(p[-2])
#     if info["return_type"][0] != "void" and info.get("is_returning", None) != True:
#         raise TypeError(str(p.lineno(1)) + ": Function return type is not void", p[-2])
#     p[0] = Node()
#     for i in p[1].extra["parameter_temp"]:
#         p[0].code += [["argdecl", i]]
#     for i in p[1].extra["return_temp"]:
#         if i!= None:
#             p[0].code += [["retdecl", i]]
#     p[0].code += p[1].code + p[2].code
#
# def p_function_body(p):
#     '''function_body    : block'''
#     p[0] = p[1]
#
# def p_method_decl(p):
#     '''method_decl  : FUNC receiver method_name add_scope function end_scope
#                     | FUNC receiver method_name add_scope signature end_scope'''
#     # p[0] = mytuple(["method_decl"] + p[1:])
#
# def p_receiver(p):
#     '''receiver : parameters'''
#     # p[0] = mytuple(["receiver"] + p[1:])
#
# def p_operand(p):
#     '''operand  : literal
#                 | operand_name
#                 | LPAREN expression RPAREN'''
#     # check_shivansh
#     # method_expr removed from the RHS of production and added to primary_expr directly
#     # method and LPAREN expression RPAREN should may be removed
#     if len(p) == 2:
#         p[0] = p[1]
#     else:
#         p[0] = p[2]
#
# def p_literal(p):
#     '''literal  : basic_lit'''
#     #TODO: Removed composite_lit for now
#     #TODO: Hritvik removed function_lit dekh lo agar ho sakta hai toh
#     p[0] = p[1]
#
# def p_basic_lit(p):
#     '''basic_lit    : int_lit
#                     | FLOAT_LIT
#                     | TRUE
#                     | FALSE
#                     | STRING_LIT '''
#     #Add imaginary and rune lit
#     if type(p[1]) == Node:
#         p[0] = p[1]
#     elif p[1] == "true" or p[1] == "false":
#         temp_v = new_temp()
#         p[0] = Node()
#         p[0].place_list = [temp_v]
#         p[0].type_list = ["bool"]
#         p[0].extra["size"] = sizeof["bool"]
#         if p[1] == "true":
#             p[0].code = [["=", temp_v, True], ["goto", temp_v]]
#             p[0].extra["true_list"] = [temp_v]
#             p[0].extra["false_list"] = []
#         else:
#             p[0].code = [["=", temp_v, False], ["goto", temp_v]]
#             p[0].extra["true_list"] = []
#             p[0].extra["false_list"] = [temp_v]
#     elif type(p[1]) == float:
#         temp_v = new_temp()
#         p[0] = Node()
#         p[0].place_list = [temp_v]
#         p[0].code = [["=", temp_v, p[1]]]
#         p[0].type_list = ["float32"]
#         p[0].extra["size"] = 4
#     else:
#         temp_v = new_temp()
#         p[0] = Node()
#         p[0].place_list = [temp_v]
#         p[0].code = [["=", temp_v, "'" + p[1][1:-1] + "'"]]
#         p[0].type_list = [["string", len(p[1][1:-1])]]
#         p[0].extra["size"] = sizeof["string"]
#
# def p_int_lit(p):
#     '''int_lit  : DECIMAL_LIT
#                 | OCTAL_LIT
#                 | HEX_LIT'''
#     temp_v = new_temp()
#     p[0] = Node()
#     p[0].place_list = [temp_v]
#     p[0].code = [["=", temp_v, p[1]]]
#     p[0].type_list = ["int"]
#     p[0].extra["size"] = 4
#
#
# #def p_qualified_ident(p):
# #    '''qualified_ident  : package_name PERIOD IDENT'''
# #    # p[0] = mytuple(["qualified_ident"] + p[1:])
#
# #def p_composite_lit(p):
# #    '''composite_lit    : literal_type literal_value'''
# #    p[0] = Node()
#     #if "type" in p[1].type_list[0]:
#         #TODO: check the type of all the elements of the struct
#     #elif "slice" in p[1].type_list[0]:
#         #TODO: check the type of all the elements they should be equal to p[1].extra["element_type"]
#         #and set the length and capacity to number of elements
#     #else:
#         #TODO: check the type of all the elements they should be equal to p[1].extra["element_type"]
#         #and the length should be less than  p[1].extra["element_length"]
#         #and set the length to the number of elements and capacity to p[1].extra["element_length"]
#
# #def p_literal_type(p):
# #    '''literal_type : array_type
# #                    | slice_type
# #                    | type_name'''
# #    p[0] = p[1]
#
# def p_literal_value(p):
#     '''literal_value    : LBRACE RBRACE
#                         | LBRACE element_list comma_opt RBRACE'''
#     if len(p) == 3:
#         p[0] = Node()
#     else:
#         p[0] = p[2]
#
# def p_element_list(p):
#     '''element_list : element_list COMMA element
#                     | element'''
#     p[0] = p[1]
#     if len(p) == 4:
#         p[0].id_list += [","] + p[3].id_list
#         p[0].type_list += [","] + p[3].type_list
# def p_element(p):
#     '''element  : expression
#                 | literal_value'''
#     p[0] = p[1]
#
# # def p_function_lit(p):
# #     '''function_lit : FUNC function'''
# #     # p[0] = mytuple(["function_lit"] + p[1:])
#
#
# # conversion deleted form the RHS of the primary expression
# def p_primary_expr(p):
#     '''primary_expr : operand
#                     | conversion
#                     | primary_expr PERIOD IDENT
#                     | primary_expr LBRACK expression RBRACK
#                     | primary_expr slice
#                     | primary_expr LPAREN arguments RPAREN'''
#     # check_shivansh
#     # | operand_selector
#     # but make sure of test cases : a.b.c(d,e)      x.a = b     foo(a,b)    etc.
#     # operand selector in RHS becomes redundant; never gets used
#     # slice may need to be removed from RHS
#     # typeassertion removed from RHS of above production
#     if "conversion" in p[1].extra:
#         p[0] = p[1]
#     elif len(p) == 2:
#         p[0] = p[1]
#     elif p[2] == ".":
#         #TODO: WE ARE NOT IMPLEMENTING IMPORTS HENCE ASSUMING PRIMARY EXPRESSION IN THIS CASE TO BE A VARIBLE
#         p[0] = p[1]
#         if "identifier" == p[0].type_list[0]:
#             info = find_info(p[0].id_list[0], p.lineno(1))
#             if info["is_var"]:
#                 temp_v = new_temp()
#                 p[0].code += [["(addr)", temp_v, info["temp"]]]
#                 # print("in p_exp", p[3],info["type"])
#                 info1 = find_info(info["type"], p.lineno(1), 0)
#             else:
#                 raise NameError(str(p.lineno(1)) + ": Variable " + str(p[0].id_list[0]) + " not defined")
#         else:
#             info1 = find_info(p[0].type_list[0][1], p.lineno(1), 0)
#             temp_v = p[0].place_list[0]
#
#         if p[3] in info1["fields"]:
#             p[0].type_list = [["pointer", info1["fields_type"][info1["fields"].index(p[3])], info1["fields_size"][info1["fields"].index(p[3])]]]
#             temp_v1 = new_temp()
#             p[0].code += [["int_+", temp_v1, temp_v, sum(info1["fields_size"][:info1["fields"].index(p[3])])]]
#             p[0].place_list = [temp_v1]
#             p[0].extra["size"] = 4
#             p[0].extra["it_is_a_pointer"] = True
#         # elif p[3] in info1["methods"]:
#         else:
#             raise NameError(str(p.lineno(3)) + ": No field or method " + str(p[3]) + " defined in " + str(info1["type"]))
#
#     elif p[2] == "[":
#         p[0] = p[1]
#         p[0].code += p[3].code
#         if "identifier" == p[0].type_list[0]:
#             info = find_info(p[0].id_list[0], p.lineno(1))
#             # print(info["type"])
#             if info["is_var"] and "array" in info["type"]:
#                 temp_v = new_temp()
#                 p[0].code += [["(addr)", temp_v, info["temp"]]]
#                 p[0].type_list = [info["type"]]
#                 p[0].extra["size"] = info["size"]
#             elif info["is_var"] and "pointer" in info["type"]:
#                 temp_v = info["temp"]
#                 p[0].extra["size"] = info["type"][0][2]
#                 p[0].type_list = [info["type"]]
#             else:
#                 raise NameError(str(p.lineno(1)) + ": Variable " + str(p[0].id_list[0]) + " not defined")
#         elif "pointer" in p[0].type_list[0]:
#             if "array" not in p[0].type_list[0][1]:
#                 raise TypeError(str(p.lineno(1)) + ": Type " + str(p[0].type_list[0]) + " not indexable")
#             p[0].extra["size"] = p[0].type_list[0][2]
#             p[0].type_list = [p[0].type_list[0][1]]
#             temp_v = p[0].place_list[0]
#         elif "array" not in p[0].type_list[0]:
#             raise TypeError(str(p.lineno(1)) + ": Type " + str(p[0].type_list[0]) + " not indexable")
#         else:
#             temp_v = p[0].place_list[0]
#         p[0].type_list = [["pointer", p[0].type_list[0][1], p[0].type_list[0][2]]]
#         temp_v1 = new_temp()
#         temp_v2 = new_temp()
#         p[0].code += [["int_*", temp_v1, p[3].place_list[0], p[0].type_list[0][2]], ["int_+", temp_v2, temp_v, temp_v1]]
#         p[0].place_list = [temp_v2]
#         p[0].extra["size"] = 4
#         p[0].extra["it_is_a_pointer"] = True
#     #TODO: Hritvik not implementing slice for now
#     # elif len(p) == 3:
#     #     if p[1].id_list[0] == "identifier":
#     elif p[2] == "(":
#         if p[1].type_list[0] == "identifier":
#             bypass = True if p[1].id_list[0] in libc_functions else False
#             if not bypass and not in_scope(p[1].id_list[0]):
#                 info = find_info("signature_" + p[1].id_list[0], p.lineno(1), 0)
#             elif not bypass:
#                 info = find_info(p[1].id_list[0], p.lineno(1), 0)
#             if bypass or info["type"] == "function" or info["type"] == "signature":
#                 p[0] = Node()
#                 p[0].code += [["push_begin"]]
#                 parameter_pushed_size = 0
#                 for i, j in reversed(list(enumerate(p[3].type_list))):
#                     bypass1 = bypass or ("pointer" in j and j[:2] == info["parameter_type"][i][:2])
#                     if bypass1 or (j == info["parameter_type"][i] and p[3].extra["size"][i] == info["parameter_size"][i]):
#                         parameter_pushed_size += p[3].extra["size"][i]
#                         # print("Wtf is this code", [k for k in p[3].code[i] if "int_*" in k])
#                         p[0].code += p[3].code[i] + [["push", p[3].place_list[i], p[3].extra["size"][i]]]
#                     else:
#                         raise TypeError(str(p.lineno(1)) + ": Function " + str(p[1].id_list[0]) + " should not be called with type " + str(j) + " at the index " + str(i))
#                 if bypass:
#                     p[0].code += [["call", p[1].id_list[0]]]
#                 else:
#                     p[0].code += [["call", info["label"]]]
#                 p[0].code += [["pop", parameter_pushed_size]]
#                 if bypass or info["return_type"][0] != "void":
#                     temp_v = new_temp()
#                     p[0].code += [["=", temp_v, "return_value"]]
#                 else:
#                     temp_v = "temp_void"
#                 p[0].place_list = [temp_v]
#                 if bypass:
#                     p[0].type_list = [libc_functions[p[1].id_list[0]]["return_type"]]
#                     p[0].extra["size"] = libc_functions[p[1].id_list[0]]["return_size"]
#                 else:
#                     p[0].type_list = [info["return_type"][0]]
#                     p[0].extra["size"] = info["return_size"][0]
#             else:
#                 raise NameError(str(p.lineno(1)) + ": Variable " + str(p[0].id_list[0]) + " not defined")
#         else:
#             raise TypeError(str(p.lineno(1)) + ": Identifier of type " + str(p[1].id_list[0]) + " not callable")
#
# def p_slice(p):
#     '''slice    : LBRACK expression_opt COLON expression_opt RBRACK
#                 | LBRACK expression_opt COLON expression COLON expression RBRACK'''
#     # p[0] = mytuple(["slice"] + p[1:])
#
# def p_arguments(p):
#     '''arguments    : epsilon
#                     | expression_list comma_opt'''
#     # check_shivansh
#     # lst RHS may have to be removed
#     p[0] = p[1]
#
# def p_expression(p):
#     '''expression   : unary_expr
#                     | expression LOR expression
#                     | expression LAND expression
#                     | expression EQL expression
#                     | expression NEQ expression
#                     | expression LSS expression
#                     | expression LEQ expression
#                     | expression GTR expression
#                     | expression GEQ expression
#                     | expression ADD expression
#                     | expression SUB expression
#                     | expression OR expression
#                     | expression XOR expression
#                     | expression MUL expression
#                     | expression QUO expression
#                     | expression REM expression
#                     | expression SHL expression
#                     | expression SHR expression
#                     | expression AND expression
#                     | expression AND_NOT expression'''
#     if len(p) == 2:
#         p[0] = p[1]
#     else:
#         temp_v = new_temp()
#         p[0] = Node()
#         p[0].extra["size"] = max(p[1].extra["size"], p[3].extra["size"])
#         if len(p[1].code) > 0 and len(p[3].code) > 0 and type(p[1].code[-1][-1]) == int and type(p[3].code[-1][-1]) == int:
#             p[0].code = p[1].code[:-1] + p[3].code[:-1]
#             p[0].code += [["=", temp_v, eval(str(p[1].code[-1][-1]) + p[2] + str(p[3].code[-1][-1]))]]
#             p[0].place_list = [temp_v]
#             if p[2] == "<" or p[2] == ">" or p[2] == "<=" or p[2] == ">=" or p[2] == "==":
#                 p[0].type_list = ["bool"]
#                 if p[0].code[-1][-1] == True:
#                     p[0].extra["true_list"] = [temp_v]
#                 else:
#                     p[0].extra["false_list"] = [temp_v]
#                 p[0].code += [["goto", temp_v]]
#             else:
#                 p[0].type_list = ["int"]
#         elif len(p[1].code) > 1 and len(p[3].code) > 1 and type(p[1].code[-2][-1]) == bool and type(p[3].code[-2][-1]) == bool:
#             if p[2] == "&&" or p[2] == "||" or p[2] == "==" or p[2] == "^":
#                 p[0].code = p[1].code[:-2] + p[3].code[:-2]
#                 p[0].place_list = [temp_v]
#                 p[0].code += [["=", temp_v, eval(str(p[1].code[-1][-1]) + p[2] + str(p[3].code[-1][-1]))]]
#                 if p[0].code[-1][-1] == True:
#                     p[0].extra["true_list"] = [temp_v]
#                 else:
#                     p[0].extra["false_list"] = [temp_v]
#                 p[0].code += [["goto", temp_v]]
#                 p[0].type_list = ["bool"]
#             else:
#                 raise TypeError(str(p.lineno(2)) + ": Cannot do operation " + str(p[2]) + " on bool literals")
#         elif len(p[1].code) > 0 and len(p[3].code) > 0 and is_number(p[1].code[-1][-1]) and is_number(p[3].code[-1][-1]):
#             p[0].code = p[1].code[:-1] + p[3].code[:-1]
#             p[0].place_list = [temp_v]
#             if p[2] == "+" or p[2] == "-" or p[2] == "/" or p[2] == "*":
#                 p[0].code += [["=", temp_v, eval(str(p[1].code[-1][-1]) + p[2] + str(p[3].code[-1][-1]))]]
#                 p[0].type_list = ["float32"]
#             elif p[2] == "<" or p[2] == ">" or p[2] == "<=" or p[2] == ">=" or p[2] == "==":
#                 p[0].code += [["=", temp_v, eval(str(p[1].code[-1][-1]) + p[2] + str(p[3].code[-1][-1]))]]
#                 if p[0].code[-1][-1] == True:
#                     p[0].extra["true_list"] = [temp_v]
#                 else:
#                     p[0].extra["false_list"] = [temp_v]
#                 p[0].code += [["goto", temp_v]]
#                 p[0].type_list = ["bool"]
#             else:
#                 raise TypeError(str(p.lineno(2)) + ": Cannot do operation " + str(p[2]) + " on float literals")
#         else:
#             if p[1].type_list[0] == p[3].type_list[0] and "bool" != p[1].type_list[0]:
#                 p[0].code = p[1].code + p[3].code
#             if p[1].type_list[0] == p[3].type_list[0]:
#                 if "bool" == p[1].type_list[0]:
#                     if p[2] == "&&" or p[2] == "||":
#                         label_v = new_label()
#                         if p[2] == "||":
#                             p[1].code = backpatch(p[1].code, p[1].extra["false_list"], label_v)
#                             p[0].extra["true_list"] = p[1].extra["true_list"] + p[3].extra["true_list"]
#                             p[0].extra["false_list"] = p[3].extra["false_list"]
#                         else:
#                             p[1].code = backpatch(p[1].code, p[1].extra["true_list"], label_v)
#                             p[0].extra["true_list"] = p[3].extra["true_list"]
#                             p[0].extra["false_list"] = p[1].extra["false_list"] + p[3].extra["false_list"]
#                         # p[0].place_list = [temp_v]
#                         # p[0].code += [["int_" + p[2], temp_v, p[1].place_list[0], p[3].place_list[0]]]
#                         p[0].code = p[1].code + [["label", label_v]] + p[3].code
#                         p[0].type_list = [p[1].type_list[0]]
#                     else:
#                         raise TypeError(str(p.lineno(2)) + ": Cannot do operation " + str(p[2]) + " on bool literals")
#                 elif "int" in p[1].type_list[0] or "byte" == p[1].type_list[0]:
#                     if p[2] == "<<" or p[2] == ">>":
#                         if int(p[3].code[-1][-1]) != p[3].code[-1][-1] and ("u" not in p[3].type_list[0] or p[3].type_list[0] != "byte"):
#                             raise TypeError(str(p.lineno(2)) + ": Shift count should be unsigned integer")
#                     p[0].place_list = [temp_v]
#                     if p[2] == "<" or p[2] == ">" or p[2] == "<=" or p[2] == ">=" or p[2] == "==" or p[2] == "!=":
#                         temp_v1 = new_temp()
#                         p[0].code += [["if", "int_" + p[2], p[1].place_list[0], p[3].place_list[0], "goto", temp_v]]
#                         p[0].code += [["goto", temp_v1]]
#                         p[0].extra["true_list"] = [temp_v]
#                         p[0].extra["false_list"] = [temp_v1]
#                         p[0].type_list = ["bool"]
#                     else:
#                         p[0].code += [["int_" + p[2], temp_v, p[1].place_list[0], p[3].place_list[0]]]
#                         p[0].type_list = [p[1].type_list[0]]
#                 elif "float" in p[1].type_list[0]:
#                     if p[2] == "+" or p[2] == "-" or p[2] == "/" or p[2] == "*":
#                         p[0].place_list = [temp_v]
#                         p[0].code += [["float_" + p[2], temp_v, p[1].place_list[0], p[3].place_list[0]]]
#                         p[0].type_list = [p[1].type_list[0]]
#                     elif p[2] == "<" or p[2] == ">" or p[2] == "<=" or p[2] == ">=" or p[2] == "==" or p[2] == "!=":
#                         p[0].place_list = [temp_v]
#                         temp_v1 = new_temp()
#                         p[0].code += [["if", "float_" + p[2], p[1].place_list[0], p[3].place_list[0], "goto", temp_v]]
#                         p[0].code += [["goto", temp_v1]]
#                         p[0].extra["true_list"] = [temp_v]
#                         p[0].extra["false_list"] = [temp_v1]
#                         p[0].type_list = ["bool"]
#                     else:
#                         raise TypeError(str(p.lineno(2)) + ": Cannot do operation " + str(p[2]) + " on float literals")
#             else:
#                 if "pointer" in p[1].type_list[0] and "pointer" in p[3].type_list[0]:
#                     if p[2] == "==" or p[2] == "!=":
#                         p[0].place_list = [temp_v]
#                         temp_v1 = new_temp()
#                         p[0].code += [["if", "int_" + p[2], p[1].place_list[0], p[3].place_list[0], "goto", temp_v]]
#                         p[0].code += [["goto", temp_v1]]
#                         p[0].extra["true_list"] = [temp_v]
#                         p[0].extra["false_list"] = [temp_v1]
#                         p[0].type_list = ["bool"]
#                     else:
#                         raise TypeError(str(p.lineno(2)) + ": Cannot do operation " + str(p[2]) + " on pointers")
#                 elif len(p[1].code) > 0 and type(p[1].code[-1][-1]) == int:
#                     if "int" in p[3].type_list[0] or p[3].type_list[0] == "byte":
#                         if p[2] == "<<" or p[2] == ">>":
#                             if "u" not in p[3].type_list[0] or p[3].type_list[0] != "byte":
#                                 raise TypeError(str(p.lineno(2)) + ": Shift count should be unsigned integer")
#                         p[0].place_list = [temp_v]
#                         p[0].code += [["int_" + p[2], temp_v, p[1].place_list[0], p[3].place_list[0]]]
#                         if p[2] == "<" or p[2] == ">" or p[2] == "<=" or p[2] == ">=" or p[2] == "==" or p[2] == "!=":
#                             p[0].type_list = ["bool"]
#                         elif p[2] == "<<" or p[2] == ">>":
#                             p[0].type_list = ["int"]
#                         else:
#                             p[0].type_list = [p[3].type_list[0]]
#                     elif "float" in p[3].type_list[0]:
#                         if p[2] == "+" or p[2] == "-" or p[2] == "/" or p[2] == "*":
#                             p[0].place_list = [temp_v]
#                             p[0].code += [["float_" + p[2], temp_v, p[1].place_list[0], p[3].place_list[0]]]
#                             p[0].type_list = [p[3].type_list[0]]
#                         elif p[2] == "<" or p[2] == ">" or p[2] == "<=" or p[2] == ">=" or p[2] == "==" or p[2] == "!=":
#                             p[0].place_list = [temp_v]
#                             p[0].code += [["float_" + p[2], temp_v, p[1].place_list[0], p[3].place_list[0]]]
#                             p[0].type_list = ["bool"]
#                         else:
#                             raise TypeError(str(p.lineno(2)) + ": Cannot do operation " + str(p[2]) + " on float literals")
#                 elif len(p[3].code) > 0 and type(p[3].code[-1][-1]) == int:
#                     if "int" in p[1].type_list[0] or p[1].type_list[0] == "byte":
#                         p[0].place_list = [temp_v]
#                         p[0].code += [["int_" + p[2], temp_v, p[1].place_list[0], p[3].place_list[0]]]
#                         if p[2] == "<" or p[2] == ">" or p[2] == "<=" or p[2] == ">=" or p[2] == "==" or p[2] == "!=":
#                             p[0].type_list = ["bool"]
#                         else:
#                             p[0].type_list = [p[1].type_list[0]]
#                     elif "float" in p[1].type_list[0]:
#                         if p[2] == "+" or p[2] == "-" or p[2] == "/" or p[2] == "*":
#                             p[0].place_list = [temp_v]
#                             p[0].code += [["float_" + p[2], temp_v, p[1].place_list[0], p[3].place_list[0]]]
#                             p[0].type_list = [p[3].type_list[0]]
#                         elif p[2] == "<" or p[2] == ">" or p[2] == "<=" or p[2] == ">=" or p[2] == "==" or p[2] == "!=":
#                             p[0].place_list = [temp_v]
#                             p[0].code += [["float_" + p[2], temp_v, p[1].place_list[0], p[3].place_list[0]]]
#                             p[0].type_list = ["bool"]
#                         else:
#                             raise TypeError(str(p.lineno(2)) + ": Cannot do operation " + str(p[2]) + " on float literals")
#                 elif len(p[1].code) > 0 and type(p[1].code[-1][-1]) == float:
#                     if p[3].type_list[0] == "float64":
#                         if p[2] == "+" or p[2] == "-" or p[2] == "/" or p[2] == "*":
#                             p[0].place_list = [temp_v]
#                             p[0].code += [["float_" + p[2], temp_v, p[1].place_list[0], p[3].place_list[0]]]
#                             p[0].type_list = [p[3].type_list[0]]
#                         elif p[2] == "<" or p[2] == ">" or p[2] == "<=" or p[2] == ">=" or p[2] == "==" or p[2] == "!=":
#                             p[0].place_list = [temp_v]
#                             p[0].code += [["float_" + p[2], temp_v, p[1].place_list[0], p[3].place_list[0]]]
#                             p[0].type_list = ["bool"]
#                         else:
#                             raise TypeError(str(p.lineno(2)) + ": Cannot do operation " + str(p[2]) + " on float literals")
#                     elif p[1].code[-1][-1] == int(p[1].code[-1][-1]):
#                         p[1].code[-1][-1] = int(p[1].code[-1][-1])
#                         if "int" in p[3].type_list[0] or p[3].type_list[0] == "byte":
#                             if p[2] == "<<" or p[2] == ">>":
#                                 if "u" not in p[3].type_list[0] or p[3].type_list[0] != "byte":
#                                     raise TypeError(str(p.lineno(2)) + ": Shift count should be unsigned integer")
#                             p[0].place_list = [temp_v]
#                             p[0].code += [["int_" + p[2], temp_v, p[1].place_list[0], p[3].place_list[0]]]
#                             if p[2] == "<" or p[2] == ">" or p[2] == "<=" or p[2] == ">=" or p[2] == "==" or p[2] == "!=":
#                                 p[0].type_list = ["bool"]
#                             elif p[2] == "<<" or p[2] == ">>":
#                                 p[0].type_list = ["int"]
#                             else:
#                                 p[0].type_list = [p[3].type_list[0]]
#                         else:
#                             raise TypeError(str(p.lineno(2)) + ": Cannot do operation " + str(p[2]) + " on " + str(p[1].type_list[0]) + " and " + str(p[3].type_list[0]))
#                     else:
#                         raise TypeError(str(p.lineno(2)) + ": Cannot truncate " + str(p[1].code[-1][-1]) + " to int")
#                 elif len(p[3].code) > 0 and type(p[3].code[-1][-1]) == float:
#                     if p[1].type_list[0] == "float64":
#                         if p[2] == "+" or p[2] == "-" or p[2] == "/" or p[2] == "*":
#                             p[0].place_list = [temp_v]
#                             p[0].code += [["float_" + p[2], temp_v, p[1].place_list[0], p[3].place_list[0]]]
#                             p[0].type_list = [p[1].type_list[0]]
#                         elif p[2] == "<" or p[2] == ">" or p[2] == "<=" or p[2] == ">=" or p[2] == "==" or p[2] == "!=":
#                             p[0].place_list = [temp_v]
#                             p[0].code += [["float_" + p[2], temp_v, p[1].place_list[0], p[3].place_list[0]]]
#                             p[0].type_list = ["bool"]
#                         else:
#                             raise TypeError(str(p.lineno(2)) + ": Cannot do operation " + str(p[2]) + " on float literals")
#                     elif p[3].code[-1][-1] == int(p[3].code[-1][-1]):
#                         p[3].code[-1][-1] = int(p[3].code[-1][-1])
#                         if "int" in p[1].type_list[0] or p[1].type_list[0] == "byte":
#                             p[0].place_list = [temp_v]
#                             p[0].code += [["int_" + p[2], temp_v, p[1].place_list[0], p[3].place_list[0]]]
#                             if p[2] == "<" or p[2] == ">" or p[2] == "<=" or p[2] == ">=" or p[2] == "==" or p[2] == "!=":
#                                 p[0].type_list = ["bool"]
#                             else:
#                                 p[0].type_list = [p[1].type_list[0]]
#                         else:
#                             raise TypeError(str(p.lineno(2)) + ": Cannot do operation " + str(p[2]) + " on " + str(p[1].type_list[0]) + " and " + str(p[3].type_list[0]))
#                     else:
#                         raise TypeError(str(p.lineno(2)) + ": Cannot truncate " + str(p[3].code[-1][-1]) + " to int")
#                 elif "int" in p[1].type_list[0] and ("byte" == p[3].type_list[0] or p[3].type_list[0].startswith("uint")) and (p[2] == "<<" or p[2] == ">>"):
#                     p[0].place_list = [temp_v]
#                     p[0].code += [["int_" + p[2], temp_v, p[1].place_list[0], p[3].place_list[0]]]
#                     p[0].type_list = [p[1].type_list[0]]
#                 else:
#                     raise TypeError(str(p.lineno(2)) + ": Cannot do operation " + str(p[2]) + " on " + str(p[1].type_list[0]) + " and " + str(p[3].type_list[0]))
#
# def p_unary_expr(p):
#     '''unary_expr   : primary_expr
#                     | unary_op unary_expr'''
#     if len(p) == 2:
#         p[0] = p[1]
#         if "identifier" == p[0].type_list[0]:
#             info = find_info(p[0].id_list[0], p.lineno(1))
#             if info["is_var"]:
#                 p[0].type_list = [info["type"]]
#                 p[0].place_list = [info["temp"]]
#                 p[0].extra["size"] = info["size"]
#             else:
#                 raise NameError(str(p.lineno(1)) + ": Variable " + str(p[0].id_list[0]) + " not defined")
#         elif p[0].extra.get("it_is_a_pointer"):
#             temp_v = new_temp()
#             p[0].code += [["(load)", temp_v, p[0].place_list[0]]]
#             #Hritvik these 2 statemnts should be written in the following order
#             p[0].extra["size"] = p[0].type_list[0][2]
#             p[0].type_list = [p[0].type_list[0][1]]
#             p[0].place_list = [temp_v]
#     else:
#         if p[1] == "!":
#             if "int" in p[2].type_list[0] or p[2].type_list[0] == "bool" or p[2].type_list[0] == "byte" :
#                 p[0] = p[2]
#                 temp_v = new_temp()
#                 p[0].code += [["!", temp_v, p[2].place_list[0]]]
#                 p[0].place_list = [temp_v]
#             else:
#                 raise TypeError(str(p.lineno(1)) + ": Type Mismatch with unary operator" + str(p[1]))
#
#         if p[1] == "+":
#             if "int" in p[2].type_list[0] or "float" in p[2].type_list[0] :
#                 p[0] = p[2]
#             else:
#                 raise TypeError(str(p.line(1)) + ": Type Mismatch with unary operator" + str(p[1]))
#
#         if p[1] == "-":
#             if "int" in p[2].type_list[0] or "float" in p[2].type_list[0] :
#                 p[0] = p[2]
#                 if "int" in p[2].type_list[0]:
#                     type_v = "int"
#                 else:
#                     type_v = "float"
#                 temp_v1 = new_temp()
#                 temp_v2 = new_temp()
#                 p[0].code += [["=", temp_v1, "0"]]
#                 p[0].code += [[type_v + "_" + p[1], temp_v2, temp_v1, p[2].place_list[0]]]
#                 p[0].place_list = [temp_v2]
#             else:
#                 raise TypeError(str(p.lineno(1)) + ": Type Mismatch with unary operator" + str(p[1]))
#
#         if p[1] == "*":
#             # print("in_star", p[2].type_list)
#             if p[2].type_list[0][0] == "pointer":
#                 p[0] = p[2]
#                 temp_v = new_temp()
#                 p[0].code += [["(load)", temp_v, p[2].place_list[0]]]
#                 #Hritvik in this same order
#                 p[0].extra["size"] = p[2].type_list[0][2]
#                 p[0].type_list = [p[2].type_list[0][1]]
#                 p[0].place_list = [temp_v]
#             else:
#                 raise TypeError(str(p.lineno(1)) + ": Type Mismatch with unary operator" + str(p[1]))
#
#         if p[1] == "&":
#             p[0] = p[2]
#             temp_v = new_temp()
#             p[0].code += [["(addr)", temp_v, p[2].place_list[0]]]
#             p[0].type_list = [["pointer", p[2].type_list[0], p[2].extra["size"]]]
#             p[0].place_list = [temp_v]
#             p[0].extra["size"] = 4
#
# def p_unary_op(p):
#     '''unary_op : ADD
#                 | SUB
#                 | MUL
#                 | AND
#                 | NOT'''
#     #TODO: can add more here
#     p[0] = p[1]
#
# def p_expression_opt(p):
#     '''expression_opt   : expression
#                         | epsilon'''
#     p[0] = p[1]
#
# def p_expression_list(p):
#     '''expression_list  : expression expression_rep'''
#     p[0] = p[1]
#     p[0].place_list += p[2].place_list
#     p[0].type_list += p[2].type_list
#     p[0].code = [p[0].code] + p[2].code
#     p[0].extra["size"] = [p[0].extra["size"]] + p[2].extra["size"]
#
# def p_expression_rep(p):
#     '''expression_rep   : COMMA expression expression_rep
#                         | epsilon'''
#     if len(p) == 2:
#         p[0] = p[1]
#         p[0].extra["size"] = []
#     else:
#         p[0] = p[2]
#         p[0].place_list += p[3].place_list
#         p[0].type_list += p[3].type_list
#         p[0].code = [p[0].code] + p[3].code
#         p[0].extra["size"] = [p[0].extra["size"]] + p[3].extra["size"]
#
# def p_identifier_list(p):
#     '''identifier_list  : identifier_list COMMA IDENT
#                         | IDENT'''
#     if len(p) == 2:
#         p[0] = Node()
#         p[0].id_list = [p[1]]
#     else:
#         p[0] = p[1]
#         p[0].id_list += [p[3]]
#
# def p_statement_list(p):
#     '''statement_list   : statement_rep'''
#     p[0] = p[1]
#
# def p_statement_rep(p):
#     '''statement_rep    : statement semicolon_opt statement_rep
#                         | epsilon'''
#     if len(p) == 4:
#         p[0] = Node()
#         p[0].code = p[1].code + p[3].code
#     else:
#         p[0] = p[1]
# def p_block(p):
#     '''block    : LBRACE statement_list RBRACE'''
#     # # p[0] = mytuple(["block"] + p[1:])
#     # Note that new label must be made by the production calling the block
#     # If the block wants to use the label of the current scope then it should be able to fetch it from symbol table (extra dict())
#     p[0] = p[2]
#
# def p_conversion(p):
#     '''conversion   : TYPECAST type_token LPAREN expression RPAREN'''
#     # check prakhar TYPECAST is added
#     # check prakhar comma is removed
#     p[0] = p[4]
#     p[0].extra["conversion"] = p[2].type_list[0]
#
#     if "int" in p[2].type_list[0] and "int" in p[4].type_list[0]:
#         temp_v = new_temp()
#         type = "(" + p[2].type_list[0] + ")"
#         p[0].code += [["typecast", temp_v, type, p[4].place_list[0]]]
#         p[0].place_list = [temp_v]
#         p[0].type_list = [p[2].type_list[0]]
#
#     if ("int" in p[2].type_list[0] or "float" in p[2].type_list[0]) and "float" in p[4].type_list[0]:
#         temp_v = new_temp()
#         type = "(" + p[2].type_list[0] + ")"
#         p[0].code += [["typecast", temp_v, type, p[4].place_list[0]]]
#         p[0].place_list = [temp_v]
#         p[0].type_list = [p[2].type_list[0]]
#
#     if "float" in p[2].type_list[0] and "int" in p[4].type_list[0]:
#         temp_v = new_temp()
#         type = "(" + p[2].type_list[0] + ")"
#         p[0].code += [["typecast", temp_v, type, p[4].place_list[0]]]
#         p[0].place_list = [temp_v]
#         p[0].type_list = [p[2].type_list[0]]
#
#
# def p_comma_opt(p):
#     '''comma_opt    : COMMA
#                     | epsilon'''
#     p[0] = p[1]
#
# ################################################# SACRED END ##########################################
#</editor-fold> SACRED END #########################


######################################################
######################################################

# Source : https ://docs.oracle.com/javase/specs/jls/se8/html/jls-19.html

def mytuple(l):
    # print(l)
    return tuple(l)


def p_empty(p):
    '''empty : '''
    p[0] = "epsilon"

#<editor-fold Section 3 Literals #########################
################################################
# SECTION 3 :
################################################

#*
def p_literal(p):
    '''Literal : BOOL_LIT
        | NULL_LIT
        | DECIMAL_LIT
        | HEX_LIT
        | OCTAL_LIT
        | BINARY_LIT
        | FLOAT_DEC_LIT
        | FLOAT_HEX_LIT
        | STRING_LIT
        | CHAR_LIT'''
    # # p[0] = mytuple(["Literal"]+p[1:])

    if p[1] == "true" or p[1] == "false":   # bool
        temp_v = new_temp()
        p[0] = Node()
        p[0].place_list = [temp_v]
        p[0].type_list = ["boolean"]
        p[0].extra["size"] = type_dict["boolean"]["size"]
        if p[1] == "true":
            p[0].code = [["=", temp_v, True], ["goto", temp_v]]
            p[0].extra["true_list"] = [temp_v]
            p[0].extra["false_list"] = []
        else:
            p[0].code = [["=", temp_v, False], ["goto", temp_v]]
            p[0].extra["true_list"] = []
            p[0].extra["false_list"] = [temp_v]
    elif p[1] == "null":                    # null
        temp_v = new_temp()
        p[0] = Node()
        p[0].place_list = [temp_v]
        p[0].code = [["=", temp_v, p[1]]]
        p[0].type_list = ["null"]
        p[0].extra["size"] = 4
    elif type(p[1]) == int:                 # int
        temp_v = new_temp()
        p[0] = Node()
        p[0].place_list = [temp_v]
        p[0].code = [["=", temp_v, p[1]]]
        p[0].type_list = ["int"]
        p[0].extra["size"] = 4
    elif type(p[1]) == float:               # float
        temp_v = new_temp()
        p[0] = Node()
        p[0].place_list = [temp_v]
        p[0].code = [["=", temp_v, p[1]]]
        p[0].type_list = ["float"]
        p[0].extra["size"] = 4
    elif type(p[1]) == str and p[1][0]=='"':    # string
        temp_v = new_temp()
        p[0] = Node()
        p[0].place_list = [temp_v]
        p[0].code = [["=", temp_v, "\"" + p[1][1:-1] + "\""]]
        p[0].type_list = [["string", len(p[1][1:-1])]]
        p[0].extra["size"] = sizeof["char"]*len(p[1][1:-1])
    elif type(p[1]) == str and p[1][0]=='\'':    # char
        temp_v = new_temp()
        p[0] = Node()
        p[0].place_list = [temp_v]
        p[0].code = [["=", temp_v, p[1]]]
        p[0].type_list = ["char"]
        p[0].extra["size"] = sizeof["char"]
    # p[0].extra["tuple"] = p[1]

#</editor-fold>############################################

#<editor-fold Section 9 : Interfaces #########################
################################################
# SECTION 9 : Interfaces
################################################

#*
def p_InterfaceDeclaration(p):
    '''InterfaceDeclaration : NormalInterfaceDeclaration
                           | AnnotationTypeDeclaration'''
    # p[0] = mytuple(["InterfaceDeclaration"]+p[1:])
    p[0] = p[1]


def p_NormalInterfaceDeclaration(p):
    '''NormalInterfaceDeclaration :  CommonModifierS INTERFACE IDENT TypeParameters ExtendsInterfaces InterfaceBody
                             | CommonModifierS INTERFACE IDENT TypeParameters InterfaceBody
                              | CommonModifierS INTERFACE IDENT ExtendsInterfaces InterfaceBody
                               | CommonModifierS INTERFACE IDENT InterfaceBody
                                | INTERFACE IDENT TypeParameters ExtendsInterfaces InterfaceBody
                            | INTERFACE IDENT TypeParameters InterfaceBody
                             | INTERFACE IDENT ExtendsInterfaces InterfaceBody
                              | INTERFACE IDENT InterfaceBody
    '''
    # p[0] = mytuple(["NormalInterfaceDeclaration"]+p[1:])


# def p_InterfaceModifierS(p):
#     '''InterfaceModifierS : Annotation InterfaceModifierS
#                           | PUBLIC InterfaceModifierS
#                           | PROTECTED InterfaceModifierS
#                           | PRIVATE InterfaceModifierS
#                           | ABSTRACT InterfaceModifierS
#                           | STATIC InterfaceModifierS
#                           | STRICTFP InterfaceModifierS
#                           | empty'''
#     # p[0] = mytuple(["InterfaceModifierS"]+p[1 :])

# def p_InterfaceModifier(p):
#     '''InterfaceModifier :
#                          | ABSTRACT
#                          | STATIC
#                          | STRICTFP'''
#     # p[0] = mytuple(["InterfaceModifier"]+p[1 :])

#*
def p_ExtendsInterfaces(p):
    '''ExtendsInterfaces : EXTENDS InterfaceTypeList'''
    # p[0] = mytuple(["ExtendsInterfaces"]+p[1:])
    p[0] = p[2]

#*
def p_InterfaceBody(p):
    '''InterfaceBody : LBRACE InterfaceMemberDeclarationS RBRACE '''
    # p[0] = mytuple(["InterfaceBody"]+p[1:])
    p[0] = p[2]

#*
def p_InterfaceMemberDeclarationS(p):
    ''' InterfaceMemberDeclarationS : InterfaceMemberDeclarationS InterfaceMemberDeclaration
                                    | InterfaceMemberDeclarationS SEMICOLON
                                    | empty '''
    # p[0] = mytuple(["InterfaceMemberDeclarationS"]+p[1:])
    if len(p) == 3 and p[2] == ";":
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = p[1]
        p[0].id_list += p[2].id_list
        p[0].type_list += p[2].type_list
        p[0].place_list += p[2].place_list
    else:
        p[0] = Node()

#*
def p_InterfaceMemberDeclaration(p):
    '''InterfaceMemberDeclaration : ConstantDeclaration
                                 | InterfaceMethodDeclaration
                                 | ClassDeclaration
                                 | InterfaceDeclaration'''
    # p[0] = mytuple(["InterfaceMemberDeclaration"]+p[1:])
    p[0] = p[1]

def p_ConstantDeclaration(p):
    '''ConstantDeclaration : CommonModifierS UnannType VariableDeclaratorList SEMICOLON
                            | CommonModifierS NumericType VariableDeclaratorList SEMICOLON
                            | CommonModifierS BOOLEAN VariableDeclaratorList SEMICOLON
                            | CommonModifierS IDENT VariableDeclaratorList SEMICOLON
                            | UnannType VariableDeclaratorList SEMICOLON
                            | NumericType VariableDeclaratorList SEMICOLON
                            | BOOLEAN VariableDeclaratorList SEMICOLON
                            | IDENT VariableDeclaratorList SEMICOLON
                            | CommonModifierS UnannType IDENT SEMICOLON
                            | CommonModifierS NumericType IDENT SEMICOLON
                            | CommonModifierS BOOLEAN IDENT SEMICOLON
                            | CommonModifierS IDENT IDENT SEMICOLON
                            | UnannType IDENT SEMICOLON
                            | NumericType IDENT SEMICOLON
                            | BOOLEAN IDENT SEMICOLON
                            | IDENT IDENT SEMICOLON'''
    # p[0] = mytuple(["ConstantDeclaration"]+p[1:])

# def p_ConstantModifierS(p):
#     '''ConstantModifierS : ConstantModifier ConstantModifierS
#                         | empty '''
#     # p[0] = mytuple(["ConstantModifierS"]+p[1 :])

# def p_ConstantModifier(p):
#     '''ConstantModifier : Annotation
#                        | PUBLIC
#                        | STATIC
#                        | FINAL'''
#     # p[0] = mytuple(["ConstantModifier"]+p[1 :])


def p_InterfaceMethodDeclaration(p):
    '''InterfaceMethodDeclaration : CommonModifierS MethodHeader MethodBody
                                | DEFAULT MethodHeader MethodBody
                                |  MethodHeader MethodBody
                                | CommonModifierS MethodHeader SEMICOLON
                                | DEFAULT MethodHeader SEMICOLON
                                |  MethodHeader SEMICOLON'''
    # p[0] = mytuple(["InterfaceMethodDeclaration"]+p[1:])

# def p_InterfaceMethodModifierS(p):
#     '''InterfaceMethodModifierS : InterfaceMethodModifier InterfaceMethodModifierS
#                                | empty'''
#     # p[0] = mytuple(["InterfaceMethodModifierS"]+p[1 :])

# def p_InterfaceMethodModifier(p):
#     '''InterfaceMethodModifier :  Annotation
#                                 | PUBLIC
#                                 | ABSTRACT
#                                 | DEFAULT
#                                 | STATIC
#                                 | STRICTFP'''
#     # p[0] = mytuple(["InterfaceMethodModifier"]+p[1 :])


def p_AnnotationTypeDeclaration(p):
    '''AnnotationTypeDeclaration : CommonModifierS ATRATE INTERFACE IDENT AnnotationTypeBody
                            | ATRATE INTERFACE IDENT AnnotationTypeBody'''
    # p[0] = mytuple(["AnnotationTypeDeclaration"]+p[1:])

# def p_InterfaceModifierS(p):
#     '''InterfaceModifierS : InterfaceModifier InterfaceModifierS
#                          | empty'''
#     # p[0] = mytuple(["InterfaceModifierS"]+p[1 :])

#*
def p_AnnotationTypeBody(p):
    '''AnnotationTypeBody :  LBRACE AnnotationTypeMemberDeclarationS RBRACE'''
    # p[0] = mytuple(["AnnotationTypeBody"]+p[1:])
    p[0] = p[2]

#*
def p_AnnotationTypeMemberDeclarationS(p):
    '''AnnotationTypeMemberDeclarationS : AnnotationTypeMemberDeclarationS AnnotationTypeMemberDeclaration
                        | AnnotationTypeMemberDeclarationS SEMICOLON
                         | empty'''
    # p[0] = mytuple(["AnnotationTypeMemberDeclarationS"]+p[1:])
    if len(p) == 3 and p[2] == ";":
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = p[1]
        p[0].id_list += p[2].id_list
        p[0].type_list += p[2].type_list
        p[0].place_list += p[2].place_list
    else:
        p[0] = Node()

#*
def p_AnnotationTypeMemberDeclaration(p):
    '''AnnotationTypeMemberDeclaration : AnnotationTypeElementDeclaration
                                        | ConstantDeclaration
                                        | ClassDeclaration
                                        | InterfaceDeclaration'''
    # p[0] = mytuple(["AnnotationTypeMemberDeclaration"]+p[1:])
    p[0] = p[1]

def p_AnnotationTypeElementDeclaration(p):
    '''AnnotationTypeElementDeclaration :  CommonModifierS UnannType IDENT LPAREN RPAREN Dims DefaultValue SEMICOLON
                                    | CommonModifierS NumericType IDENT LPAREN RPAREN Dims DefaultValue SEMICOLON
                                    | CommonModifierS BOOLEAN IDENT LPAREN RPAREN Dims DefaultValue SEMICOLON
                                    |  CommonModifierS IDENT IDENT LPAREN RPAREN Dims DefaultValue SEMICOLON
                                    |    CommonModifierS UnannType IDENT LPAREN RPAREN  DefaultValue SEMICOLON
                                    |    CommonModifierS NumericType IDENT LPAREN RPAREN  DefaultValue SEMICOLON
                                    |    CommonModifierS BOOLEAN IDENT LPAREN RPAREN  DefaultValue SEMICOLON
                                    |  CommonModifierS IDENT IDENT LPAREN RPAREN  DefaultValue SEMICOLON
                                    |    CommonModifierS UnannType IDENT LPAREN RPAREN Dims  SEMICOLON
                                    |    CommonModifierS NumericType IDENT LPAREN RPAREN Dims  SEMICOLON
                                    |    CommonModifierS BOOLEAN IDENT LPAREN RPAREN Dims  SEMICOLON
                                    |  CommonModifierS IDENT IDENT LPAREN RPAREN Dims  SEMICOLON
                                    |    CommonModifierS UnannType IDENT LPAREN RPAREN SEMICOLON
                                    |    CommonModifierS NumericType IDENT LPAREN RPAREN SEMICOLON
                                    |    CommonModifierS BOOLEAN IDENT LPAREN RPAREN SEMICOLON
                                    |  CommonModifierS IDENT IDENT LPAREN RPAREN SEMICOLON
                                    | UnannType IDENT LPAREN RPAREN Dims DefaultValue SEMICOLON
                                    | NumericType IDENT LPAREN RPAREN Dims DefaultValue SEMICOLON
                                    | BOOLEAN IDENT LPAREN RPAREN Dims DefaultValue SEMICOLON
                                        |  IDENT IDENT LPAREN RPAREN Dims DefaultValue SEMICOLON
                                    |    UnannType IDENT LPAREN RPAREN  DefaultValue SEMICOLON
                                    |    NumericType IDENT LPAREN RPAREN  DefaultValue SEMICOLON
                                    |    BOOLEAN IDENT LPAREN RPAREN  DefaultValue SEMICOLON
                                    |  IDENT IDENT LPAREN RPAREN  DefaultValue SEMICOLON
                                    |    UnannType IDENT LPAREN RPAREN Dims  SEMICOLON
                                    |    NumericType IDENT LPAREN RPAREN Dims  SEMICOLON
                                    |    BOOLEAN IDENT LPAREN RPAREN Dims  SEMICOLON
                                    |  IDENT IDENT LPAREN RPAREN Dims  SEMICOLON
                                    |    UnannType IDENT LPAREN RPAREN SEMICOLON
                                    |    NumericType IDENT LPAREN RPAREN SEMICOLON
                                    |    BOOLEAN IDENT LPAREN RPAREN SEMICOLON
                                    |  IDENT IDENT LPAREN RPAREN SEMICOLON'''
    # p[0] = mytuple(["AnnotationTypeElementDeclaration"]+p[1:])

# def p_AnnotationTypeElementModifierS(p):
#     '''AnnotationTypeElementModifierS : AnnotationTypeElementModifier AnnotationTypeElementModifierS
#                                       | empty'''
#     # p[0] = mytuple(["AnnotationTypeElementModifierS"]+p[1 :])

# def p_AnnotationTypeElementModifier(p):
#     '''AnnotationTypeElementModifier : Annotation
#                                      | PUBLIC
#                                      | ABSTRACT'''
#     # p[0] = mytuple(["AnnotationTypeElementModifier"]+p[1 :])

#*
def p_DefaultValue(p):
    '''DefaultValue : DEFAULT ElementValue
                        | DEFAULT IDENT'''
    # p[0] = mytuple(["DefaultValue"]+p[1:])
    if type(p[2]) == str:
        p[0] = Node()
        p[0].id_list = [p[2]]
        p[0].type_list = ["identifier"]
    else:
        p[0] = p[2]

#*
def p_Annotation(p):
    '''Annotation : NormalAnnotation
                  | MarkerAnnotation
                  | SingleElementAnnotation'''
    # p[0] = mytuple(["Annotation"]+p[1:])
    p[0] = p[1]


def p_NormalAnnotation(p):
    '''NormalAnnotation : ATRATE IDENT LPAREN ElementValuePairList RPAREN
                        | ATRATE IDENT LPAREN  RPAREN
                        | ATRATE IDENT CommonName LPAREN ElementValuePairList RPAREN
                        | ATRATE IDENT CommonName LPAREN  RPAREN '''
    # p[0] = mytuple(["NormalAnnotation"]+p[1:])

#*
def p_ElementValuePairList(p):
    '''ElementValuePairList : ElementValuePair COMMAElementValuePairS'''
    # p[0] = mytuple(["ElementValuePairList"]+p[1:])
    p[0] = p[1]
    p[0].id_list += p[2].id_list
    p[0].type_list += p[2].type_list
    p[0].place_list += p[2].place_list

#*
def p_COMMAElementValuePairS(p):
    '''COMMAElementValuePairS : COMMAElementValuePairS COMMA ElementValuePair
                              | empty'''
    # p[0] = mytuple(["COMMAElementValuePairS"]+p[1:])
    if len(p) == 4:
        p[0] = p[1]
        p[0].id_list += p[3].id_list
        p[0].type_list += p[3].type_list
        p[0].place_list += p[3].place_list

    else:
        p[0] = Node()

#* DOUBT verify
def p_ElementValuePair(p):
    '''ElementValuePair : IDENT ASSIGN ElementValue
                        | IDENT ASSIGN IDENT '''
    # p[0] = mytuple(["ElementValuePair"]+p[1:])

    p[0] = Node()
    p[0].id_list = [p[1]]
    p[0].type_list = ["identifier"]

    if type(p[3]) == str:
        p[3] = Node()
        p[3].id_list = [p[3]]
        p[3].type_list = ["identifier"]

    expr_type_list_key = p[0].type_list
    expr_type_list_val = p[3].type_list
    expr_place_list_key = p[0].place_list
    expr_place_list_val = p[3].place_list

    for i in range(len(expr_type_list_key)):
        newtype = higher(expr_type_list_key[i], expr_type_list_val[i])

        if newtype == -1 or (newtype == expr_type_list_val[i] and not (expr_type_list_key[i] == newtype or expr_type_list_key[i] == "identifier")):   # downcasting not allowed in Java
            raise TypeError(str(p.lineno(1)) + ": Type mismatch for identifier " + str(expr_place_list_key[i]))
        else:
            new_temp_var = new_temp()
            p[0].code += [["=", new_temp_var, "convert_to_"+newtype+"("+str(expr_place_list_val[i])+")"]]
            p[0].code += [["=", expr_place_list_key[i], new_temp_var]]

        p[0].type_list[i] = newtype


#*
def p_ElementValue(p):
    '''ElementValue : ConditionalExpression
                    | ElementValueArrayInitializer
                    | Annotation '''
    # p[0] = mytuple(["ElementValue"]+p[1:])
    p[0] = p[1]


#* DOUBT unfinished
def p_ElementValueArrayInitializer(p):
    '''ElementValueArrayInitializer : LBRACE ElementValueList COMMA RBRACE
    | LBRACE ElementValueList  RBRACE
    | LBRACE IDENT COMMA RBRACE
    | LBRACE IDENT  RBRACE
    | LBRACE  COMMA RBRACE
    | LBRACE   RBRACE'''
    # p[0] = mytuple(["ElementValueArrayInitializer"]+p[1:])
    p[0] = Node()

#*
def p_ElementValueList(p):
    '''ElementValueList : ElementValue  COMMAElementValueS
                    |  IDENT  COMMAElementValueS
                    | ElementValue'''
    # p[0] = mytuple(["ElementValueList"]+p[1:])
    if len(p) == 2:
        p[0] = p[1]
    else:
        if type(p[1]) == str:
            p[0] = p[2]
            p[0].id_list.insert(0, p[1])
            p[0].type_list.insert(0, "identifier")
        else:
            p[0] = p[1]
            p[0].id_list += p[2].id_list
            p[0].type_list += p[2].type_list
            p[0].place_list += p[2].place_list

#*
def p_COMMAElementValueS(p):
    '''COMMAElementValueS : COMMAElementValueS COMMA ElementValue
                    | COMMAElementValueS COMMA IDENT
                    | COMMA ElementValue
                    | COMMA IDENT'''
    # p[0] = mytuple(["COMMAElementValueS"]+p[1:])
    if len(p) == 4:
        p[0] = p[1]
    else:
        p[0] = Node()

    if type(p[len(p)-1]) == str:
        p[0].id_list.append(p[len(p)-1])
        p[0].type_list.append("identifier")
    else:
        p[0].id_list += p[len(p)-1].id_list
        p[0].type_list += p[len(p)-1].type_list
        p[0].place_list += p[len(p)-1].place_list

#*
def p_MarkerAnnotation(p):
    '''MarkerAnnotation : ATRATE IDENT
                | ATRATE IDENT CommonName'''
    # p[0] = mytuple(["MarkerAnnotation"]+p[1:])
    if len(p) == 3:
        p[0] = Node()
        p[0].id_list = [p[2]]
        p[0].type_list = ["identifier"]
    else:
        p[0] = p[3]
        p[0].id_list.append(p[2])
        p[0].type_list.append("identifier")

def p_SingleElementAnnotation(p):
    '''SingleElementAnnotation : ATRATE IDENT LPAREN ElementValue RPAREN
                        | ATRATE IDENT LPAREN IDENT RPAREN
                        | ATRATE IDENT CommonName LPAREN ElementValue RPAREN
                        | ATRATE IDENT CommonName LPAREN IDENT RPAREN'''
    # p[0] = mytuple(["SingleElementAnnotation"]+p[1:])

#</editor-fold>############################################

#<editor-fold Section 10 : Arrays #########################
################################################
# Section 10 : Arrays
################################################


def p_ArrayInitializer(p):
    '''ArrayInitializer : LBRACE VariableInitializerList COMMA RBRACE
    | LBRACE VariableInitializerList RBRACE
    | LBRACE COMMA RBRACE
    | LBRACE RBRACE '''
    # print("In arrrayIntializer")
    # print(p[1:])
    # p[0] = mytuple(["ArrayInitializer"]+p[1:])


# def p_lbrace(p):
#     '''LBRACE : LBRACE'''
#     # p[0] = mytuple(["LBRACE"]+p[1:])


# def p_rbrace(p):
#     '''RBRACE : RBRACE'''
#     # p[0] = mytuple(["RBRACE"]+p[1:])

#*
def p_VariableInitializerList(p):
    '''VariableInitializerList : VariableInitializer COMMAVariableInitializerS
                                | VariableInitializer '''
    # p[0] = mytuple(["VariableInitializerList"]+p[1:])
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1]
        p[0].id_list += p[2].id_list
        p[0].place_list += p[2].place_list
        p[0].type_list += p[2].type_list

#*
def p_COMMAVariableInitializerS(p):
    '''COMMAVariableInitializerS : COMMAVariableInitializerS COMMA VariableInitializer
                                 | COMMA VariableInitializer'''
    # p[0] = mytuple(["COMMAVariableInitializerS"]+p[1:])
    if len(p)==3:
        p[0] = p[2]
    else:
        p[0] = p[1]
        p[0].id_list += p[3].id_list
        p[0].place_list += p[3].place_list
        p[0].type_list += p[3].type_list

#</editor-fold>############################################

#<editor-fold Section 15 : Expressions #########################
################################################
# Section 15 : Expressions
################################################

#*
def p_Primary(p):
    '''Primary : PrimaryNoNewArray
              | ArrayCreationExpression '''
    # p[0] = mytuple(["Primary"]+p[1:])
    p[0] = p[1]

#* DOUBT 'this' ka kya kare?
def p_PrimaryNoNewArray(p):
    '''PrimaryNoNewArray : Literal
                        | ClassLiteral
                        | THIS
                        | IDENT PERIOD THIS
                        | IDENT CommonName PERIOD THIS
                        | LPAREN IDENT RPAREN
                        | LPAREN Expression RPAREN
                        | ClassInstanceCreationExpression
                        | FieldAccess
                        | ArrayAccess
                        | MethodInvocation
                        | MethodReference'''
    # p[0] = mytuple(["PrimaryNoNewArray"]+p[1:])
    # Remember Literal is a token
    if len(p) == 2 and type(p[1])!=str:
        p[0] = p[1]
    elif len(p) == 2:
        p[0] = Node()
    elif p[1] == "(":
        if type(p[2]) == str:
            p[0] = Node()
            p[0].id_list = [p[2]]
            p[0].type_list = ["identifier"]
        else:
            p[0] = p[2]
    elif len(p) == 4:
        p[0] = Node()
        p[0].id_list = [p[1]]
        p[0].type_list = ["identifier"]
    elif len(p) == 5:
        p[0] = p[2]
        p[0].id_list.insert(0, p[1])
        p[0].type_list.insert(0, "identifier")

#* DOUBT else waali condition
def p_ClassLiteral(p):
    '''ClassLiteral : IDENT LBRACKRBRACKS PERIOD CLASS
                    | IDENT CommonName LBRACKRBRACKS PERIOD CLASS
                   | NumericType LBRACKRBRACKS PERIOD CLASS
                   | BOOLEAN LBRACKRBRACKS PERIOD CLASS
                   | VOID PERIOD CLASS '''
    # p[0] = mytuple(["ClassLiteral"]+p[1:])
    p[0] = Node()

    if len(p) == 4:
        p[0].type_list = [["class", "void"]]
    elif len(p) == 5:
        if type(p[1]) == str and (p[1]=="true" or p[1]=="false"):
            if p[2].extra["depth"]==0:
                p[0].type_list = [["class", "bool"]]
            else:
                p[0].type_list = [["class", ["array", "bool", p[2].extra["depth"], []]]]
        elif type(p[1]) == str:
            if p[2].extra["depth"]==0:
                p[0].type_list = [["class", "identifier"]]
                p[0].id_list = [p[1]]
            else:
                p[0].type_list = [["class", ["array", "identifier", p[2].extra["depth"], []]]]
                p[0].id_list = [p[1]]
    else:
        p[0] = p[2]
        # p[0].id_list.insert(0, p[1])
        p[0].id_list = [p[0].id_list[-1]]   # storing the identifier that corresponds to the class type only. makes it easier to access using [0] or [-1], and also maintains one-one correspondence in type_list and id_list
        if p[3].extra["depth"]==0:
            p[0].type_list = [["class", "identifier"]]
        else:
            p[0].type_list = [["class", ["array", "identifier", p[3].extra["depth"], []]]]

#*
def p_LBRACKRBRACKS(p):
    '''LBRACKRBRACKS : LBRACKRBRACKS LBRACK RBRACK
                    | empty'''
    # p[0] = mytuple(["LBRACKRBRACKS"]+p[1:])
    if len(p)==4:
        p[0] = p[1]
        p[0].extra["depth"] += 1
    else:
        p[0] = Node()
        p[0].extra["depth"] = 0


def p_ClassInstanceCreationExpression(p):
    '''ClassInstanceCreationExpression : UnqualifiedClassInstanceCreationExpression
                                      | IDENT CommonName PERIOD UnqualifiedClassInstanceCreationExpression
                                      | IDENT PERIOD UnqualifiedClassInstanceCreationExpression
                                      | Primary PERIOD UnqualifiedClassInstanceCreationExpression'''
    # p[0] = mytuple(["ClassInstanceCreationExpression"]+p[1:])


def p_UnqualifiedClassInstanceCreationExpression(p):
    '''UnqualifiedClassInstanceCreationExpression : NEW TypeArguments ClassOrInterfaceTypeToInstantiate LPAREN ArgumentList RPAREN ClassBody
    | NEW TypeArguments ClassOrInterfaceTypeToInstantiate LPAREN  RPAREN ClassBody
    | NEW TypeArguments ClassOrInterfaceTypeToInstantiate LPAREN ArgumentList RPAREN
    | NEW TypeArguments ClassOrInterfaceTypeToInstantiate LPAREN  RPAREN
    | NEW ClassOrInterfaceTypeToInstantiate LPAREN ArgumentList RPAREN ClassBody
    | NEW ClassOrInterfaceTypeToInstantiate LPAREN  RPAREN ClassBody
    | NEW ClassOrInterfaceTypeToInstantiate LPAREN ArgumentList RPAREN
    | NEW ClassOrInterfaceTypeToInstantiate LPAREN  RPAREN
    | NEW TypeArguments IDENT LPAREN ArgumentList RPAREN ClassBody
    | NEW TypeArguments IDENT LPAREN  RPAREN ClassBody
    | NEW TypeArguments IDENT LPAREN ArgumentList RPAREN
    | NEW TypeArguments IDENT LPAREN  RPAREN
    | NEW IDENT LPAREN ArgumentList RPAREN ClassBody
    | NEW IDENT LPAREN  RPAREN ClassBody
    | NEW IDENT LPAREN ArgumentList RPAREN
    | NEW IDENT LPAREN  RPAREN'''
    # p[0] = mytuple(["UnqualifiedClassInstanceCreationExpression"]+p[1:])

def p_ClassOrInterfaceTypeToInstantiate(p):
    '''ClassOrInterfaceTypeToInstantiate : AnnotationS IDENT PERIODAnnotationSIDENTS TypeArgumentsOrDiamond
                                        | AnnotationS IDENT PERIODAnnotationSIDENTS
                                         |  IDENT PERIODAnnotationSIDENTS
                                         |  IDENT PERIODAnnotationSIDENTS TypeArgumentsOrDiamond
                                         | AnnotationS IDENT TypeArgumentsOrDiamond
                                         | AnnotationS IDENT
                                         |  IDENT TypeArgumentsOrDiamond'''
    # p[0] = mytuple(["ClassOrInterfaceTypeToInstantiate"]+p[1:])


def p_AnnotationS(p):
    '''AnnotationS : AnnotationS Annotation
                  | Annotation'''
    # p[0] = mytuple(["AnnotationS"]+p[1:])

def p_PERIODAnnotationSIDENTS(p):
    '''PERIODAnnotationSIDENTS : PERIODAnnotationSIDENTS PERIOD AnnotationS IDENT
                                | PERIODAnnotationSIDENTS PERIOD IDENT
                                | PERIOD AnnotationS IDENT
                                | PERIOD IDENT'''
    # p[0] = mytuple(["PERIODAnnotationSIDENTS"]+p[1:])

# TODO fix function name of Zoo and ...S(p); also in general
# TODO fix ''' in next line


def p_TypeArgumentsOrDiamond(p):
    '''TypeArgumentsOrDiamond : TypeArguments
                             | LSS GTR'''
    # print("I am TypeArgumentsOrDiamond!!!!")
    # print("\n"*20)
    # p[0] = mytuple(["TypeArgumentsOrDiamond"]+p[1:])


def p_FieldAccess(p):
    '''FieldAccess : Primary PERIOD IDENT
                  | SUPER PERIOD IDENT
                  | IDENT CommonName PERIOD SUPER PERIOD IDENT
                  | IDENT PERIOD SUPER PERIOD IDENT'''
    # p[0] = mytuple(["FieldAccess"]+p[1:])


def p_ArrayAccess(p):
    '''ArrayAccess : IDENT CommonName LBRACK Expression RBRACK
                    | IDENT PERIOD IDENT LBRACK Expression RBRACK
                    | IDENT LBRACK Expression RBRACK
                  | PrimaryNoNewArray LBRACK Expression RBRACK'''
    # p[0] = mytuple(["ArrayAccess"]+p[1:])


def p_MethodInvocation(p):
    '''MethodInvocation : IDENT LPAREN RPAREN
                       | IDENT LPAREN ArgumentList RPAREN
                       | IDENT PERIOD TypeArguments IDENT LPAREN ArgumentList RPAREN
                       | IDENT PERIOD TypeArguments IDENT LPAREN  RPAREN
                       | IDENT PERIOD  IDENT LPAREN ArgumentList RPAREN
                       | IDENT PERIOD  IDENT LPAREN  RPAREN
                       | IDENT PERIOD SUPER PERIOD TypeArguments IDENT LPAREN ArgumentList RPAREN
                       | IDENT PERIOD SUPER PERIOD TypeArguments IDENT LPAREN  RPAREN
                       | IDENT PERIOD SUPER PERIOD  IDENT LPAREN ArgumentList RPAREN
                       | IDENT PERIOD SUPER PERIOD  IDENT LPAREN  RPAREN
                       | IDENT CommonName PERIOD TypeArguments IDENT LPAREN ArgumentList RPAREN
                       | IDENT CommonName PERIOD TypeArguments IDENT LPAREN  RPAREN
                       | IDENT CommonName PERIOD  IDENT LPAREN ArgumentList RPAREN
                       | IDENT CommonName PERIOD  IDENT LPAREN  RPAREN
                       | IDENT CommonName PERIOD SUPER PERIOD TypeArguments IDENT LPAREN ArgumentList RPAREN
                       | IDENT CommonName PERIOD SUPER PERIOD TypeArguments IDENT LPAREN  RPAREN
                       | IDENT CommonName PERIOD SUPER PERIOD  IDENT LPAREN ArgumentList RPAREN
                       | IDENT CommonName PERIOD SUPER PERIOD  IDENT LPAREN  RPAREN
                       | Primary PERIOD TypeArguments IDENT LPAREN ArgumentList RPAREN
                       | Primary PERIOD TypeArguments IDENT LPAREN  RPAREN
                       | Primary PERIOD  IDENT LPAREN ArgumentList RPAREN
                       | Primary PERIOD  IDENT LPAREN  RPAREN
                       | SUPER PERIOD TypeArguments IDENT LPAREN ArgumentList RPAREN
                       | SUPER PERIOD TypeArguments IDENT LPAREN  RPAREN
                       | SUPER PERIOD  IDENT LPAREN ArgumentList RPAREN
                       | SUPER PERIOD  IDENT LPAREN  RPAREN'''
    # p[0] = mytuple(["MethodInvocation"]+p[1:])


def p_ArgumentList(p):
    '''ArgumentList : Expression COMMAExpressionS'''
    # p[0] = mytuple(["ArgumentList"]+p[1:])


def p_COMMAExpressionS(p):
    '''COMMAExpressionS : COMMAExpressionS COMMA Expression
                       | empty'''
    # p[0] = mytuple(["COMMAExpressionS"]+p[1:])


def p_MethodReference(p):
    '''MethodReference : IDENT COLON_SEP TypeArguments IDENT
                    | IDENT CommonName  COLON_SEP TypeArguments IDENT
                      | ReferenceType COLON_SEP TypeArguments IDENT
                      | Primary COLON_SEP TypeArguments IDENT
                      | SUPER COLON_SEP TypeArguments IDENT
                      | IDENT PERIOD SUPER COLON_SEP TypeArguments IDENT
                      | IDENT CommonName PERIOD SUPER COLON_SEP TypeArguments IDENT
                      | ClassType COLON_SEP TypeArguments NEW
                      | TypeVariable COLON_SEP TypeArguments NEW
                      | IDENT PERIOD IDENT COLON_SEP TypeArguments NEW
                      | IDENT COLON_SEP TypeArguments NEW
                      | IDENT COLON_SEP IDENT
                      | IDENT CommonName COLON_SEP IDENT
                    | ReferenceType COLON_SEP IDENT
                    | Primary COLON_SEP IDENT
                    | SUPER COLON_SEP IDENT
                    | IDENT PERIOD SUPER COLON_SEP IDENT
                    | IDENT CommonName PERIOD SUPER COLON_SEP IDENT
                    | ClassType COLON_SEP NEW
                    | TypeVariable COLON_SEP NEW
                    | IDENT PERIOD IDENT COLON_SEP NEW
                    | IDENT COLON_SEP NEW
                      | ArrayType COLON_SEP NEW'''
    # p[0] = mytuple(["MethodReference"]+p[1:])


def p_ArrayCreationExpression(p):
    '''ArrayCreationExpression : NEW PrimitiveType DimExprs Dims
                              | NEW BOOLEAN DimExprs Dims
                              | NEW ClassType DimExprs Dims
                              | NEW TypeVariable DimExprs Dims
                              | NEW IDENT PERIOD IDENT DimExprs Dims
                              | NEW IDENT DimExprs Dims
                              | NEW PrimitiveType DimExprs
                              | NEW BOOLEAN DimExprs
                              | NEW ClassType DimExprs
                              | NEW TypeVariable DimExprs
                              | NEW IDENT PERIOD IDENT DimExprs
                              | NEW IDENT DimExprs
                              | NEW PrimitiveType Dims ArrayInitializer
                              | NEW BOOLEAN Dims ArrayInitializer
                              | NEW ClassType Dims ArrayInitializer
                              | NEW TypeVariable Dims ArrayInitializer
                              | NEW IDENT PERIOD IDENT Dims ArrayInitializer
                              | NEW IDENT Dims ArrayInitializer'''
    # p[0] = mytuple(["ArrayCreationExpression : "]+p[1:])


def p_DimExprs(p):
    '''DimExprs : DimExprs DimExpr
                | DimExpr'''
    # p[0] = mytuple(["DimExprs"]+p[1:])

# def p_DimExprS(p):
#     '''DimExprS : DimExprS DimExpr
#                | DimExpr'''
#     # p[0] = mytuple(["DimExprS"]+p[1 :])


def p_DimExpr(p):
    '''DimExpr : AnnotationS LBRACK Expression RBRACK
                | LBRACK Expression RBRACK'''
    # p[0] = mytuple(["DimExpr"]+p[1:])

#*
def p_Expression(p):
    '''Expression : LambdaExpression
                 | AssignmentExpression
                | IDENT '''
    # p[0] = mytuple(["Expression"]+p[1:])
    if type(p[1]) != str:
        p[0] = p[1]
    else:
        p[0] = Node()
        p[0].id_list = [p[1]]
        p[0].type_list = ["identifier"]

#* DOUBT
def p_LambdaExpression(p):
    '''LambdaExpression : LambdaParameters ARROW LambdaBody'''
    # p[0] = mytuple(["LambdaExpression"]+p[1:])
    p[0] = p[1]
    p[0].id_list += p[3].id_list
    p[0].type_list += p[3].type_list
    p[0].place_list += p[3].place_list

#*
def p_LambdaParameters(p):
    '''LambdaParameters : IDENT
                       | LPAREN FormalParameterList RPAREN
                       | LPAREN  RPAREN
                       | LPAREN InferredFormalParameterList RPAREN'''
    # p[0] = mytuple(["LambdaParameters"]+p[1:])
    if len(p) == 2:
        p[0] = Node()
        p[0].id_list = [p[1]]
        p[0].type_list = ["identifier"]
    elif len(p) == 4:
        p[0] = p[2]

#*
def p_InferredFormalParameterList(p):
    '''InferredFormalParameterList : IDENT COMMAIDENTS'''
    # p[0] = mytuple(["InferredFormalParameterList"]+p[1:])
    p[0] = p[2]
    p[0].id_list.insert(0, p[1])
    p[0].type_list.insert(0, "identifier")

#*
def p_COMMAIDENTS(p):
    '''COMMAIDENTS : COMMAIDENTS COMMA IDENT
                  | empty'''
    # p[0] = mytuple(["COMMAIDENTS"]+p[1:])
    if len(p) == 4:
        p[0] = p[1]
        p[0].id_list.append(p[3])
        p[0].type_list.append("identifier")

#*
def p_LambdaBody(p):
    '''LambdaBody : Expression
                 | Block'''
    # p[0] = mytuple(["LambdaBody"]+p[1:])
    p[0] = p[1]

#*
def p_AssignmentExpression(p):
    '''AssignmentExpression : ConditionalExpression
                           | Assignment'''
    # p[0] = mytuple(["AssignmentExpression"]+p[1:])
    p[0] = p[1]

#*
def p_Assignment(p):
    '''Assignment : LeftHandSide AssignmentOperator Expression
                    | IDENT AssignmentOperator Expression'''
    # p[0] = mytuple(["Assignment"]+p[1:])
    # Remember AssignmentOperator is a token

    if type(p[1]) == str:
        p[0] = Node()
        p[0].id_list = [p[1]]
        p[0].type_list = ["identifier"]
    else:
        p[0] = p[1]
        p[0].code += p[3].code

    expr_type_list_key = p[0].type_list
    expr_type_list_val = p[3].type_list
    expr_place_list_key = p[0].place_list
    expr_place_list_val = p[3].place_list

    for i in range(len(expr_type_list_key)):
        newtype = higher(expr_type_list_key[i], expr_type_list_val[i])
        if newtype == -1 or (newtype == expr_type_list_val[i] and not (expr_type_list_key[i] == newtype or expr_type_list_key[i] == "identifier")):   # downcasting not allowed in Java
            raise TypeError(str(p.lineno(1)) + ": Type mismatch for identifier " + str(expr_place_list_key[i]))
        else:
            new_temp_var = new_temp()
            p[0].code += [["=", new_temp_var, "convert_to_"+newtype+"("+str(expr_place_list_val[i])+")"]]
            if p[2]=="=":
                p[0].code += [["=", expr_place_list_key[i], new_temp_var]]
            else:
                # format: operator, lhs, rhs - 1st op, rhs - 2nd op
                p[0].code += [[p[2][:-1], expr_place_list_key[i], expr_place_list_key[i], new_temp_var]]

        p[0].type_list[i] = newtype


#*
def p_LeftHandSide(p):
    '''LeftHandSide : IDENT
                    | IDENT CommonName
                   | FieldAccess
                   | ArrayAccess'''
    # p[0] = mytuple(["LeftHandSide"]+p[1:])
    if len(p) == 2 and type(p[1])!=str:
        p[0]=p[1]
    elif len(p)==2:
        p[0] = Node()
        p[0].id_list = [p[1]]
        p[0].type_list = ["identifier"]
    else:
        p[0] = p[2]
        p[0].id_list += [p[1]]
        p[0].type_list += ["identifier"]

#*
def p_AssignmentOperator(p):
    '''AssignmentOperator : ASSIGN
                         | MUL_ASSIGN
                         | QUO_ASSIGN
                         | REM_ASSIGN
                         | ADD_ASSIGN
                         | SUB_ASSIGN
                         | SHL_ASSIGN
                         | SHR_ASSIGN
                         | SHR_UN_ASSIGN
                         | AND_ASSIGN
                         | XOR_ASSIGN
                         | OR_ASSIGN'''
    p[0] = p[1]
    # # p[0] = mytuple(["AssignmentOperator"]+p[1:])

def chk_var(name, excluded_type_list=[], operator="", line=-1):
    if not in_scope_var(name):
        raise NameError(str(line) + ": Identifier " + name + " is not in any scope.")
    elif find_info(name, line)[1] in excluded_type_list:
        raise NameError(str(line) + ": bad operand type "+find_info(name, line)[1]+" for operator '"+operator+"'.")

# Checked if types of p1 and p2 match the operator specification and returns the resultant type
def get_combined_type(p1, p2, excluded_type_list=[], operator, line):
    type1 = ""
    type2 = ""

    if hasattr(p1, 'type'): # we have an IDENT
        chk_var(p1.value, excluded_type_list, operator, line)
        type1 = find_info(p1.value, line)[1] ## type of the var stored in the symbol table
    else:
        type1 = p1.type_list[0]

    if hasattr(p3, 'type'): # we have an IDENT
        chk_var(p3.value, excluded_type_list, operator, line)
        type2 = find_info(p3.value, line)[1] ## type of the var stored in the symbol table
    else:
        type2 = p3.type_list[0]

    if type1 in excluded_type_list or type2 in excluded_type_list:
        raise NameError(str(line) + ": bad operand type for operator '"+operator+"'.")
    if type1 not in type_list.keys() or type2 not in type_list.keys():
        raise NameError(str(line) + ": bad operand type for operator '"+operator+"'.")

    return type1, type2

def get_type(p1, line):
    type = ""

    if hasattr(p1, 'type'): # we have an IDENT
        chk_var(p1.value, excluded_type_list, operator, line)
        type = find_info(p1.value, line)[1] ## type of the var stored in the symbol table
    else:
        type = p1.type_list[0]

    return type

def p_ConditionalExpression(p):
    '''ConditionalExpression : ConditionalOrExpression
                            | ConditionalOrExpression QUES Expression COLON ConditionalExpression
                            | ConditionalOrExpression QUES Expression COLON IDENT
                            | ConditionalOrExpression QUES Expression COLON LambdaExpression
                            | IDENT QUES Expression COLON ConditionalExpression
                            | IDENT QUES Expression COLON IDENT
                            | IDENT QUES Expression COLON LambdaExpression '''
    # # p[0] = mytuple(["ConditionalExpression"]+p[1:])

    # A ? B : C
    # A must be boolean
    # B and C must be compatible (must have a LCA in the type DAG)

    if len(p) == 2:
        p[0] = p[1]
    else:
        if get_type(p[1]) != "boolean":
            raise NameError(str(p.lineno(1)) + ": Operand type " + get_type(p[1]) + " if not boolean.")
        type1 = get_type(p[3])
        type2 = get_type(p[5])
        if higher(type1, type2) == -1:
            raise NameError(str(p.lineno(1)) + ": Operands of types " + type1 + " and " + type2 + " are incompatible.")
        p[0].type_list = [higher(type1, type2)]

    p[0].extra["last_rule"] = "ConditionalExpression"


def p_ConditionalOrExpression(p):
    '''ConditionalOrExpression : ConditionalAndExpression
                              | ConditionalOrExpression LOR ConditionalAndExpression
                              | ConditionalOrExpression LOR IDENT
                              | IDENT LOR ConditionalAndExpression
                              | IDENT LOR IDENT'''
    # # p[0] = mytuple(["ConditionalOrExpression"]+p[1:])
    if len(p) == 2:
        p[0] = p[1]
    elif get_type(p[1]) != "boolean" or get_type(p[3]) != "boolean":
        raise NameError(str(p.lineno(1)) + ": Operands of types " + get_type(p[1]) + " and " + get_type(p[3]) + " cannot be compared.")
    else:
        p[0].type_list = ["boolean"]

    p[0].extra["last_rule"] = "ConditionalOrExpression"


def p_ConditionalAndExpression(p):
    '''ConditionalAndExpression : InclusiveOrExpression
                               | ConditionalAndExpression LAND InclusiveOrExpression
                               | ConditionalAndExpression LAND IDENT
                               | IDENT LAND InclusiveOrExpression
                               | IDENT LAND IDENT'''
    # # p[0] = mytuple(["ConditionalAndExpression"]+p[1:])
    if len(p) == 2:
        p[0] = p[1]
    elif get_type(p[1]) != "boolean" or get_type(p[3]) != "boolean":
        raise NameError(str(p.lineno(1)) + ": Operands of types " + get_type(p[1]) + " and " + get_type(p[3]) + " cannot be compared.")
    else:
        p[0].type_list = ["boolean"]

    p[0].extra["last_rule"] = "ConditionalAndExpression"


def p_InclusiveOrExpression(p):
    '''InclusiveOrExpression : ExclusiveOrExpression
                            | InclusiveOrExpression OR ExclusiveOrExpression
                            | InclusiveOrExpression OR IDENT
                            | IDENT OR ExclusiveOrExpression
                            | IDENT OR IDENT'''
    # # p[0] = mytuple(["InclusiveOrExpression"]+p[1:])
    if len(p) == 2:
        p[0] = p[1]
    else:
        type1, type2 = get_combined_type(p[1], p[3], ["double", "float", "boolean"], p[2].value, p.lineno(1))
        p[0].type_list = [higher(type1, type2)]

    p[0].extra["last_rule"] = "InclusiveOrExpression"

def p_ExclusiveOrExpression(p):
    '''ExclusiveOrExpression : AndExpression
                            | ExclusiveOrExpression XOR AndExpression
                            | ExclusiveOrExpression XOR IDENT
                            | IDENT XOR AndExpression
                            | IDENT XOR IDENT'''
    # # p[0] = mytuple(["ExclusiveOrExpression"]+p[1:])
    if len(p) == 2:
        p[0] = p[1]
    else:
        type1, type2 = get_combined_type(p[1], p[3], ["double", "float", "boolean"], p[2].value, p.lineno(1))
        p[0].type_list = [higher(type1, type2)]

    p[0].extra["last_rule"] = "ExclusiveOrExpression"


def p_AndExpression(p):
    '''AndExpression : EqualityExpression
                    | AndExpression AND EqualityExpression
                    | AndExpression AND IDENT
                    | IDENT AND EqualityExpression
                    | IDENT AND IDENT'''
    # # p[0] = mytuple(["AndExpression"]+p[1:])
    if len(p) == 2:
        p[0] = p[1]
    else:
        type1, type2 = get_combined_type(p[1], p[3], ["double", "float", "char", "short", "byte"], p[2].value, p.lineno(1))
        p[0].type_list = [higher(type1, type2)]

    p[0].extra["last_rule"] = "AndExpression"



def p_EqualityExpression(p):
    '''EqualityExpression : RelationalExpression
                         | EqualityExpression EQL RelationalExpression
                         | EqualityExpression NEQ RelationalExpression
                         | EqualityExpression EQL IDENT
                         | EqualityExpression NEQ IDENT
                         | IDENT EQL RelationalExpression
                         | IDENT NEQ RelationalExpression
                         | IDENT EQL IDENT
                         | IDENT NEQ IDENT'''
    # # p[0] = mytuple(["EqualityExpression"]+p[1:])
    if len(p) == 2:
        p[0] = p[1]
    else:
        if get_type(p[1]) != get_type(p[3]):
            if get_type(p[1]) == "boolean" or get_type(p[3]) == "boolean":
                raise NameError(str(p.lineno(1)) + ": Operands of types " + get_type(p[1]) + " and " + get_type(p[3]) + " cannot be compared.")
            else if get_type(p[1]) not in type_list.keys() or get_type(p[3]) not in type_list.keys():
                raise NameError(str(p.lineno(1)) + ": Operands of type " + get_type(p[1]) + " and " + get_type(p[3]) + " cannot be compared.")
        p[0].type_list = ["boolean"]
        # TODO (anay): updare get_type to handle classes.

    p[0].extra["last_rule"] = "EqualityExpression"

# TODO:    Hack added these lines which were not needed to pass LexicalScope.java in sir's examples
                           # | IDENT PERIOD IDENT LSS IDENT
                           # | IDENT PERIOD IDENT GTR IDENT
                           # | IDENT PERIOD IDENT LEQ IDENT
                           # | IDENT PERIOD IDENT GEQ IDENT


def p_RelationalExpression(p):
    '''RelationalExpression : ShiftExpression
                           | RelationalExpression LSS ShiftExpression
                           | RelationalExpression GTR ShiftExpression
                           | RelationalExpression LEQ ShiftExpression
                           | RelationalExpression GEQ ShiftExpression
                           | RelationalExpression LSS IDENT
                           | RelationalExpression GTR IDENT
                           | RelationalExpression LEQ IDENT
                           | RelationalExpression GEQ IDENT
                           | IDENT LSS ShiftExpression
                           | IDENT GTR ShiftExpression
                           | IDENT LEQ ShiftExpression
                           | IDENT GEQ ShiftExpression
                           | IDENT PERIOD IDENT LSS ShiftExpression
                           | IDENT PERIOD IDENT GTR ShiftExpression
                           | IDENT PERIOD IDENT LEQ ShiftExpression
                           | IDENT PERIOD IDENT GEQ ShiftExpression
                           | IDENT LSS IDENT
                           | IDENT GTR IDENT
                           | IDENT LEQ IDENT
                           | IDENT GEQ IDENT
                           | IDENT PERIOD IDENT LSS IDENT
                           | IDENT PERIOD IDENT GTR IDENT
                           | IDENT PERIOD IDENT LEQ IDENT
                           | IDENT PERIOD IDENT GEQ IDENT
                           | RelationalExpression INSTANCEOF ReferenceType
                           | RelationalExpression INSTANCEOF IDENT
                           | IDENT INSTANCEOF ReferenceType
                           | IDENT INSTANCEOF IDENT'''
    # # p[0] = mytuple(["RelationalExpression"]+p[1:])
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        if p[2].value.lower() == "INSTANCEOF".lower():
            raise NameError("TODO (anay): Rule with IDENT INSTANCEOF... not handled yet.")

        if get_type(p[1]) == "boolean" or get_type(p[3]) == "boolean":
            raise NameError(str(p.lineno(1)) + ": Operands of types " + get_type(p[1]) + " and " + get_type(p[3]) + " cannot be compared.")
        else if get_type(p[1]) not in type_list.keys() or get_type(p[3]) not in type_list.keys():
            raise NameError(str(p.lineno(1)) + ": Operands of type " + get_type(p[1]) + " and " + get_type(p[3]) + " cannot be compared.")
        p[0].type_list = ["boolean"]

    elif len(p) == 6:
        raise NameError("TODO (anay): Rule with IDENT.IDENT... not handled yet.")

    p[0].extra["last_rule"] = "RelationalExpression"

def p_ShiftExpression(p):
    '''ShiftExpression : AdditiveExpression
                      | ShiftExpression SHL AdditiveExpression
                      | ShiftExpression SHR AdditiveExpression
                      | ShiftExpression SHR_UN AdditiveExpression
                      | ShiftExpression SHL IDENT
                      | ShiftExpression SHR IDENT
                      | ShiftExpression SHR_UN IDENT
                      | IDENT SHL AdditiveExpression
                      | IDENT SHR AdditiveExpression
                      | IDENT SHR_UN AdditiveExpression
                      | IDENT SHL IDENT
                      | IDENT SHR IDENT
                      | IDENT SHR_UN IDENT'''
    # # p[0] = mytuple(["ShiftExpression"]+p[1:])
    if len(p) == 2:
        p[0] = p[1]
    else:
        type1, type2 = get_combined_type(p[1], p[3], ["double", "float", "char", "short", "byte", "boolean"], p[2].value, p.lineno(1))
        p[0].type_list = [higher(type1, type2)]

    p[0].extra["last_rule"] = "ShiftExpression"

def p_AdditiveExpression(p):
    '''AdditiveExpression : MultiplicativeExpression
                         | AdditiveExpression ADD MultiplicativeExpression
                         | AdditiveExpression SUB MultiplicativeExpression
                          | AdditiveExpression ADD IDENT
                          | AdditiveExpression SUB IDENT
                          | IDENT ADD MultiplicativeExpression
                          | IDENT SUB MultiplicativeExpression
                           | IDENT ADD IDENT
                           | IDENT SUB IDENT'''
    # # p[0] = mytuple(["AdditiveExpression"]+p[1:])
    if len(p) == 2:
        p[0] = p[1]
    else:
        type1, type2 = get_combined_type(p[1], p[3], ["char", "short", "byte", "boolean"], p[2].value, p.lineno(1))
        p[0].type_list = [higher(type1, type2)]

    p[0].extra["last_rule"] = "AdditiveExpression"

def p_MultiplicativeExpression(p):
    '''MultiplicativeExpression : UnaryExpression
                               | MultiplicativeExpression MUL UnaryExpression
                               | MultiplicativeExpression QUO UnaryExpression
                               | MultiplicativeExpression REM UnaryExpression
                               | MultiplicativeExpression MUL IDENT
                               | MultiplicativeExpression QUO IDENT
                               | MultiplicativeExpression REM IDENT
                               | IDENT MUL UnaryExpression
                               | IDENT QUO UnaryExpression
                               | IDENT REM UnaryExpression
                               | IDENT MUL IDENT
                               | IDENT QUO IDENT
                               | IDENT REM IDENT'''
    # # p[0] = mytuple(["MultiplicativeExpression"]+p[1:])
    if len(p) == 2:
        p[0] = p[1]
    else:
        type1, type2 = get_combined_type(p[1], p[3], ["char", "short", "byte", "boolean"], p[2].value, p.lineno(1))
        p[0].type_list = [higher(type1, type2)]

    p[0].extra["last_rule"] = "MultiplicativeExpression"

def p_UnaryExpression(p):
    '''UnaryExpression : PreIncrementExpression
                      | PreDecrementExpression
                      | ADD UnaryExpression
                      | SUB UnaryExpression
                      | ADD IDENT
                      | SUB IDENT
                      | UnaryExpressionNotPlusMinus
                      | IDENT CommonName'''
    # # p[0] = mytuple(["UnaryExpression"]+p[1:])
    if len(p) == 2:
        p[0] = p[1]
    elif p[1].value in ['+', '-']:
        if hasattr(p[2], 'type'): # we have an IDENT
            chk_var(p[2].value, ["char", "short", "byte", "boolean"], p[1].value, p.lineno(1))
            p[0].type_list = [find_info(p[2].value, p.lineno(1))[1]] ## the type of the variable stored in the symbol table
        else:
            if p[2].type_list[0] in ["char", "short", "byte", "boolean"]:
                raise NameError(str(p.lineno(1)) + ": bad operand type "+p[2].type_list[0]+" for operator '"+p[1].value+"'.")
            else:
                p[0].type_list = p[2].type_list
    else: # rule is: IDENT CommonName
        raise NameError("TODO (anay): Case with IDENT.IDENT... not handled yet, handle with CommonName.")

    p[0].extra["last_rule"] = "UnaryExpression"



# updated (anay)
def p_PreIncrementExpression(p):
    '''PreIncrementExpression : INC UnaryExpression
                                | INC IDENT'''
    # # p[0] = mytuple(["PreIncrementExpression"]+p[1:])
    p[0] = p[1]

    if p[0].type_list[0] in type_list and p[0].type_list[0] != 'boolean':
        # write some 3ac code.
        temp=0
        # p[0].code += [[type_v + "_" + p[2][1], p[0].place_list[0], p[0].place_list[0], "1"]]
    else:
        raise TypeError("PreIncrement on classes (or custom types) not implemented yet.")

    p[0].extra["last_rule"] = "PreIncrementExpression"



# updated (anay)
def p_PreDecrementExpression(p):
    '''PreDecrementExpression : DEC UnaryExpression
                                | DEC IDENT'''
    # # p[0] = mytuple(["PreDecrementExpression"]+p[1:])
    p[0] = p[1]

    if p[0].type_list[0] in type_list and p[0].type_list[0] != 'boolean':
        # write some 3ac code.
        temp=0
        # p[0].code += [[type_v + "_" + p[2][1], p[0].place_list[0], p[0].place_list[0], "1"]]
    else:
        raise TypeError("PreDecrement on classes (or custom types) not implemented yet.")

    p[0].extra["last_rule"] = "PreDecrementExpression"


# updated (anay)
def p_UnaryExpressionNotPlusMinus(p):
    '''UnaryExpressionNotPlusMinus : PostfixExpression
                                   | LNOT UnaryExpression
                                   | NOT UnaryExpression
                                   | LNOT IDENT
                                   | NOT IDENT
                                   | CastExpression'''
    # # p[0] = mytuple(["UnaryExpressionNotPlusMinus"]+p[1:])
    if len(p) == 2:
        p[0] = p[1]
    elif p[1].value == "~":
        p[0] = p[2]
        if p[3].type_list[0] in ["float", "double", "boolean"]:
            raise NameError("Bad operand type float for unary operator '~'.")
    elif p[1].value == "!":
        p[0] = p[2]
        if p[3].type_list[0] not in ["boolean"]:
            raise NameError("Bad operand type float for unary operator '!'.")
    else:
        assert False

    p[0].extra["last_rule"] = "UnaryExpressionNotPlusMinus"



# updated (anay)
def p_PostfixExpression(p):
    '''PostfixExpression : Primary
                        | PostIncrementExpression
                        | PostDecrementExpression'''
    # # p[0] = mytuple(["PostfixExpression"]+p[1:])
    p[0] = p[1]
    p[0].extra["last_rule"] = "PostfixExpression"


# updated (anay)
def p_PostIncrementExpression(p):
    '''PostIncrementExpression : PostfixExpression INC
                                | IDENT CommonName INC
                                | IDENT INC'''
    # # p[0] = mytuple(["PostIncrementExpression"]+p[1:])
    p[0] = p[1]

    if len(p) == 3:
        if p[0].type_list[0] in type_list and p[0].type_list[0] != 'boolean':
            # write some 3ac code.
            temp=0
            # p[0].code += [[type_v + "_" + p[2][1], p[0].place_list[0], p[0].place_list[0], "1"]]
        else:
            raise TypeError(str(p.lineno(1)) + ": Can't do " + str(p[2]) + " operation on type " + str(p[0].type_list[0]))
    else:
        raise NameError("TODO (anay): Case with IDENT.IDENT... not handled yet, handle with CommonName.")

    p[0].extra["last_rule"] = "PostIncrementExpression"



# updated (anay)
def p_PostDecrementExpression(p):
    '''PostDecrementExpression : PostfixExpression DEC
                                | IDENT CommonName DEC
                                | IDENT DEC'''
    # # p[0] = mytuple(["PostDecrementExpression"]+p[1:])
    p[0] = p[1]

    if len(p) == 3:
        if p[0].type_list[0] in type_list and p[0].type_list[0] != 'boolean':
            # write some 3ac code.
            temp=0
            # p[0].code += [[type_v + "_" + p[2][1], p[0].place_list[0], p[0].place_list[0], "1"]]
        else:
            raise TypeError(str(p.lineno(1)) + ": Can't do " + str(p[2]) + " operation on type " + str(p[0].type_list[0]))
    else:
        raise NameError("TODO (anay): Case with IDENT.IDENT... not handled yet, handle with CommonName.")

    p[0].extra["last_rule"] = "PostDecrementExpression"

# updated (anay)
def p_CastExpression(p):
    '''CastExpression : LPAREN PrimitiveType RPAREN UnaryExpression
                     | LPAREN PrimitiveType RPAREN IDENT
                     | LPAREN BOOLEAN RPAREN UnaryExpression
                     | LPAREN BOOLEAN RPAREN IDENT
                     | LPAREN ReferenceType AdditionalBoundS RPAREN UnaryExpressionNotPlusMinus
                     | LPAREN ReferenceType AdditionalBoundS RPAREN IDENT CommonName
                     | LPAREN ReferenceType AdditionalBoundS RPAREN IDENT
                     | LPAREN ReferenceType AdditionalBoundS RPAREN LambdaExpression
                     | LPAREN IDENT AdditionalBoundS RPAREN UnaryExpressionNotPlusMinus
                     | LPAREN IDENT AdditionalBoundS RPAREN IDENT CommonName
                     | LPAREN IDENT AdditionalBoundS RPAREN IDENT
                     | LPAREN IDENT AdditionalBoundS RPAREN LambdaExpression
                     | LPAREN ReferenceType RPAREN UnaryExpressionNotPlusMinus
                     | LPAREN ReferenceType RPAREN IDENT CommonName
                     | LPAREN ReferenceType RPAREN IDENT
                     | LPAREN ReferenceType RPAREN LambdaExpression
                     | LPAREN IDENT RPAREN UnaryExpressionNotPlusMinus
                     | LPAREN IDENT RPAREN IDENT CommonName
                     | LPAREN IDENT RPAREN IDENT
                     | LPAREN IDENT RPAREN LambdaExpression'''
    # # p[0] = mytuple(["CastExpression"]+p[1:])

    # TODO (anay): The following rules sseem incorrect. IDENT should not be a type.
    if len(p) != 5:
        raise NameError("Bounded types are not implemented yet!")

    p[0] = p[4]

    if hasattr(p[2], 'type'): #p[2] is an IDENT
        if not in_scope_class(p[2].value):
            raise NameError("Unknown type "+p[2].value)
        raise NameError("Casting between classes not implemented yet!")

    # TODO (anay): Would throw errors if casting is between classes, i.e., if we have ReferenceType.
    if higher(p[2].type_list[0], p[4].type_list[0]) == p[4].type_list[0]:
        p[0].type_list[0] = p[2].type_list[0]

    p[0].extra["last_rule"] = "CastExpression"



def p_AdditionalBoundS(p):
    '''AdditionalBoundS : AdditionalBoundS AdditionalBound
                       | AdditionalBound'''

    raise NameError("Bounded types are not implemented yet!")
    # p[0] = mytuple(["AdditionalBoundS"]+p[1:])


# updated (Anay)
def p_ConstantExpression(p):
    '''ConstantExpression : Expression'''
    p[0] = p[1]
    p[0].extra["last_rule"] = "ConstantExpression"
    # # p[0] = mytuple(["ConstantExpression"]+p[1:])

#</editor-fold>############################################

#<editor-fold Section 7 : Packages #########################
################################################
# Section 7 : Packages
################################################


def p_CompilationUnit(p):
    '''CompilationUnit : ImportDeclarationS TypeDeclarationS
                    | PackageDeclaration ImportDeclarationS TypeDeclarationS'''
    # p[0] = mytuple(["CompilationUnit"]+p[1:])

def p_ImportDeclarationS(p):
    '''ImportDeclarationS : ImportDeclarationS ImportDeclaration
                          | empty'''
    # p[0] = mytuple(["ImportDeclarationS"]+p[1:])


def p_TypeDeclarationS(p):
    '''TypeDeclarationS : TypeDeclarationS TypeDeclaration
                        | TypeDeclarationS SEMICOLON
                          | empty'''
    # p[0] = mytuple(["TypeDeclarationS"]+p[1:])


def p_PackageDeclaration(p):
    '''PackageDeclaration : PackageModifierS PACKAGE IDENT PERIODIDENTS SEMICOLON'''
    # p[0] = mytuple(["PackageDeclaration"]+p[1:])


def p_PackageModifierS(p):
    '''PackageModifierS : PackageModifierS PackageModifier
                          | empty'''
    # p[0] = mytuple(["PackageModifierS"]+p[1:])


def p_PERIODIDENTS(p):
    '''PERIODIDENTS : PERIODIDENTS PERIOD IDENT
                   | empty'''
    # p[0] = mytuple(["PERIODIDENTS"]+p[1:])


def p_PackageModifier(p):
    '''PackageModifier : Annotation'''
    # p[0] = mytuple(["PackageModifier"]+p[1:])


def p_ImportDeclaration(p):
    '''ImportDeclaration : SingleTypeImportDeclaration
                        | TypeImportOnDemandDeclaration
                        | SingleStaticImportDeclaration
                        | StaticImportOnDemandDeclaration'''
    # p[0] = mytuple(["ImportDeclaration"]+p[1:])


def p_SingleTypeImportDeclaration(p):
    '''SingleTypeImportDeclaration : IMPORT IDENT SEMICOLON
                        | IMPORT IDENT CommonName SEMICOLON'''
    # p[0] = mytuple(["SingleTypeImportDeclaration"]+p[1:])


def p_TypeImportOnDemandDeclaration(p):
    '''TypeImportOnDemandDeclaration : IMPORT IDENT PERIOD MUL SEMICOLON
                                    | IMPORT IDENT CommonName PERIOD MUL SEMICOLON
'''
    # p[0] = mytuple(["TypeImportOnDemandDeclaration"]+p[1:])


def p_SingleStaticImportDeclaration(p):
    '''SingleStaticImportDeclaration : IMPORT STATIC IDENT PERIOD IDENT SEMICOLON
                        | IMPORT STATIC IDENT CommonName PERIOD IDENT SEMICOLON'''
    # p[0] = mytuple(["SingleStaticImportDeclaration"]+p[1:])


def p_StaticImportOnDemandDeclaration(p):
    '''StaticImportOnDemandDeclaration : IMPORT STATIC IDENT PERIOD MUL SEMICOLON
                                    | IMPORT STATIC IDENT CommonName PERIOD MUL SEMICOLON'''
    # p[0] = mytuple(["StaticImportOnDemandDeclaration"]+p[1:])


def p_TypeDeclaration(p):
    '''TypeDeclaration : ClassDeclaration
                      | InterfaceDeclaration'''
    # p[0] = mytuple(["TypeDeclaration"]+p[1:])

#</editor-fold>############################################

#<editor-fold Section 6 #########################
####################################
########## Section 6 : ##############
####################################

# def p_TypeName(p):
#     '''CommonName : IDENT
#                 | CommonName PERIOD IDENT '''
#     # p[0] = mytuple(["type_name"]+p[1 :])

# def p_TypeName(p):
#     '''TypeName : CommonName'''
#     # p[0] = mytuple(["type_name"]+p[1 :])

# def p_PackageOrTypeName(p):
#     '''CommonName : IDENT
#                         | CommonName PERIOD IDENT '''
#     # p[0] = mytuple(["CommonName"]+p[1 :])

#*
def p_CommonName(p):
    '''CommonName : PERIOD IDENT
                        | CommonName PERIOD IDENT'''
    if len(p)==3:
        p[0] = Node()
        p[0].id_list = [p[2]]
        p[0].type_list = ["identifier"]
    else:
        p[0] = p[1]
        p[0].id_list += [p[3]]
        p[0].type_list += ["identifier"]
    # p[0] = mytuple(["CommonName"]+p[1:])


# def p_MethodName(p):
#     '''MethodName : IDENT'''
#     # p[0] = mytuple(["MethodName"]+p[1 :])

# def p_PackageName(p):
#     '''PackageName : IDENT
#                     | PackageName PERIOD IDENT'''
#     # p[0] = mytuple(["PackageName"]+p[1 :])

# def p_AmbiguousName(p):
#     '''CommonName : IDENT
#                     | CommonName PERIOD IDENT'''
#     # p[0] = mytuple(["CommonName"]+p[1 :])

####################################
########## SECTION #8 ##############
####################################

def p_ClassDeclaration(p):
    '''ClassDeclaration : NormalClassDeclaration
                        | EnumDeclaration'''
    # p[0] = mytuple(["ClassDeclaration"]+p[1:])


def p_SuperClass(p):
    '''SuperClass : EXTENDS ClassType
                    | EXTENDS TypeVariable
                    | EXTENDS IDENT PERIOD IDENT
                    | EXTENDS IDENT
    '''
    # p[0] = mytuple(["SuperClass"] + p[1:])

# def p_Superinterfaces(p):
#     '''Superinterfaces : IMPLEMENTS InterfaceTypeList
#     '''
#     # p[0] = mytuple(["Superinterfaces"] + p[1:])

def p_NormalClassDeclaration(p):
    '''NormalClassDeclaration : CommonModifierS CLASS IDENT TypeParameters SuperClass Superinterfaces ClassBody
                            | CommonModifierS CLASS IDENT TypeParameters Superinterfaces ClassBody
                            | CommonModifierS CLASS IDENT TypeParameters SuperClass  ClassBody
                            | CommonModifierS CLASS IDENT TypeParameters ClassBody
                            | CommonModifierS CLASS IDENT SuperClass Superinterfaces ClassBody
                            | CommonModifierS CLASS IDENT Superinterfaces ClassBody
                            | CommonModifierS CLASS IDENT SuperClass  ClassBody
                            | CommonModifierS CLASS IDENT ClassBody
                            | CLASS IDENT TypeParameters SuperClass Superinterfaces ClassBody
                            | CLASS IDENT TypeParameters Superinterfaces ClassBody
                            | CLASS IDENT TypeParameters SuperClass  ClassBody
                            | CLASS IDENT TypeParameters ClassBody
                            | CLASS IDENT SuperClass Superinterfaces ClassBody
                            | CLASS IDENT Superinterfaces ClassBody
                            | CLASS IDENT SuperClass  ClassBody
                            | CLASS IDENT ClassBody'''
    # p[0] = mytuple(["NormalClassDeclaration"]+p[1:])

# def p_ClassModifier(p):
#     '''ClassModifier : Annotation
#                     | PUBLIC
#                     | PROTECTED
#                     | PRIVATE
#                     | ABSTRACT
#                     | STATIC
#                     | FINAL
#                     | STRICTFP
#     '''
#     # p[0] = mytuple(["ClassModifier"]+p[1 :])

# def p_ClassModifier(p):
#     '''ClassModifier : Annotation
#                     | Annotation
#                     | PUBLIC
#                     | PROTECTED
#                     | PRIVATE
#                     | FINAL
#                     | ABSTRACT
#                     | STATIC
#                     | STRICTFP
#     '''
#     # p[0] = mytuple(["ClassModifier"]+p[1 :])


def p_TypeParameters(p):
    '''TypeParameters : LSS TypeParameterList GTR
    '''
    # print("I am TypeParameters!!!!")
    # print("\n"*20)
    # p[0] = mytuple(["TypeParameters"]+p[1:])


def p_COMMMATypeParameterS(p):
    '''COMMMATypeParameterS : COMMMATypeParameterS COMMA TypeParameter
                            | empty
    '''
    # p[0] = mytuple(["COMMMATypeParameterS"]+p[1:])


def p_TypeParameterList(p):
    '''TypeParameterList : TypeParameter COMMMATypeParameterS
    '''
    # p[0] = mytuple(["TypeParameterList"]+p[1:])

# def p_Superclass(p):
#     '''Superclass : EXTENDS ClassType
#     '''
#     # p[0] = mytuple(["Superclass"]+p[1 :])


def p_Superinterfaces(p):
    '''Superinterfaces : IMPLEMENTS InterfaceTypeList
    '''
    # p[0] = mytuple(["Superinterfaces"]+p[1:])


def p_COMMAInterfaceTypeS(p):
    '''COMMAInterfaceTypeS : COMMA InterfaceTypeList
                            | empty
    '''
    # p[0] = mytuple(["COMMAInterfaceTypeS"]+p[1:])


def p_InterfaceTypeList(p):
    '''InterfaceTypeList : ClassType COMMAInterfaceTypeS
                    | TypeVariable COMMAInterfaceTypeS
                    | IDENT PERIOD IDENT COMMAInterfaceTypeS
                    | IDENT COMMAInterfaceTypeS
    '''
    # p[0] = mytuple(["InterfaceTypeList"]+p[1:])


def p_ClassBodyDeclarationS(p):
    '''ClassBodyDeclarationS : ClassBodyDeclarationS ClassBodyDeclaration
                            | ClassBodyDeclarationS SEMICOLON
                             | empty
    '''
    # p[0] = mytuple(["ClassBodyDeclarationS"]+p[1:])


def p_ClassBody(p):
    '''ClassBody : LBRACE ClassBodyDeclarationS RBRACE
    '''
    # p[0] = mytuple(["ClassBody"]+p[1:])


def p_ClassBodyDeclaration(p):
    '''ClassBodyDeclaration : ClassMemberDeclaration
                            | Block
                            | StaticInitializer
                            | ConstructorDeclaration
    '''
    # p[0] = mytuple(["ClassBodyDeclaration"]+p[1:])


def p_ClassMemberDeclaration(p):
    '''ClassMemberDeclaration : FieldDeclaration
                            | MethodDeclaration
                            | ClassDeclaration
                            | InterfaceDeclaration
    '''
    # p[0] = mytuple(["ClassMemberDeclaration"]+p[1:])

# def p_FieldModifierS(p):
#     '''CommonModifierS : CommonModifier CommonModifierS
#                         | CommonModifier
#     '''
#     # p[0] = mytuple(["CommonModifierS"]+p[1 :])


def p_FieldDeclaration(p):
    '''FieldDeclaration : CommonModifierS UnannType VariableDeclaratorList SEMICOLON
                        | CommonModifierS NumericType VariableDeclaratorList SEMICOLON
                        | CommonModifierS BOOLEAN VariableDeclaratorList SEMICOLON
                        | CommonModifierS IDENT VariableDeclaratorList SEMICOLON
                        | UnannType VariableDeclaratorList SEMICOLON
                        | NumericType VariableDeclaratorList SEMICOLON
                        | BOOLEAN VariableDeclaratorList SEMICOLON
                        | IDENT VariableDeclaratorList SEMICOLON
                        | CommonModifierS UnannType IDENT SEMICOLON
                        | CommonModifierS NumericType IDENT SEMICOLON
                        | CommonModifierS BOOLEAN IDENT SEMICOLON
                        | CommonModifierS IDENT IDENT SEMICOLON
                        | UnannType IDENT SEMICOLON
                        | NumericType IDENT SEMICOLON
                        | BOOLEAN IDENT SEMICOLON
                        | IDENT IDENT SEMICOLON
                        '''
    # p[0] = mytuple(["FieldDeclaration"]+p[1:])

# def p_FieldModifier(p):
#     '''CommonModifier : Annotation
#                     | PUBLIC
#                     | PROTECTED
#                     | PRIVATE
#                      | STATIC
#                      | FINAL
#                      | TRANSIENT
#                      | VOLATILE
#     '''
#     # p[0] = mytuple(["CommonModifier"]+p[1 :])


def p_COMMAVariableDeclaratorS(p):
    '''COMMAVariableDeclaratorS : COMMAVariableDeclaratorS COMMA VariableDeclarator
                            | COMMAVariableDeclaratorS COMMA IDENT
                                | COMMA IDENT
                                | COMMA VariableDeclarator
    '''
    # p[0] = mytuple(["COMMAVariableDeclaratorS"]+p[1:])


def p_VariableDeclaratorList(p):
    '''VariableDeclaratorList : VariableDeclarator COMMAVariableDeclaratorS
                    | IDENT COMMAVariableDeclaratorS
                    | VariableDeclarator
    '''
    # p[0] = mytuple(["VariableDeclaratorList"]+p[1:])

def p_VariableDeclarator(p):
    '''VariableDeclarator : VariableDeclaratorId ASSIGN VariableInitializer
                        | IDENT ASSIGN VariableInitializer
                        | VariableDeclaratorId
    '''
    # p[0] = mytuple(["VariableDeclarator"]+p[1:])

def p_VariableDeclaratorId(p):
    '''VariableDeclaratorId : IDENT Dims'''
    # p[0] = mytuple(["VariableDeclaratorId"]+p[1:])

#*
def p_VariableInitializer(p):
    '''VariableInitializer : Expression
                            | ArrayInitializer
    '''
    # p[0] = mytuple(["VariableInitializer"]+p[1:])
    p[0] = p[1]


def p_UnannType(p):
    '''UnannType : UnannReferenceType
                | IDENT PERIOD IDENT
    '''
    # p[0] = mytuple(["UnannType"]+p[1:])

# def p_UnannPrimitiveType(p):
#     '''UnannPrimitiveType :  NumericType
#     '''
#     # p[0] = mytuple(["UnannPrimitiveType"]+p[1 :])

#*
def p_UnannReferenceType(p):
    '''UnannReferenceType :  UnannClassType
                        | UnannArrayType
    '''
    # p[0] = mytuple(["UnannReferenceType"]+p[1:])
    p[0] = p[1]

# def p_UnannClassOrInterfaceType(p):
#     '''UnannClassType :  UnannClassType'''
#     # p[0] = mytuple(["UnannClassType"]+p[1 :])

# def p_AnnotationS(p):
#     '''AnnotationS : Annotation AnnotationS
#                     | empty
#     '''


def p_UnannClassType(p):
    '''UnannClassType : IDENT TypeArguments
                        | UnannClassType PERIOD IDENT
                        | UnannClassType PERIOD IDENT TypeArguments
                        | UnannClassType PERIOD AnnotationS IDENT
                        | UnannClassType PERIOD AnnotationS IDENT TypeArguments
                        | IDENT PERIOD IDENT TypeArguments
                        | IDENT PERIOD AnnotationS IDENT
                        | IDENT PERIOD AnnotationS IDENT TypeArguments
    '''
    # p[0] = mytuple(["UnannClassType"]+p[1:])

# def p_UnannInterfaceType(p):
#     '''UnannClassType : UnannClassType
#     '''
#     # p[0] = mytuple(["UnannClassType"]+p[1 :])

# def p_UnannTypeVariable(p):
#     '''IDENT : IDENT
#     '''
#     # p[0] = mytuple(["IDENT"]+p[1 :])


def p_UnannArrayType(p):
    '''UnannArrayType :  NumericType Dims
                        | BOOLEAN Dims
                        | UnannClassType Dims
                        | IDENT PERIOD IDENT Dims
                        | IDENT Dims
    '''
    # p[0] = mytuple(["UnannArrayType"]+p[1:])


# def p_MethodModifierS(p):
#     '''CommonModifierS : CommonModifier CommonModifierS
#                         | CommonModifier
#     '''
#     # p[0] = mytuple(["CommonModifierS"]+p[1 :])
def p_MethodDeclaration(p):
    '''MethodDeclaration : CommonModifierS MethodHeader MethodBody
                         | MethodHeader MethodBody
                        | CommonModifierS MethodHeader SEMICOLON
                        | MethodHeader SEMICOLON
    '''
    # p[0] = mytuple(["MethodDeclaration"]+p[1:])

# def p_MethodModifier(p):
#     '''CommonModifier : Annotation
#                     | PUBLIC
#                     | PROTECTED
#                     | PRIVATE
#                     | ABSTRACT
#                     | STATIC
#                     | FINAL
#                     | SYNCHRONIZED
#                     | NATIVE
#                     | STRICTFP
#     '''
#     # p[0] = mytuple(["CommonModifier"]+p[1 :])


# TODO: Major hacks here!!! We removed Throws non-terminal
def p_MethodHeader(p):
    '''MethodHeader : TypeParameters AnnotationS UnannType MethodDeclarator THROWS IDENT
                    | TypeParameters AnnotationS UnannType MethodDeclarator THROWS IDENT PERIOD IDENT
                    | TypeParameters AnnotationS UnannType MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT
                    | TypeParameters AnnotationS UnannType MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | TypeParameters AnnotationS UnannType MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | TypeParameters AnnotationS UnannType MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | TypeParameters UnannType MethodDeclarator THROWS IDENT
                    | TypeParameters UnannType MethodDeclarator THROWS IDENT PERIOD IDENT
                    | TypeParameters UnannType MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT
                    | TypeParameters UnannType MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | TypeParameters UnannType MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | TypeParameters UnannType MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | TypeParameters AnnotationS NumericType MethodDeclarator THROWS IDENT
                    | TypeParameters AnnotationS NumericType MethodDeclarator THROWS IDENT PERIOD IDENT
                    | TypeParameters AnnotationS NumericType MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT
                    | TypeParameters AnnotationS NumericType MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | TypeParameters AnnotationS NumericType MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | TypeParameters AnnotationS NumericType MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | TypeParameters NumericType MethodDeclarator THROWS IDENT
                    | TypeParameters NumericType MethodDeclarator THROWS IDENT PERIOD IDENT
                    | TypeParameters NumericType MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT
                    | TypeParameters NumericType MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | TypeParameters NumericType MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | TypeParameters NumericType MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | TypeParameters AnnotationS BOOLEAN MethodDeclarator THROWS IDENT
                    | TypeParameters AnnotationS BOOLEAN MethodDeclarator THROWS IDENT PERIOD IDENT
                    | TypeParameters AnnotationS BOOLEAN MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT
                    | TypeParameters AnnotationS BOOLEAN MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | TypeParameters AnnotationS BOOLEAN MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | TypeParameters AnnotationS BOOLEAN MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | TypeParameters BOOLEAN MethodDeclarator THROWS IDENT
                    | TypeParameters BOOLEAN MethodDeclarator THROWS IDENT PERIOD IDENT
                    | TypeParameters BOOLEAN MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT
                    | TypeParameters BOOLEAN MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | TypeParameters BOOLEAN MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | TypeParameters BOOLEAN MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | TypeParameters AnnotationS VOID MethodDeclarator THROWS IDENT
                    | TypeParameters AnnotationS VOID MethodDeclarator THROWS IDENT PERIOD IDENT
                    | TypeParameters AnnotationS VOID MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT
                    | TypeParameters AnnotationS VOID MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | TypeParameters AnnotationS VOID MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | TypeParameters AnnotationS VOID MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | TypeParameters VOID MethodDeclarator THROWS IDENT
                    | TypeParameters VOID MethodDeclarator THROWS IDENT PERIOD IDENT
                    | TypeParameters VOID MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT
                    | TypeParameters VOID MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | TypeParameters VOID MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | TypeParameters VOID MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | TypeParameters AnnotationS IDENT MethodDeclarator THROWS IDENT
                    | TypeParameters AnnotationS IDENT MethodDeclarator THROWS IDENT PERIOD IDENT
                    | TypeParameters AnnotationS IDENT MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT
                    | TypeParameters AnnotationS IDENT MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | TypeParameters AnnotationS IDENT MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | TypeParameters AnnotationS IDENT MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | TypeParameters IDENT MethodDeclarator THROWS IDENT
                    | TypeParameters IDENT MethodDeclarator THROWS IDENT PERIOD IDENT
                    | TypeParameters IDENT MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT
                    | TypeParameters IDENT MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | TypeParameters IDENT MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | TypeParameters IDENT MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | TypeParameters AnnotationS UnannType MethodDeclarator
                    | TypeParameters UnannType MethodDeclarator
                    | TypeParameters AnnotationS NumericType MethodDeclarator
                    | TypeParameters NumericType MethodDeclarator
                    | TypeParameters AnnotationS BOOLEAN MethodDeclarator
                    | TypeParameters BOOLEAN MethodDeclarator
                    | TypeParameters AnnotationS VOID MethodDeclarator
                    | TypeParameters VOID MethodDeclarator
                    | TypeParameters AnnotationS IDENT MethodDeclarator
                    | TypeParameters IDENT MethodDeclarator
                    | BOOLEAN MethodDeclarator THROWS IDENT
                    | BOOLEAN MethodDeclarator THROWS IDENT PERIOD IDENT
                    | BOOLEAN MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT
                    | BOOLEAN MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | BOOLEAN MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | BOOLEAN MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | BOOLEAN MethodDeclarator
                    | IDENT MethodDeclarator THROWS IDENT
                    | IDENT MethodDeclarator THROWS IDENT PERIOD IDENT
                    | IDENT MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT
                    | IDENT MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | IDENT MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | IDENT MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | IDENT MethodDeclarator
                    | VOID MethodDeclarator THROWS IDENT
                    | VOID MethodDeclarator THROWS IDENT PERIOD IDENT
                    | VOID MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT
                    | VOID MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | VOID MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | VOID MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | VOID MethodDeclarator
                    | UnannType MethodDeclarator
                    | UnannType MethodDeclarator THROWS IDENT
                    | UnannType MethodDeclarator THROWS IDENT PERIOD IDENT
                    | UnannType MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT
                    | UnannType MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | UnannType MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | UnannType MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | NumericType MethodDeclarator THROWS IDENT
                    | NumericType MethodDeclarator THROWS IDENT PERIOD IDENT
                    | NumericType MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT
                    | NumericType MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | NumericType MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | NumericType MethodDeclarator THROWS IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT PERIOD IDENT
                    | NumericType MethodDeclarator
    '''
    # p[0] = mytuple(["MethodHeader"]+p[1:])

# def p_Result(p):
#     '''Result :  UnannType
#     '''
#     # p[0] = mytuple(["Result"]+p[1 :])


def p_MethodDeclarator(p):
    '''MethodDeclarator : IDENT LPAREN FormalParameterList RPAREN
                        | LPAREN FormalParameterList RPAREN Dims
                        | IDENT LPAREN RPAREN Dims
                        | IDENT LPAREN RPAREN
    '''
    # p[0] = mytuple(["MethodDeclarator"]+p[1:])


def p_FormalParameterList(p):
    '''FormalParameterList :  ReceiverParameter
                            | FormalParameters COMMA LastFormalParameter
                            | LastFormalParameter
                            | FormalParameters
    '''
    # p[0] = mytuple(["FormalParameterList"]+p[1:])


def p_COMMAFormalParameterS(p):
    '''COMMAFormalParameterS : COMMAFormalParameterS COMMA FormalParameter
                            | COMMA FormalParameter
    '''
    # p[0] = mytuple(["COMMAFormalParameterS"]+p[1:])


# def p_VariableModifier(p):
#     '''CommonModifier : Annotation
#                         | FINAL
#     '''
#     # p[0] = mytuple(["CommonModifier"] + p[1 :])


# def p_VariableModifierS(p):
#     '''CommonModifierS : CommonModifier CommonModifierS
#                         | empty
#     '''
#     # p[0] = mytuple(["CommonModifierS"] + p[1 :])

def p_FormalParameters(p):
    '''FormalParameters : FormalParameter COMMAFormalParameterS
                        | ReceiverParameter COMMAFormalParameterS
                        | FormalParameter COMMA FormalParameter
                        | ReceiverParameter COMMA FormalParameter
    '''
    # p[0] = mytuple(["FormalParameters"]+p[1:])


def p_FormalParameter(p):
    '''FormalParameter : CommonModifier UnannType VariableDeclaratorId
                        | CommonModifier NumericType VariableDeclaratorId
                        | CommonModifier BOOLEAN VariableDeclaratorId
                        | CommonModifier IDENT VariableDeclaratorId
                        | CommonModifier UnannType IDENT
                        | CommonModifier NumericType IDENT
                        | CommonModifier BOOLEAN IDENT
                        | CommonModifier IDENT IDENT
                        |  UnannType VariableDeclaratorId
                        |  NumericType VariableDeclaratorId
                        |  BOOLEAN VariableDeclaratorId
                        |  IDENT VariableDeclaratorId
                        |  UnannType IDENT
                        |  NumericType IDENT
                        |  BOOLEAN IDENT
                        |  IDENT IDENT
    '''
    # p[0] = mytuple(["FormalParameter"] + p[1:])


# TODO: Dropped this rule..., p_LastFormalParameter was used only in p_FormalParameterList.
def p_LastFormalParameter(p):
    '''LastFormalParameter : CommonModifierS UnannType AnnotationS ELLIPSIS VariableDeclaratorId
                            | CommonModifierS NumericType AnnotationS ELLIPSIS VariableDeclaratorId
                            | CommonModifierS BOOLEAN AnnotationS ELLIPSIS VariableDeclaratorId
                            | CommonModifierS IDENT AnnotationS ELLIPSIS VariableDeclaratorId
                            | FormalParameter
                            | CommonModifierS UnannType ELLIPSIS VariableDeclaratorId
                            | CommonModifierS NumericType ELLIPSIS VariableDeclaratorId
                            | CommonModifierS BOOLEAN ELLIPSIS VariableDeclaratorId
                            | CommonModifierS IDENT ELLIPSIS VariableDeclaratorId
                            | CommonModifierS UnannType AnnotationS ELLIPSIS IDENT
                            | CommonModifierS NumericType AnnotationS ELLIPSIS IDENT
                            | CommonModifierS BOOLEAN AnnotationS ELLIPSIS IDENT
                            | CommonModifierS IDENT AnnotationS ELLIPSIS IDENT
                            | CommonModifierS UnannType ELLIPSIS IDENT
                            | CommonModifierS NumericType ELLIPSIS IDENT
                            | CommonModifierS BOOLEAN ELLIPSIS IDENT
                            | CommonModifierS IDENT ELLIPSIS IDENT
                            |  UnannType AnnotationS ELLIPSIS VariableDeclaratorId
                            |  NumericType AnnotationS ELLIPSIS VariableDeclaratorId
                            |  BOOLEAN AnnotationS ELLIPSIS VariableDeclaratorId
                            |  IDENT AnnotationS ELLIPSIS VariableDeclaratorId
                            |  UnannType ELLIPSIS VariableDeclaratorId
                            |  NumericType ELLIPSIS VariableDeclaratorId
                            |  BOOLEAN ELLIPSIS VariableDeclaratorId
                            |  IDENT ELLIPSIS VariableDeclaratorId
                            |  UnannType AnnotationS ELLIPSIS IDENT
                            |  BOOLEAN AnnotationS ELLIPSIS IDENT
                            |  IDENT AnnotationS ELLIPSIS IDENT
                            |  UnannType ELLIPSIS IDENT
                            |  BOOLEAN ELLIPSIS IDENT
                            |  IDENT ELLIPSIS IDENT

    '''
    # p[0] = mytuple(["LastFormalParameter"] + p[1:])


def p_ReceiverParameter(p):
    '''ReceiverParameter : AnnotationS UnannType IDENT PERIOD THIS
                            | AnnotationS NumericType IDENT PERIOD THIS
                            | AnnotationS BOOLEAN IDENT PERIOD THIS
                            | AnnotationS IDENT IDENT PERIOD THIS
                            | UnannType IDENT PERIOD THIS
                            | NumericType IDENT PERIOD THIS
                            | BOOLEAN IDENT PERIOD THIS
                            | IDENT IDENT PERIOD THIS
                            | AnnotationS UnannType THIS
                            | AnnotationS NumericType THIS
                            | AnnotationS BOOLEAN THIS
                            | AnnotationS IDENT THIS
                            | UnannType THIS
                            | NumericType THIS
                            | BOOLEAN THIS
                            | IDENT THIS
    '''
    # p[0] = mytuple(["ReceiverParameter"] + p[1:])


def p_Throws(p):
    '''Throws :  THROWS ExceptionTypeList
                | THROWS IDENT
    '''
    # p[0] = mytuple(["Throws"] + p[1:])


def p_COMMAExceptionTypeS(p):
    '''COMMAExceptionTypeS : COMMAExceptionTypeS COMMA ExceptionType
                    | COMMAExceptionTypeS COMMA IDENT
                    | COMMA ExceptionType
                    | COMMA IDENT
    '''
    # p[0] = mytuple(["COMMAExceptionTypeS"] + p[1:])


def p_ExceptionTypeList(p):
    '''ExceptionTypeList : ExceptionType COMMAExceptionTypeS
                    | IDENT COMMAExceptionTypeS
                    | ExceptionType
    '''
    # p[0] = mytuple(["ExceptionTypeList"] + p[1:])


def p_ExceptionType(p):
    ''' ExceptionType :  ClassType
                        | IDENT PERIOD IDENT
                        | TypeVariable
    '''
    # p[0] = mytuple(["ExceptionType"] + p[1:])

#*
def p_MethodBody(p):
    '''MethodBody : Block
    '''
    # p[0] = mytuple(["MethodBody"] + p[1:])
    p[0] = p[1]

# def p_InstanceInitializer(p):
#     '''Block : Block
#     '''
#     # p[0] = mytuple(["Block"] + p[1 :])


def p_StaticInitializer(p):
    '''StaticInitializer : STATIC Block
    '''
    # p[0] = mytuple(["StaticInitializer"] + p[1:])

# def p_ConstructorModifierS(p):
#     '''ConstructorModifierS : ConstructorModifier ConstructorModifierS
#                             | ConstructorModifier
#     '''
#     # p[0] = mytuple(["ConstructorModifierS"] + p[1 :])


def p_ConstructorDeclaration(p):
    '''ConstructorDeclaration : CommonModifierS ConstructorDeclarator ConstructorBody
                                | CommonModifierS ConstructorDeclarator Throws ConstructorBody
                                |  ConstructorDeclarator ConstructorBody
                                |  ConstructorDeclarator Throws ConstructorBody
    '''
    # p[0] = mytuple(["ConstructorDeclaration"] + p[1:])


# def p_ConstructorModifier(p):
#     '''ConstructorModifier : Annotation
#                             | PUBLIC
#                             | PROTECTED
#                             | PRIVATE
#     '''
#     # p[0] = mytuple(["ConstructorModifier"] + p[1 :])

def p_ConstructorDeclarator(p):
    '''ConstructorDeclarator : TypeParameters IDENT LPAREN FormalParameterList RPAREN
                            |  IDENT LPAREN FormalParameterList RPAREN
                            | TypeParameters IDENT LPAREN  RPAREN
                            |  IDENT LPAREN  RPAREN
    '''
    # p[0] = mytuple(["ConstructorDeclarator"] + p[1:])

# def p_SimpleTypeName(p):
#     '''IDENT : IDENT
#     '''
#     # p[0] = mytuple(["IDENT"] + p[1 :])


def p_ConstructorBody(p):
    '''ConstructorBody : LBRACE  ExplicitConstructorInvocation BlockStatements  RBRACE
                        | LBRACE  ExplicitConstructorInvocation SEMICOLON  RBRACE
                        | LBRACE  ExplicitConstructorInvocation  RBRACE
                        | LBRACE  BlockStatements  RBRACE
                        | LBRACE  SEMICOLON  RBRACE
                        | LBRACE  RBRACE
    '''
    # p[0] = mytuple(["ConstructorBody"] + p[1:])

def p_ExplicitConstructorInvocation(p):
    '''ExplicitConstructorInvocation : TypeArguments THIS LPAREN ArgumentList RPAREN SEMICOLON
                                    | TypeArguments THIS LPAREN  RPAREN SEMICOLON
                                    |  THIS LPAREN ArgumentList RPAREN SEMICOLON
                                    |  THIS LPAREN  RPAREN SEMICOLON
                                    | TypeArguments SUPER LPAREN ArgumentList RPAREN SEMICOLON
                                    | TypeArguments SUPER LPAREN  RPAREN SEMICOLON
                                    |  SUPER LPAREN ArgumentList RPAREN SEMICOLON
                                    |  SUPER LPAREN  RPAREN SEMICOLON
                                    | IDENT PERIOD TypeArguments SUPER LPAREN ArgumentList RPAREN SEMICOLON
                                    | IDENT PERIOD  SUPER LPAREN ArgumentList RPAREN SEMICOLON
                                    | IDENT PERIOD TypeArguments SUPER LPAREN  RPAREN SEMICOLON
                                    | IDENT PERIOD  SUPER LPAREN  RPAREN SEMICOLON
                                    | IDENT CommonName PERIOD TypeArguments SUPER LPAREN ArgumentList RPAREN SEMICOLON
                                    | IDENT CommonName PERIOD  SUPER LPAREN ArgumentList RPAREN SEMICOLON
                                    | IDENT CommonName PERIOD TypeArguments SUPER LPAREN  RPAREN SEMICOLON
                                    | IDENT CommonName PERIOD  SUPER LPAREN  RPAREN SEMICOLON
                                    | Primary PERIOD TypeArguments SUPER LPAREN ArgumentList RPAREN SEMICOLON
                                    | Primary PERIOD TypeArguments SUPER LPAREN RPAREN SEMICOLON
                                    | Primary PERIOD  SUPER LPAREN ArgumentList RPAREN SEMICOLON
                                    | Primary PERIOD  SUPER LPAREN  RPAREN SEMICOLON
    '''
    # p[0] = mytuple(["ExplicitConstructorInvocation"] + p[1:])

# def p_ClassModifierS(p):
#     '''ClassModifierS : Annotation ClassModifierS
#                         | PUBLIC ClassModifierS
#                         | PROTECTED ClassModifierS
#                         | PRIVATE ClassModifierS
#                         | FINAL ClassModifierS
#                         | ABSTRACT ClassModifierS
#                         | STATIC ClassModifierS
#                         | STRICTFP ClassModifierS
#                         | empty
#     '''
#     # p[0] = mytuple(["ClassModifierS"] + p[1 :])


def p_EnumDeclaration(p):
    '''EnumDeclaration : CommonModifierS ENUM IDENT Superinterfaces EnumBody
                    | CommonModifierS ENUM IDENT EnumBody
                    |  ENUM IDENT Superinterfaces EnumBody
                    |  ENUM IDENT EnumBody
    '''
    # p[0] = mytuple(["EnumDeclaration"] + p[1:])


def p_EnumBody(p):
    '''EnumBody : LBRACE EnumConstantList COMMA EnumBodyDeclarations  RBRACE
                | LBRACE EnumConstantList COMMA   RBRACE
                | LBRACE EnumConstantList  EnumBodyDeclarations  RBRACE
                | LBRACE EnumConstantList    RBRACE
                | LBRACE COMMA EnumBodyDeclarations  RBRACE
                | LBRACE COMMA   RBRACE
                | LBRACE  EnumBodyDeclarations  RBRACE
                | LBRACE    RBRACE
    '''
    # p[0] = mytuple(["EnumBody"] + p[1:])


def p_COMMAEnumConstantS(p):
    '''COMMAEnumConstantS : COMMAEnumConstantS COMMA EnumConstant
                          | empty
    '''
    # p[0] = mytuple(["COMMAEnumConstantS"] + p[1:])


def p_EnumConstantList(p):
    '''EnumConstantList : EnumConstant COMMAEnumConstantS
    '''
    # p[0] = mytuple(["EnumConstantList"] + p[1:])


def p_EnumConstant(p):
    '''EnumConstant : EnumConstantModifierS IDENT LPAREN RPAREN ClassBody
    | EnumConstantModifierS IDENT LPAREN ArgumentList  RPAREN ClassBody
    | EnumConstantModifierS IDENT  ClassBody
    | EnumConstantModifierS IDENT LPAREN RPAREN
    | EnumConstantModifierS IDENT LPAREN ArgumentList  RPAREN
    | EnumConstantModifierS IDENT
    '''
    # p[0] = mytuple(["EnumConstant"] + p[1:])


def p_EnumConstantModifierS(p):
    '''EnumConstantModifierS : EnumConstantModifierS EnumConstantModifier
                            | empty
    '''
    # p[0] = mytuple(["EnumConstantModifierS"] + p[1:])

#*
def p_EnumConstantModifier(p):
    '''EnumConstantModifier : Annotation
    '''
    # p[0] = mytuple(["EnumConstantModifier"] + p[1:])
    p[0] = p[1]


def p_EnumBodyDeclarations(p):
    '''EnumBodyDeclarations : SEMICOLON ClassBodyDeclarationS
    '''
    # p[0] = mytuple(["EnumBodyDeclarations"] + p[1:])

#</editor-fold> Section 7 : Packages #########################

#<editor-fold> Section 4 #########################
###################################
# Section 4
# #################################

# def p_Type(p):
#     '''Type : PrimitiveType
#             | ReferenceType
#             | IDENT'''
#     p[0]=mytuple(["Type"]+p[1 :])

#


def p_PrimitiveType(p):
    '''PrimitiveType : AnnotationS NumericType
                     | NumericType
                     | AnnotationS BOOLEAN'''
    # p[0] = mytuple(["PrimitiveType"]+p[1:])

# def p_AnnotationS(p):
#     '''AnnotationS : Annotation AnnotationS
#                        | empty '''
#     p[0]=mytuple(["AnnotationS"]+p[1 :])

#

#*
def p_NumericType(p):
    '''NumericType : IntegralType
                   | FloatingPointType'''
    # p[0] = mytuple(["NumericType"]+p[1:])
    p[0] = p[1]
#

#*
def p_IntegralType(p):
    '''IntegralType : BYTE
                    | SHORT
                    | INT
                    | LONG
                    | CHAR'''
    # p[0] = mytuple(["IntegralType"]+p[1:])
    p[0] = Node()
    p[0].type_list = [p[1]]
#

#*
def p_FloatingPointType(p):
    '''FloatingPointType : FLOAT
                         | DOUBLE'''
    # p[0] = mytuple(["FloatingPointType"]+p[1:])
    p[0] = Node()
    p[0].type_list = [p[1]]
#

#*
def p_ReferenceType(p):
    '''ReferenceType : ExceptionType
                     | ArrayType'''
    # p[0] = mytuple(["ReferenceType"]+p[1:])
    p[0] = p[1]
#

# def p_ClassOrInterfaceType(p):
#     '''ClassType : ClassType '''
#     p[0]=mytuple(["ClassType"]+p[1 :])

#

# def p_ClassType(p):
#     '''ClassType : AnnotationS IDENT ZooTypeArguments
#                  | ClassType PERIOD AnnotationS IDENT ZooTypeArguments '''
#     p[0]=mytuple(["ClassType"]+p[1 :])


def p_ClassType(p):
    '''ClassType : TypeVariable TypeArguments
                 | IDENT TypeArguments
                 | ClassType PERIOD TypeVariable TypeArguments
                 | ClassType PERIOD IDENT TypeArguments
                 | IDENT PERIOD TypeVariable TypeArguments
                 | IDENT PERIOD IDENT TypeArguments
                 | ClassType PERIOD TypeVariable
                 | ClassType PERIOD IDENT
                 | IDENT PERIOD TypeVariable'''
    # p[0] = mytuple(["ClassType"]+p[1:])



# def p_InterfaceType(p):
#     '''ClassType : ClassType'''
#     p[0]=mytuple(["ClassType"]+p[1 :])

#
def p_TypeVariable(p):
    '''TypeVariable : AnnotationS IDENT'''
    # p[0] = mytuple(["TypeVariable"]+p[1:])

#


def p_ArrayType(p):
    '''ArrayType :  PrimitiveType Dims
                 | BOOLEAN Dims
                 |  ClassType Dims
                 |  IDENT PERIOD IDENT Dims
                 |  TypeVariable Dims
                 | IDENT Dims'''
    # p[0] = mytuple(["ArrayType"]+p[1:])

#


def p_Dims(p):
    '''Dims : AnnotationS LBRACK RBRACK AnnotationSLBRACKRBRACKS
            | LBRACK RBRACK AnnotationSLBRACKRBRACKS'''
    # p[0] = mytuple(["Dims"]+p[1:])


def p_AnnotationSLBRACKRBRACKS(p):
    '''AnnotationSLBRACKRBRACKS : AnnotationSLBRACKRBRACKS AnnotationS LBRACK RBRACK
                                | AnnotationSLBRACKRBRACKS LBRACK RBRACK
                                | empty '''
    # p[0] = mytuple(["AnnotationSLBRACKRBRACKS"]+p[1:])

#


def p_TypeParameter(p):
    '''TypeParameter :  TypeParameterModifierS IDENT TypeBound
                    | TypeParameterModifierS IDENT'''
    # p[0] = mytuple(["TypeParameter"]+p[1:])


def p_TypeParameterModifierS(p):
    '''TypeParameterModifierS : TypeParameterModifierS TypeParameterModifier
                              | empty '''
    # p[0] = mytuple(["TypeParameterModifierS"]+p[1:])


#*
def p_TypeParameterModifier(p):
    '''TypeParameterModifier : Annotation '''
    # p[0] = mytuple(["TypeParameterModifier"]+p[1:])
    p[0] = p[1]

#


def p_TypeBound(p):
    '''TypeBound : EXTENDS TypeVariable
                 | EXTENDS IDENT
                 | EXTENDS ClassType AdditionalBoundS
                 | EXTENDS ClassType
                 | EXTENDS TypeVariable AdditionalBoundS
                 | EXTENDS IDENT PERIOD IDENT AdditionalBoundS
                 | EXTENDS IDENT PERIOD IDENT
                 | EXTENDS IDENT AdditionalBoundS'''
    # p[0] = mytuple(["TypeBound"]+p[1:])


def p_AdditionalBound(p):
    '''AdditionalBound : AND ClassType
                        | AND TypeVariable
                        | AND IDENT PERIOD IDENT
                        | AND IDENT'''
    # p[0] = mytuple(["AdditionalBound"]+p[1:])

#


def p_TypeArguments(p):
    '''TypeArguments : LSS TypeArgumentList GTR'''
    # p[0] = mytuple(["TypeArguments"]+p[1:])

#


def p_TypeArgumentList(p):
    '''TypeArgumentList : TypeArgument COMMATypeArgumentS
                        |  IDENT COMMATypeArgumentS'''
    # p[0] = mytuple(["TypeArgumentList"]+p[1:])


def p_COMMATypeArgumentS(p):
    '''COMMATypeArgumentS : COMMATypeArgumentS COMMA TypeArgument
                        | COMMATypeArgumentS COMMA IDENT
                          | empty '''
    # p[0] = mytuple(["COMMATypeArgumentS"]+p[1:])

#

#*
def p_TypeArgument(p):
    '''TypeArgument : ReferenceType
                    | Wildcard '''
    # p[0] = mytuple(["TypeArgument"]+p[1:])
    p[0] = p[1]

#


def p_Wildcard(p):
    '''Wildcard : AnnotationS QUES WildcardBounds
                | AnnotationS QUES
                | QUES WildcardBounds
                | QUES'''
    # p[0] = mytuple(["Wildcard"]+p[1:])

def p_WildcardBounds(p):
    '''WildcardBounds : EXTENDS ReferenceType
                      | EXTENDS IDENT
                      | SUPER ReferenceType
                      | SUPER IDENT'''
    # p[0] = mytuple(["WildcardBounds"]+p[1:])

#</editor-fold> Section 4 #########################

#<editor-fold> Section 14 #########################
###################################
# Section 14
# #################################

#*H
def p_Block(p):
    '''Block : LBRACE RBRACE
    | LBRACE BlockStatements RBRACE
    | LBRACE SEMICOLON RBRACE
'''
    if(len(p)==3):
        p[0] = Node()
    elif(type(p[2])==str): #for SEMICOLON
        p[0] = Node()
    else:
        p[0] = p[2]


#*H
def p_BlockStatements(p):
    '''BlockStatements : BlockStatement BlockStatements
                        | SEMICOLON BlockStatements
                        | BlockStatement SEMICOLON
                        | BlockStatement
'''
                        # TODO: This was removed: | SEMICOLON SEMICOLON
    if(len(p)==2):
        p[0] = p[1]
    elif(p[1]==';'):
        p[0] = p[2]
    elif(p[2]==';'):
        p[0] = p[1]
    else:
        p[0] = p[1]
        p[0].id_list += p[2].id_list
        p[0].type_list += p[2].type_list
        p[0].place_list += p[2].place_list
    # p[0] = mytuple(["BlockStatements"]+p[1:])

# def p_BlockStatementsS(p):
#     '''BlockStatementsS : BlockStatement BlockStatementsS
# | empty'''
#     p[0]=mytuple(["BlockStatementsS"]+p[1 :])

#*H
def p_BlockStatement(p):
    '''BlockStatement : LocalVariableDeclarationStatement
                    | ClassDeclaration
                    | Statement
                    '''
    # p[0] = mytuple(["BlockStatement"]+p[1:])
    p[0] = p[1]


#*H
def p_LocalVariableDeclarationStatement(p):
    '''LocalVariableDeclarationStatement : LocalVariableDeclaration SEMICOLON
'''
    p[0] = p[1]
    # p[0] = mytuple(["LocalVariableDeclarationStatement"]+p[1:])


def p_LocalVariableDeclaration(p):
    '''LocalVariableDeclaration : CommonModifierS UnannType VariableDeclaratorList
                                | CommonModifierS NumericType VariableDeclaratorList
                                | CommonModifierS BOOLEAN VariableDeclaratorList
                                | CommonModifierS IDENT VariableDeclaratorList
                                |  UnannType VariableDeclaratorList
                                |  NumericType VariableDeclaratorList
                                |  BOOLEAN VariableDeclaratorList
                                |  IDENT VariableDeclaratorList
                                | CommonModifierS UnannType IDENT
                                | CommonModifierS NumericType IDENT
                                | CommonModifierS BOOLEAN IDENT
                                | CommonModifierS IDENT IDENT
                                |  UnannType IDENT
                                |  NumericType IDENT
                                |  BOOLEAN IDENT
                                |  IDENT IDENT
'''

    if(len(p)==3):
        if( ( p[1]=="true" or p[1] == "false" ) and type(p[2])==str):
            new_n1 = Node()
            new_n1.type_list = ["boolean"]
            new_n2 = Node()
            new_n2.id_list = [p[2]]
            new_n2.type_list = ["identifier"]
            p[0] = new_n1
            p[0].id_list += new_n2.id_list
            p[0].type_list += new_n2.type_list
            p[0].place_list += new_n2.place_list
        elif(type(p[1])==str and type(p[2])==str):
            new_n1 = Node()
            new_n1.id_list = [p[1]]
            new_n1.type_list = ["identifier"]
            new_n2 = Node()
            new_n2.id_list = [p[2]]
            new_n2.type_list = ["identifier"]
            p[0] = new_n1
            p[0].id_list += new_n2.id_list
            p[0].type_list += new_n2.type_list
            p[0].place_list += new_n2.place_list
        elif(type(p[2])==str):
            new_node = Node()
            new_node.id_list = [p[2]]
            new_node.type_list = ["identifier"]
            p[0] = p[1]
            p[0].id_list += new_node.id_list
            p[0].type_list += new_node.type_list
            p[0].place_list += new_node.place_list
        elif(p[1]=="true" or p[1] == "false"):
            new_node = Node()
            new_node.type_list = ["boolean"]
            p[0] = new_node
            p[0].id_list += p[2].id_list
            p[0].type_list += p[2].type_list
            p[0].place_list += p[2].place_list
        elif(type(p[1])==str):
            new_node = Node()
            new_node.id_list = [p[1]]
            new_node.type_list = ["identifier"]
            p[0] = new_node
            p[0].id_list += p[2].id_list
            p[0].type_list += p[2].type_list
            p[0].place_list += p[2].place_list
        else:
            p[0] = p[1]
            p[0].id_list += p[2].id_list
            p[0].type_list += p[2].type_list
            p[0].place_list += p[2].place_list
    else:
        if(type(p[3])==str):
            if( p[2]=="true" or p[2] == "false" ):
                new_n1 = Node()
                new_n1.type_list = ["boolean"]
                new_n2 = Node()
                new_n2.id_list = [p[3]]
                new_n2.type_list = ["identifier"]
                p[0] = p[1]
                p[0].id_list += new_n1.id_list
                p[0].type_list += new_n1.type_list
                p[0].place_list += new_n1.place_list
                p[0].id_list += new_n2.id_list
                p[0].type_list += new_n2.type_list
                p[0].place_list += new_n2.place_list
            elif(type(p[2]) ==str):
                new_n1 = Node()
                new_n2.id_list = [p[2]]
                new_n2.type_list = ["identifier"]
                new_n2 = Node()
                new_n2.id_list = [p[3]]
                new_n2.type_list = ["identifier"]
                p[0] = p[1]
                p[0].id_list += new_n1.id_list
                p[0].type_list += new_n1.type_list
                p[0].place_list += new_n1.place_list
                p[0].id_list += new_n2.id_list
                p[0].type_list += new_n2.type_list
                p[0].place_list += new_n2.place_list
            else:
                new_n2 = Node()
                new_n2.id_list = [p[3]]
                new_n2.type_list = ["identifier"]
                p[0] = p[1]
                p[0].id_list += p[2].id_list
                p[0].type_list += p[2].type_list
                p[0].place_list += p[2].place_list
                p[0].id_list += new_n2.id_list
                p[0].type_list += new_n2.type_list
                p[0].place_list += new_n2.place_list
        else:
            if( p[2]=="true" or p[2] == "false" ):
                new_n1 = Node()
                new_n1.type_list = ["boolean"]

                p[0] = p[1]
                p[0].id_list += new_n1.id_list
                p[0].type_list += new_n1.type_list
                p[0].place_list += new_n1.place_list
                p[0].id_list += p[3].id_list
                p[0].type_list += p[3].type_list
                p[0].place_list += p[3].place_list
            elif(type(p[2]) ==str):
                new_n1 = Node()
                new_n2.id_list = [p[2]]
                new_n2.type_list = ["identifier"]
                p[0] = p[1]
                p[0].id_list += new_n1.id_list
                p[0].type_list += new_n1.type_list
                p[0].place_list += new_n1.place_list
                p[0].id_list += p[3].id_list
                p[0].type_list += p[3].type_list
                p[0].place_list += p[3].place_list
            else:
                p[0] = p[1]
                p[0].id_list += p[2].id_list
                p[0].type_list += p[2].type_list
                p[0].place_list += p[2].place_list
                p[0].id_list += p[3].id_list
                p[0].type_list += p[3].type_list
                p[0].place_list += p[3].place_list
    # p[0] = mytuple(["LocalVariableDeclaration"]+p[1:])
# def p_VariableModifierS(p):
#     '''CommonModifierS : CommonModifier CommonModifierS
# | empty'''
#     p[0]=mytuple(["CommonModifierS"]+p[1 :])

#*H
def p_Statement(p):
    '''Statement : StatementWithoutTrailingSubstatement
        | LabeledStatement
        | IfThenStatement
        | IfThenElseStatement
        | WhileStatement
        | ForStatement
        '''
    p[0] = p[1]
    # p[0] = mytuple(["Statement"]+p[1:])

#*
def p_StatementNoShortIf(p):
    '''StatementNoShortIf : StatementWithoutTrailingSubstatement
| LabeledStatementNoShortIf
| IfThenElseStatementNoShortIf
| WhileStatementNoShortIf
| ForStatementNoShortIf
'''
    # p[0] = mytuple(["StatementNoShortIf"]+p[1:])
    p[0] = p[1]

#*
def p_StatementWithoutTrailingSubstatement(p):
    '''StatementWithoutTrailingSubstatement : Block
            | ExpressionStatement
            | AssertStatement
            | SwitchStatement
            | DoStatement
            | BreakStatement
            | ContinueStatement
            | ReturnStatement
            | SynchronizedStatement
            | ThrowStatement
            | TryStatement
            '''
    # p[0] = mytuple(["StatementWithoutTrailingSubstatement"]+p[1:])
    p[0] = p[1]

# def p_EmptyStatement(p):
#     '''EmptyStatement : SEMICOLON
# '''
#     p[0]=mytuple(["EmptyStatement"]+p[1 :])


def p_LabeledStatement(p):
    '''LabeledStatement : IDENT  COLON  Statement
                    | IDENT COLON SEMICOLON
'''
    # p[0] = mytuple(["LabeledStatement"]+p[1:])


def p_LabeledStatementNoShortIf(p):
    '''LabeledStatementNoShortIf : IDENT  COLON  StatementNoShortIf
                        | IDENT COLON SEMICOLON
'''
    # p[0] = mytuple(["LabeledStatementNoShortIf"]+p[1:])


def p_ExpressionStatement(p):
    '''ExpressionStatement : StatementExpression SEMICOLON
'''
    # p[0] = mytuple(["ExpressionStatement"]+p[1:])

#*
def p_StatementExpression(p):
    '''StatementExpression : Assignment
| PreIncrementExpression
| PreDecrementExpression
| PostIncrementExpression
| PostDecrementExpression
| MethodInvocation
| ClassInstanceCreationExpression
'''
    # p[0] = mytuple(["StatementExpression"]+p[1:])
    p[0] = p[1]


def p_IfThenStatement(p):
    '''IfThenStatement : IF LPAREN Expression RPAREN Statement
        | IF LPAREN Expression RPAREN SEMICOLON
'''
    # p[0] = mytuple(["IfThenStatement"]+p[1:])


def p_IfThenElseStatement(p):
    '''IfThenElseStatement : IF LPAREN Expression RPAREN StatementNoShortIf ELSE Statement
            | IF LPAREN Expression RPAREN SEMICOLON ELSE Statement
            | IF LPAREN Expression RPAREN StatementNoShortIf ELSE SEMICOLON
            | IF LPAREN Expression RPAREN SEMICOLON ELSE SEMICOLON
'''
    # p[0] = mytuple(["IfThenElseStatement"]+p[1:])


def p_IfThenElseStatementNoShortIf(p):
    '''IfThenElseStatementNoShortIf : IF LPAREN Expression RPAREN StatementNoShortIf ELSE StatementNoShortIf
        | IF LPAREN Expression RPAREN SEMICOLON ELSE StatementNoShortIf
        | IF LPAREN Expression RPAREN StatementNoShortIf ELSE SEMICOLON
        | IF LPAREN Expression RPAREN SEMICOLON ELSE SEMICOLON
'''
    # p[0] = mytuple(["IfThenElseStatementNoShortIf"]+p[1:])


def p_AssertStatement(p):
    '''AssertStatement : ASSERT Expression SEMICOLON
| ASSERT Expression  COLON  Expression SEMICOLON
'''
    # p[0] = mytuple(["AssertStatement"]+p[1:])
    if higher(p[2].type_list[0], 'boolean') != 'boolean':
        NameError(str(p.lineno(1)) + ": Losst conversion from " + p[2].type_list[0] + " to boolean.")
    else:
        #
        # the type of expresion is boolean
        tmp = 1

def p_SwitchStatement(p):
    '''SwitchStatement : SWITCH LPAREN Expression RPAREN SwitchBlock
'''
    # p[0] = mytuple(["SwitchStatement"]+p[1:])
    if higher(p[3].type_list[0], 'int') != 'int':
        NameError(str(p.lineno(1)) + ": Losst conversion from " + p[3].type_list[0] + " to int.")
    else:
        #
        # the type of expresion is fine
        # TODO (anay): add code to type_cast expression to int.
        tmp = 1 ## type_cast


def p_SwitchBlock(p):
    '''SwitchBlock : LBRACE SwitchBlockStatementGroupS SwitchLabels RBRACE
            | LBRACE SwitchBlockStatementGroupS DEFAULTCOLON RBRACE
            | LBRACE SwitchBlockStatementGroupS RBRACE
'''
    # p[0] = mytuple(["SwitchBlock"]+p[1:])


def p_DEFAULTCOLON(p):
    '''DEFAULTCOLON : DEFAULT COLON'''
    # p[0] = mytuple(["DEFAULTCOLON"]+p[1:])


def p_SwitchBlockStatementGroupS(p):
    '''SwitchBlockStatementGroupS : SwitchBlockStatementGroupS SwitchBlockStatementGroup
| empty'''
    # p[0] = mytuple(["SwitchBlockStatementGroupS"]+p[1:])

# def p_SwitchBlockStatementGroupS(p):
#     '''SwitchBlockStatementGroupS : SwitchBlockStatementGroup SwitchBlockStatementGroupS
# | empty'''
#     p[0]=mytuple(["SwitchBlockStatementGroupS"]+p[1 :])


def p_SwitchBlockStatementGroup(p):
    '''SwitchBlockStatementGroup : SwitchLabels BlockStatements
                                    | SwitchLabels SEMICOLON
                                    | DEFAULTCOLON BlockStatements
                                    | DEFAULTCOLON SEMICOLON
'''
    # p[0] = mytuple(["SwitchBlockStatementGroup"]+p[1:])


def p_SwitchLabels(p):
    '''SwitchLabels : SwitchLabels SwitchLabel
                    | SwitchLabels DEFAULT  COLON
                    | SwitchLabel
'''
    # p[0] = mytuple(["SwitchLabels"]+p[1:])

# def p_SwitchLabelS(p):
#     '''SwitchLabelS : SwitchLabelS SwitchLabel
# | empty'''
#     p[0]=mytuple(["SwitchLabelS"]+p[1 :])


# DOUBT (anay): removed the following rule   `| CASE IDENT COLON`
# incorrect grammar as per codechef.
def p_SwitchLabel(p):
    '''SwitchLabel : CASE ConstantExpression COLON'''
    # p[0] = mytuple(["SwitchLabel"]+p[1:])

# def p_EnumConstantName(p):
#     '''IDENT : IDENT
# '''
#     p[0]=mytuple(["IDENT"]+p[1 :])


def p_WhileStatement(p):
    '''WhileStatement : WHILE LPAREN Expression RPAREN Statement
        | WHILE LPAREN Expression RPAREN SEMICOLON'''
    # p[0] = mytuple(["WhileStatement"]+p[1:])
    if higher(p[3].type_list[0], 'boolean') != 'boolean':
        NameError(str(p.lineno(1)) + ": Losst conversion from " + p[3].type_list[0] + " to boolean.")
    else:
        #
        # the type of expresion is boolean
        tmp = 1

def p_WhileStatementNoShortIf(p):
    '''WhileStatementNoShortIf : WHILE LPAREN Expression RPAREN StatementNoShortIf
        | WHILE LPAREN Expression RPAREN SEMICOLON'''
    # p[0] = mytuple(["WhileStatementNoShortIf"]+p[1:])
    if higher(p[3].type_list[0], 'boolean') != 'boolean':
        NameError(str(p.lineno(1)) + ": Losst conversion from " + p[3].type_list[0] + " to boolean.")
    else:
        #
        # the type of expresion is boolean
        tmp = 1


def p_DoStatement(p):
    '''DoStatement : DO Statement WHILE LPAREN Expression RPAREN SEMICOLON
                   | DO SEMICOLON WHILE LPAREN Expression RPAREN SEMICOLON'''
    # p[0] = mytuple(["DoStatement"]+p[1:])
    if higher(p[5].type_list[0], 'boolean') != 'boolean':
        NameError(str(p.lineno(1)) + ": Losst conversion from " + p[5].type_list[0] + " to boolean.")
    else:
        #
        # the type of expresion is boolean
        tmp = 1


def p_ForStatement(p):
    '''ForStatement : BasicForStatement
                    | EnhancedForStatement'''
    # p[0] = mytuple(["ForStatement"]+p[1:])


def p_ForStatementNoShortIf(p):
    '''ForStatementNoShortIf : BasicForStatementNoShortIf
                             | EnhancedForStatementNoShortIf'''
    # p[0] = mytuple(["ForStatementNoShortIf"]+p[1:])

# | FOR LPAREN ForInit SEMICOLON Expression SEMICOLON ForUpdate RPAREN Statement 10
# | FOR LPAREN ForInit SEMICOLON Expression SEMICOLON ForUpdate RPAREN SEMICOLON 10
# | FOR LPAREN ForInit SEMICOLON Expression SEMICOLON RPAREN Statement 9
# | FOR LPAREN ForInit SEMICOLON Expression SEMICOLON RPAREN SEMICOLON 9
# | FOR LPAREN ForInit SEMICOLON SEMICOLON ForUpdate RPAREN Statement 9
# | FOR LPAREN ForInit SEMICOLON SEMICOLON ForUpdate RPAREN SEMICOLON 9
# | FOR LPAREN SEMICOLON Expression SEMICOLON ForUpdate RPAREN Statement 9
# | FOR LPAREN SEMICOLON Expression SEMICOLON ForUpdate RPAREN SEMICOLON 9
# | FOR LPAREN ForInit SEMICOLON SEMICOLON  RPAREN Statement 8
# | FOR LPAREN SEMICOLON Expression SEMICOLON RPAREN Statement 8
# | FOR LPAREN SEMICOLON Expression SEMICOLON RPAREN SEMICOLON 8
# | FOR LPAREN SEMICOLON SEMICOLON ForUpdate RPAREN Statement 8
# | FOR LPAREN SEMICOLON SEMICOLON ForUpdate RPAREN SEMICOLON 8
# | FOR LPAREN ForInit SEMICOLON SEMICOLON  RPAREN SEMICOLON 8
# | FOR LPAREN SEMICOLON SEMICOLON  RPAREN Statement 7
# | FOR LPAREN SEMICOLON SEMICOLON  RPAREN SEMICOLON 7

def p_BasicForStatement(p):
    '''BasicForStatement : FOR LPAREN ForInit SEMICOLON Expression SEMICOLON ForUpdate RPAREN Statement
    | FOR LPAREN ForInit SEMICOLON Expression SEMICOLON ForUpdate RPAREN SEMICOLON
    | FOR LPAREN ForInit SEMICOLON Expression SEMICOLON RPAREN Statement
    | FOR LPAREN ForInit SEMICOLON Expression SEMICOLON RPAREN SEMICOLON
    | FOR LPAREN ForInit SEMICOLON SEMICOLON ForUpdate RPAREN Statement
    | FOR LPAREN ForInit SEMICOLON SEMICOLON ForUpdate RPAREN SEMICOLON
    | FOR LPAREN SEMICOLON Expression SEMICOLON ForUpdate RPAREN Statement
    | FOR LPAREN SEMICOLON Expression SEMICOLON ForUpdate RPAREN SEMICOLON
    | FOR LPAREN ForInit SEMICOLON SEMICOLON  RPAREN Statement
    | FOR LPAREN SEMICOLON Expression SEMICOLON RPAREN Statement
    | FOR LPAREN SEMICOLON Expression SEMICOLON RPAREN SEMICOLON
    | FOR LPAREN SEMICOLON SEMICOLON ForUpdate RPAREN Statement
    | FOR LPAREN SEMICOLON SEMICOLON ForUpdate RPAREN SEMICOLON
    | FOR LPAREN ForInit SEMICOLON SEMICOLON  RPAREN SEMICOLON
    | FOR LPAREN SEMICOLON SEMICOLON  RPAREN Statement
    | FOR LPAREN SEMICOLON SEMICOLON  RPAREN SEMICOLON
'''
    # p[0] = mytuple(["BasicForStatement"]+p[1:])
    if len(p) ==  10:
        if higher(p[5].type_list[0], 'boolean') != 'boolean':
            NameError(str(p.lineno(1)) + ": Losst conversion from " + p[5].type_list[0] + " to boolean.")
        else:
            tmp = 1
    elif len(p) == 9:
        if p[3] != ";" and p[5] != ";" and higher(p[5].type_list[0], 'boolean') != 'boolean':
            NameError(str(p.lineno(1)) + ": Losst conversion from " + p[5].type_list[0] + " to boolean.")
        elif p[3] == ";" and higher(p[5].type_list[0], 'boolean') != 'boolean':
            NameError(str(p.lineno(1)) + ": Losst conversion from " + p[5].type_list[0] + " to boolean.")
        else:
            tmp = 1
    elif len(p) == 8:
        if p[3] == ";" and p[4] != ";" and higher(p[4].type_list[0], 'boolean') != 'boolean':
            NameError(str(p.lineno(1)) + ": Losst conversion from " + p[4].type_list[0] + " to boolean.")
        else:
            tmp = 1
    elif len(p) == 7:
        tmp = 1

# | FOR LPAREN ForInit SEMICOLON Expression SEMICOLON ForUpdate RPAREN StatementNoShortIf 10
# | FOR LPAREN ForInit SEMICOLON Expression SEMICOLON ForUpdate RPAREN SEMICOLON 10
# | FOR LPAREN ForInit SEMICOLON Expression SEMICOLON RPAREN StatementNoShortIf 9
# | FOR LPAREN ForInit SEMICOLON Expression SEMICOLON RPAREN SEMICOLON 9
# | FOR LPAREN ForInit SEMICOLON SEMICOLON ForUpdate RPAREN StatementNoShortIf 9
# | FOR LPAREN ForInit SEMICOLON SEMICOLON ForUpdate RPAREN SEMICOLON 9
# | FOR LPAREN SEMICOLON Expression SEMICOLON ForUpdate RPAREN StatementNoShortIf 9
# | FOR LPAREN SEMICOLON Expression SEMICOLON ForUpdate RPAREN SEMICOLON 9
# | FOR LPAREN ForInit SEMICOLON SEMICOLON RPAREN StatementNoShortIf 8
# | FOR LPAREN ForInit SEMICOLON SEMICOLON RPAREN SEMICOLON 8
# | FOR LPAREN SEMICOLON Expression SEMICOLON RPAREN StatementNoShortIf 8
# | FOR LPAREN SEMICOLON Expression SEMICOLON RPAREN SEMICOLON 8
# | FOR LPAREN SEMICOLON SEMICOLON ForUpdate RPAREN StatementNoShortIf 8
# | FOR LPAREN SEMICOLON SEMICOLON ForUpdate RPAREN SEMICOLON 8
# | FOR LPAREN SEMICOLON SEMICOLON RPAREN StatementNoShortIf 7
# | FOR LPAREN SEMICOLON SEMICOLON RPAREN SEMICOLON 7

def p_BasicForStatementNoShortIf(p):
    '''BasicForStatementNoShortIf : FOR LPAREN ForInit SEMICOLON Expression SEMICOLON ForUpdate RPAREN StatementNoShortIf
                                | FOR LPAREN ForInit SEMICOLON Expression SEMICOLON ForUpdate RPAREN SEMICOLON
                                | FOR LPAREN ForInit SEMICOLON Expression SEMICOLON RPAREN StatementNoShortIf
                                | FOR LPAREN ForInit SEMICOLON Expression SEMICOLON RPAREN SEMICOLON
                                | FOR LPAREN ForInit SEMICOLON SEMICOLON ForUpdate RPAREN StatementNoShortIf
                                | FOR LPAREN ForInit SEMICOLON SEMICOLON ForUpdate RPAREN SEMICOLON
                                | FOR LPAREN SEMICOLON Expression SEMICOLON ForUpdate RPAREN StatementNoShortIf
                                | FOR LPAREN SEMICOLON Expression SEMICOLON ForUpdate RPAREN SEMICOLON
                                | FOR LPAREN ForInit SEMICOLON SEMICOLON RPAREN StatementNoShortIf
                                | FOR LPAREN ForInit SEMICOLON SEMICOLON RPAREN SEMICOLON
                                | FOR LPAREN SEMICOLON Expression SEMICOLON RPAREN StatementNoShortIf
                                | FOR LPAREN SEMICOLON Expression SEMICOLON RPAREN SEMICOLON
                                | FOR LPAREN SEMICOLON SEMICOLON ForUpdate RPAREN StatementNoShortIf
                                | FOR LPAREN SEMICOLON SEMICOLON ForUpdate RPAREN SEMICOLON
                                | FOR LPAREN SEMICOLON SEMICOLON RPAREN StatementNoShortIf
                                | FOR LPAREN SEMICOLON SEMICOLON RPAREN SEMICOLON'''
    # p[0] = mytuple(["BasicForStatementNoShortIf"]+p[1:])
    if len(p) ==  10:
        if higher(p[5].type_list[0], 'boolean') != 'boolean':
            NameError(str(p.lineno(1)) + ": Losst conversion from " + p[5].type_list[0] + " to boolean.")
        else:
            tmp = 1
    elif len(p) == 9:
        if p[3] != ";" and p[5] != ";" and higher(p[5].type_list[0], 'boolean') != 'boolean':
            NameError(str(p.lineno(1)) + ": Losst conversion from " + p[5].type_list[0] + " to boolean.")
        elif p[3] == ";" and higher(p[5].type_list[0], 'boolean') != 'boolean':
            NameError(str(p.lineno(1)) + ": Losst conversion from " + p[5].type_list[0] + " to boolean.")
        else:
            tmp = 1
    elif len(p) == 8:
        if p[3] == ";" and p[4] != ";" and higher(p[4].type_list[0], 'boolean') != 'boolean':
            NameError(str(p.lineno(1)) + ": Losst conversion from " + p[4].type_list[0] + " to boolean.")
        else:
            tmp = 1
    elif len(p) == 7:
        tmp = 1


def p_ForInit(p):
    '''ForInit : StatementExpressionList
               | LocalVariableDeclaration'''
    # p[0] = mytuple(["ForInit"]+p[1:])


def p_ForUpdate(p):
    '''ForUpdate : StatementExpressionList
'''
    # p[0] = mytuple(["ForUpdate"]+p[1:])


def p_StatementExpressionList(p):
    '''StatementExpressionList : StatementExpression COMMAStatementExpressionS
'''
    # p[0] = mytuple(["StatementExpressionList"]+p[1:])


def p_COMMAStatementExpressionS(p):
    '''COMMAStatementExpressionS : COMMAStatementExpressionS COMMA StatementExpression
                    | empty'''
    # p[0] = mytuple(["COMMAStatementExpressionS"]+p[1:])

# Skipped! (anay)
def p_EnhancedForStatement(p):
    '''EnhancedForStatement : FOR LPAREN CommonModifierS UnannType VariableDeclaratorId  COLON  Expression RPAREN Statement
                            | FOR LPAREN CommonModifierS NumericType VariableDeclaratorId  COLON  Expression RPAREN Statement
                            | FOR LPAREN CommonModifierS BOOLEAN VariableDeclaratorId  COLON  Expression RPAREN Statement
                            | FOR LPAREN CommonModifierS IDENT VariableDeclaratorId  COLON  Expression RPAREN Statement
                            | FOR LPAREN CommonModifierS UnannType IDENT  COLON  Expression RPAREN Statement
                            | FOR LPAREN CommonModifierS NumericType IDENT  COLON  Expression RPAREN Statement
                            | FOR LPAREN CommonModifierS BOOLEAN IDENT  COLON  Expression RPAREN Statement
                            | FOR LPAREN CommonModifierS IDENT IDENT  COLON  Expression RPAREN Statement
                            | FOR LPAREN UnannType VariableDeclaratorId  COLON  Expression RPAREN Statement
                            | FOR LPAREN NumericType VariableDeclaratorId  COLON  Expression RPAREN Statement
                            | FOR LPAREN BOOLEAN VariableDeclaratorId  COLON  Expression RPAREN Statement
                            | FOR LPAREN IDENT VariableDeclaratorId  COLON  Expression RPAREN Statement
                            | FOR LPAREN UnannType IDENT  COLON  Expression RPAREN Statement
                            | FOR LPAREN NumericType IDENT  COLON  Expression RPAREN Statement
                            | FOR LPAREN BOOLEAN IDENT  COLON  Expression RPAREN Statement
                            | FOR LPAREN IDENT IDENT  COLON  Expression RPAREN Statement
                            | FOR LPAREN CommonModifierS UnannType VariableDeclaratorId  COLON  Expression RPAREN SEMICOLON
                            | FOR LPAREN CommonModifierS NumericType VariableDeclaratorId  COLON  Expression RPAREN SEMICOLON
                            | FOR LPAREN CommonModifierS BOOLEAN VariableDeclaratorId  COLON  Expression RPAREN SEMICOLON
                            | FOR LPAREN CommonModifierS IDENT VariableDeclaratorId  COLON  Expression RPAREN SEMICOLON
                            | FOR LPAREN CommonModifierS UnannType IDENT  COLON  Expression RPAREN SEMICOLON
                            | FOR LPAREN CommonModifierS NumericType IDENT  COLON  Expression RPAREN SEMICOLON
                            | FOR LPAREN CommonModifierS BOOLEAN IDENT  COLON  Expression RPAREN SEMICOLON
                            | FOR LPAREN CommonModifierS IDENT IDENT  COLON  Expression RPAREN SEMICOLON
                            | FOR LPAREN UnannType VariableDeclaratorId  COLON  Expression RPAREN SEMICOLON
                            | FOR LPAREN NumericType VariableDeclaratorId  COLON  Expression RPAREN SEMICOLON
                            | FOR LPAREN BOOLEAN VariableDeclaratorId  COLON  Expression RPAREN SEMICOLON
                            | FOR LPAREN IDENT VariableDeclaratorId  COLON  Expression RPAREN SEMICOLON
                            | FOR LPAREN UnannType IDENT  COLON  Expression RPAREN SEMICOLON
                            | FOR LPAREN NumericType IDENT  COLON  Expression RPAREN SEMICOLON
                            | FOR LPAREN BOOLEAN IDENT  COLON  Expression RPAREN SEMICOLON
                            | FOR LPAREN IDENT IDENT  COLON  Expression RPAREN SEMICOLON
'''
    # p[0] = mytuple(["EnhancedForStatement"]+p[1:])


# Skipped! (anay)
def p_EnhancedForStatementNoShortIf(p):
    '''EnhancedForStatementNoShortIf : FOR LPAREN CommonModifierS UnannType VariableDeclaratorId  COLON  Expression RPAREN StatementNoShortIf
                                    | FOR LPAREN CommonModifierS NumericType VariableDeclaratorId  COLON  Expression RPAREN StatementNoShortIf
                                    | FOR LPAREN CommonModifierS BOOLEAN VariableDeclaratorId  COLON  Expression RPAREN StatementNoShortIf
                                    | FOR LPAREN CommonModifierS IDENT VariableDeclaratorId  COLON  Expression RPAREN StatementNoShortIf
                                    | FOR LPAREN CommonModifierS UnannType IDENT  COLON  Expression RPAREN StatementNoShortIf
                                    | FOR LPAREN CommonModifierS NumericType IDENT  COLON  Expression RPAREN StatementNoShortIf
                                    | FOR LPAREN CommonModifierS BOOLEAN IDENT  COLON  Expression RPAREN StatementNoShortIf
                                    | FOR LPAREN CommonModifierS IDENT IDENT  COLON  Expression RPAREN StatementNoShortIf
                                    | FOR LPAREN  UnannType VariableDeclaratorId  COLON  Expression RPAREN StatementNoShortIf
                                    | FOR LPAREN  NumericType VariableDeclaratorId  COLON  Expression RPAREN StatementNoShortIf
                                    | FOR LPAREN  BOOLEAN VariableDeclaratorId  COLON  Expression RPAREN StatementNoShortIf
                                    | FOR LPAREN  IDENT VariableDeclaratorId  COLON  Expression RPAREN StatementNoShortIf
                                    | FOR LPAREN  UnannType IDENT  COLON  Expression RPAREN StatementNoShortIf
                                    | FOR LPAREN  NumericType IDENT  COLON  Expression RPAREN StatementNoShortIf
                                    | FOR LPAREN  BOOLEAN IDENT  COLON  Expression RPAREN StatementNoShortIf
                                    | FOR LPAREN  IDENT IDENT  COLON  Expression RPAREN StatementNoShortIf
                                    | FOR LPAREN CommonModifierS UnannType VariableDeclaratorId  COLON  Expression RPAREN SEMICOLON
                                    | FOR LPAREN CommonModifierS NumericType VariableDeclaratorId  COLON  Expression RPAREN SEMICOLON
                                    | FOR LPAREN CommonModifierS BOOLEAN VariableDeclaratorId  COLON  Expression RPAREN SEMICOLON
                                    | FOR LPAREN CommonModifierS IDENT VariableDeclaratorId  COLON  Expression RPAREN SEMICOLON
                                    | FOR LPAREN CommonModifierS UnannType IDENT  COLON  Expression RPAREN SEMICOLON
                                    | FOR LPAREN CommonModifierS NumericType IDENT  COLON  Expression RPAREN SEMICOLON
                                    | FOR LPAREN CommonModifierS BOOLEAN IDENT  COLON  Expression RPAREN SEMICOLON
                                    | FOR LPAREN CommonModifierS IDENT IDENT  COLON  Expression RPAREN SEMICOLON
                                    | FOR LPAREN  UnannType VariableDeclaratorId  COLON  Expression RPAREN SEMICOLON
                                    | FOR LPAREN  NumericType VariableDeclaratorId  COLON  Expression RPAREN SEMICOLON
                                    | FOR LPAREN  BOOLEAN VariableDeclaratorId  COLON  Expression RPAREN SEMICOLON
                                    | FOR LPAREN  IDENT VariableDeclaratorId  COLON  Expression RPAREN SEMICOLON
                                    | FOR LPAREN  UnannType IDENT  COLON  Expression RPAREN SEMICOLON
                                    | FOR LPAREN  NumericType IDENT  COLON  Expression RPAREN SEMICOLON
                                    | FOR LPAREN  BOOLEAN IDENT  COLON  Expression RPAREN SEMICOLON
                                    | FOR LPAREN  IDENT IDENT  COLON  Expression RPAREN SEMICOLON
'''
    # p[0] = mytuple(["EnhancedForStatementNoShortIf"]+p[1:])


def p_BreakStatement(p):
    '''BreakStatement : BREAK SEMICOLON
                    | BREAK IDENT SEMICOLON
'''
    # p[0] = mytuple(["BreakStatement"]+p[1:])


def p_ContinueStatement(p):
    '''ContinueStatement : CONTINUE IDENT SEMICOLON
                        | CONTINUE SEMICOLON
'''
    # p[0] = mytuple(["ContinueStatement"]+p[1:])


def p_ReturnStatement(p):
    '''ReturnStatement : RETURN Expression SEMICOLON
                    |  RETURN  SEMICOLON
'''
    # p[0] = mytuple(["ReturnStatement"]+p[1:])
    if len(p) == 3:
        p[0].extra["return_type"] = p[2].type_list[0]
    else
        p[0].extra["return_type"] = "void"



def p_ThrowStatement(p):
    '''ThrowStatement : THROW Expression SEMICOLON
'''
    # p[0] = mytuple(["ThrowStatement"]+p[1:])

# Skipped! (anay)
def p_SynchronizedStatement(p):
    '''SynchronizedStatement : SYNCHRONIZED LPAREN Expression RPAREN Block
'''
    # p[0] = mytuple(["SynchronizedStatement"]+p[1:])


def p_TryStatement(p):
    '''TryStatement : TRY Block Catches
    | TRY Block  Finally
    | TRY Block Catches Finally
    | TryWithResourcesStatement'''
    # p[0] = mytuple(["TryStatement"]+p[1:])

def p_Catches(p):
    '''Catches : CatchClause CatchClauseS'''
    # p[0] = mytuple(["Catches"]+p[1:])


def p_CatchClauseS(p):
    '''CatchClauseS : CatchClauseS CatchClause
                    | empty'''
    # p[0] = mytuple(["CatchClauseS"]+p[1:])


def p_CatchClause(p):
    '''CatchClause : CATCH LPAREN CatchFormalParameter RPAREN Block'''
    # p[0] = mytuple(["CatchClause"]+p[1:])


def p_CatchFormalParameter(p):
    '''CatchFormalParameter : CommonModifierS CatchType VariableDeclaratorId
                            | CommonModifierS CatchType IDENT
                            | CatchType VariableDeclaratorId
                            | CatchType IDENT
'''
    # p[0] = mytuple(["CatchFormalParameter"]+p[1:])


def p_CatchType(p):
    '''CatchType : UnannClassType ORClassTypeS
                | IDENT PERIOD IDENT ORClassTypeS
                | IDENT ORClassTypeS'''
    # p[0] = mytuple(["CatchType"]+p[1:])


def p_ORClassTypeS(p):
    '''ORClassTypeS : ORClassTypeS OR ClassType
                    | ORClassTypeS OR TypeVariable
                    | ORClassTypeS OR IDENT PERIOD IDENT
                    | ORClassTypeS OR IDENT
                    | empty'''
    # p[0] = mytuple(["ORClassTypeS"]+p[1:])


def p_Finally(p):
    '''Finally : FINALLY Block'''
    # p[0] = mytuple(["Finally"]+p[1:])


def p_TryWithResourcesStatement(p):
    '''TryWithResourcesStatement : TRY ResourceSpecification Block Catches Finally
                                | TRY ResourceSpecification Block  Finally
                                | TRY ResourceSpecification Block Catches
                                | TRY ResourceSpecification Block
'''
    # p[0] = mytuple(["TryWithResourcesStatement"]+p[1:])


def p_ResourceSpecification(p):
    '''ResourceSpecification : LPAREN ResourceList SEMICOLON RPAREN
                            | LPAREN ResourceList RPAREN
'''
    # p[0] = mytuple(["ResourceSpecification"]+p[1:])


def p_ResourceList(p):
    '''ResourceList : Resource SEMICOLONResourceS
                | Resource
'''
    # p[0] = mytuple(["ResourceList"]+p[1:])


def p_SEMICOLONResourceS(p):
    '''SEMICOLONResourceS : SEMICOLONResourceS SEMICOLON Resource
                    | SEMICOLON Resource'''
    # p[0] = mytuple(["SEMICOLONResourceS"]+p[1:])


def p_CommonModifierS(p):
    '''CommonModifierS : CommonModifierS CommonModifier
                        | CommonModifier
    '''
    # p[0] = mytuple(["CommonModifierS"]+p[1:])


def p_CommonModifier(p):
    '''CommonModifier : Annotation
                    | PUBLIC
                    | PROTECTED
                    | PRIVATE
                     | STATIC
                     | FINAL
                     | TRANSIENT
                     | VOLATILE
                     | ABSTRACT
                     | SYNCHRONIZED
                    | NATIVE
                    | STRICTFP
    '''
    # TODO: Remove annotation
    # p[0] = mytuple(["CommonModifier"]+p[1:])


def p_Resource(p):
    '''Resource : CommonModifierS UnannType VariableDeclaratorId ASSIGN Expression
                | CommonModifierS NumericType VariableDeclaratorId ASSIGN Expression
                | CommonModifierS BOOLEAN VariableDeclaratorId ASSIGN Expression
                | CommonModifierS IDENT VariableDeclaratorId ASSIGN Expression
                | CommonModifierS UnannType IDENT ASSIGN Expression
                | CommonModifierS NumericType IDENT ASSIGN Expression
                | CommonModifierS BOOLEAN IDENT ASSIGN Expression
                | CommonModifierS IDENT IDENT ASSIGN Expression
                |  UnannType VariableDeclaratorId ASSIGN Expression
                |  NumericType VariableDeclaratorId ASSIGN Expression
                |  BOOLEAN VariableDeclaratorId ASSIGN Expression
                |  IDENT VariableDeclaratorId ASSIGN Expression
                |  UnannType IDENT ASSIGN Expression
                |  NumericType IDENT ASSIGN Expression
                |  BOOLEAN IDENT ASSIGN Expression
                |  IDENT IDENT ASSIGN Expression'''
    # p[0] = mytuple(["Resource"]+p[1:])


def p_StartCompilationUnit(p):
    '''start : INC CompilationUnit'''
    p[0] = p[2]

# def p_start_expression( p):
#     '''start : DEC expression'''
#     p[0] = p[2]


# def p_start_statement( p):
#     '''start : MUL block_statement'''
#     p[0] = p[2]

#</editor-fold> Section 14 #########################


def p_error(p):
    print('error: {}'.format(p))


# precedence = (
#     ('right', 'ASSIGN', 'NOT'),
#     ('left', 'LOR'),
#     ('left', 'LAND'),
#     ('nonassoc', 'EQL', 'NEQ', 'LSS', 'LEQ', 'GTR', 'GEQ'),
#     ('left', 'ADD', 'SUB', 'OR', 'XOR'),
#     ('left', 'MUL', 'QUO', 'REM', 'SHL', 'SHR', 'AND')
# )
lexer = lex.lex(module=lexRule)
parser = yacc.yacc(start='start', debug=1)
        # parser = yacc.yacc(start='start', debug = 0)

    # def tokenize_string( code):
    #     lexer.input(code)
    #     for token in lexer :
    #         print(token)

    # def tokenize_file( _file):
    #     if type(_file) == str :
    #         _file = open(_file)
    #     content = ''
    #     for line in _file :
    #         content += line
    #     return tokenize_string(content)

    # def parse_expression( code, debug=0, lineno=1):
    #     return parse_string(code, debug, lineno, prefix='--')

    # def parse_statement( code, debug=0, lineno=1):
    #     return parse_string(code, debug, lineno, prefix='* ')
global HASH_MAP
HASH_MAP = {}
def parse_string(code, debug=0, lineno=1, prefix='++'):
    if(verbose_flag):
        print("Lexing Started")
    lexer.input(code)
    while True:
        tok = lexer.token()
        if not tok:  # No more input
            break
        elif tok.type in lexRule.literals_ :
            HASH_MAP[tok.value] = "Literal"
        elif tok.type in lexRule.separators :
            HASH_MAP[tok.value] = "Separator"
        elif tok.type == 'IDENT' :
            HASH_MAP[tok.value] = "IDENT"
        elif tok.type in lexRule.operators :
            HASH_MAP[tok.value] = "Operator"
        elif tok.type in list(lexRule.reserved.values()):
            HASH_MAP[tok.value] = "Keyword"
        else : # Comments or unknown
            continue

    lexer.lineno = lineno
    if(verbose_flag):
        print("Lexing Done")
        print("Parsing Start")
    return parser.parse(prefix + code, lexer=lexer, debug=0)


def parse_file(_file, debug=0):
    if type(_file) == str:
        _file = open(_file)
    content = _file.read()
    return parse_string(content, debug=debug)


# get_parse = Parser()
# parse_out = get_parse.parse_file("../test/ackermann.java")
# print(parse_out)
# t = tac.code
# print(t)
# parse_out = parse_file(sys.argv[1])
# print(parse_out)


def plot_ast(output,filename,input_file):
    ast = Digraph(comment='Abstract Syntax Tree')
    node_i = 0

    def process_node(data, parent):
        if type(data) == str:
            nonlocal node_i
            node_i = node_i + 1
            if data in HASH_MAP:
                data = data + "\n(" + HASH_MAP[data]+")"
            ast.node(str(node_i), data)
            ast.edge(str(parent), str(node_i))
            return

        process_node(data[0], parent)
        lparent = node_i
        for i in data[1:]:
            if type(i) == str:
                process_node(i, lparent)
            elif type(i) == tuple:
                process_node(i, lparent)
    process_node(output, 0)
    ast.node(str(0), os.path.basename(input_file))
    ast.render(filename + ".dot", view=True)



def reduce(ele):
    new_ele = []

    new_ele.append(ele[0])
    if(type(ele) ==str):
	    return ele
    elif(type(ele)==tuple and len(ele)==1):
        return ele
    if(len(ele)==2):
        return reduce(ele[1])
    else:
        for data in ele[1:]:
            new_ele.append(reduce(data))
        return tuple(new_ele)


def reduce_epsilon(ele):
    new_ele = []
    new_ele.append(ele[0])
    if(type(ele)==str):
        return ele
    else:
        for data in ele[1:]:
            if(data!="epsilon"):
                new_ele.append(reduce_epsilon(data))
        return tuple(new_ele)

import os
import argparse
argument_parser = argparse.ArgumentParser(description = "AST generator for Java!")

requiredNamed = argument_parser.add_argument_group('required named arguments')
requiredNamed.add_argument("-i", "--input", type = str, nargs = 1,
                    metavar = "file_name", required = True,
                    help = "Input file for parsing")

argument_parser.add_argument("-o", "--output", type = str, nargs = 1,
                    metavar = "file_name", default = "graph",
                    help = "Enter output file name without extension. Creates DOT(.dot) file and PDF(.pdf) file with same name")

argument_parser.add_argument("-v", "--verbose", type = bool, nargs = 1,
                    metavar = "verbose", default = False,
                    help = "Takes boolean value.")

args = argument_parser.parse_args()

if args.input != None:
    input_file = args.input[0]

if args.output != None:
    if(type(args.output)==list):
        output_file = args.output[0]
    else:
        output_file = args.output

verbose_flag = False
if args.verbose != None:
    if(type(args.verbose)==list):
        verbose_flag = args.verbose[0]
    else:
        verbose_flag = args.verbose


parse_out = parse_file(input_file)
if(verbose_flag):
    print("Parsing Done")
    print("Graph Plotting Started")
# print(parse_out)
# plot_ast(reduce(reduce_epsilon(reduce(parse_out))), output_file,input_file)
if(verbose_flag):
    print("Graph Plotting Ended")
