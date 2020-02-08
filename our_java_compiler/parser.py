import pydot
import lexRule
import ply.lex as lex
import ply.yacc as yacc
from model import *
import pdb
global tokens

WhileForBreak=[]
WhileForContinue=[]


# class ExpressionParser(object):

# class MyParser(ExpressionParser, NameParser, LiteralParser, TypeParser, ClassParser, StatementParser, CompilationUnitParser):
# class MyParser(object):
tokens = lexRule.tokens

# def p_comment(p):
#     ''' comment : COMMENT '''


def p_expression( p):
    '''expression : assignment_expression'''
    p[0] = p[1]

def p_expression_not_name( p):
    '''expression_not_name : assignment_expression_not_name'''
    p[0] = p[1]

def p_assignment_expression( p):
    '''assignment_expression : assignment
                                | conditional_expression'''
    p[0] = p[1]

def p_assignment_expression_not_name( p):
    '''assignment_expression_not_name : assignment
                                        | conditional_expression_not_name'''
    p[0] = p[1]

def p_assignment( p):
    '''assignment : postfix_expression assignment_operator assignment_expression'''
    p[0] = Assignment(p[2], p[1], p[3])

def p_assignment_operator( p):
    '''assignment_operator : ASSIGN
                            | MUL_ASSIGN
                            | QUO_ASSIGN
                            |  REM_ASSIGN
                            |  ADD_ASSIGN
                            | SUB_ASSIGN
                            | SHL_ASSIGN
                            | SHR_ASSIGN
                            | SHR_UN_ASSIGN
                            | AND_ASSIGN
                            | OR_ASSIGN
                            | XOR_ASSIGN'''
    p[0] = p[1]

def p_conditional_expression( p):
    '''conditional_expression : conditional_or_expression
                                | conditional_or_expression QUES expression COLON conditional_expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Conditional(p[1], p[3], p[5])

def p_conditional_expression_not_name( p):
    '''conditional_expression_not_name : conditional_or_expression_not_name
                                        | conditional_or_expression_not_name QUES expression COLON conditional_expression
                                        | name QUES expression COLON conditional_expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Conditional(p[1], p[3], p[5])

def binop( p, ctor):
    if len(p) == 2:
        p[0] = p[1]
    else:
        #Here i have chnged p[3] to p[4] and not handling bitwise | and &
        p[0] = ctor(p[2], p[1], p[3])

def binopmy( p, ctor):
    if len(p) == 2:
        p[0] = p[1]
    else:
        #Here i have chnged p[3] to p[4] and not handling bitwise | and &
        p[0] = ctor(p[2], p[1], p[4])

def p_conditional_or_expression( p):
    '''conditional_or_expression : conditional_and_expression
                                    | conditional_or_expression LOR marker_next_quad conditional_and_expression'''
    binopmy(p, ConditionalOr)
    if len(p) == 5:
        #print("or");print(p[1].falselist);print('_');print(p[3])
        tac.backpatch(p[1].falselist,p[3])
        p[0].truelist = p[1].truelist+p[4].truelist
        p[0].falselist = p[4].falselist

def p_conditional_or_expression_not_name( p):
    '''conditional_or_expression_not_name : conditional_and_expression_not_name
                                            | conditional_or_expression_not_name LOR marker_next_quad conditional_and_expression
                                            | name LOR marker_next_quad conditional_and_expression'''
    binopmy(p, ConditionalOr)
    if len(p) == 5:
        #print("or")
        #print(p[1].falselist)
        #print('_');print(p[3])
        tac.backpatch(p[1].falselist,p[3])
        p[0].truelist = p[1].truelist+p[4].truelist
        p[0].falselist = p[4].falselist

def p_conditional_and_expression( p):
    '''conditional_and_expression : inclusive_or_expression
                                    | conditional_and_expression LAND marker_next_quad inclusive_or_expression'''
    binopmy(p, ConditionalAnd)
    if len(p) == 5:
        #print("and");print(p[1].falselist);print('_');print(p[4].falselist);
        tac.backpatch(p[1].truelist,p[3])
        p[0].truelist = p[4].truelist
        p[0].falselist = p[1].falselist+p[4].falselist

def p_conditional_and_expression_not_name( p):
    '''conditional_and_expression_not_name : inclusive_or_expression_not_name
                                            | conditional_and_expression_not_name LAND marker_next_quad inclusive_or_expression
                                            | name LAND marker_next_quad inclusive_or_expression'''
    binopmy(p, ConditionalAnd)
    if len(p) == 5:
        #print("and");print(p[1].falselist);print('_');print(p[4].falselist);
        tac.backpatch(p[1].truelist,p[3])
        p[0].truelist = p[4].truelist
        p[0].falselist = p[1].falselist+p[4].falselist

def p_marker_next_quad( p):
    '''marker_next_quad : '''
    p[0] = ST.new_label()
    tac.emit('label :','','',p[0])

def p_inclusive_or_expression( p):
    '''inclusive_or_expression : exclusive_or_expression
                                | inclusive_or_expression OR exclusive_or_expression'''
    binop(p, Or)

def p_inclusive_or_expression_not_name( p):
    '''inclusive_or_expression_not_name : exclusive_or_expression_not_name
                                        | inclusive_or_expression_not_name OR exclusive_or_expression
                                        | name OR exclusive_or_expression'''
    binop(p, Or)

def p_exclusive_or_expression( p):
    '''exclusive_or_expression : and_expression
                                | exclusive_or_expression XOR and_expression'''
    binop(p, Xor)

def p_exclusive_or_expression_not_name( p):
    '''exclusive_or_expression_not_name : and_expression_not_name
                                        | exclusive_or_expression_not_name XOR and_expression
                                        | name XOR and_expression'''
    binop(p, Xor)

def p_and_expression( p):
    '''and_expression : equality_expression
                        | and_expression AND equality_expression'''
    binop(p, And)

def p_and_expression_not_name( p):
    '''and_expression_not_name : equality_expression_not_name
                                | and_expression_not_name AND equality_expression
                                | name AND equality_expression'''
    binop(p, And)

def p_equality_expression( p):
    '''equality_expression : instanceof_expression
                            | equality_expression EQL instanceof_expression
                            | equality_expression NEQ instanceof_expression'''
    binop(p, Equality)

def p_equality_expression_not_name( p):
    '''equality_expression_not_name : instanceof_expression_not_name
                                    | equality_expression_not_name EQL instanceof_expression
                                    | name EQL instanceof_expression
                                    | equality_expression_not_name NEQ instanceof_expression
                                    | name NEQ instanceof_expression'''
    binop(p, Equality)

def p_instanceof_expression( p):
    '''instanceof_expression : relational_expression
                                | instanceof_expression INSTANCEOF reference_type'''
    binop(p, InstanceOf)

def p_instanceof_expression_not_name( p):
    '''instanceof_expression_not_name : relational_expression_not_name
                                        | name INSTANCEOF reference_type
                                        | instanceof_expression_not_name INSTANCEOF reference_type'''
    binop(p, InstanceOf)

def p_relational_expression( p):
    '''relational_expression : shift_expression
                                | relational_expression GTR shift_expression
                                | relational_expression LSS shift_expression
                                | relational_expression GEQ shift_expression
                                | relational_expression LEQ shift_expression'''
    binop(p, Relational)

def p_relational_expression_not_name( p):
    '''relational_expression_not_name : shift_expression_not_name
                                        | shift_expression_not_name LSS shift_expression
                                        | name LSS shift_expression
                                        | shift_expression_not_name GTR shift_expression
                                        | name GTR shift_expression
                                        | shift_expression_not_name GEQ shift_expression
                                        | name GEQ shift_expression
                                        | shift_expression_not_name LEQ shift_expression
                                        | name LEQ shift_expression'''
    binop(p, Relational)

def p_shift_expression( p):
    '''shift_expression : additive_expression
                        | shift_expression SHL additive_expression
                        | shift_expression SHR additive_expression
                        | shift_expression SHR_UN  additive_expression'''
    binop(p, Shift)

def p_shift_expression_not_name( p):
    '''shift_expression_not_name : additive_expression_not_name
                                    | shift_expression_not_name SHL additive_expression
                                    | name SHL additive_expression
                                    | shift_expression_not_name SHR additive_expression
                                    | name SHR additive_expression
                                    | shift_expression_not_name SHR_UN  additive_expression
                                    | name SHR_UN  additive_expression'''
    binop(p, Shift)

