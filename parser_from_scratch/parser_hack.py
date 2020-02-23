import lexRule
import ply.lex as lex
import ply.yacc as yacc
tokens = lexRule.tokens



## Source : https ://docs.oracle.com/javase/specs/jls/se8/html/jls-19.html

def mytuple(l):
    print(l)
    return tuple(l)



def p_empty(p):
    '''empty : '''
    p[0]="epsilon"

#<editor-fold Section 3 #########################
################################################
### SECTION 3 :
################################################
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
    p[0] = mytuple(["Literal"]+p[1 :])

#</editor-fold>############################################

#<editor-fold Section 9 : Interfaces #########################
################################################
### SECTION 9 : Interfaces
################################################
def p_InterfaceDeclaration(p):
    '''InterfaceDeclaration : NormalInterfaceDeclaration
                           | AnnotationTypeDeclaration'''
    p[0] = mytuple(["InterfaceDeclaration"]+p[1 :])

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
    p[0] = mytuple(["NormalInterfaceDeclaration"]+p[1 :])

# def p_ZooTypeParameters(p):
#     '''ZooTypeParameters :  TypeParameters
#                         | empty'''
#     p[0] = mytuple(["ZooTypeParameters"]+p[1 :])
#
# def p_ZooExtendsInterfaces(p):
#     '''ZooExtendsInterfaces : ExtendsInterfaces
#                             | empty '''
#     p[0] = mytuple(["ZooExtendsInterfaces"]+p[1 :])
#

# def p_InterfaceModifierS(p):
#     '''InterfaceModifierS : Annotation InterfaceModifierS
#                           | PUBLIC InterfaceModifierS
#                           | PROTECTED InterfaceModifierS
#                           | PRIVATE InterfaceModifierS
#                           | ABSTRACT InterfaceModifierS
#                           | STATIC InterfaceModifierS
#                           | STRICTFP InterfaceModifierS
#                           | empty'''
#     p[0] = mytuple(["InterfaceModifierS"]+p[1 :])

# def p_InterfaceModifier(p):
#     '''InterfaceModifier :
#                          | ABSTRACT
#                          | STATIC
#                          | STRICTFP'''
#     p[0] = mytuple(["InterfaceModifier"]+p[1 :])


def p_ExtendsInterfaces(p):
    '''ExtendsInterfaces : EXTENDS InterfaceTypeList'''
    p[0] = mytuple(["ExtendsInterfaces"]+p[1 :])


def p_InterfaceBody(p):
    '''InterfaceBody : LBRACE InterfaceMemberDeclarationS RBRACE '''
    p[0] = mytuple(["InterfaceBody"]+p[1 :])


def p_InterfaceMemberDeclarationS(p):
    ''' InterfaceMemberDeclarationS : InterfaceMemberDeclaration InterfaceMemberDeclarationS
                                    | SEMICOLON InterfaceMemberDeclarationS
                                    | empty '''
    p[0] = mytuple(["InterfaceMemberDeclarationS"]+p[1 :])


def p_InterfaceMemberDeclaration(p):
    '''InterfaceMemberDeclaration : ConstantDeclaration
                                 | InterfaceMethodDeclaration
                                 | ClassDeclaration
                                 | InterfaceDeclaration'''
    p[0] = mytuple(["InterfaceMemberDeclaration"]+p[1 :])

def p_ConstantDeclaration(p):
    '''ConstantDeclaration : CommonModifierS UnannType VariableDeclaratorList SEMICOLON
                            | CommonModifierS IDENT VariableDeclaratorList SEMICOLON
                            | UnannType VariableDeclaratorList SEMICOLON
                            | IDENT VariableDeclaratorList SEMICOLON
                            | CommonModifierS UnannType IDENT SEMICOLON
                            | CommonModifierS IDENT IDENT SEMICOLON
                            | UnannType IDENT SEMICOLON
                            | IDENT IDENT SEMICOLON'''
    p[0] = mytuple(["ConstantDeclaration"]+p[1 :])

# def p_ConstantModifierS(p):
#     '''ConstantModifierS : ConstantModifier ConstantModifierS
#                         | empty '''
#     p[0] = mytuple(["ConstantModifierS"]+p[1 :])

# def p_ConstantModifier(p):
#     '''ConstantModifier : Annotation
#                        | PUBLIC
#                        | STATIC
#                        | FINAL'''
#     p[0] = mytuple(["ConstantModifier"]+p[1 :])

def p_InterfaceMethodDeclaration(p):
    '''InterfaceMethodDeclaration : CommonModifierS MethodHeader MethodBody
                                |  MethodHeader MethodBody
                                | CommonModifierS MethodHeader SEMICOLON
                                |  MethodHeader SEMICOLON'''
    p[0] = mytuple(["InterfaceMethodDeclaration"]+p[1 :])

# def p_InterfaceMethodModifierS(p):
#     '''InterfaceMethodModifierS : InterfaceMethodModifier InterfaceMethodModifierS
#                                | empty'''
#     p[0] = mytuple(["InterfaceMethodModifierS"]+p[1 :])

# def p_InterfaceMethodModifier(p):
#     '''InterfaceMethodModifier :  Annotation
#                                 | PUBLIC
#                                 | ABSTRACT
#                                 | DEFAULT
#                                 | STATIC
#                                 | STRICTFP'''
#     p[0] = mytuple(["InterfaceMethodModifier"]+p[1 :])

def p_AnnotationTypeDeclaration(p):
    '''AnnotationTypeDeclaration : CommonModifierS ATRATE INTERFACE IDENT AnnotationTypeBody
                            | ATRATE INTERFACE IDENT AnnotationTypeBody'''
    p[0] = mytuple(["AnnotationTypeDeclaration"]+p[1 :])

# def p_InterfaceModifierS(p):
#     '''InterfaceModifierS : InterfaceModifier InterfaceModifierS
#                          | empty'''
#     p[0] = mytuple(["InterfaceModifierS"]+p[1 :])

def p_AnnotationTypeBody(p):
    '''AnnotationTypeBody :  LBRACE AnnotationTypeMemberDeclarationS RBRACE'''
    p[0] = mytuple(["AnnotationTypeBody"]+p[1 :])

def p_AnnotationTypeMemberDeclarationS(p):
    '''AnnotationTypeMemberDeclarationS : AnnotationTypeMemberDeclaration AnnotationTypeMemberDeclarationS
                        | SEMICOLON AnnotationTypeMemberDeclarationS
                         | empty'''
    p[0] = mytuple(["AnnotationTypeMemberDeclarationS"]+p[1 :])

def p_AnnotationTypeMemberDeclaration(p):
    '''AnnotationTypeMemberDeclaration : AnnotationTypeElementDeclaration
                                        | ConstantDeclaration
                                        | ClassDeclaration
                                        | InterfaceDeclaration'''
    p[0] = mytuple(["AnnotationTypeMemberDeclaration"]+p[1 :])

def p_AnnotationTypeElementDeclaration(p):
    '''AnnotationTypeElementDeclaration :  CommonModifierS UnannType IDENT LPAREN RPAREN Dims DefaultValue SEMICOLON
                                        |  CommonModifierS IDENT IDENT LPAREN RPAREN Dims DefaultValue SEMICOLON
                                    |    CommonModifierS UnannType IDENT LPAREN RPAREN  DefaultValue SEMICOLON
                                    |  CommonModifierS IDENT IDENT LPAREN RPAREN  DefaultValue SEMICOLON
                                    |    CommonModifierS UnannType IDENT LPAREN RPAREN Dims  SEMICOLON
                                    |  CommonModifierS IDENT IDENT LPAREN RPAREN Dims  SEMICOLON
                                    |    CommonModifierS UnannType IDENT LPAREN RPAREN SEMICOLON
                                    |  CommonModifierS IDENT IDENT LPAREN RPAREN SEMICOLON
                                    | UnannType IDENT LPAREN RPAREN Dims DefaultValue SEMICOLON
                                        |  IDENT IDENT LPAREN RPAREN Dims DefaultValue SEMICOLON
                                    |    UnannType IDENT LPAREN RPAREN  DefaultValue SEMICOLON
                                    |  IDENT IDENT LPAREN RPAREN  DefaultValue SEMICOLON
                                    |    UnannType IDENT LPAREN RPAREN Dims  SEMICOLON
                                    |  IDENT IDENT LPAREN RPAREN Dims  SEMICOLON
                                    |    UnannType IDENT LPAREN RPAREN SEMICOLON
                                    |  IDENT IDENT LPAREN RPAREN SEMICOLON'''
    p[0] = mytuple(["AnnotationTypeElementDeclaration"]+p[1 :])

# def p_ZooDims(p):
#     '''ZooDims : Dims
#               | empty'''
#     p[0] = mytuple(["ZooDims"]+p[1 :])
#
# def p_ZooDefaultValue(p):
#     '''ZooDefaultValue : DefaultValue
#               | empty'''
#     p[0] = mytuple(["ZooDefaultValue"]+p[1 :])
#

# def p_AnnotationTypeElementModifierS(p):
#     '''AnnotationTypeElementModifierS : AnnotationTypeElementModifier AnnotationTypeElementModifierS
#                                       | empty'''
#     p[0] = mytuple(["AnnotationTypeElementModifierS"]+p[1 :])

# def p_AnnotationTypeElementModifier(p):
#     '''AnnotationTypeElementModifier : Annotation
#                                      | PUBLIC
#                                      | ABSTRACT'''
#     p[0] = mytuple(["AnnotationTypeElementModifier"]+p[1 :])

def p_DefaultValue(p):
    '''DefaultValue : DEFAULT ElementValue'''
    p[0] = mytuple(["DefaultValue"]+p[1 :])

def p_Annotation(p):
    '''Annotation : NormalAnnotation
                  | MarkerAnnotation
                  | SingleElementAnnotation'''
    p[0] = mytuple(["Annotation"]+p[1 :])

def p_NormalAnnotation(p):
    '''NormalAnnotation : ATRATE TypeName LPAREN ElementValuePairList RPAREN
                        | ATRATE TypeName LPAREN  RPAREN '''
    p[0] = mytuple(["NormalAnnotation"]+p[1 :])


# def p_ZooElementValuePairList(p):
#     '''ZooElementValuePairList : ElementValuePairList
#               | empty'''
#     p[0] = mytuple(["ZooElementValuePairList"]+p[1 :])


def p_ElementValuePairList(p):
    '''ElementValuePairList : ElementValuePair COMMAElementValuePairS'''
    p[0] = mytuple(["ElementValuePairList"]+p[1 :])

def p_COMMAElementValuePairS(p):
    '''COMMAElementValuePairS : COMMA ElementValuePair COMMAElementValuePairS
                              | empty'''
    p[0] = mytuple(["COMMAElementValuePairS"]+p[1 :])

def p_ElementValuePair(p):
    '''ElementValuePair : IDENT ASSIGN ElementValue'''
    p[0] = mytuple(["ElementValuePair"]+p[1 :])

def p_ElementValue(p):
    '''ElementValue : ConditionalExpression
                    | ElementValueArrayInitializer
                    | Annotation '''
    p[0] = mytuple(["ElementValue"]+p[1 :])

def p_ElementValueArrayInitializer(p):
    '''ElementValueArrayInitializer : LBRACE ElementValueList COMMA RBRACE
    | LBRACE ElementValueList  RBRACE
    | LBRACE  COMMA RBRACE
    | LBRACE   RBRACE'''
    p[0] = mytuple(["ElementValueArrayInitializer"]+p[1 :])


# def p_ZooElementValueList(p):
#     '''ZooElementValueList : ElementValueList
#                           | empty '''
#     p[0] = mytuple(["ZooElementValueList"]+p[1 :])

# def p_ZooCOMMA(p):
#     '''ZooCOMMA : COMMA
#                | empty '''
#     p[0] = mytuple(["ZooCOMMA"]+p[1 :])

def p_ElementValueList(p):
    '''ElementValueList : ElementValue  COMMAElementValueS'''
    p[0] = mytuple(["ElementValueList"]+p[1 :])