def p_additive_expression( p):
    '''additive_expression : multiplicative_expression
                            | additive_expression ADD multiplicative_expression
                            | additive_expression SUB multiplicative_expression'''
    binop(p, Additive)

def p_additive_expression_not_name( p):
    '''additive_expression_not_name : multiplicative_expression_not_name
                                    | additive_expression_not_name ADD multiplicative_expression
                                    | name ADD multiplicative_expression
                                    | additive_expression_not_name SUB multiplicative_expression
                                    | name SUB multiplicative_expression'''
    binop(p, Additive)

def p_multiplicative_expression( p):
    '''multiplicative_expression : unary_expression
                                    | multiplicative_expression MUL unary_expression
                                    | multiplicative_expression QUO unary_expression
                                    | multiplicative_expression REM unary_expression'''
    binop(p, Multiplicative)

def p_multiplicative_expression_not_name( p):
    '''multiplicative_expression_not_name : unary_expression_not_name
                                            | multiplicative_expression_not_name MUL unary_expression
                                            | name MUL unary_expression
                                            | multiplicative_expression_not_name QUO unary_expression
                                            | name QUO unary_expression
                                            | multiplicative_expression_not_name REM unary_expression
                                            | name REM unary_expression'''
    binop(p, Multiplicative)

def p_unary_expression( p):
    '''unary_expression : pre_increment_expression
                        | pre_decrement_expression
                        | ADD unary_expression
                        | SUB unary_expression
                        | unary_expression_not_plus_minus'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Unary(p[1], p[2])

def p_unary_expression_not_name( p):
    '''unary_expression_not_name : pre_increment_expression
                                    | pre_decrement_expression
                                    | ADD unary_expression
                                    | SUB unary_expression
                                    | unary_expression_not_plus_minus_not_name'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Unary(p[1], p[2])

def p_pre_increment_expression( p):
    '''pre_increment_expression : INC unary_expression'''
    p[0] = Unary('++x', p[2])

def p_pre_decrement_expression( p):
    '''pre_decrement_expression : DEC unary_expression'''
    p[0] = Unary('--x', p[2])

def p_unary_expression_not_plus_minus( p):
    '''unary_expression_not_plus_minus : postfix_expression
                                        | LNOT unary_expression
                                        | NOT unary_expression
                                        | cast_expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Unary(p[1], p[2])

def p_unary_expression_not_plus_minus_not_name( p):
    '''unary_expression_not_plus_minus_not_name : postfix_expression_not_name
                                                | LNOT unary_expression
                                                | NOT unary_expression
                                                | cast_expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Unary(p[1], p[2])

def p_postfix_expression( p):
    '''postfix_expression : primary
                            | name
                            | post_increment_expression
                            | post_decrement_expression'''
    p[0] = p[1]

def p_postfix_expression_not_name( p):
    '''postfix_expression_not_name : primary
                                    | post_increment_expression
                                    | post_decrement_expression'''
    p[0] = p[1]

def p_post_increment_expression( p):
    '''post_increment_expression : postfix_expression INC'''
    p[0] = Unary('x++', p[1])

def p_post_decrement_expression( p):
    '''post_decrement_expression : postfix_expression DEC'''
    p[0] = Unary('x--', p[1])

def p_primary( p):
    '''primary : primary_no_new_array
                | array_creation_with_array_initializer
                | array_creation_without_array_initializer'''
    p[0] = p[1]

def p_primary_no_new_array( p):
    '''primary_no_new_array : literal
                            | THIS
                            | class_instance_creation_expression
                            | field_access
                            | method_invocation
                            | array_access'''
    p[0] = p[1]

def p_primary_no_new_array2( p):
    '''primary_no_new_array : LPAREN name RPAREN
                            | LPAREN expression_not_name RPAREN '''
    p[0] = p[2]

def p_primary_no_new_array3( p):
    '''primary_no_new_array : name PERIOD THIS
                            | name PERIOD SUPER'''
    p[1].append_name(p[3])
    p[0] = p[1]

def p_primary_no_new_array4( p):
    '''primary_no_new_array : name PERIOD CLASS
                            | name dims PERIOD CLASS
                            | primitive_type dims PERIOD CLASS
                            | primitive_type PERIOD CLASS'''
    if len(p) == 4:
        p[0] = ClassLiteral(Type(p[1]))
    else:
        p[0] = ClassLiteral(Type(p[1], dimensions=p[2]))

def p_dims_opt( p):
    '''dims_opt : dims'''
    p[0] = p[1]

def p_dims_opt2( p):
    '''dims_opt : empty'''
    p[0] = 0

def p_dims( p):
    '''dims : dims_loop'''
    p[0] = p[1]

def p_dims_loop( p):
    '''dims_loop : one_dim_loop
                    | dims_loop one_dim_loop'''
    if len(p) == 2:
        p[0] = 1
    else:
        p[0] = 1 + p[1]

def p_one_dim_loop( p):
    '''one_dim_loop : LBRACK RBRACK '''
    # ignore

def p_cast_expression( p):
    '''cast_expression : LPAREN primitive_type dims_opt RPAREN unary_expression'''
    p[0] = Cast(Type(p[2], dimensions=p[3]), p[5])

def p_cast_expression2( p):
    '''cast_expression : LPAREN name type_arguments dims_opt RPAREN unary_expression_not_plus_minus'''
    p[0] = Cast(Type(p[2], type_arguments=p[3], dimensions=p[4]), p[6])

def p_cast_expression3( p):
    '''cast_expression : LPAREN name type_arguments PERIOD class_or_interface_type dims_opt RPAREN unary_expression_not_plus_minus'''
    p[5].dimensions = p[6]
    p[5].enclosed_in = Type(p[2], type_arguments=p[3])
    p[0] = Cast(p[5], p[8])

def p_cast_expression4( p):
    '''cast_expression : LPAREN name RPAREN unary_expression_not_plus_minus'''
    # technically itMULs not necessarily a type but could be a type parameter
    p[0] = Cast(Type(p[2]), p[4])

def p_cast_expression5( p):
    '''cast_expression : LPAREN name dims RPAREN unary_expression_not_plus_minus'''
    # technically itMULs not necessarily a type but could be a type parameter
    p[0] = Cast(Type(p[2], dimensions=p[3]), p[5])

# class StatementParser(object):

def p_block( p):
    '''block : LBRACE inc_scope block_statements_opt dec_scope RBRACE '''
    p[0] = Block(p[3])

def p_block_statements_opt( p):
    '''block_statements_opt : block_statements'''
    p[0] = p[1]

def p_block_statements_opt2( p):
    '''block_statements_opt : empty'''
    p[0] = []

def p_block_statements( p):
    '''block_statements : block_statement
                        | block_statements block_statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_block_statement( p):
    '''block_statement : local_variable_declaration_statement
                        | statement
                        | class_declaration
                        | interface_declaration
                        '''
    p[0] = p[1]

def p_local_variable_declaration_statement( p):
    '''local_variable_declaration_statement : local_variable_declaration SEMICOLON '''
    p[0] = p[1]

def p_local_variable_declaration( p):
    '''local_variable_declaration : type variable_declarators'''
    p[0] = VariableDeclaration(p[1], p[2])


def p_local_variable_declaration2( p):
    '''local_variable_declaration : modifiers type variable_declarators'''
    p[0] = VariableDeclaration(p[2], p[3], modifiers=p[1])

def p_variable_declarators( p):
    '''variable_declarators : variable_declarator
                            | variable_declarators COMMA variable_declarator'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_variable_declarator( p):
    '''variable_declarator : variable_declarator_id
                            | variable_declarator_id ASSIGN variable_initializer'''
    if len(p) == 2:
        p[0] = VariableDeclarator(p[1])
    else:
        p[0] = VariableDeclarator(p[1], initializer=p[3])

def p_variable_declarator_id( p):
    '''variable_declarator_id : IDENT dims_opt'''
    p[0] = Variable(p[1], dimensions=p[2])

def p_variable_initializer( p):
    '''variable_initializer : expression
                            | array_initializer'''
    p[0] = p[1]

def p_statement( p):
    '''statement : statement_without_trailing_substatement
                    | labeled_statement
                    | if_then_statement
                    | if_then_else_statement
                    | while_statement
                    | for_statement
                    | enhanced_for_statement'''
    p[0] = p[1]

def p_statement_without_trailing_substatement( p):
    '''statement_without_trailing_substatement : block
                                                | expression_statement
                                                | assert_statement
                                                | empty_statement
                                                | switch_statement
                                                | do_statement
                                                | break_statement
                                                | continue_statement
                                                | return_statement
                                                | synchronized_statement
                                                | throw_statement
                                                | try_statement
                                                | try_statement_with_resources'''
    p[0] = p[1]

def p_expression_statement( p):
    '''expression_statement : statement_expression SEMICOLON
                            | explicit_constructor_invocation'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ExpressionStatement(p[1])

def p_statement_expression( p):
    '''statement_expression : assignment
                            | pre_increment_expression
                            | pre_decrement_expression
                            | post_increment_expression
                            | post_decrement_expression
                            | method_invocation
                            | class_instance_creation_expression'''
    p[0] = p[1]

def p_comma_opt( p):
    '''comma_opt : COMMA
                    | empty'''
    # ignore

def p_array_initializer( p):
    '''array_initializer : LBRACE comma_opt RBRACE '''
    p[0] = ArrayInitializer()

def p_array_initializer2( p):
    '''array_initializer : LBRACE variable_initializers RBRACE
                            | LBRACE variable_initializers COMMA RBRACE '''
    p[0] = ArrayInitializer(p[2])

def p_variable_initializers( p):
    '''variable_initializers : variable_initializer
                                | variable_initializers COMMA variable_initializer'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_method_invocation( p):
    '''method_invocation : IDENT LPAREN argument_list_opt RPAREN '''
    #We are currently only dealing with this
    p[0] = MethodInvocation(p[1], arguments=p[3])

def p_method_invocation2( p):
    '''method_invocation : name PERIOD type_arguments IDENT LPAREN argument_list_opt RPAREN
                            | primary PERIOD type_arguments IDENT LPAREN argument_list_opt RPAREN
                            | SUPER PERIOD type_arguments IDENT LPAREN argument_list_opt RPAREN '''
    p[0] = MethodInvocation(p[4], target=p[1], type_arguments=p[3], arguments=p[6])

def p_method_invocation3( p):
    '''method_invocation : name PERIOD IDENT LPAREN argument_list_opt RPAREN
                            | primary PERIOD IDENT LPAREN argument_list_opt RPAREN
                            | SUPER PERIOD IDENT LPAREN argument_list_opt RPAREN '''
    p[0] = MethodInvocation(p[3], target=p[1], arguments=p[5])

def p_labeled_statement( p):
    '''labeled_statement : label COLON statement'''
    p[3].label = p[1]
    p[0] = p[3]

def p_labeled_statement_no_short_if( p):
    '''labeled_statement_no_short_if : label COLON statement_no_short_if'''
    p[3].label = p[1]
    p[0] = p[3]

def p_label( p):
    '''label : IDENT'''
    p[0] = p[1]

def p_if_then_statement( p):
    '''if_then_statement : IF LPAREN inc_scope expression RPAREN label_for_if1 statement label_for_if1'''
    p[0] = IfThenElse(p[4], p[7])
    tac.backpatch(p[4].truelist,p[6])
    tac.backpatch(p[4].falselist,p[8])

def p_label_for_if1(p):
    '''label_for_if1 : '''
    l1 = ST.new_label()
    #handle array here
    #pdb.set_trace()
    #tac.emit('ifgoto', p[-2].place, 'eq0', l1)
    p[0] = l1
    tac.emit('label :','','',l1)

def p_label_for_if2(p):
    '''label_for_if2 : '''
    #handle array here
    #pdb.set_trace()
    tac.emit('label :', '', '',  p[-2][0])

def p_label_for_if3(p):
    '''label_for_if3 : '''
    #l1 = ST.new_label()
    #tac.emit('goto',l1,'COMMA')
    #tac.emit('label : ',p[-3],'COMMA')
    #p[0] = l1
    l1 = ST.new_label()
    l2 = ST.new_label()
    p[0] = [l1, l2]
    tac.emit('goto','','',l1)
    tac.emit('label :','', '', l2)

def p_if_then_else_statement( p):
    '''if_then_else_statement : IF LPAREN inc_scope expression RPAREN label_for_if1 statement_no_short_if ELSE label_for_if3 statement label_for_if2'''
    p[0] = IfThenElse(p[4], p[7], p[10])
    tac.backpatch(p[4].truelist,p[6])
    tac.backpatch(p[4].falselist,p[9][1])

def p_if_then_else_statement_no_short_if( p):
    '''if_then_else_statement_no_short_if : IF LPAREN inc_scope expression RPAREN label_for_if1 statement_no_short_if ELSE label_for_if3 statement_no_short_if label_for_if2'''
    p[0] = IfThenElse(p[4], p[7], p[10])
    tac.backpatch(p[4].truelist,p[6])
    tac.backpatch(p[4].falselist,p[9][1])

def p_while_statement( p):
    '''while_statement : WHILE inc_for_while_stack LPAREN inc_scope label_for_while1 expression RPAREN label_for_while1 statement label_for_while2'''
    p[0] = While(p[6], p[9])
    print(p[5])
    #pdb.set_trace()
    tac.backpatch(WhileForContinue[-1],p[5])
    tac.backpatch(WhileForBreak[-1],p[10])
    tac.backpatch(p[6].truelist,p[8])
    tac.backpatch(p[6].falselist,p[10])

    WhileForBreak.pop()
    WhileForContinue.pop()

def p_while_statement_no_short_if( p):
    '''while_statement_no_short_if : WHILE inc_for_while_stack LPAREN inc_scope label_for_while1 expression RPAREN label_for_while1 statement_no_short_if label_for_while2'''
    p[0] = While(p[6], p[9])
    tac.backpatch(WhileForContinue[-1],p[5])
    tac.backpatch(WhileForBreak[-1],p[10])
    tac.backpatch(p[6].truelist,p[8])
    tac.backpatch(p[6].falselist,p[10])
    WhileForContinue.pop()
    WhileForBreak.pop()

def p_inc_for_while_stack(p):
    '''inc_for_while_stack : '''
    WhileForContinue.append([])
    WhileForBreak.append([])

def p_label_for_while1(p):
    '''label_for_while1 : '''
    l1 = ST.new_label()
    p[0] = l1
    tac.emit('label :','', '', l1)

def p_label_for_while2(p):
    '''label_for_while2 : '''
    l1 = ST.new_label()
    p[0] = l1
    tac.emit('goto','', '', p[-5])
    tac.emit('label :','', '', l1)

def p_for_statement( p):
    '''for_statement : FOR inc_for_while_stack LPAREN inc_scope for_init_opt SEMICOLON label_for_for1 expression_opt SEMICOLON label_for_for1 for_update_opt label_for_for3 RPAREN label_for_for1 statement label_for_for2'''
    p[0] = For(p[5], p[8], p[11], p[15])
    #pdb.set_trace()
    tac.backpatch(WhileForContinue[-1],p[10])
    tac.backpatch(WhileForBreak[-1],p[16])
    tac.backpatch(p[8].truelist,p[14])
    tac.backpatch(p[8].falselist,p[16])
    WhileForContinue.pop()
    WhileForBreak.pop()

def p_for_statement_no_short_if( p):
    '''for_statement_no_short_if : FOR inc_for_while_stack LPAREN inc_scope for_init_opt SEMICOLON label_for_for1 expression_opt SEMICOLON label_for_for1 for_update_opt label_for_for3 RPAREN label_for_for1 statement_no_short_if label_for_for2'''
    p[0] = For(p[5], p[8], p[11], p[15])
    tac.backpatch(WhileForContinue[-1],p[10])
    tac.backpatch(WhileForBreak[-1],p[16])
    tac.backpatch(p[8].truelist,p[14])
    tac.backpatch(p[8].falselist,p[16])
    WhileForContinue.pop()
    WhileForBreak.pop()

def p_label_for_for1(p):
    '''label_for_for1 : '''
    l1 = ST.new_label()
    p[0] = l1
    tac.emit('label :','', '', l1)

def p_label_for_for2(p):
    '''label_for_for2 : '''
    l1 = ST.new_label()
    p[0] = l1
    tac.emit('goto','', '', p[-6])
    tac.emit('label :','', '', l1)

def p_label_for_for3(p):
    '''label_for_for3 : '''
    tac.emit('goto','', '', p[-5])