def p_COMMAElementValueS(p):
    '''COMMAElementValueS : COMMA ElementValue COMMAElementValueS
                         | empty '''
    p[0] = mytuple(["COMMAElementValueS"]+p[1 :])

def p_MarkerAnnotation(p):
    '''MarkerAnnotation : ATRATE TypeName'''
    p[0] = mytuple(["MarkerAnnotation"]+p[1 :])

def p_SingleElementAnnotation(p):
    '''SingleElementAnnotation : ATRATE TypeName LPAREN ElementValue RPAREN'''
    p[0] = mytuple(["SingleElementAnnotation"]+p[1 :])

#</editor-fold>############################################

#<editor-fold Section 10 : Arrays #########################
################################################
### Section 10 : Arrays
################################################
def p_ArrayInitializer(p):
    '''ArrayInitializer : LBRACE VariableInitializerList COMMA RBRACE
    | LBRACE VariableInitializerList RBRACE
    | LBRACE COMMA RBRACE
    | LBRACE RBRACE '''
    p[0] = mytuple(["ArrayInitializer"]+p[1 :])


# def p_ZooVariableInitializerList(p):
#     '''ZooVariableInitializerList : VariableInitializerList
#                                  | empty'''
#     p[0] = mytuple(["ZooVariableInitializerList"]+p[1 :])

def p_VariableInitializerList(p):
    '''VariableInitializerList : VariableInitializer COMMAVariableInitializerS'''
    p[0] = mytuple(["VariableInitializerList"]+p[1 :])

def p_COMMAVariableInitializerS(p):
    '''COMMAVariableInitializerS : COMMA VariableInitializer COMMAVariableInitializerS
                                 | empty'''
    p[0] = mytuple(["COMMAVariableInitializerS"]+p[1 :])

#</editor-fold>############################################

#<editor-fold Section 15 : Expressions #########################
################################################
### Section 15 : Expressions
################################################

def p_Primary(p):
    '''Primary : PrimaryNoNewArray
              | ArrayCreationExpression '''
    p[0] = mytuple(["Primary"]+p[1 :])

def p_PrimaryNoNewArray(p):
    '''PrimaryNoNewArray : Literal
                        | ClassLiteral
                        | THIS
                        | TypeName PERIOD THIS
                        | LPAREN Expression RPAREN
                        | ClassInstanceCreationExpression
                        | FieldAccess
                        | ArrayAccess
                        | MethodInvocation
                        | MethodReference'''
    p[0] = mytuple(["PrimaryNoNewArray"]+p[1 :])

def p_ClassLiteral(p):
    '''ClassLiteral : TypeName LBRACKRBRACKS PERIOD CLASS
                   | NumericType LBRACKRBRACKS PERIOD CLASS
                   | BOOLEAN LBRACKRBRACKS PERIOD CLASS
                   | VOID PERIOD CLASS '''
    p[0] = mytuple(["ClassLiteral"]+p[1 :])

def p_LBRACKRBRACKS(p):
    '''LBRACKRBRACKS : LBRACK RBRACK LBRACKRBRACKS
                    | empty'''
    p[0] = mytuple(["LBRACKRBRACKS"]+p[1 :])

def p_ClassInstanceCreationExpression(p):
    '''ClassInstanceCreationExpression : UnqualifiedClassInstanceCreationExpression
                                      | ExpressionName PERIOD UnqualifiedClassInstanceCreationExpression
                                      | IDENT PERIOD UnqualifiedClassInstanceCreationExpression
                                      | Primary PERIOD UnqualifiedClassInstanceCreationExpression'''
    p[0] = mytuple(["ClassInstanceCreationExpression"]+p[1 :])

def p_UnqualifiedClassInstanceCreationExpression(p):
    '''UnqualifiedClassInstanceCreationExpression : NEW TypeArguments ClassOrInterfaceTypeToInstantiate LPAREN ArgumentList RPAREN ClassBody
    | NEW TypeArguments ClassOrInterfaceTypeToInstantiate LPAREN  RPAREN ClassBody
    | NEW TypeArguments ClassOrInterfaceTypeToInstantiate LPAREN ArgumentList RPAREN
    | NEW TypeArguments ClassOrInterfaceTypeToInstantiate LPAREN  RPAREN
    | NEW ClassOrInterfaceTypeToInstantiate LPAREN ArgumentList RPAREN ClassBody
    | NEW ClassOrInterfaceTypeToInstantiate LPAREN  RPAREN ClassBody
    | NEW ClassOrInterfaceTypeToInstantiate LPAREN ArgumentList RPAREN
    | NEW ClassOrInterfaceTypeToInstantiate LPAREN  RPAREN'''
    p[0] = mytuple(["UnqualifiedClassInstanceCreationExpression"]+p[1 :])

# def p_ZooTypeArguments(p):
#     '''ZooTypeArguments : TypeArguments
#                        | empty'''
#     p[0] = mytuple(["ZooTypeArguments"]+p[1 :])
#
# def p_ZooArgumentList(p):
#     '''ZooArgumentList : ArgumentList
#                        | empty'''
#     p[0] = mytuple(["ZooArgumentList"]+p[1 :])
#
# def p_ZooClassBody(p):
#     '''ZooClassBody : ClassBody
#                        | empty'''
#     p[0] = mytuple(["ZooClassBody"]+p[1 :])

def p_ClassOrInterfaceTypeToInstantiate(p):
    '''ClassOrInterfaceTypeToInstantiate : AnnotationS IDENT PERIODAnnotationSIDENTS TypeArgumentsOrDiamond
                                        | AnnotationS IDENT PERIODAnnotationSIDENTS
                                         |  IDENT PERIODAnnotationSIDENTS
                                         |  IDENT PERIODAnnotationSIDENTS TypeArgumentsOrDiamond'''
    p[0] = mytuple(["ClassOrInterfaceTypeToInstantiate"]+p[1 :])

def p_AnnotationS(p):
    '''AnnotationS : Annotation AnnotationS
                  | Annotation'''
    p[0] = mytuple(["AnnotationS"]+p[1 :])

# def p_ZooTypeArgumentsOrDiamond(p):
#     '''ZooTypeArgumentsOrDiamond : TypeArgumentsOrDiamond
#                                 | empty'''
#     p[0] = mytuple(["ZooTypeArgumentsOrDiamond"]+p[1 :])

def p_PERIODAnnotationSIDENTS(p):
    '''PERIODAnnotationSIDENTS : PERIOD AnnotationS IDENT PERIODAnnotationSIDENTS
                                | PERIOD IDENT PERIODAnnotationSIDENTS
                              | empty'''
    p[0] = mytuple(["PERIODAnnotationSIDENTS"]+p[1 :])

# TODO fix function name of Zoo and ...S(p); also in general
# TODO fix ''' in next line

def p_TypeArgumentsOrDiamond(p):
    '''TypeArgumentsOrDiamond : TypeArguments
                             | LSS GTR'''
    p[0] = mytuple(["TypeArgumentsOrDiamond"]+p[1 :])

def p_FieldAccess(p):
    '''FieldAccess : Primary PERIOD IDENT
                  | SUPER PERIOD IDENT
                  | TypeName PERIOD SUPER PERIOD IDENT'''
    p[0] = mytuple(["FieldAccess"]+p[1 :])


def p_ArrayAccess(p):
    '''ArrayAccess : ExpressionName LBRACK Expression RBRACK
                    | IDENT LBRACK Expression RBRACK
                  | PrimaryNoNewArray LBRACK Expression RBRACK'''
    p[0] = mytuple(["ArrayAccess"]+p[1 :])

def p_MethodInvocation(p):
    '''MethodInvocation : IDENT LPAREN RPAREN
                        | IDENT LPAREN ArgumentList RPAREN
                       | TypeName PERIOD TypeArguments IDENT LPAREN ArgumentList RPAREN
                       | TypeName PERIOD TypeArguments IDENT LPAREN  RPAREN
                       | TypeName PERIOD  IDENT LPAREN ArgumentList RPAREN
                       | TypeName PERIOD  IDENT LPAREN  RPAREN
                       | ExpressionName PERIOD TypeArguments IDENT LPAREN ArgumentList RPAREN
                       | ExpressionName PERIOD  IDENT LPAREN ArgumentList RPAREN
                       | ExpressionName PERIOD TypeArguments IDENT LPAREN  RPAREN
                       | ExpressionName PERIOD  IDENT LPAREN  RPAREN
                       | IDENT PERIOD TypeArguments IDENT LPAREN ArgumentList RPAREN
                       | IDENT PERIOD TypeArguments IDENT LPAREN  RPAREN
                       | IDENT PERIOD  IDENT LPAREN ArgumentList RPAREN
                       | IDENT PERIOD  IDENT LPAREN  RPAREN
                       | Primary PERIOD TypeArguments IDENT LPAREN ArgumentList RPAREN
                       | Primary PERIOD TypeArguments IDENT LPAREN  RPAREN
                       | Primary PERIOD  IDENT LPAREN ArgumentList RPAREN
                       | Primary PERIOD  IDENT LPAREN  RPAREN
                       | SUPER PERIOD TypeArguments IDENT LPAREN ArgumentList RPAREN
                       | SUPER PERIOD TypeArguments IDENT LPAREN  RPAREN
                       | SUPER PERIOD  IDENT LPAREN ArgumentList RPAREN
                       | SUPER PERIOD  IDENT LPAREN  RPAREN
                       | TypeName PERIOD SUPER PERIOD TypeArguments IDENT LPAREN ArgumentList RPAREN
                       | TypeName PERIOD SUPER PERIOD TypeArguments IDENT LPAREN  RPAREN
                       | TypeName PERIOD SUPER PERIOD  IDENT LPAREN ArgumentList RPAREN
                       | TypeName PERIOD SUPER PERIOD  IDENT LPAREN  RPAREN '''
    p[0] = mytuple(["MethodInvocation"]+p[1 :])


def p_ArgumentList(p):
    '''ArgumentList : Expression COMMAExpressionS'''
    p[0] = mytuple(["ArgumentList"]+p[1 :])

def p_COMMAExpressionS(p):
    '''COMMAExpressionS : COMMA Expression COMMAExpressionS
                       | empty'''
    p[0] = mytuple(["COMMAExpressionS"]+p[1 :])

def p_MethodReference(p):
    '''MethodReference : ExpressionName COLON_SEP TypeArguments IDENT
                      | ReferenceType COLON_SEP TypeArguments IDENT
                      | IDENT COLON_SEP TypeArguments IDENT
                      | Primary COLON_SEP TypeArguments IDENT
                      | SUPER COLON_SEP TypeArguments IDENT
                      | TypeName PERIOD SUPER COLON_SEP TypeArguments IDENT
                      | ClassType COLON_SEP TypeArguments NEW
                      | IDENT COLON_SEP TypeArguments NEW
                      | ExpressionName COLON_SEP IDENT
                    | ReferenceType COLON_SEP IDENT
                    | IDENT COLON_SEP IDENT
                    | Primary COLON_SEP IDENT
                    | SUPER COLON_SEP IDENT
                    | TypeName PERIOD SUPER COLON_SEP IDENT
                    | ClassType COLON_SEP NEW
                    | IDENT COLON_SEP NEW
                      | ArrayType COLON_SEP NEW'''
    p[0] = mytuple(["MethodReference"]+p[1 :])

def p_ArrayCreationExpression(p):
    '''ArrayCreationExpression : NEW PrimitiveType DimExprs Dims
                              | NEW BOOLEAN DimExprs Dims
                              | NEW ClassType DimExprs Dims
                              | NEW IDENT DimExprs Dims
                              | NEW PrimitiveType DimExprs
                              | NEW BOOLEAN DimExprs
                              | NEW ClassType DimExprs
                              | NEW IDENT DimExprs
                              | NEW PrimitiveType Dims ArrayInitializer
                              | NEW BOOLEAN Dims ArrayInitializer
                              | NEW ClassType Dims ArrayInitializer
                              | NEW IDENT Dims ArrayInitializer'''
    p[0] = mytuple(["ArrayCreationExpression : "]+p[1 :])