def p_for_init_opt( p):
    '''for_init_opt : for_init
                    | empty'''
    p[0] = p[1]

def p_for_init( p):
    '''for_init : statement_expression_list
                | local_variable_declaration'''
    p[0] = p[1]

def p_statement_expression_list( p):
    '''statement_expression_list : statement_expression
                                    | statement_expression_list COMMA statement_expression'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_expression_opt( p):
    '''expression_opt : expression
                        | empty'''
    p[0] = p[1]

def p_for_update_opt( p):
    '''for_update_opt : for_update
                        | empty'''
    p[0] = p[1]

def p_for_update( p):
    '''for_update : statement_expression_list'''
    p[0] = p[1]

def p_enhanced_for_statement( p):
    '''enhanced_for_statement : enhanced_for_statement_header statement'''
    p[0] = ForEach(p[1]['type'], p[1]['variable'], p[1]['iterable'], p[2], modifiers=p[1]['modifiers'])

def p_enhanced_for_statement_no_short_if( p):
    '''enhanced_for_statement_no_short_if : enhanced_for_statement_header statement_no_short_if'''
    p[0] = ForEach(p[1]['type'], p[1]['variable'], p[1]['iterable'], p[2], modifiers=p[1]['modifiers'])

def p_enhanced_for_statement_header( p):
    '''enhanced_for_statement_header : enhanced_for_statement_header_init COLON expression RPAREN '''
    p[1]['iterable'] = p[3]
    p[0] = p[1]

def p_enhanced_for_statement_header_init( p):
    '''enhanced_for_statement_header_init : FOR inc_for_while_stack LPAREN inc_scope type IDENT dims_opt'''
    p[0] = {'modifiers': [], 'type': p[5], 'variable': Variable(p[6], dimensions=p[7])}
    WhileForContinue.pop()
    WhileForBreak.pop()

def p_enhanced_for_statement_header_init2( p):
    '''enhanced_for_statement_header_init : FOR inc_for_while_stack LPAREN inc_scope modifiers type IDENT dims_opt'''
    p[0] = {'modifiers': p[5], 'type': p[6], 'variable': Variable(p[7], dimensions=p[8])}
    WhileForContinue.pop()
    WhileForBreak.pop()

def p_statement_no_short_if( p):
    '''statement_no_short_if : statement_without_trailing_substatement
                                | labeled_statement_no_short_if
                                | if_then_else_statement_no_short_if
                                | while_statement_no_short_if
                                | for_statement_no_short_if
                                | enhanced_for_statement_no_short_if'''
    p[0] = p[1]

def p_assert_statement( p):
    '''assert_statement : ASSERT expression SEMICOLON
                        | ASSERT expression COLON expression SEMICOLON '''
    if len(p) == 4:
        p[0] = Assert(p[2])
    else:
        p[0] = Assert(p[2], message=p[4])

def p_empty_statement( p):
    '''empty_statement : SEMICOLON '''
    p[0] = Empty()

def p_switch_statement( p):
    '''switch_statement : SWITCH LPAREN inc_scope expression RPAREN switch_block'''
    p[0] = Switch(p[4], p[6])

def p_switch_block( p):
    '''switch_block : LBRACE RBRACE '''
    p[0] = []

def p_switch_block2( p):
    '''switch_block : LBRACE switch_block_statements dec_scope RBRACE '''
    p[0] = p[2]

def p_switch_block3( p):
    '''switch_block : LBRACE switch_labels dec_scope RBRACE '''
    p[0] = [SwitchCase(p[2])]

def p_switch_block4( p):
    '''switch_block : LBRACE switch_block_statements switch_labels dec_scope RBRACE '''
    p[0] = p[2] + [SwitchCase(p[3])]

def p_switch_block_statements( p):
    '''switch_block_statements : switch_block_statement
                                | switch_block_statements switch_block_statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_switch_block_statement( p):
    '''switch_block_statement : switch_labels block_statements'''
    p[0] = SwitchCase(p[1], body=p[2])

def p_switch_labels( p):
    '''switch_labels : switch_label
                        | switch_labels switch_label'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_switch_label( p):
    '''switch_label : CASE constant_expression COLON
                    | DEFAULT COLON '''
    if len(p) == 3:
        p[0] = 'default'
    else:
        p[0] = p[2]

def p_constant_expression( p):
    '''constant_expression : expression'''
    p[0] = p[1]

def p_do_statement( p):
    '''do_statement : DO statement WHILE LPAREN expression RPAREN SEMICOLON '''
    p[0] = DoWhile(p[5], body=p[2])

def p_break_statement( p):
    '''break_statement : BREAK SEMICOLON
                        | BREAK IDENT SEMICOLON '''
    if len(p) == 3:
        WhileForBreak[-1].append(len(tac.code))
        tac.emit('goto','','','')
        p[0] = Break()
    else:
        p[0] = Break(p[2])

def p_continue_statement( p):
    '''continue_statement : CONTINUE SEMICOLON
                            | CONTINUE IDENT SEMICOLON '''
    if len(p) == 3:
        WhileForContinue[-1].append(len(tac.code))
        tac.emit('goto','','','')
        p[0] = Continue()
    else:
        p[0] = Continue(p[2])

def p_return_statement( p):
    '''return_statement : RETURN expression_opt SEMICOLON '''
    p[0] = Return(p[2])

def p_synchronized_statement( p):
    '''synchronized_statement : SYNCHRONIZED LPAREN expression RPAREN block'''
    p[0] = Synchronized(p[3], p[5])

def p_throw_statement( p):
    '''throw_statement : THROW expression SEMICOLON '''
    p[0] = Throw(p[2])

def p_try_statement( p):
    '''try_statement : TRY try_block catches
                        | TRY try_block catches_opt finally'''
    if len(p) == 4:
        p[0] = Try(p[2], catches=p[3])
    else:
        p[0] = Try(p[2], catches=p[3], _finally=p[4])

def p_try_block( p):
    '''try_block : block'''
    p[0] = p[1]

def p_catches( p):
    '''catches : catch_clause
                | catches catch_clause'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_catches_opt( p):
    '''catches_opt : catches'''
    p[0] = p[1]

def p_catches_opt2( p):
    '''catches_opt : empty'''
    p[0] = []

def p_catch_clause( p):
    '''catch_clause : CATCH LPAREN catch_formal_parameter RPAREN block'''
    p[0] = Catch(p[3]['variable'], types=p[3]['types'], modifiers=p[3]['modifiers'], block=p[5])

def p_catch_formal_parameter( p):
    '''catch_formal_parameter : modifiers_opt catch_type variable_declarator_id'''
    p[0] = {'modifiers': p[1], 'types': p[2], 'variable': p[3]}

def p_catch_type( p):
    '''catch_type : union_type'''
    p[0] = p[1]

def p_union_type( p):
    '''union_type : type
                    | union_type OR type'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_try_statement_with_resources( p):
    '''try_statement_with_resources : TRY resource_specification try_block catches_opt
                                    | TRY resource_specification try_block catches_opt finally'''
    if len(p) == 5:
        p[0] = Try(p[3], resources=p[2], catches=p[4])
    else:
        p[0] = Try(p[3], resources=p[2], catches=p[4], _finally=p[5])

def p_resource_specification( p):
    '''resource_specification : LPAREN resources semi_opt RPAREN '''
    p[0] = p[2]

def p_semi_opt( p):
    '''semi_opt : SEMICOLON
                | empty'''
    # ignore

def p_resources( p):
    '''resources : resource
                    | resources trailing_semicolon resource'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_trailing_semicolon( p):
    '''trailing_semicolon : SEMICOLON '''
    # ignore

def p_resource( p):
    '''resource : type variable_declarator_id ASSIGN variable_initializer'''
    p[0] = Resource(p[2], type=p[1], initializer=p[4])

def p_resource2( p):
    '''resource : modifiers type variable_declarator_id ASSIGN variable_initializer'''
    p[0] = Resource(p[3], type=p[2], modifiers=p[1], initializer=p[5])

def p_finally( p):
    '''finally : FINALLY block'''
    p[0] = p[2]

def p_explicit_constructor_invocation( p):
    '''explicit_constructor_invocation : THIS LPAREN argument_list_opt RPAREN SEMICOLON
                                        | SUPER LPAREN argument_list_opt RPAREN SEMICOLON '''
    p[0] = ConstructorInvocation(p[1], arguments=p[3])

def p_explicit_constructor_invocation2( p):
    '''explicit_constructor_invocation : type_arguments SUPER LPAREN argument_list_opt RPAREN SEMICOLON
                                        | type_arguments THIS LPAREN argument_list_opt RPAREN SEMICOLON '''
    p[0] = ConstructorInvocation(p[2], type_arguments=p[1], arguments=p[4])

def p_explicit_constructor_invocation3( p):
    '''explicit_constructor_invocation : primary PERIOD SUPER LPAREN argument_list_opt RPAREN SEMICOLON
                                        | name PERIOD SUPER LPAREN argument_list_opt RPAREN SEMICOLON
                                        | primary PERIOD THIS LPAREN argument_list_opt RPAREN SEMICOLON
                                        | name PERIOD THIS LPAREN argument_list_opt RPAREN SEMICOLON '''
    p[0] = ConstructorInvocation(p[3], target=p[1], arguments=p[5])

def p_explicit_constructor_invocation4( p):
    '''explicit_constructor_invocation : primary PERIOD type_arguments SUPER LPAREN argument_list_opt RPAREN SEMICOLON
                                        | name PERIOD type_arguments SUPER LPAREN argument_list_opt RPAREN SEMICOLON
                                        | primary PERIOD type_arguments THIS LPAREN argument_list_opt RPAREN SEMICOLON
                                        | name PERIOD type_arguments THIS LPAREN argument_list_opt RPAREN SEMICOLON '''
    p[0] = ConstructorInvocation(p[4], target=p[1], type_arguments=p[3], arguments=p[6])

def p_class_instance_creation_expression( p):
    '''class_instance_creation_expression : NEW type_arguments class_type LPAREN argument_list_opt RPAREN class_body_opt'''
    p[0] = InstanceCreation(p[3], type_arguments=p[3], arguments=p[5], body=p[7])

def p_class_instance_creation_expression2( p):
    '''class_instance_creation_expression : NEW class_type LPAREN argument_list_opt RPAREN class_body_opt'''
    p[0] = InstanceCreation(p[2], arguments=p[4], body=p[6])

def p_class_instance_creation_expression3( p):
    '''class_instance_creation_expression : primary PERIOD NEW type_arguments class_type LPAREN argument_list_opt RPAREN class_body_opt'''
    p[0] = InstanceCreation(p[5], enclosed_in=p[1], type_arguments=p[4], arguments=p[7], body=p[9])

def p_class_instance_creation_expression4( p):
    '''class_instance_creation_expression : primary PERIOD NEW class_type LPAREN argument_list_opt RPAREN class_body_opt'''
    p[0] = InstanceCreation(p[4], enclosed_in=p[1], arguments=p[6], body=p[8])

def p_class_instance_creation_expression5( p):
    '''class_instance_creation_expression : class_instance_creation_expression_name NEW class_type LPAREN argument_list_opt RPAREN class_body_opt'''
    p[0] = InstanceCreation(p[3], enclosed_in=p[1], arguments=p[5], body=p[7])

def p_class_instance_creation_expression6( p):
    '''class_instance_creation_expression : class_instance_creation_expression_name NEW type_arguments class_type LPAREN argument_list_opt RPAREN class_body_opt'''
    p[0] = InstanceCreation(p[4], enclosed_in=p[1], type_arguments=p[3], arguments=p[6], body=p[8])

def p_class_instance_creation_expression_name( p):
    '''class_instance_creation_expression_name : name PERIOD '''
    p[0] = p[1]

def p_class_body_opt( p):
    '''class_body_opt : class_body
                        | empty'''
    p[0] = p[1]

def p_field_access( p):
    '''field_access : primary PERIOD IDENT
                    | SUPER PERIOD IDENT'''
    p[0] = FieldAccess(p[3], p[1])

def p_array_access( p):
    '''array_access : name LBRACK expression RBRACK
                    | primary_no_new_array LBRACK expression RBRACK
                    | array_creation_with_array_initializer LBRACK expression RBRACK '''
    p[0] = ArrayAccess(p[3], p[1])

def p_array_creation_with_array_initializer( p):
    '''array_creation_with_array_initializer : NEW primitive_type dim_with_or_without_exprs array_initializer
                                                | NEW class_or_interface_type dim_with_or_without_exprs array_initializer'''
    p[0] = ArrayCreation(p[2], dimensions=p[3], initializer=p[4])

def p_dim_with_or_without_exprs( p):
    '''dim_with_or_without_exprs : dim_with_or_without_expr
                                    | dim_with_or_without_exprs dim_with_or_without_expr'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_dim_with_or_without_expr( p):
    '''dim_with_or_without_expr : LBRACK expression RBRACK
                                | LBRACK RBRACK '''
    if len(p) == 3:
        p[0] = None
    else:
        p[0] = p[2]

def p_array_creation_without_array_initializer( p):
    '''array_creation_without_array_initializer : NEW primitive_type dim_with_or_without_exprs
                                                | NEW class_or_interface_type dim_with_or_without_exprs'''
    p[0] = ArrayCreation(p[2], dimensions=p[3])

# class NameParser(object):

def p_name( p):
    '''name : simple_name
            | qualified_name'''
    p[0] = p[1]

def p_simple_name( p):
    '''simple_name : IDENT'''
    p[0] = Name(p[1])

def p_qualified_name( p):
    '''qualified_name : name PERIOD simple_name'''
    p[1].append_name(p[3])
    p[0] = p[1]

# class LiteralParser(object):

def p_literal( p):
    '''literal : HEX_LIT
                | OCTAL_LIT
                | BINARY_LIT
                | DECIMAL_LIT
                | FLOAT_HEX_LIT
                | FLOAT_DEC_LIT
                | CHAR_LIT
                | STRING_LIT
                | BOOL_LIT
                | NULL_LIT'''
    p[0] = Literal(p[1])

# class TypeParser(object):

def p_modifiers_opt( p):
    '''modifiers_opt : modifiers'''
    p[0] = p[1]

def p_modifiers_opt2( p):
    '''modifiers_opt : empty'''
    p[0] = []

def p_modifiers( p):
    '''modifiers : modifier
                    | modifiers modifier'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_modifier( p):
    '''modifier : PUBLIC
                | PROTECTED
                | PRIVATE
                | STATIC
                | ABSTRACT
                | FINAL
                | NATIVE
                | SYNCHRONIZED
                | TRANSIENT
                | VOLATILE
                | STRICTFP
                | annotation'''
    p[0] = p[1]

def p_type( p):
    '''type : primitive_type
            | reference_type'''
    p[0] = p[1]

def p_primitive_type( p):
    '''primitive_type : BOOLEAN
                        | VOID
                        | BYTE
                        | SHORT
                        | INT
                        | LONG
                        | CHAR
                        | FLOAT
                        | DOUBLE'''
    p[0] = p[1]

def p_reference_type( p):
    '''reference_type : class_or_interface_type
                        | array_type'''
    p[0] = p[1]

def p_class_or_interface_type( p):
    '''class_or_interface_type : class_or_interface
                                | generic_type'''
    p[0] = p[1]

def p_class_type( p):
    '''class_type : class_or_interface_type'''
    p[0] = p[1]

def p_class_or_interface( p):
    '''class_or_interface : name
                            | generic_type PERIOD name'''
    if len(p) == 2:
        p[0] = Type(p[1])
    else:
        p[0] = Type(p[3], enclosed_in=p[1])

def p_generic_type( p):
    '''generic_type : class_or_interface type_arguments'''
    p[1].type_arguments = p[2]
    p[0] = p[1]

def p_generic_type2( p):
    '''generic_type : class_or_interface LSS GTR '''
    p[0] = Type(p[1], type_arguments='diamond')

#    def p_array_type( p):
#        '''array_type : primitive_type dims
#                      | name dims
#                      | array_type_with_type_arguments_name dims
#                      | generic_type dims'''
#        p[0] = p[1] + LBRACK + p[2] + RBRACK
#
#    def p_array_type_with_type_arguments_name( p):
#        '''array_type_with_type_arguments_name : generic_type PERIOD name'''
#        p[0] = p[1] + PERIOD + p[3]

def p_array_type( p):
    '''array_type : primitive_type dims
                    | name dims'''
    p[0] = Type(p[1], dimensions=p[2])

def p_array_type2( p):
    '''array_type : generic_type dims'''
    p[1].dimensions = p[2]
    p[0] = p[1]