def p_DimExprs(p):
    '''DimExprs : DimExpr DimExprS'''
    p[0] = mytuple(["DimExprs"]+p[1 :])

def p_DimExprS(p):
    '''DimExprS : DimExpr DimExprS
               | empty'''
    p[0] = mytuple(["DimExprS"]+p[1 :])

def p_DimExpr(p):
    '''DimExpr : AnnotationS LBRACK Expression RBRACK
                | LBRACK Expression RBRACK'''
    p[0] = mytuple(["DimExpr"]+p[1 :])

def p_Expression(p):
    '''Expression : LambdaExpression
                 | AssignmentExpression'''
    p[0] = mytuple(["Expression"]+p[1 :])

def p_LambdaExpression(p):
    '''LambdaExpression : LambdaParameters ARROW LambdaBody'''
    p[0] = mytuple(["LambdaExpression"]+p[1 :])


def p_LambdaParameters(p):
    '''LambdaParameters : IDENT
                       | LPAREN FormalParameterList RPAREN
                       | LPAREN  RPAREN
                       | LPAREN InferredFormalParameterList RPAREN'''
    p[0] = mytuple(["LambdaParameters"]+p[1 :])

# def p_ZooFormalParameterList(p):
#     '''ZooFormalParameterList : FormalParameterList
#                        | empty'''
#     p[0] = mytuple(["ZooFormalParameterList"]+p[1 :])


def p_InferredFormalParameterList(p):
    '''InferredFormalParameterList : IDENT COMMAIDENTS'''
    p[0] = mytuple(["InferredFormalParameterList"]+p[1 :])

def p_COMMAIDENTS(p):
    '''COMMAIDENTS : COMMA IDENT COMMAIDENTS
                  | empty'''
    p[0] = mytuple(["COMMAIDENTS"]+p[1 :])

def p_LambdaBody(p):
    '''LambdaBody : Expression
                 | Block'''
    p[0] = mytuple(["LambdaBody"]+p[1 :])

def p_AssignmentExpression(p):
    '''AssignmentExpression : ConditionalExpression
                           | Assignment'''
    p[0] = mytuple(["AssignmentExpression"]+p[1 :])

def p_Assignment(p):
    '''Assignment : LeftHandSide AssignmentOperator Expression
                    | IDENT AssignmentOperator Expression'''
    p[0] = mytuple(["Assignment"]+p[1 :])

def p_LeftHandSide(p):
    '''LeftHandSide : ExpressionName
                   | FieldAccess
                   | ArrayAccess'''
    p[0] = mytuple(["LeftHandSide"]+p[1 :])

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
    p[0] = mytuple(["AssignmentOperator"]+p[1 :])

def p_ConditionalExpression(p):
    '''ConditionalExpression : ConditionalOrExpression
                            | ConditionalOrExpression QUES Expression COLON ConditionalExpression
                            | ConditionalOrExpression QUES Expression COLON LambdaExpression '''
    p[0] = mytuple(["ConditionalExpression"]+p[1 :])

def p_ConditionalOrExpression(p):
    '''ConditionalOrExpression : ConditionalAndExpression
                              | ConditionalOrExpression LOR ConditionalAndExpression'''
    p[0] = mytuple(["ConditionalOrExpression"]+p[1 :])

def p_ConditionalAndExpression(p):
    '''ConditionalAndExpression : InclusiveOrExpression
                               | ConditionalAndExpression LAND InclusiveOrExpression'''
    p[0] = mytuple(["ConditionalAndExpression"]+p[1 :])

def p_InclusiveOrExpression(p):
    '''InclusiveOrExpression : ExclusiveOrExpression
                            | InclusiveOrExpression OR ExclusiveOrExpression'''
    p[0] = mytuple(["InclusiveOrExpression"]+p[1 :])

def p_ExclusiveOrExpression(p):
    '''ExclusiveOrExpression : AndExpression
                            | ExclusiveOrExpression XOR AndExpression'''
    p[0] = mytuple(["ExclusiveOrExpression"]+p[1 :])

def p_AndExpression(p):
    '''AndExpression : EqualityExpression
                    | AndExpression AND EqualityExpression'''
    p[0] = mytuple(["AndExpression"]+p[1 :])

def p_EqualityExpression(p):
    '''EqualityExpression : RelationalExpression
                         | EqualityExpression EQL RelationalExpression
                         | EqualityExpression NEQ RelationalExpression'''
    p[0] = mytuple(["EqualityExpression"]+p[1 :])

def p_RelationalExpression(p):
    '''RelationalExpression : ShiftExpression
                           | RelationalExpression LSS ShiftExpression
                           | RelationalExpression GTR ShiftExpression
                           | RelationalExpression LEQ ShiftExpression
                           | RelationalExpression GEQ ShiftExpression
                           | RelationalExpression INSTANCEOF ReferenceType
                           | RelationalExpression INSTANCEOF IDENT'''
    p[0] = mytuple(["RelationalExpression"]+p[1 :])

def p_ShiftExpression(p):
    '''ShiftExpression : AdditiveExpression
                      | ShiftExpression SHL AdditiveExpression
                      | ShiftExpression SHR AdditiveExpression
                      | ShiftExpression SHR_UN AdditiveExpression'''
    p[0] = mytuple(["ShiftExpression"]+p[1 :])

def p_AdditiveExpression(p):
    '''AdditiveExpression : MultiplicativeExpression
                         | AdditiveExpression ADD MultiplicativeExpression
                         | AdditiveExpression SUB MultiplicativeExpression
                          | AdditiveExpression ADD IDENT
                          | AdditiveExpression SUB IDENT'''
    p[0] = mytuple(["AdditiveExpression"]+p[1 :])

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
    p[0] = mytuple(["MultiplicativeExpression"]+p[1 :])

def p_UnaryExpression(p):
    '''UnaryExpression : PreIncrementExpression
                      | PreDecrementExpression
                      | ADD UnaryExpression
                      | SUB UnaryExpression
                      | UnaryExpressionNotPlusMinus'''
    p[0] = mytuple(["UnaryExpression"]+p[1 :])

def p_PreIncrementExpression(p):
    '''PreIncrementExpression : INC UnaryExpression
                                | INC IDENT'''
    p[0] = mytuple(["PreIncrementExpression"]+p[1 :])

def p_PreDecrementExpression(p):
    '''PreDecrementExpression : DEC UnaryExpression
                                | DEC IDENT'''
    p[0] = mytuple(["PreDecrementExpression"]+p[1 :])


def p_UnaryExpressionNotPlusMinus(p):
    '''UnaryExpressionNotPlusMinus : PostfixExpression
                                   | LNOT UnaryExpression
                                   | NOT UnaryExpression
                                   | LNOT IDENT
                                   | NOT IDENT
                                   | CastExpression'''
    p[0] = mytuple(["UnaryExpressionNotPlusMinus"]+p[1 :])

def p_PostfixExpression(p):
    '''PostfixExpression : Primary
                        | ExpressionName
                        | PostIncrementExpression
                        | PostDecrementExpression'''
    p[0] = mytuple(["PostfixExpression"]+p[1 :])

def p_PostIncrementExpression(p):
    '''PostIncrementExpression : PostfixExpression INC
                                | IDENT INC'''
    p[0] = mytuple(["PostIncrementExpression"]+p[1 :])

def p_PostDecrementExpression(p):
    '''PostDecrementExpression : PostfixExpression DEC
                                | IDENT DEC'''
    p[0] = mytuple(["PostDecrementExpression"]+p[1 :])

def p_CastExpression(p):
    '''CastExpression : LPAREN PrimitiveType RPAREN UnaryExpression
                     | LPAREN PrimitiveType RPAREN IDENT
                     | LPAREN BOOLEAN RPAREN UnaryExpression
                  | LPAREN BOOLEAN RPAREN IDENT
                     | LPAREN ReferenceType AdditionalBoundS RPAREN UnaryExpressionNotPlusMinus
                     | LPAREN ReferenceType AdditionalBoundS RPAREN IDENT
                     | LPAREN ReferenceType AdditionalBoundS RPAREN LambdaExpression
                  | LPAREN IDENT AdditionalBoundS RPAREN UnaryExpressionNotPlusMinus
                  | LPAREN IDENT AdditionalBoundS RPAREN IDENT
                  | LPAREN IDENT AdditionalBoundS RPAREN LambdaExpression
                  | LPAREN ReferenceType RPAREN UnaryExpressionNotPlusMinus
                  | LPAREN ReferenceType RPAREN IDENT
                  | LPAREN ReferenceType RPAREN LambdaExpression
               | LPAREN IDENT RPAREN UnaryExpressionNotPlusMinus
               | LPAREN IDENT RPAREN IDENT
               | LPAREN IDENT RPAREN LambdaExpression'''
    p[0] = mytuple(["CastExpression"]+p[1 :])

def p_AdditionalBoundS(p):
    '''AdditionalBoundS : AdditionalBound AdditionalBoundS
                       | AdditionalBound'''
    p[0] = mytuple(["AdditionalBoundS"]+p[1 :])

def p_ConstantExpression(p):
    '''ConstantExpression : Expression'''
    p[0] = mytuple(["ConstantExpression"]+p[1 :])

#</editor-fold>############################################

#<editor-fold Section 7 : Packages #########################
################################################
### Section 7 : Packages
################################################
def p_CompilationUnit(p):
    '''CompilationUnit : ImportDeclarationS TypeDeclarationS
                    | PackageDeclaration ImportDeclarationS TypeDeclarationS'''
    p[0] = mytuple(["CompilationUnit"]+p[1 :])

# def p_ZooPackageDeclaration(p):
#     '''ZooPackageDeclaration :  PackageDeclaration
#                              | empty'''
#     p[0] = mytuple(["ZooPackageDeclaration"]+p[1 :])

def p_ImportDeclarationS(p):
    '''ImportDeclarationS : ImportDeclaration ImportDeclarationS
                          | empty'''
    p[0] = mytuple(["ImportDeclarationS"]+p[1 :])

def p_TypeDeclarationS(p):
    '''TypeDeclarationS : TypeDeclaration TypeDeclarationS
                        | SEMICOLON TypeDeclarationS
                          | empty'''
    p[0] = mytuple(["TypeDeclarationS"]+p[1 :])

def p_PackageDeclaration(p):
    '''PackageDeclaration : PackageModifierS PACKAGE IDENT PERIODIDENTS SEMICOLON'''
    p[0] = mytuple(["PackageDeclaration"]+p[1 :])

def p_PackageModifierS(p):
    '''PackageModifierS : PackageModifier PackageModifierS
                          | empty'''
    p[0] = mytuple(["PackageModifierS"]+p[1 :])

def p_PERIODIDENTS(p):
    '''PERIODIDENTS : PERIOD IDENT PERIODIDENTS
                   | empty'''
    p[0] = mytuple(["PERIODIDENTS"]+p[1 :])

def p_PackageModifier(p):
    '''PackageModifier : Annotation'''
    p[0] = mytuple(["PackageModifier"]+p[1 :])

def p_ImportDeclaration(p):
    '''ImportDeclaration : SingleTypeImportDeclaration
                        | TypeImportOnDemandDeclaration
                        | SingleStaticImportDeclaration
                        | StaticImportOnDemandDeclaration'''
    p[0] = mytuple(["ImportDeclaration"]+p[1 :])

def p_SingleTypeImportDeclaration(p):
    '''SingleTypeImportDeclaration : IMPORT TypeName SEMICOLON'''
    p[0] = mytuple(["SingleTypeImportDeclaration"]+p[1 :])

def p_TypeImportOnDemandDeclaration(p):
    '''TypeImportOnDemandDeclaration : IMPORT ExpressionName PERIOD MUL SEMICOLON
                                     | IMPORT IDENT PERIOD MUL SEMICOLON'''
    p[0] = mytuple(["TypeImportOnDemandDeclaration"]+p[1 :])

def p_SingleStaticImportDeclaration(p):
    '''SingleStaticImportDeclaration : IMPORT STATIC TypeName PERIOD IDENT SEMICOLON'''
    p[0] = mytuple(["SingleStaticImportDeclaration"]+p[1 :])

def p_StaticImportOnDemandDeclaration(p):
    '''StaticImportOnDemandDeclaration : IMPORT STATIC TypeName PERIOD MUL SEMICOLON'''
    p[0] = mytuple(["StaticImportOnDemandDeclaration"]+p[1 :])

def p_TypeDeclaration(p):
    '''TypeDeclaration : ClassDeclaration
                      | InterfaceDeclaration'''
    p[0] = mytuple(["TypeDeclaration"]+p[1 :])

#</editor-fold>############################################

#<editor-fold Section 6 #########################
####################################
########## Section 6 : ##############
####################################

# def p_TypeName(p):
#     '''TypeName : IDENT
#                 | ExpressionName PERIOD IDENT '''
#     p[0] = mytuple(["type_name"]+p[1 :])

def p_TypeName(p):
    '''TypeName : ExpressionName'''
    p[0] = mytuple(["type_name"]+p[1 :])

# def p_PackageOrTypeName(p):
#     '''ExpressionName : IDENT
#                         | ExpressionName PERIOD IDENT '''
#     p[0] = mytuple(["ExpressionName"]+p[1 :])


def p_ExpressionName(p):
    '''ExpressionName : PERIOD IDENT
                        | ExpressionName PERIOD IDENT'''
    p[0] = mytuple(["ExpressionName"]+p[1 :])


# def p_MethodName(p):
#     '''MethodName : IDENT'''
#     p[0] = mytuple(["MethodName"]+p[1 :])

# def p_PackageName(p):
#     '''PackageName : IDENT
#                     | PackageName PERIOD IDENT'''
#     p[0] = mytuple(["PackageName"]+p[1 :])

# def p_AmbiguousName(p):
#     '''ExpressionName : IDENT
#                     | ExpressionName PERIOD IDENT'''
#     p[0] = mytuple(["ExpressionName"]+p[1 :])

####################################
########## SECTION #8 ##############
####################################

def p_ClassDeclaration(p):
    '''ClassDeclaration : NormalClassDeclaration
                        | EnumDeclaration'''
    p[0] = mytuple(["ClassDeclaration"]+p[1 :])

# def p_ZooTypeParameters(p):
#     ''' ZooTypeParameters : TypeParameters
#                           | empty
#     '''
#     p[0] = mytuple(["ZooTypeParameters"]+p[1 :])
def p_SuperClass(p):
    '''SuperClass : EXTENDS ClassType
                    | EXTENDS IDENT
    '''
    p[0] = mytuple(["SuperClass"] + p[1:])


# def p_ZooSuperClass(p):
#     ''' ZooSuperClass : SuperClass
#                           | empty
#     '''
#     p[0] = mytuple(["ZooSuperClass"]+p[1 :])

# def p_Superinterfaces(p):
#     '''Superinterfaces : IMPLEMENTS InterfaceTypeList
#     '''
#     p[0] = mytuple(["Superinterfaces"] + p[1:])

# def p_ZooSuperinterfaces(p):
#     ''' ZooSuperinterfaces : Superinterfaces
#                           | empty
#     '''
#     p[0] = mytuple(["ZooSuperinterfaces"]+p[1 :])

def p_NormalClassDeclaration(p):
    '''NormalClassDeclaration : CommonModifierS CLASS IDENT TypeParameters
                            | CommonModifierS CLASS IDENT
                            | CLASS IDENT TypeParameters
                            | CLASS IDENT
                              | SuperClass Superinterfaces ClassBody
                              | SuperClass  ClassBody
                              | Superinterfaces ClassBody
                              | ClassBody'''
    p[0] = mytuple(["NormalClassDeclaration"]+p[1 :])

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
#     p[0] = mytuple(["ClassModifier"]+p[1 :])

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
#     p[0] = mytuple(["ClassModifier"]+p[1 :])

def p_TypeParameters(p):
    '''TypeParameters : LSS TypeParameterList GTR
    '''
    p[0] = mytuple(["TypeParameters"]+p[1 :])

def p_COMMMATypeParameterS(p):
    '''COMMMATypeParameterS : COMMA TypeParameter COMMMATypeParameterS
                            | empty
    '''
    p[0] = mytuple(["COMMMATypeParameterS"]+p[1 :])

def p_TypeParameterList(p):
    '''TypeParameterList : TypeParameter COMMMATypeParameterS
    '''
    p[0] = mytuple(["TypeParameterList"]+p[1 :])

# def p_Superclass(p):
#     '''Superclass : EXTENDS ClassType
#     '''
#     p[0] = mytuple(["Superclass"]+p[1 :])

def p_Superinterfaces(p):
    '''Superinterfaces : IMPLEMENTS InterfaceTypeList
    '''
    p[0] = mytuple(["Superinterfaces"]+p[1 :])

def p_COMMAInterfaceTypeS(p):
    '''COMMAInterfaceTypeS : COMMA ClassType COMMAInterfaceTypeS
                            | COMMA IDENT COMMAInterfaceTypeS
                            | empty
    '''
    p[0] = mytuple(["COMMAInterfaceTypeS"]+p[1 :])

def p_InterfaceTypeList(p):
    '''InterfaceTypeList : ClassType COMMAInterfaceTypeS
                    | IDENT COMMAInterfaceTypeS
    '''
    p[0] = mytuple(["InterfaceTypeList"]+p[1 :])

def p_ClassBodyDeclarationS(p):
    '''ClassBodyDeclarationS : ClassBodyDeclaration ClassBodyDeclarationS
                            | SEMICOLON ClassBodyDeclarationS
                             | empty
    '''
    p[0] = mytuple(["ClassBodyDeclarationS"]+p[1 :])

def p_ClassBody(p):
    '''ClassBody : LBRACE ClassBodyDeclarationS RBRACE
    '''
    p[0] = mytuple(["ClassBody"]+p[1 :])

def p_ClassBodyDeclaration(p):
    '''ClassBodyDeclaration : ClassMemberDeclaration
                            | Block
                            | StaticInitializer
                            | ConstructorDeclaration
    '''
    p[0] = mytuple(["ClassBodyDeclaration"]+p[1 :])

def p_ClassMemberDeclaration(p):
    '''ClassMemberDeclaration : FieldDeclaration
                            | MethodDeclaration
                            | ClassDeclaration
                            | InterfaceDeclaration
    '''
    p[0] = mytuple(["ClassMemberDeclaration"]+p[1 :])

# def p_FieldModifierS(p):
#     '''CommonModifierS : CommonModifier CommonModifierS
#                         | CommonModifier
#     '''
#     p[0] = mytuple(["CommonModifierS"]+p[1 :])

def p_FieldDeclaration(p):
    '''FieldDeclaration : CommonModifierS UnannType VariableDeclaratorList SEMICOLON
                        | CommonModifierS IDENT VariableDeclaratorList SEMICOLON
                        | UnannType VariableDeclaratorList SEMICOLON
                        | IDENT VariableDeclaratorList SEMICOLON
                        | CommonModifierS UnannType IDENT SEMICOLON
                        | CommonModifierS IDENT IDENT SEMICOLON
                        | UnannType IDENT SEMICOLON
                        | IDENT IDENT SEMICOLON
                        '''
    p[0] = mytuple(["FieldDeclaration"]+p[1 :])

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
#     p[0] = mytuple(["CommonModifier"]+p[1 :])
def p_COMMAVariableDeclaratorS(p):
    '''COMMAVariableDeclaratorS : COMMA VariableDeclarator COMMAVariableDeclaratorS
                            | COMMA IDENT COMMAVariableDeclaratorS
                                | COMMA IDENT
                                | COMMA VariableDeclarator
    '''
    p[0] = mytuple(["COMMAVariableDeclaratorS"]+p[1 :])

def p_VariableDeclaratorList(p):
    '''VariableDeclaratorList : VariableDeclarator COMMAVariableDeclaratorS
                    | IDENT COMMAVariableDeclaratorS
                    | VariableDeclarator
    '''
    p[0] = mytuple(["VariableDeclaratorList"]+p[1 :])
#
# def p_ZooASSIGNVariableInitializer(p):
#     '''ZooASSIGNVariableInitializer : ASSIGN VariableInitializer
#                                     | empty
#     '''
#     p[0] = mytuple(["ZooASSIGNVariableInitializer"]+p[1 :])

def p_VariableDeclarator(p):
    '''VariableDeclarator : VariableDeclaratorId ASSIGN VariableInitializer
                        | IDENT ASSIGN VariableInitializer
                        | VariableDeclaratorId
    '''
    p[0] = mytuple(["VariableDeclarator"]+p[1 :])

# def p_ZooDims(p):
#     '''ZooDims : Dims
#                 | empty
#     '''
#     p[0] = mytuple(["ZooDims"]+p[1 :])

def p_VariableDeclaratorId(p):
    '''VariableDeclaratorId : IDENT Dims'''
    p[0] = mytuple(["VariableDeclaratorId"]+p[1 :])

def p_VariableInitializer (p):
    '''VariableInitializer : Expression
                            | ArrayInitializer
    '''
    p[0] = mytuple(["VariableInitializer"]+p[1 :])

def p_UnannType(p):
    '''UnannType :  UnannPrimitiveType
                | UnannReferenceType
    '''
    p[0] = mytuple(["UnannType"]+p[1 :])

def p_UnannPrimitiveType (p):
    '''UnannPrimitiveType :  NumericType
                        | BOOLEAN
    '''
    p[0] = mytuple(["UnannPrimitiveType"]+p[1 :])

def p_UnannReferenceType (p):
    '''UnannReferenceType :  UnannClassType
                        | UnannArrayType
    '''
    p[0] = mytuple(["UnannReferenceType"]+p[1 :])

# def p_UnannClassOrInterfaceType (p):
#     '''UnannClassType :  UnannClassType'''
#     p[0] = mytuple(["UnannClassType"]+p[1 :])

# def p_ZooTypeArguments(p):
#     '''ZooTypeArguments : TypeArguments
#                         | empty
#     '''
# def p_AnnotationS(p):
#     '''AnnotationS : Annotation AnnotationS
#                     | empty
#     '''

def p_UnannClassType (p):
    '''UnannClassType : IDENT TypeArguments
                        | UnannClassType PERIOD IDENT
                        | UnannClassType PERIOD IDENT TypeArguments
                        | UnannClassType PERIOD AnnotationS IDENT
                        | UnannClassType PERIOD AnnotationS IDENT TypeArguments
                        | IDENT PERIOD IDENT
                        | IDENT PERIOD IDENT TypeArguments
                        | IDENT PERIOD AnnotationS IDENT
                        | IDENT PERIOD AnnotationS IDENT TypeArguments
    '''
    p[0] = mytuple(["UnannClassType"]+p[1 :])

# def p_UnannInterfaceType (p):
#     '''UnannClassType : UnannClassType
#     '''
#     p[0] = mytuple(["UnannClassType"]+p[1 :])

# def p_UnannTypeVariable (p):
#     '''IDENT : IDENT
#     '''
#     p[0] = mytuple(["IDENT"]+p[1 :])

def p_UnannArrayType (p):
    '''UnannArrayType :  UnannPrimitiveType Dims
                        | UnannClassType Dims
                        | IDENT Dims
    '''
    p[0] = mytuple(["UnannArrayType"]+p[1 :])


# def p_MethodModifierS(p):
#     '''CommonModifierS : CommonModifier CommonModifierS
#                         | CommonModifier
#     '''
#     p[0] = mytuple(["CommonModifierS"]+p[1 :])
def p_MethodDeclaration (p):
    '''MethodDeclaration : CommonModifierS MethodHeader MethodBody
                         | MethodHeader MethodBody
                        | CommonModifierS MethodHeader SEMICOLON
                        | MethodHeader SEMICOLON
    '''
    p[0] = mytuple(["MethodDeclaration"]+p[1 :])