def p_array_type3( p):
    '''array_type : generic_type PERIOD name dims'''
    p[0] = Type(p[3], enclosed_in=p[1], dimensions=p[4])

def p_type_arguments( p):
    '''type_arguments : LSS type_argument_list1'''
    p[0] = p[2]

def p_type_argument_list1( p):
    '''type_argument_list1 : type_argument1
                            | type_argument_list COMMA type_argument1'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_type_argument_list( p):
    '''type_argument_list : type_argument
                            | type_argument_list COMMA type_argument'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_type_argument( p):
    '''type_argument : reference_type
                        | wildcard'''
    p[0] = p[1]

def p_type_argument1( p):
    '''type_argument1 : reference_type1
                        | wildcard1'''
    p[0] = p[1]

def p_reference_type1( p):
    '''reference_type1 : reference_type GTR
                        | class_or_interface LSS type_argument_list2'''
    if len(p) == 3:
        p[0] = p[1]
    else:
        p[1].type_arguments = p[3]
        p[0] = p[1]

def p_type_argument_list2( p):
    '''type_argument_list2 : type_argument2
                            | type_argument_list COMMA type_argument2'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_type_argument2( p):
    '''type_argument2 : reference_type2
                        | wildcard2'''
    p[0] = p[1]

def p_reference_type2( p):
    '''reference_type2 : reference_type SHR
                        | class_or_interface LSS type_argument_list3'''
    if len(p) == 3:
        p[0] = p[1]
    else:
        p[1].type_arguments = p[3]
        p[0] = p[1]

def p_type_argument_list3( p):
    '''type_argument_list3 : type_argument3
                            | type_argument_list COMMA type_argument3'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_type_argument3( p):
    '''type_argument3 : reference_type3
                        | wildcard3'''
    p[0] = p[1]

def p_reference_type3( p):
    '''reference_type3 : reference_type SHR_UN '''
    p[0] = p[1]

def p_wildcard( p):
    '''wildcard : QUES
                | QUES wildcard_bounds'''
    if len(p) == 2:
        p[0] = Wildcard()
    else:
        p[0] = Wildcard(bounds=p[2])

def p_wildcard_bounds( p):
    '''wildcard_bounds : EXTENDS reference_type
                        | SUPER reference_type'''
    if p[1] == 'extends':
        p[0] = WildcardBound(p[2], extends=True)
    else:
        p[0] = WildcardBound(p[2], _super=True)

def p_wildcard1( p):
    '''wildcard1 : QUES GTR
                    | QUES wildcard_bounds1'''
    if p[2] == GTR:
        p[0] = Wildcard()
    else:
        p[0] = Wildcard(bounds=p[2])

def p_wildcard_bounds1( p):
    '''wildcard_bounds1 : EXTENDS reference_type1
                        | SUPER reference_type1'''
    if p[1] == 'extends':
        p[0] = WildcardBound(p[2], extends=True)
    else:
        p[0] = WildcardBound(p[2], _super=True)

def p_wildcard2( p):
    '''wildcard2 : QUES SHR
                    | QUES wildcard_bounds2'''
    if p[2] == '>>':
        p[0] = Wildcard()
    else:
        p[0] = Wildcard(bounds=p[2])

def p_wildcard_bounds2( p):
    '''wildcard_bounds2 : EXTENDS reference_type2
                        | SUPER reference_type2'''
    if p[1] == 'extends':
        p[0] = WildcardBound(p[2], extends=True)
    else:
        p[0] = WildcardBound(p[2], _super=True)

def p_wildcard3( p):
    '''wildcard3 : QUES SHR_UN
                    | QUES wildcard_bounds3'''
    if p[2] == '>>>':
        p[0] = Wildcard()
    else:
        p[0] = Wildcard(bounds=p[2])

def p_wildcard_bounds3( p):
    '''wildcard_bounds3 : EXTENDS reference_type3
                        | SUPER reference_type3'''
    if p[1] == 'extends':
        p[0] = WildcardBound(p[2], extends=True)
    else:
        p[0] = WildcardBound(p[2], _super=True)

def p_type_parameter_header( p):
    '''type_parameter_header : IDENT'''
    p[0] = p[1]

def p_type_parameters( p):
    '''type_parameters : LSS type_parameter_list1'''
    p[0] = p[2]

def p_type_parameter_list( p):
    '''type_parameter_list : type_parameter
                            | type_parameter_list COMMA type_parameter'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_type_parameter( p):
    '''type_parameter : type_parameter_header
                        | type_parameter_header EXTENDS reference_type
                        | type_parameter_header EXTENDS reference_type additional_bound_list'''
    if len(p) == 2:
        p[0] = TypeParameter(p[1])
    elif len(p) == 4:
        p[0] = TypeParameter(p[1], extends=[p[3]])
    else:
        p[0] = TypeParameter(p[1], extends=[p[3]] + p[4])

def p_additional_bound_list( p):
    '''additional_bound_list : additional_bound
                                | additional_bound_list additional_bound'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_additional_bound( p):
    '''additional_bound : AND reference_type'''
    p[0] = p[2]

def p_type_parameter_list1( p):
    '''type_parameter_list1 : type_parameter1
                            | type_parameter_list COMMA type_parameter1'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_type_parameter1( p):
    '''type_parameter1 : type_parameter_header GTR
                        | type_parameter_header EXTENDS reference_type1
                        | type_parameter_header EXTENDS reference_type additional_bound_list1'''
    if len(p) == 3:
        p[0] = TypeParameter(p[1])
    elif len(p) == 4:
        p[0] = TypeParameter(p[1], extends=[p[3]])
    else:
        p[0] = TypeParameter(p[1], extends=[p[3]] + p[4])

def p_additional_bound_list1( p):
    '''additional_bound_list1 : additional_bound1
                                | additional_bound_list additional_bound1'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_additional_bound1( p):
    '''additional_bound1 : AND reference_type1'''
    p[0] = p[2]

# class ClassParser(object):

def p_type_declaration( p):
    '''type_declaration : class_declaration
                        | interface_declaration'''
    p[0] = p[1]

def p_type_declaration2( p):
    '''type_declaration : SEMICOLON '''
    p[0] = EmptyDeclaration()

def p_class_declaration( p):
    '''class_declaration : class_header class_body'''
    p[0] = ClassDeclaration(p[1]['name'], p[2], modifiers=p[1]['modifiers'],
                            extends=p[1]['extends'], implements=p[1]['implements'],
                            type_parameters=p[1]['type_parameters'])

def p_class_header( p):
    '''class_header : class_header_name empty empty'''
    p[1]['extends'] = p[2]
    p[1]['implements'] = p[3]
    p[0] = p[1]

def p_class_header_name( p):
    '''class_header_name : class_header_name1 type_parameters
                            | class_header_name1'''
    if len(p) == 2:
        p[1]['type_parameters'] = []
    else:
        p[1]['type_parameters'] = p[2]
    p[0] = p[1]
    ST.Add('classes',p[0]['name'],None,p[0]['type_parameters'],p[0]['modifiers'])

def p_class_header_name1( p):
    '''class_header_name1 : modifiers_opt CLASS IDENT'''
    p[0] = {'modifiers': p[1], 'name': p[3]}



def p_interface_type_list( p):
    '''interface_type_list : interface_type
                            | interface_type_list COMMA interface_type'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_interface_type( p):
    '''interface_type : class_or_interface_type'''
    p[0] = p[1]

def p_class_body( p):
    '''class_body : LBRACE inc_scope class_body_declarations_opt dec_scope RBRACE '''
    p[0] = p[3]

def p_class_body_declarations_opt( p):
    '''class_body_declarations_opt : class_body_declarations'''
    p[0] = p[1]

def p_class_body_declarations_opt2( p):
    '''class_body_declarations_opt : empty'''
    p[0] = []

def p_class_body_declarations( p):
    '''class_body_declarations : class_body_declaration
                                | class_body_declarations class_body_declaration'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_class_body_declaration( p):
    '''class_body_declaration : class_member_declaration
                                | static_initializer
                                | constructor_declaration'''
    p[0] = p[1]

def p_class_body_declaration2( p):
    '''class_body_declaration : block'''
    p[0] = ClassInitializer(p[1])

def p_class_member_declaration( p):
    '''class_member_declaration : field_declaration
                                | class_declaration
                                | method_declaration
                                | interface_declaration'''
    p[0] = p[1]