# def p_MethodModifier (p):
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
#     p[0] = mytuple(["CommonModifier"]+p[1 :])


# def p_ZooThrows(p):
#     '''ZooThrows : Throws
#                 | empty
#     '''
#     p[0] = mytuple(["ZooThrows"]+p[1 :])

def p_MethodHeader (p):
    '''MethodHeader : UnannType MethodDeclarator Throws
                    | TypeParameters AnnotationS UnannType MethodDeclarator Throws
                    | TypeParameters UnannType MethodDeclarator Throws
                    | VOID MethodDeclarator Throws
                    | TypeParameters AnnotationS VOID MethodDeclarator Throws
                    | TypeParameters VOID MethodDeclarator Throws
                    | IDENT MethodDeclarator Throws
                    | TypeParameters AnnotationS IDENT MethodDeclarator Throws
                    | TypeParameters IDENT MethodDeclarator Throws
                    | UnannType MethodDeclarator
                    | TypeParameters AnnotationS UnannType MethodDeclarator
                    | TypeParameters UnannType MethodDeclarator
                    | VOID MethodDeclarator
                    | TypeParameters AnnotationS VOID MethodDeclarator
                    | TypeParameters VOID MethodDeclarator
                    | IDENT MethodDeclarator
                    | TypeParameters AnnotationS IDENT MethodDeclarator
                    | TypeParameters IDENT MethodDeclarator
    '''
    p[0] = mytuple(["MethodHeader"]+p[1 :])

# def p_Result (p):
#     '''Result :  UnannType
#     '''
#     p[0] = mytuple(["Result"]+p[1 :])

# def p_ZooFormalParameterList (p):
#     '''ZooFormalParameterList : FormalParameterList
#                                 | empty
#     '''
#     p[0] = mytuple(["ZooFormalParameterList"]+p[1 :])

def p_MethodDeclarator (p):
    '''MethodDeclarator : IDENT LPAREN FormalParameterList RPAREN Dims
                        | IDENT LPAREN FormalParameterList RPAREN
                        | IDENT LPAREN RPAREN Dims
                        | IDENT LPAREN RPAREN
    '''
    p[0] = mytuple(["MethodDeclarator"]+p[1 :])



def p_FormalParameterList (p):
    '''FormalParameterList :  ReceiverParameter
                            | FormalParameters COMMA LastFormalParameter
                            | LastFormalParameter
    '''
    p[0] = mytuple(["FormalParameterList"]+p[1 :])

def p_COMMAFormalParameterS (p):
    '''COMMAFormalParameterS : COMMA FormalParameter COMMAFormalParameterS
                            | empty
    '''
    p[0] = mytuple(["COMMAFormalParameterS"]+p[1 :])

def p_FormalParameters (p):
    '''FormalParameters : FormalParameter COMMAFormalParameterS
                        | ReceiverParameter COMMAFormalParameterS
    '''
    p[0] = mytuple(["FormalParameters"]+p[1 :])

# def p_ZooVariableModifier (p):
#     '''ZooVariableModifier : CommonModifier
#                             | empty
#     '''
#     p[0] = mytuple(["ZooVariableModifier"] + p[1 :])

def p_FormalParameter (p):
    '''FormalParameter : CommonModifier UnannType VariableDeclaratorId
                        | CommonModifier IDENT VariableDeclaratorId
                        | CommonModifier UnannType IDENT
                        | CommonModifier IDENT IDENT
                        |  UnannType VariableDeclaratorId
                        |  IDENT VariableDeclaratorId
                        |  UnannType IDENT
                        |  IDENT IDENT
    '''
    p[0] = mytuple(["FormalParameter"] + p[1 :])



# def p_VariableModifier (p):
#     '''CommonModifier : Annotation
#                         | FINAL
#     '''
#     p[0] = mytuple(["CommonModifier"] + p[1 :])


# def p_VariableModifierS (p):
#     '''CommonModifierS : CommonModifier CommonModifierS
#                         | empty
#     '''
#     p[0] = mytuple(["CommonModifierS"] + p[1 :])

def p_LastFormalParameter (p):
    '''LastFormalParameter : CommonModifierS UnannType AnnotationS ELLIPSIS VariableDeclaratorId
                            | CommonModifierS IDENT AnnotationS ELLIPSIS VariableDeclaratorId
                            | FormalParameter
                            | CommonModifierS UnannType ELLIPSIS VariableDeclaratorId
                            | CommonModifierS IDENT ELLIPSIS VariableDeclaratorId
                            | CommonModifierS UnannType AnnotationS ELLIPSIS IDENT
                            | CommonModifierS IDENT AnnotationS ELLIPSIS IDENT
                            | CommonModifierS UnannType ELLIPSIS IDENT
                            | CommonModifierS IDENT ELLIPSIS IDENT
                            |  UnannType AnnotationS ELLIPSIS VariableDeclaratorId
                            |  IDENT AnnotationS ELLIPSIS VariableDeclaratorId
                            |  UnannType ELLIPSIS VariableDeclaratorId
                            |  IDENT ELLIPSIS VariableDeclaratorId
                            |  UnannType AnnotationS ELLIPSIS IDENT
                            |  IDENT AnnotationS ELLIPSIS IDENT
                            |  UnannType ELLIPSIS IDENT
                            |  IDENT ELLIPSIS IDENT

    '''
    p[0] = mytuple(["LastFormalParameter"] + p[1 :])

# def p_ZooIDENTPERIOD (p):
#     '''ZooIDENTPERIOD : IDENT PERIOD
#                         | empty
#     '''
#     p[0] = mytuple(["ZooIDENTPERIOD"] + p[1 :])

def p_ReceiverParameter (p):
    '''ReceiverParameter : AnnotationS UnannType IDENT PERIOD THIS
                            | AnnotationS IDENT IDENT PERIOD THIS
                            | UnannType IDENT PERIOD THIS
                            | IDENT IDENT PERIOD THIS
                            | AnnotationS UnannType THIS
                            | AnnotationS IDENT THIS
                            | UnannType THIS
                            | IDENT THIS
    '''
    p[0] = mytuple(["ReceiverParameter"] + p[1 :])


def p_Throws (p):
    '''Throws :  THROWS ExceptionTypeList
    '''
    p[0] = mytuple(["Throws"] + p[1 :])

def p_COMMAExceptionTypeS (p):
    '''COMMAExceptionTypeS : COMMA ExceptionType COMMAExceptionTypeS
                    | COMMA IDENT COMMAExceptionTypeS
                            | empty
    '''
    p[0] = mytuple(["COMMAExceptionTypeS"] + p[1 :])


def p_ExceptionTypeList (p):
    '''ExceptionTypeList : ExceptionType COMMAExceptionTypeS
                    | IDENT COMMAExceptionTypeS
    '''
    p[0] = mytuple(["ExceptionTypeList"] + p[1 :])


def p_ExceptionType (p):
    ''' ExceptionType :  ClassType
                        | TypeVariable
    '''
    p[0] = mytuple(["ExceptionType"] + p[1 :])

def p_MethodBody (p):
    '''MethodBody : Block
    '''
    p[0] = mytuple(["MethodBody"] + p[1 :])

# def p_InstanceInitializer (p):
#     '''Block : Block
#     '''
#     p[0] = mytuple(["Block"] + p[1 :])

def p_StaticInitializer (p):
    '''StaticInitializer : STATIC Block
    '''
    p[0] = mytuple(["StaticInitializer"] + p[1 :])

# def p_ConstructorModifierS (p):
#     '''ConstructorModifierS : ConstructorModifier ConstructorModifierS
#                             | ConstructorModifier
#     '''
#     p[0] = mytuple(["ConstructorModifierS"] + p[1 :])

def p_ConstructorDeclaration (p):
    '''ConstructorDeclaration : CommonModifierS ConstructorDeclarator ConstructorBody
                                | CommonModifierS ConstructorDeclarator Throws ConstructorBody
                                |  ConstructorDeclarator ConstructorBody
                                |  ConstructorDeclarator Throws ConstructorBody
    '''
    p[0] = mytuple(["ConstructorDeclaration"] + p[1 :])



# def p_ConstructorModifier (p):
#     '''ConstructorModifier : Annotation
#                             | PUBLIC
#                             | PROTECTED
#                             | PRIVATE
#     '''
#     p[0] = mytuple(["ConstructorModifier"] + p[1 :])

def p_ConstructorDeclarator (p):
    '''ConstructorDeclarator : TypeParameters IDENT LPAREN FormalParameterList RPAREN
                            |  IDENT LPAREN FormalParameterList RPAREN
                            | TypeParameters IDENT LPAREN  RPAREN
                            |  IDENT LPAREN  RPAREN
    '''
    p[0] = mytuple(["ConstructorDeclarator"] + p[1 :])

# def p_SimpleTypeName (p):
#     '''IDENT : IDENT
#     '''
#     p[0] = mytuple(["IDENT"] + p[1 :])

def p_ConstructorBody (p):
    '''ConstructorBody : LBRACE  ExplicitConstructorInvocation BlockStatements  RBRACE
                        | LBRACE  ExplicitConstructorInvocation SEMICOLON  RBRACE
                        | LBRACE  ExplicitConstructorInvocation  RBRACE
                        | LBRACE  BlockStatements  RBRACE
                        | LBRACE  SEMICOLON  RBRACE
                        | LBRACE  RBRACE
    '''
    p[0] = mytuple(["ConstructorBody"] + p[1 :])

# def p_ZooExplicitConstructorInvocation (p):
#     '''ZooExplicitConstructorInvocation : ExplicitConstructorInvocation
#                                         | empty
#     '''
#     p[0] = mytuple(["ZooExplicitConstructorInvocation"] + p[1 :])

# def p_ZooBlockStatements (p):
#     '''ZooBlockStatements : BlockStatements
#                             | empty
#     '''
#     p[0] = mytuple(["ZooBlockStatements"] + p[1 :])

# def p_ZooArgumentList (p):
#     '''ZooArgumentList : ArgumentList
#                         | empty
#     '''
#     p[0] = mytuple(["ZooArgumentList"] + p[1 :])

def p_ExplicitConstructorInvocation (p):
    '''ExplicitConstructorInvocation : TypeArguments THIS LPAREN ArgumentList RPAREN SEMICOLON
                                    | TypeArguments THIS LPAREN  RPAREN SEMICOLON
                                    |  THIS LPAREN ArgumentList RPAREN SEMICOLON
                                    |  THIS LPAREN  RPAREN SEMICOLON
                                    | TypeArguments SUPER LPAREN ArgumentList RPAREN SEMICOLON
                                    | TypeArguments SUPER LPAREN  RPAREN SEMICOLON
                                    |  SUPER LPAREN ArgumentList RPAREN SEMICOLON
                                    |  SUPER LPAREN  RPAREN SEMICOLON
                                    | ExpressionName PERIOD TypeArguments SUPER LPAREN ArgumentList RPAREN SEMICOLON
                                    | ExpressionName PERIOD  SUPER LPAREN ArgumentList RPAREN SEMICOLON
                                    | ExpressionName PERIOD TypeArguments SUPER LPAREN  RPAREN SEMICOLON
                                    | ExpressionName PERIOD  SUPER LPAREN  RPAREN SEMICOLON
                                    | IDENT PERIOD TypeArguments SUPER LPAREN ArgumentList RPAREN SEMICOLON
                                    | IDENT PERIOD  SUPER LPAREN ArgumentList RPAREN SEMICOLON
                                    | IDENT PERIOD TypeArguments SUPER LPAREN  RPAREN SEMICOLON
                                    | IDENT PERIOD  SUPER LPAREN  RPAREN SEMICOLON
                                    | Primary PERIOD TypeArguments SUPER LPAREN ArgumentList RPAREN SEMICOLON
                                    | Primary PERIOD TypeArguments SUPER LPAREN RPAREN SEMICOLON
                                    | Primary PERIOD  SUPER LPAREN ArgumentList RPAREN SEMICOLON
                                    | Primary PERIOD  SUPER LPAREN  RPAREN SEMICOLON
    '''
    p[0] = mytuple(["ExplicitConstructorInvocation"] + p[1:])