def p_class_member_declaration2( p):
    '''class_member_declaration : SEMICOLON '''
    p[0] = EmptyDeclaration()

def p_field_declaration( p):
    '''field_declaration : modifiers_opt type variable_declarators SEMICOLON '''
    p[0] = FieldDeclaration(p[2], p[3], modifiers=p[1])

def p_static_initializer( p):
    '''static_initializer : STATIC block'''
    p[0] = ClassInitializer(p[2], static=True)

def p_constructor_declaration( p):
    '''constructor_declaration : constructor_header method_body'''
    p[0] = ConstructorDeclaration(p[1]['name'], p[2], modifiers=p[1]['modifiers'],
                                    type_parameters=p[1]['type_parameters'],
                                    parameters=p[1]['parameters'], throws=p[1]['throws'])

def p_constructor_header( p):
    '''constructor_header : constructor_header_name formal_parameter_list_opt RPAREN method_header_throws_clause_opt'''
    p[1]['parameters'] = p[2]
    p[1]['throws'] = p[4]
    p[0] = p[1]

def p_constructor_header_name( p):
    '''constructor_header_name : modifiers_opt type_parameters IDENT LPAREN
                                | modifiers_opt IDENT LPAREN '''
    if len(p) == 4:
        p[0] = {'modifiers': p[1], 'type_parameters': [], 'name': p[2]}
    else:
        p[0] = {'modifiers': p[1], 'type_parameters': p[2], 'name': p[3]}

def p_formal_parameter_list_opt( p):
    '''formal_parameter_list_opt : formal_parameter_list'''
    p[0] = p[1]

def p_formal_parameter_list_opt2( p):
    '''formal_parameter_list_opt : empty'''
    p[0] = []

def p_formal_parameter_list( p):
    '''formal_parameter_list : formal_parameter
                                | formal_parameter_list COMMA formal_parameter'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_formal_parameter( p):
    '''formal_parameter : modifiers_opt type variable_declarator_id
                        | modifiers_opt type ELLIPSIS variable_declarator_id'''
    if len(p) == 4:
        p[0] = FormalParameter(p[3], p[2], modifiers=p[1])
    else:
        p[0] = FormalParameter(p[4], p[2], modifiers=p[1], vararg=True)

def p_method_header_throws_clause_opt( p):
    '''method_header_throws_clause_opt : method_header_throws_clause
                                        | empty'''
    p[0] = p[1]

def p_method_header_throws_clause( p):
    '''method_header_throws_clause : THROWS class_type_list'''
    p[0] = Throws(p[2])

def p_class_type_list( p):
    '''class_type_list : class_type_elt
                        | class_type_list COMMA class_type_elt'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_class_type_elt( p):
    '''class_type_elt : class_type'''
    p[0] = p[1]

def p_method_body( p):
    '''method_body : LBRACE block_statements_opt dec_scope RBRACE '''
    p[0] = p[2]

def p_method_declaration( p):
    '''method_declaration : abstract_method_declaration
                            | method_header method_body'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = MethodDeclaration(p[1]['name'], parameters=p[1]['parameters'],
                                    extended_dims=p[1]['extended_dims'], type_parameters=p[1]['type_parameters'],
                                    return_type=p[1]['type'], modifiers=p[1]['modifiers'],
                                    throws=p[1]['throws'], body=p[2])

def p_abstract_method_declaration( p):
    '''abstract_method_declaration : method_header101 SEMICOLON '''
    p[0] = MethodDeclaration(p[1]['name'], abstract=True, parameters=p[1]['parameters'],
                                extended_dims=p[1]['extended_dims'], type_parameters=p[1]['type_parameters'],
                                return_type=p[1]['type'], modifiers=p[1]['modifiers'],
                                throws=p[1]['throws'])

def p_method_header101( p):
    '''method_header101 : method_header_name formal_parameter_list_opt RPAREN method_header_extended_dims method_header_throws_clause_opt dec_scope'''
    p[1]['parameters'] = p[2]
    p[1]['extended_dims'] = p[4]
    p[1]['throws'] = p[5]
    p[0] = p[1]
    global ST
    ST.Add('methods',p[1]['name'],p[1]['parameters'],p[1]['type'],'abstract',1)


def p_method_header( p):
    '''method_header : method_header_name formal_parameter_list_opt RPAREN method_header_extended_dims method_header_throws_clause_opt'''
    p[1]['parameters'] = p[2]
    p[1]['extended_dims'] = p[4]
    p[1]['throws'] = p[5]
    p[0] = p[1]
    global ST
    ST.Add('methods',p[1]['name'],p[1]['parameters'],p[1]['type'],p[1]['modifiers'],1)
    q = []
    for x in p[2]:
        q = q + [x.variable.name + '_'+str(ST.scope)]
    tac.emit('func',p[1]['name']+str(len(p[2])),q,'')
    ST.makeMethodArgument()

def p_method_header_name( p):
    '''method_header_name : modifiers_opt type_parameters type IDENT LPAREN
                            | modifiers_opt type IDENT LPAREN '''
    if len(p) == 5:
        p[0] = {'modifiers': p[1], 'type_parameters': [], 'type': p[2], 'name': p[3]}
    else:
        p[0] = {'modifiers': p[1], 'type_parameters': p[2], 'type': p[3], 'name': p[4]}
    ST.inc_scope(p[0]['name'])


def p_method_header_extended_dims( p):
    '''method_header_extended_dims : dims_opt'''
    p[0] = p[1]

def p_interface_declaration( p):
    '''interface_declaration : interface_header interface_body'''
    p[0] = InterfaceDeclaration(p[1]['name'], modifiers=p[1]['modifiers'],
                                type_parameters=p[1]['type_parameters'],
                                extends=p[1]['extends'],
                                body=p[2])

def p_interface_header( p):
    '''interface_header : interface_header_name interface_header_extends_opt'''
    p[1]['extends'] = p[2]
    p[0] = p[1]

def p_interface_header_name( p):
    '''interface_header_name : interface_header_name1 type_parameters
                                | interface_header_name1'''
    if len(p) == 2:
        p[1]['type_parameters'] = []
    else:
        p[1]['type_parameters'] = p[2]
    p[0] = p[1]

def p_interface_header_name1( p):
    '''interface_header_name1 : modifiers_opt INTERFACE IDENT'''
    p[0] = {'modifiers': p[1], 'name': p[3]}

def p_interface_header_extends_opt( p):
    '''interface_header_extends_opt : interface_header_extends'''
    p[0] = p[1]

def p_interface_header_extends_opt2( p):
    '''interface_header_extends_opt : empty'''
    p[0] = []

def p_interface_header_extends( p):
    '''interface_header_extends : EXTENDS interface_type_list'''
    p[0] = p[2]

def p_interface_body( p):
    '''interface_body : LBRACE interface_member_declarations_opt RBRACE '''
    p[0] = p[2]

def p_interface_member_declarations_opt( p):
    '''interface_member_declarations_opt : interface_member_declarations'''
    p[0] = p[1]

def p_interface_member_declarations_opt2( p):
    '''interface_member_declarations_opt : empty'''
    p[0] = []

def p_interface_member_declarations( p):
    '''interface_member_declarations : interface_member_declaration
                                        | interface_member_declarations interface_member_declaration'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_interface_member_declaration( p):
    '''interface_member_declaration : constant_declaration
                                    | abstract_method_declaration
                                    | class_declaration
                                    | interface_declaration'''
    p[0] = p[1]

def p_interface_member_declaration2( p):
    '''interface_member_declaration : SEMICOLON '''
    p[0] = EmptyDeclaration()

def p_constant_declaration( p):
    '''constant_declaration : field_declaration'''
    p[0] = p[1]

def p_argument_list_opt( p):
    '''argument_list_opt : argument_list'''
    p[0] = p[1]

def p_argument_list_opt2( p):
    '''argument_list_opt : empty'''
    p[0] = []

def p_argument_list( p):
    '''argument_list : expression
                        | argument_list COMMA expression'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_member_value( p):
    '''member_value : conditional_expression_not_name
                    | name
                    | annotation
                    | member_value_array_initializer'''
    p[0] = p[1]

def p_member_value_array_initializer( p):
    '''member_value_array_initializer : LBRACE member_values COMMA RBRACE
                                        | LBRACE member_values RBRACE '''
    p[0] = ArrayInitializer(p[2])

def p_member_value_array_initializer2( p):
    '''member_value_array_initializer : LBRACE COMMA RBRACE
                                        | LBRACE RBRACE '''
    # ignore

def p_member_values( p):
    '''member_values : member_value
                        | member_values COMMA member_value'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_annotation( p):
    '''annotation : normal_annotation
                    | marker_annotation
                    | single_member_annotation'''
    p[0] = p[1]

def p_normal_annotation( p):
    '''normal_annotation : annotation_name LPAREN member_value_pairs_opt RPAREN '''
    p[0] = Annotation(p[1], members=p[3])

def p_annotation_name( p):
    '''annotation_name : ATRATE name'''
    p[0] = p[2]

def p_member_value_pairs_opt( p):
    '''member_value_pairs_opt : member_value_pairs'''
    p[0] = p[1]

def p_member_value_pairs_opt2( p):
    '''member_value_pairs_opt : empty'''
    p[0] = []

def p_member_value_pairs( p):
    '''member_value_pairs : member_value_pair
                            | member_value_pairs COMMA member_value_pair'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_member_value_pair( p):
    '''member_value_pair : simple_name ASSIGN member_value'''
    p[0] = AnnotationMember(p[1], p[3])

def p_marker_annotation( p):
    '''marker_annotation : annotation_name'''
    p[0] = Annotation(p[1])

def p_single_member_annotation( p):
    '''single_member_annotation : annotation_name LPAREN single_member_annotation_member_value RPAREN '''
    p[0] = Annotation(p[1], single_member=p[3])

def p_single_member_annotation_member_value( p):
    '''single_member_annotation_member_value : member_value'''
    p[0] = p[1]

# class CompilationUnitParser(object):

def p_compilation_unit( p):
    '''compilation_unit : package_declaration'''
    p[0] = CompilationUnit(package_declaration=p[1])

def p_compilation_unit2( p):
    '''compilation_unit : package_declaration import_declarations'''
    p[0] = CompilationUnit(package_declaration=p[1], import_declarations=p[2])

def p_compilation_unit3( p):
    '''compilation_unit : package_declaration import_declarations type_declarations'''
    p[0] = CompilationUnit(package_declaration=p[1], import_declarations=p[2], type_declarations=p[3])

def p_compilation_unit4( p):
    '''compilation_unit : package_declaration type_declarations'''
    p[0] = CompilationUnit(package_declaration=p[1], type_declarations=p[2])

def p_compilation_unit5( p):
    '''compilation_unit : import_declarations'''
    p[0] = CompilationUnit(import_declarations=p[1])

def p_compilation_unit6( p):
    '''compilation_unit : type_declarations'''
    p[0] = CompilationUnit(type_declarations=p[1])

def p_compilation_unit7( p):
    '''compilation_unit : import_declarations type_declarations'''
    p[0] = CompilationUnit(import_declarations=p[1], type_declarations=p[2])

def p_compilation_unit8( p):
    '''compilation_unit : empty'''
    p[0] = CompilationUnit()

def p_package_declaration( p):
    '''package_declaration : package_declaration_name SEMICOLON '''
    if p[1][0]:
        p[0] = PackageDeclaration(p[1][1], modifiers=p[1][0])
    else:
        p[0] = PackageDeclaration(p[1][1])

def p_package_declaration_name( p):
    '''package_declaration_name : modifiers PACKAGE name
                                | PACKAGE name'''
    if len(p) == 3:
        p[0] = (None, p[2])
    else:
        p[0] = (p[1], p[3])

def p_import_declarations( p):
    '''import_declarations : import_declaration
                            | import_declarations import_declaration'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_import_declaration( p):
    '''import_declaration : single_type_import_declaration
                            | type_import_on_demand_declaration
                            | single_static_import_declaration
                            | static_import_on_demand_declaration'''
    p[0] = p[1]

def p_single_type_import_declaration( p):
    '''single_type_import_declaration : IMPORT name SEMICOLON '''
    p[0] = ImportDeclaration(p[2])

def p_type_import_on_demand_declaration( p):
    '''type_import_on_demand_declaration : IMPORT name PERIOD MUL SEMICOLON '''
    p[0] = ImportDeclaration(p[2], on_demand=True)

def p_single_static_import_declaration( p):
    '''single_static_import_declaration : IMPORT STATIC name SEMICOLON '''
    p[0] = ImportDeclaration(p[3], static=True)

def p_static_import_on_demand_declaration( p):
    '''static_import_on_demand_declaration : IMPORT STATIC name PERIOD MUL SEMICOLON '''
    p[0] = ImportDeclaration(p[3], static=True, on_demand=True)

def p_type_declarations( p):
    '''type_declarations : type_declaration
                            | type_declarations type_declaration'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_start_compilation_unit( p):
    '''start : INC compilation_unit'''
    p[0] = p[2]

def p_start_expression( p):
    '''start : DEC expression'''
    p[0] = p[2]


def p_start_statement( p):
    '''start : MUL block_statement'''
    p[0] = p[2]


def p_error( p):
    print('error: {}'.format(p))

def p_empty( p):
    '''empty :'''

def p_inc_scope(p):
    '''inc_scope : '''
    global ST
    ST.inc_scope()
    #print(p[-2])
    #pdb.set_trace()
def p_dec_scope(p):
    '''dec_scope : '''
    global ST
    ST.dec_scope()
    #print(p[-2])
    #pdb.set_trace()

# class Parser(object):

#     def __init__(self):
#         lexer = lex.lex(module=lexRule)
#         parser = yacc.yacc(module=MyParser(), start='start', debug = 0)
#         # parser = yacc.yacc(start='start', debug = 0)

#     def tokenize_string( code):
#         lexer.input(code)
#         for token in lexer:
#             print(token)

#     def tokenize_file( _file):
#         if type(_file) == str:
#             _file = open(_file)
#         content = ''
#         for line in _file:
#             content += line
#         return tokenize_string(content)

#     def parse_expression( code, debug=0, lineno=1):
#         return parse_string(code, debug, lineno, prefix='--')

#     def parse_statement( code, debug=0, lineno=1):
#         return parse_string(code, debug, lineno, prefix='* ')

#     def parse_string( code, debug=0, lineno=1, prefix='++'):
#         lexer.lineno = lineno
#         return parser.parse(prefix + code, lexer=lexer, debug=debug)

#     def parse_file( _file, debug=0):
#         if type(_file) == str:
#             _file = open(_file)
#         content = _file.read()
#         return parse_string(content, debug=debug)



lexer = lex.lex(module=lexRule)
parser = yacc.yacc(start='start', debug = 1)
        # parser = yacc.yacc(start='start', debug = 0)

    # def tokenize_string( code):
    #     lexer.input(code)
    #     for token in lexer:
    #         print(token)

    # def tokenize_file( _file):
    #     if type(_file) == str:
    #         _file = open(_file)
    #     content = ''
    #     for line in _file:
    #         content += line
    #     return tokenize_string(content)

    # def parse_expression( code, debug=0, lineno=1):
    #     return parse_string(code, debug, lineno, prefix='--')

    # def parse_statement( code, debug=0, lineno=1):
    #     return parse_string(code, debug, lineno, prefix='* ')
global HASH_MAP
def parse_string(code, debug=0, lineno=1, prefix='++'):
    lexer.input(code)
    print("In parse_string!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    while True:
        tok = lexer.token()
        if not tok: # No more input
            break
        elif tok.type in lexRule.literals_:
            HASH_MAP[tok.value] = "Literal"
        elif tok.type in lexRule.separators:
            HASH_MAP[tok.value] = "Separator"
        elif tok.type == 'IDENT':
            HASH_MAP[tok.value] = "Identifier"
        elif tok.type in lexRule.operators:
            HASH_MAP[tok.value] = "Operator"
        elif tok.type in list(lexRule.reserved.values()):
            HASH_MAP[tok.value] = "Keyword"
        else: # Comments or unknown
            continue

        print(tok)

    lexer.lineno = lineno
    return parser.parse(prefix + code, lexer=lexer, debug=debug)

def parse_file(_file, debug=0):
    print("In parse_file!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    if type(_file) == str:
        _file = open(_file)
    content = _file.read()
    return parse_string(content, debug=debug)

# get_parse = Parser()
# parse_out = get_parse.parse_file("../test/ackermann.java")
# print(parse_out)
# t = tac.code
# print(t)