# def p_ClassModifierS (p):
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
#     p[0] = mytuple(["ClassModifierS"] + p[1 :])


def p_EnumDeclaration (p):
    '''EnumDeclaration : CommonModifierS ENUM IDENT Superinterfaces EnumBody
                    | CommonModifierS ENUM IDENT EnumBody
                    |  ENUM IDENT Superinterfaces EnumBody
                    |  ENUM IDENT EnumBody
    '''
    p[0] = mytuple(["EnumDeclaration"] + p[1 :])

# def p_ZooEnumConstantList (p):
#     '''ZooEnumConstantList : EnumConstantList
#                             | empty
#     '''
#     p[0] = mytuple(["ZooEnumConstantList"] + p[1 :])
#
# def p_ZooCOMMA (p):
#     '''ZooCOMMA : COMMA
#                 | empty
#     '''
#     p[0] = mytuple(["ZooCOMMA"] + p[1 :])
#
# def p_ZooEnumBodyDeclarations (p):
#     '''ZooEnumBodyDeclarations : EnumBodyDeclarations
#                                 | empty
#     '''
#     p[0] = mytuple(["ZooEnumBodyDeclarations"] + p[1 :])


def p_EnumBody (p):
    '''EnumBody : LBRACE EnumConstantList COMMA EnumBodyDeclarations  RBRACE
                | LBRACE EnumConstantList COMMA   RBRACE
                | LBRACE EnumConstantList  EnumBodyDeclarations  RBRACE
                | LBRACE EnumConstantList    RBRACE
                | LBRACE COMMA EnumBodyDeclarations  RBRACE
                | LBRACE COMMA   RBRACE
                | LBRACE  EnumBodyDeclarations  RBRACE
                | LBRACE    RBRACE
    '''
    p[0] = mytuple(["EnumBody"] + p[1 :])

def p_COMMAEnumConstantS (p):
    '''COMMAEnumConstantS : COMMA EnumConstant COMMAEnumConstantS
                          | empty
    '''
    p[0] = mytuple(["COMMAEnumConstantS"] + p[1 :])


def p_EnumConstantList (p):
    '''EnumConstantList : EnumConstant COMMAEnumConstantS
    '''
    p[0] = mytuple(["EnumConstantList"] + p[1 :])


def p_EnumConstant (p):
    '''EnumConstant : EnumConstantModifierS IDENT LPAREN RPAREN ClassBody
    | EnumConstantModifierS IDENT LPAREN ArgumentList  RPAREN ClassBody
    | EnumConstantModifierS IDENT  ClassBody
    | EnumConstantModifierS IDENT LPAREN RPAREN
    | EnumConstantModifierS IDENT LPAREN ArgumentList  RPAREN
    | EnumConstantModifierS IDENT
    '''
    p[0] = mytuple(["EnumConstant"] + p[1 :])


def p_EnumConstantModifierS (p):
    '''EnumConstantModifierS : EnumConstantModifier EnumConstantModifierS
                            | empty
    '''
    p[0] = mytuple(["EnumConstantModifierS"] + p[1 :])


# def p_ZooClassBody (p):
#     '''ZooClassBody : ClassBody
#                     | empty
#     '''
#     p[0] = mytuple(["ZooClassBody"] + p[1 :])
#

# def p_ZooLPARENZooArgumentListRPAREN (p):
#     '''ZooLPARENZooArgumentListRPAREN : LPAREN ZooArgumentList RPAREN
#                                         | LPAREN RPAREN
#                                         | empty
#     '''
#     p[0] = mytuple(["ZooLPARENZooArgumentListRPAREN"] + p[1 :])

def p_EnumConstantModifier (p):
    '''EnumConstantModifier : Annotation
    '''
    p[0] = mytuple(["EnumConstantModifier"] + p[1 :])


def p_EnumBodyDeclarations (p):
    '''EnumBodyDeclarations : SEMICOLON ClassBodyDeclarationS
    '''
    p[0] = mytuple(["EnumBodyDeclarations"] + p[1 :])

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
    p[0]=mytuple(["PrimitiveType"]+p[1 :])

# def p_AnnotationS(p):
#     '''AnnotationS : Annotation AnnotationS
#                        | empty '''
#     p[0]=mytuple(["AnnotationS"]+p[1 :])

#

def p_NumericType(p):
    '''NumericType : IntegralType
                   | FloatingPointType'''
    p[0]=mytuple(["NumericType"]+p[1 :])

#

def p_IntegralType(p):
    '''IntegralType : BYTE
                    | SHORT
                    | INT
                    | LONG
                    | CHAR'''
    p[0]=mytuple(["IntegralType"]+p[1 :])

#

def p_FloatingPointType(p):
    '''FloatingPointType : FLOAT
                         | DOUBLE'''
    p[0]=mytuple(["FloatingPointType"]+p[1 :])

#

def p_ReferenceType(p):
    '''ReferenceType : ClassType
                     | TypeVariable
                     | ArrayType'''
    p[0]=mytuple(["ReferenceType"]+p[1 :])

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
                | TypeVariable
                 | IDENT TypeArguments
                 | ClassType PERIOD TypeVariable TypeArguments
                 | ClassType PERIOD IDENT TypeArguments
                 | IDENT PERIOD TypeVariable TypeArguments
                 | IDENT PERIOD IDENT TypeArguments
                 | ClassType PERIOD TypeVariable
                 | ClassType PERIOD IDENT
                 | IDENT PERIOD TypeVariable
                 | IDENT PERIOD IDENT  '''
    p[0]=mytuple(["ClassType"]+p[1 :])


# def p_ZooTypeArguments(p):
#     '''ZooTypeArguments : TypeArguments
#                         | empty '''
#     p[0]=mytuple(["ZooTypeArguments"]+p[1 :])

#

# def p_InterfaceType(p):
#     '''ClassType : ClassType'''
#     p[0]=mytuple(["ClassType"]+p[1 :])

#
def p_TypeVariable(p):
    '''TypeVariable : AnnotationS IDENT'''
    p[0]=mytuple(["TypeVariable"]+p[1 :])

#

def p_ArrayType(p):
    '''ArrayType :  PrimitiveType Dims
                | BOOLEAN Dims
                 |  ClassType Dims
                 |  TypeVariable Dims
                 | IDENT Dims'''
    p[0]=mytuple(["ArrayType"]+p[1 :])

#

def p_Dims(p):
    '''Dims : AnnotationS LBRACE RBRACE AnnotationSLBRACERBRACES
            | LBRACE RBRACE AnnotationSLBRACERBRACES'''
    p[0]=mytuple(["Dims"]+p[1 :])

def p_AnnotationSLBRACERBRACES(p):
    '''AnnotationSLBRACERBRACES : AnnotationS LBRACE RBRACE AnnotationSLBRACERBRACES
                                | LBRACE RBRACE AnnotationSLBRACERBRACES
                                | empty '''
    p[0]=mytuple(["AnnotationSLBRACERBRACES"]+p[1 :])

#

def p_TypeParameter(p):
    '''TypeParameter :  TypeParameterModifierS IDENT TypeBound
                    | TypeParameterModifierS IDENT'''
    p[0]=mytuple(["TypeParameter"]+p[1 :])

def p_TypeParameterModifierS(p):
    '''TypeParameterModifierS : TypeParameterModifier TypeParameterModifierS
                              | empty '''
    p[0]=mytuple(["TypeParameterModifierS"]+p[1 :])

# def p_ZooTypeBound(p):
#     '''ZooTypeBound : TypeBound
#                     | empty '''
#     p[0]=mytuple(["ZooTypeBound"]+p[1 :])
#
# #


def p_TypeParameterModifier(p):
    '''TypeParameterModifier : Annotation '''
    p[0]=mytuple(["TypeParameterModifier"]+p[1 :])

#

def p_TypeBound(p):
    '''TypeBound : EXTENDS TypeVariable
                 | EXTENDS IDENT
                 | EXTENDS ClassType AdditionalBoundS
                 | EXTENDS ClassType
                 | EXTENDS IDENT AdditionalBoundS'''
    p[0]=mytuple(["TypeBound"]+p[1 :])

# def p_AdditionalBoundS(p):
#     '''AdditionalBounds : AdditionalBound AdditionalBounds
#                         | empty '''
#     p[0]=mytuple(["AdditionalBoundS"]+p[1 :])

#

def p_AdditionalBound(p):
    '''AdditionalBound : AND ClassType
                        | AND IDENT'''
    p[0]=mytuple(["AdditionalBound"]+p[1 :])

#

def p_TypeArguments(p):
    '''TypeArguments : LSS TypeArgumentList GTR '''
    p[0]=mytuple(["TypeArguments"]+p[1 :])

#

def p_TypeArgumentList(p):
    '''TypeArgumentList : TypeArgument COMMATypeArgumentS
                        |  IDENT COMMATypeArgumentS'''
    p[0]=mytuple(["TypeArgumentList"]+p[1 :])

def p_COMMATypeArgumentS(p):
    '''COMMATypeArgumentS : COMMA TypeArgument COMMATypeArgumentS
                        | COMMA IDENT COMMATypeArgumentS
                          | empty '''
    p[0]=mytuple(["COMMATypeArgumentS"]+p[1 :])

#

def p_TypeArgument(p):
    '''TypeArgument : ReferenceType
                    | Wildcard '''
    p[0]=mytuple(["TypeArgument"]+p[1 :])

#

def p_Wildcard(p):
    '''Wildcard : AnnotationS QUES WildcardBounds
                | AnnotationS QUES
                | QUES WildcardBounds
                | QUES'''
    p[0]=mytuple(["Wildcard"]+p[1 :])

# def p_ZooWildcardBounds(p):
#     '''ZooWildcardBounds : WildcardBounds
#                          | empty '''
#     p[0]=mytuple(["ZooWildcardBounds"]+p[1 :])

#

def p_WildcardBounds(p):
    '''WildcardBounds : EXTENDS ReferenceType
                      | EXTENDS IDENT
                      | SUPER ReferenceType
                      | SUPER IDENT'''
    p[0]=mytuple(["WildcardBounds"]+p[1 :])

#</editor-fold> Section 4 #########################

#<editor-fold> Section 14 #########################
###################################
# Section 14
# #################################


def p_Block(p):
    '''Block : LBRACE RBRACE
    | LBRACE BlockStatements RBRACE
    | LBRACE SEMICOLON RBRACE
'''
    p[0]=mytuple(["Block"]+p[1 :])

# def p_ZooBlockStatements(p):
#     '''ZooBlockStatements : BlockStatements
# | empty'''
#     p[0]=mytuple(["ZooBlockStatements"]+p[1 :])

def p_BlockStatements(p):
    '''BlockStatements : BlockStatement BlockStatements
                        | SEMICOLON BlockStatements
                        | BlockStatement SEMICOLON
                        | BlockStatement
'''
                        # TODO: This was removed: | SEMICOLON SEMICOLON
    p[0]=mytuple(["BlockStatements"]+p[1 :])

# def p_BlockStatementsS(p):
#     '''BlockStatementsS : BlockStatement BlockStatementsS
# | empty'''
#     p[0]=mytuple(["BlockStatementsS"]+p[1 :])


def p_BlockStatement(p):
    '''BlockStatement : LocalVariableDeclarationStatement
                    | ClassDeclaration
                    | Statement
                    '''
    p[0]=mytuple(["BlockStatement"]+p[1 :])

def p_LocalVariableDeclarationStatement(p):
    '''LocalVariableDeclarationStatement : LocalVariableDeclaration SEMICOLON
'''
    p[0]=mytuple(["LocalVariableDeclarationStatement"]+p[1 :])

def p_LocalVariableDeclaration(p):
    '''LocalVariableDeclaration : CommonModifierS UnannType VariableDeclaratorList
                                | CommonModifierS IDENT VariableDeclaratorList
                                |  UnannType VariableDeclaratorList
                                |  IDENT VariableDeclaratorList
                                | CommonModifierS UnannType IDENT
                                | CommonModifierS IDENT IDENT
                                |  UnannType IDENT
                                |  IDENT IDENT
'''
    p[0]=mytuple(["LocalVariableDeclaration"]+p[1 :])
# def p_VariableModifierS(p):
#     '''CommonModifierS : CommonModifier CommonModifierS
# | empty'''
#     p[0]=mytuple(["CommonModifierS"]+p[1 :])

def p_Statement(p):
    '''Statement : StatementWithoutTrailingSubstatement
        | LabeledStatement
        | IfThenStatement
        | IfThenElseStatement
        | WhileStatement
        | ForStatement
        '''
    p[0]=mytuple(["Statement"]+p[1 :])

def p_StatementNoShortIf(p):
    '''StatementNoShortIf : StatementWithoutTrailingSubstatement
| LabeledStatementNoShortIf
| IfThenElseStatementNoShortIf
| WhileStatementNoShortIf
| ForStatementNoShortIf
'''
    p[0]=mytuple(["StatementNoShortIf"]+p[1 :])

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
    p[0]=mytuple(["StatementWithoutTrailingSubstatement"]+p[1 :])

# def p_EmptyStatement(p):
#     '''EmptyStatement : SEMICOLON
# '''
#     p[0]=mytuple(["EmptyStatement"]+p[1 :])

def p_LabeledStatement(p):
    '''LabeledStatement : IDENT  COLON  Statement
                    | IDENT COLON SEMICOLON
'''
    p[0]=mytuple(["LabeledStatement"]+p[1 :])

def p_LabeledStatementNoShortIf(p):
    '''LabeledStatementNoShortIf : IDENT  COLON  StatementNoShortIf
                        | IDENT COLON SEMICOLON
'''
    p[0]=mytuple(["LabeledStatementNoShortIf"]+p[1 :])

def p_ExpressionStatement(p):
    '''ExpressionStatement : StatementExpression SEMICOLON
'''
    p[0]=mytuple(["ExpressionStatement"]+p[1 :])

def p_StatementExpression(p):
    '''StatementExpression : Assignment
| PreIncrementExpression
| PreDecrementExpression
| PostIncrementExpression
| PostDecrementExpression
| MethodInvocation
| ClassInstanceCreationExpression
'''
    p[0]=mytuple(["StatementExpression"]+p[1 :])

def p_IfThenStatement(p):
    '''IfThenStatement : IF LPAREN Expression RPAREN Statement
        | IF LPAREN Expression RPAREN SEMICOLON
'''
    p[0]=mytuple(["IfThenStatement"]+p[1 :])

def p_IfThenElseStatement(p):
    '''IfThenElseStatement : IF LPAREN Expression RPAREN StatementNoShortIf ELSE Statement
            | IF LPAREN Expression RPAREN SEMICOLON ELSE Statement
            | IF LPAREN Expression RPAREN StatementNoShortIf ELSE SEMICOLON
            | IF LPAREN Expression RPAREN SEMICOLON ELSE SEMICOLON
'''
    p[0]=mytuple(["IfThenElseStatement"]+p[1 :])

def p_IfThenElseStatementNoShortIf(p):
    '''IfThenElseStatementNoShortIf : IF LPAREN Expression RPAREN StatementNoShortIf ELSE StatementNoShortIf
        | IF LPAREN Expression RPAREN SEMICOLON ELSE StatementNoShortIf
        | IF LPAREN Expression RPAREN StatementNoShortIf ELSE SEMICOLON
        | IF LPAREN Expression RPAREN SEMICOLON ELSE SEMICOLON
'''
    p[0]=mytuple(["IfThenElseStatementNoShortIf"]+p[1 :])

def p_AssertStatement(p):
    '''AssertStatement : ASSERT Expression SEMICOLON
| ASSERT Expression  COLON  Expression SEMICOLON
'''
    p[0]=mytuple(["AssertStatement"]+p[1 :])

def p_SwitchStatement(p):
    '''SwitchStatement : SWITCH LPAREN Expression RPAREN SwitchBlock
'''
    p[0]=mytuple(["SwitchStatement"]+p[1 :])

def p_SwitchBlock(p):
    '''SwitchBlock : LBRACE SwitchBlockStatementGroupS SwitchLabelS RBRACE
'''
    p[0]=mytuple(["SwitchBlock"]+p[1 :])
def p_SwitchBlockStatementGroupS(p):
    '''SwitchBlockStatementGroupS : SwitchBlockStatementGroup SwitchBlockStatementGroupS
| empty'''
    p[0]=mytuple(["SwitchBlockStatementGroupS"]+p[1 :])

# def p_SwitchBlockStatementGroupS(p):
#     '''SwitchBlockStatementGroupS : SwitchBlockStatementGroup SwitchBlockStatementGroupS
# | empty'''
#     p[0]=mytuple(["SwitchBlockStatementGroupS"]+p[1 :])

def p_SwitchBlockStatementGroup(p):
    '''SwitchBlockStatementGroup : SwitchLabels BlockStatements
                                    | SwitchLabels SEMICOLON
'''
    p[0]=mytuple(["SwitchBlockStatementGroup"]+p[1 :])

def p_SwitchLabels(p):
    '''SwitchLabels : SwitchLabel SwitchLabelS
'''
    p[0]=mytuple(["SwitchLabels"]+p[1 :])
def p_SwitchLabelS(p):
    '''SwitchLabelS : SwitchLabel SwitchLabelS
| empty'''
    p[0]=mytuple(["SwitchLabelS"]+p[1 :])

def p_SwitchLabel(p):
    '''SwitchLabel : CASE ConstantExpression  COLON
    | CASE IDENT COLON
    | DEFAULT  COLON '''
    p[0]=mytuple(["SwitchLabel"]+p[1 :])

# def p_EnumConstantName(p):
#     '''IDENT : IDENT
# '''
#     p[0]=mytuple(["IDENT"]+p[1 :])

def p_WhileStatement(p):
    '''WhileStatement : WHILE LPAREN Expression RPAREN Statement
        | WHILE LPAREN Expression RPAREN SEMICOLON
'''
    p[0]=mytuple(["WhileStatement"]+p[1 :])

def p_WhileStatementNoShortIf(p):
    '''WhileStatementNoShortIf : WHILE LPAREN Expression RPAREN StatementNoShortIf
        | WHILE LPAREN Expression RPAREN SEMICOLON
'''
    p[0]=mytuple(["WhileStatementNoShortIf"]+p[1 :])

def p_DoStatement(p):
    '''DoStatement : DO Statement WHILE LPAREN Expression RPAREN SEMICOLON
        | DO SEMICOLON WHILE LPAREN Expression RPAREN SEMICOLON
'''
    p[0]=mytuple(["DoStatement"]+p[1 :])

def p_ForStatement(p):
    '''ForStatement : BasicForStatement
| EnhancedForStatement
'''
    p[0]=mytuple(["ForStatement"]+p[1 :])

def p_ForStatementNoShortIf(p):
    '''ForStatementNoShortIf : BasicForStatementNoShortIf
| EnhancedForStatementNoShortIf
'''
    p[0]=mytuple(["ForStatementNoShortIf"]+p[1 :])

def p_BasicForStatement(p):
    '''BasicForStatement : FOR LPAREN ForInit SEMICOLON Expression SEMICOLON ForUpdate RPAREN Statement
    | FOR LPAREN ForInit SEMICOLON Expression SEMICOLON RPAREN Statement
    | FOR LPAREN ForInit SEMICOLON SEMICOLON ForUpdate RPAREN Statement
    | FOR LPAREN ForInit SEMICOLON SEMICOLON  RPAREN Statement
    | FOR LPAREN  SEMICOLON Expression SEMICOLON ForUpdate RPAREN Statement
    | FOR LPAREN  SEMICOLON Expression SEMICOLON RPAREN Statement
    | FOR LPAREN  SEMICOLON SEMICOLON ForUpdate RPAREN Statement
    | FOR LPAREN  SEMICOLON SEMICOLON  RPAREN Statement
    | FOR LPAREN ForInit SEMICOLON Expression SEMICOLON ForUpdate RPAREN SEMICOLON
    | FOR LPAREN ForInit SEMICOLON Expression SEMICOLON RPAREN SEMICOLON
    | FOR LPAREN ForInit SEMICOLON SEMICOLON ForUpdate RPAREN SEMICOLON
    | FOR LPAREN ForInit SEMICOLON SEMICOLON  RPAREN SEMICOLON
    | FOR LPAREN  SEMICOLON Expression SEMICOLON ForUpdate RPAREN SEMICOLON
    | FOR LPAREN  SEMICOLON Expression SEMICOLON RPAREN SEMICOLON
    | FOR LPAREN  SEMICOLON SEMICOLON ForUpdate RPAREN SEMICOLON
    | FOR LPAREN  SEMICOLON SEMICOLON  RPAREN SEMICOLON
'''
    p[0]=mytuple(["BasicForStatement"]+p[1 :])

# def p_ZooForUpdate(p):
#     '''ZooForUpdate : ForUpdate
# | empty'''
#     p[0]=mytuple(["ZooForUpdate"]+p[1 :])
#
# def p_ZooExpression(p):
#     '''ZooExpression : Expression
# | empty'''
#     p[0]=mytuple(["ZooExpression"]+p[1 :])
#
# def p_ZooForInit(p):
#     '''ZooForInit : ForInit
# | empty'''
#     p[0]=mytuple(["ZooForInit"]+p[1 :])

def p_BasicForStatementNoShortIf(p):
    '''BasicForStatementNoShortIf : FOR LPAREN ForInit SEMICOLON Expression SEMICOLON ForUpdate RPAREN StatementNoShortIf
                                | FOR LPAREN ForInit SEMICOLON Expression SEMICOLON  RPAREN StatementNoShortIf
                                | FOR LPAREN ForInit SEMICOLON  SEMICOLON ForUpdate RPAREN StatementNoShortIf
                                | FOR LPAREN ForInit SEMICOLON  SEMICOLON  RPAREN StatementNoShortIf
                                | FOR LPAREN  SEMICOLON Expression SEMICOLON ForUpdate RPAREN StatementNoShortIf
                                | FOR LPAREN  SEMICOLON Expression SEMICOLON  RPAREN StatementNoShortIf
                                | FOR LPAREN  SEMICOLON  SEMICOLON ForUpdate RPAREN StatementNoShortIf
                                | FOR LPAREN  SEMICOLON  SEMICOLON  RPAREN StatementNoShortIf
                                | FOR LPAREN ForInit SEMICOLON Expression SEMICOLON ForUpdate RPAREN SEMICOLON
                                | FOR LPAREN ForInit SEMICOLON Expression SEMICOLON  RPAREN SEMICOLON
                                | FOR LPAREN ForInit SEMICOLON  SEMICOLON ForUpdate RPAREN SEMICOLON
                                | FOR LPAREN ForInit SEMICOLON  SEMICOLON  RPAREN SEMICOLON
                                | FOR LPAREN  SEMICOLON Expression SEMICOLON ForUpdate RPAREN SEMICOLON
                                | FOR LPAREN  SEMICOLON Expression SEMICOLON  RPAREN SEMICOLON
                                | FOR LPAREN  SEMICOLON  SEMICOLON ForUpdate RPAREN SEMICOLON
                                | FOR LPAREN  SEMICOLON  SEMICOLON  RPAREN SEMICOLON

'''
    p[0]=mytuple(["BasicForStatementNoShortIf"]+p[1 :])

def p_ForInit(p):
    '''ForInit : StatementExpressionList
| LocalVariableDeclaration
'''
    p[0]=mytuple(["ForInit"]+p[1 :])

def p_ForUpdate(p):
    '''ForUpdate : StatementExpressionList
'''
    p[0]=mytuple(["ForUpdate"]+p[1 :])

def p_StatementExpressionList(p):
    '''StatementExpressionList : StatementExpression COMMAStatementExpressionS
'''
    p[0]=mytuple(["StatementExpressionList"]+p[1 :])


def p_COMMAStatementExpressionS(p):
    '''COMMAStatementExpressionS : COMMA StatementExpression COMMAStatementExpressionS
                    | empty'''
    p[0]=mytuple(["COMMAStatementExpressionS"]+p[1 :])



def p_EnhancedForStatement(p):
    '''EnhancedForStatement : FOR LPAREN CommonModifierS UnannType VariableDeclaratorId  COLON  Expression RPAREN Statement
                            | FOR LPAREN CommonModifierS IDENT VariableDeclaratorId  COLON  Expression RPAREN Statement
                            | FOR LPAREN CommonModifierS UnannType IDENT  COLON  Expression RPAREN Statement
                            | FOR LPAREN CommonModifierS IDENT IDENT  COLON  Expression RPAREN Statement
                            | FOR LPAREN  UnannType VariableDeclaratorId  COLON  Expression RPAREN Statement
                            | FOR LPAREN  IDENT VariableDeclaratorId  COLON  Expression RPAREN Statement
                            | FOR LPAREN  UnannType IDENT  COLON  Expression RPAREN Statement
                            | FOR LPAREN  IDENT IDENT  COLON  Expression RPAREN Statement
                            | FOR LPAREN CommonModifierS UnannType VariableDeclaratorId  COLON  Expression RPAREN SEMICOLON
                            | FOR LPAREN CommonModifierS IDENT VariableDeclaratorId  COLON  Expression RPAREN SEMICOLON
                            | FOR LPAREN CommonModifierS UnannType IDENT  COLON  Expression RPAREN SEMICOLON
                            | FOR LPAREN CommonModifierS IDENT IDENT  COLON  Expression RPAREN SEMICOLON
                            | FOR LPAREN  UnannType VariableDeclaratorId  COLON  Expression RPAREN SEMICOLON
                            | FOR LPAREN  IDENT VariableDeclaratorId  COLON  Expression RPAREN SEMICOLON
                            | FOR LPAREN  UnannType IDENT  COLON  Expression RPAREN SEMICOLON
                            | FOR LPAREN  IDENT IDENT  COLON  Expression RPAREN SEMICOLON
'''
    p[0]=mytuple(["EnhancedForStatement"]+p[1 :])

def p_EnhancedForStatementNoShortIf(p):
    '''EnhancedForStatementNoShortIf : FOR LPAREN CommonModifierS UnannType VariableDeclaratorId  COLON  Expression RPAREN StatementNoShortIf
                                    | FOR LPAREN CommonModifierS IDENT VariableDeclaratorId  COLON  Expression RPAREN StatementNoShortIf
                                    | FOR LPAREN CommonModifierS UnannType IDENT  COLON  Expression RPAREN StatementNoShortIf
                                    | FOR LPAREN CommonModifierS IDENT IDENT  COLON  Expression RPAREN StatementNoShortIf
                                    | FOR LPAREN  UnannType VariableDeclaratorId  COLON  Expression RPAREN StatementNoShortIf
                                    | FOR LPAREN  IDENT VariableDeclaratorId  COLON  Expression RPAREN StatementNoShortIf
                                    | FOR LPAREN  UnannType IDENT  COLON  Expression RPAREN StatementNoShortIf
                                    | FOR LPAREN  IDENT IDENT  COLON  Expression RPAREN StatementNoShortIf
                                    | FOR LPAREN CommonModifierS UnannType VariableDeclaratorId  COLON  Expression RPAREN SEMICOLON
                                    | FOR LPAREN CommonModifierS IDENT VariableDeclaratorId  COLON  Expression RPAREN SEMICOLON
                                    | FOR LPAREN CommonModifierS UnannType IDENT  COLON  Expression RPAREN SEMICOLON
                                    | FOR LPAREN CommonModifierS IDENT IDENT  COLON  Expression RPAREN SEMICOLON
                                    | FOR LPAREN  UnannType VariableDeclaratorId  COLON  Expression RPAREN SEMICOLON
                                    | FOR LPAREN  IDENT VariableDeclaratorId  COLON  Expression RPAREN SEMICOLON
                                    | FOR LPAREN  UnannType IDENT  COLON  Expression RPAREN SEMICOLON
                                    | FOR LPAREN  IDENT IDENT  COLON  Expression RPAREN SEMICOLON
'''
    p[0]=mytuple(["EnhancedForStatementNoShortIf"]+p[1 :])

def p_BreakStatement(p):
    '''BreakStatement : BREAK SEMICOLON
                    | BREAK IDENT SEMICOLON
'''
    p[0]=mytuple(["BreakStatement"]+p[1 :])
# def p_ZooIDENT(p):
#     '''ZooIDENT : IDENT
# | empty'''
#     p[0]=mytuple(["ZooIDENT"]+p[1 :])

def p_ContinueStatement(p):
    '''ContinueStatement : CONTINUE IDENT SEMICOLON
                        | CONTINUE SEMICOLON
'''
    p[0]=mytuple(["ContinueStatement"]+p[1 :])

def p_ReturnStatement(p):
    '''ReturnStatement : RETURN Expression SEMICOLON
                    |  RETURN  SEMICOLON
'''
    p[0]=mytuple(["ReturnStatement"]+p[1 :])
# def p_ZooExpression(p):
#     '''ZooExpression : Expression
# | empty'''
#     p[0]=mytuple(["ZooExpression"]+p[1 :])

def p_ThrowStatement(p):
    '''ThrowStatement : THROW Expression SEMICOLON
'''
    p[0]=mytuple(["ThrowStatement"]+p[1 :])

def p_SynchronizedStatement(p):
    '''SynchronizedStatement : SYNCHRONIZED LPAREN Expression RPAREN Block
'''
    p[0]=mytuple(["SynchronizedStatement"]+p[1 :])

def p_TryStatement(p):
    '''TryStatement : TRY Block Catches
| TRY Block  Finally
| TRY Block Catches Finally
| TryWithResourcesStatement
'''
    p[0]=mytuple(["TryStatement"]+p[1 :])
# def p_ZooCatches(p):
#     '''ZooCatches : Catches
# | empty'''
#     p[0]=mytuple(["ZooCatches"]+p[1 :])

def p_Catches(p):
    '''Catches : CatchClause CatchClauseS
'''
    p[0]=mytuple(["Catches"]+p[1 :])
def p_CatchClauseS(p):
    '''CatchClauseS : CatchClause CatchClauseS
| empty'''
    p[0]=mytuple(["CatchClauseS"]+p[1 :])

def p_CatchClause(p):
    '''CatchClause : CATCH LPAREN CatchFormalParameter RPAREN Block
'''
    p[0]=mytuple(["CatchClause"]+p[1 :])

def p_CatchFormalParameter(p):
    '''CatchFormalParameter : CommonModifierS CatchType VariableDeclaratorId
                            | CommonModifierS CatchType IDENT
                            |  CatchType VariableDeclaratorId
                            |  CatchType IDENT
'''
    p[0]=mytuple(["CatchFormalParameter"]+p[1 :])

def p_CatchType(p):
    '''CatchType : UnannClassType ORClassTypeS
                | IDENT ORClassTypeS
'''
    p[0]=mytuple(["CatchType"]+p[1 :])

def p_ORClassTypeS(p):
    '''ORClassTypeS : OR ClassType ORClassTypeS
                    | OR IDENT ORClassTypeS
                    | empty'''
    p[0]=mytuple(["ORClassTypeS"]+p[1 :])


def p_Finally(p):
    '''Finally : FINALLY Block
'''
    p[0]=mytuple(["Finally"]+p[1 :])

def p_TryWithResourcesStatement(p):
    '''TryWithResourcesStatement : TRY ResourceSpecification Block Catches Finally
                                | TRY ResourceSpecification Block  Finally
                                | TRY ResourceSpecification Block Catches
                                | TRY ResourceSpecification Block
'''
    p[0]=mytuple(["TryWithResourcesStatement"]+p[1 :])
# def p_ZooFinally(p):
#     '''ZooFinally : Finally
# | empty'''
#     p[0]=mytuple(["ZooFinally"]+p[1 :])
#
#
# def p_ZooSEMICOLON(p):
#     '''ZooSEMICOLON : SEMICOLON
# | empty'''
#     p[0]=mytuple(["ZooSEMICOLON"]+p[1 :])

def p_ResourceSpecification(p):
    '''ResourceSpecification : LPAREN ResourceList SEMICOLON RPAREN
                            | LPAREN ResourceList RPAREN
'''
    p[0]=mytuple(["ResourceSpecification"]+p[1 :])

def p_ResourceList(p):
    '''ResourceList : Resource SEMICOLONResourceS
                | Resource
'''
    p[0]=mytuple(["ResourceList"]+p[1 :])


def p_SEMICOLONResourceS(p):
    '''SEMICOLONResourceS : SEMICOLON Resource SEMICOLONResourceS
                    | SEMICOLON Resource'''
    p[0]=mytuple(["SEMICOLONResourceS"]+p[1 :])




def p_CommonModifierS(p):
    '''CommonModifierS : CommonModifier CommonModifierS
                        | CommonModifier
    '''
    p[0]=mytuple(["CommonModifierS"]+p[1 :])


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
                    | DEFAULT
    '''
    p[0]=mytuple(["CommonModifier"]+p[1 :])


def p_Resource(p):
    '''Resource : CommonModifierS UnannType VariableDeclaratorId ASSIGN Expression
                | CommonModifierS IDENT VariableDeclaratorId ASSIGN Expression
                | CommonModifierS UnannType IDENT ASSIGN Expression
                | CommonModifierS IDENT IDENT ASSIGN Expression
                |  UnannType VariableDeclaratorId ASSIGN Expression
                |  IDENT VariableDeclaratorId ASSIGN Expression
                |  UnannType IDENT ASSIGN Expression
                |  IDENT IDENT ASSIGN Expression'''
    p[0]=mytuple(["Resource"]+p[1 :])

def p_StartCompilationUnit( p):
    '''start : INC CompilationUnit'''
    p[0] = p[2]

# def p_start_expression( p):
#     '''start : DEC expression'''
#     p[0] = p[2]


# def p_start_statement( p):
#     '''start : MUL block_statement'''
#     p[0] = p[2]

#</editor-fold> Section 14 #########################


def p_error( p):
    print('error: {}'.format(p))


lexer = lex.lex(module=lexRule)
parser = yacc.yacc(start='start', debug = 1)
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
def parse_string(code, debug=0, lineno=1, prefix='++'):
    lexer.input(code)
    print("In parse_string!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    while True :
        tok = lexer.token()
        if not tok : # No more input
            break
        # elif tok.type in lexRule.literals_ :
        #     HASH_MAP[tok.value] = "Literal"
        # elif tok.type in lexRule.separators :
        #     HASH_MAP[tok.value] = "Separator"
        # elif tok.type == 'IDENT' :
        #     HASH_MAP[tok.value] = "IDENT"
        # elif tok.type in lexRule.operators :
        #     HASH_MAP[tok.value] = "Operator"
        # elif tok.type in list(lexRule.reserved.values()):
        #     HASH_MAP[tok.value] = "Keyword"
        # else : # Comments or unknown
        # continue
#
        # print(tok)
#
    print("END of TOKENS")
    lexer.lineno = lineno
    return parser.parse(prefix + code, lexer=lexer, debug=1)

def parse_file(_file, debug=0):
    print("In parse_file!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    if type(_file) == str :
        _file = open(_file)
    content = _file.read()
    return parse_string(content, debug=debug)

# get_parse = Parser()
# parse_out = get_parse.parse_file("../test/ackermann.java")
# print(parse_out)
# t = tac.code
# print(t)
parse_out = parse_file("./ackermann.java")
print(parse_out)
