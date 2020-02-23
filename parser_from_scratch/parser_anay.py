import pydot
import lexRule
import ply.lex as lex
import ply.yacc as yacc
from model import *
import pdb
global tokens


tokens = lexRule.tokens


## Source: https://docs.oracle.com/javase/specs/jls/se8/html/jls-19.html

def p_empty(p):
    '''empty:'''
    p[0]="epsilon"

#<editor-fold Section 3 #########################
################################################
### SECTION 3:
################################################
def p_literal(p):
    '''literal: BOOL_LIT
        | NULL_LIT
        | DECIMAL_LIT
        | HEX_LIT
        | OCTAL_LIT
        | BINARY_LIT
        | FLOAT_DEC_LIT
        | FLOAT_HEX_LIT
        | STRING_LIT
        | CHAR_LIT'''
    p[0] = tuple(["literal"]+p[1:])

#</editor-fold>############################################

#<editor-fold Section 9: Interfaces #########################
################################################
### SECTION 9: Interfaces
################################################
def p_InterfaceDeclaration(p):
    '''InterfaceDeclaration: NormalInterfaceDeclaration
                           | AnnotationTypeDeclaration'''
    p[0] = tuple(["InterfaceDeclaration"]+p[1:])

def p_NormalInterfaceDeclaration(p):
    '''NormalInterfaceDeclaration:  InterfaceModifierS INTERFACE IDENT ZooTypeParameters ZooExtendsInterfaces InterfaceBody'''
    p[0] = tuple(["NormalInterfaceDeclaration"]+p[1:])

def p_ZooTypeParameters(p):
    '''ZooTypeParameters:  TypeParameters | empty'''
    p[0] = tuple(["ZooTypeParameters"]+p[1:])

def p_ZooExtendsInterfaces(p):
    '''ZooExtendsInterfaces: ExtendsInterfaces | empty '''
    p[0] = tuple(["ZooExtendsInterfaces"]+p[1:])

def p_InterfaceModifierS(p):
    '''InterfaceModifierS: InterfaceModifier InterfaceModifierS
                          | empty'''
    p[0] = tuple(["InterfaceModifierS"]+p[1:])

def p_InterfaceModifier(p):
    '''InterfaceModifier: Annotation
                         | PUBLIC
                         | PROTECTED
                         | PRIVATE
                         | ABSTRACT
                         | STATIC
                         | STRICTFP'''
    p[0] = tuple(["InterfaceModifier"]+p[1:])


def p_ExtendsInterfaces(p):
    '''ExtendsInterfaces: EXTENDS InterfaceTypeList'''
    p[0] = tuple(["ExtendsInterfaces"]+p[1:])


def p_InterfaceBody(p):
    '''InterfaceBody: LBRACE InterfaceMemberDeclarationS RBRACE '''
    p[0] = tuple(["InterfaceBody"]+p[1:])


def p_InterfaceMemberDeclarationS(p):
    ''' InterfaceMemberDeclarationS: InterfaceMemberDeclaration InterfaceMemberDeclarationS
                                    | empty '''
    p[0] = tuple(["InterfaceMemberDeclarationS"]+p[1:])


def p_InterfaceMemberDeclaration(p):
    '''InterfaceMemberDeclaration: ConstantDeclaration
                                 | InterfaceMethodDeclaration
                                 | ClassDeclaration
                                 | InterfaceDeclaration
                                 | SEMICOLON'''
    p[0] = tuple(["InterfaceMemberDeclaration"]+p[1:])

def p_ConstantDeclaration(p):
    '''ConstantDeclaration: ConstantModifierS UnannType VariableDeclaratorList SEMICOLON'''
    p[0] = tuple(["ConstantDeclaration"]+p[1:])

def p_ConstantModifierS(p):
    '''ConstantModifierS: ConstantModifier ConstantModifierS
                        | empty '''
    p[0] = tuple(["ConstantModifierS"]+p[1:])

def p_ConstantModifier(p):
    '''ConstantModifier: Annotation
                       | PUBLIC
                       | STATIC
                       | FINAL'''
    p[0] = tuple(["ConstantModifier"]+p[1:])

def p_InterfaceMethodDeclaration(p):
    '''InterfaceMethodDeclaration: InterfaceMethodModifierS MethodHeader MethodBody'''
    p[0] = tuple(["InterfaceMethodDeclaration"]+p[1:])

def p_InterfaceMethodModifierS(p):
    '''InterfaceMethodModifierS: InterfaceMethodModifier InterfaceMethodModifierS
                               | empty'''
    p[0] = tuple(["InterfaceMethodModifierS"]+p[1:])

def p_InterfaceMethodModifier(p):
    '''InterfaceMethodModifier:  Annotation
                                | PUBLIC
                                | ABSTRACT
                                | DEFAULT
                                | STATIC
                                | STRICTFP'''
    p[0] = tuple(["InterfaceMethodModifier"]+p[1:])

def p_AnnotationTypeDeclaration(p):
    '''AnnotationTypeDeclaration: InterfaceModifierS ATRATE INTERFACE IDENT AnnotationTypeBody'''
    p[0] = tuple(["AnnotationTypeDeclaration"]+p[1:])

def p_InterfaceModifierS(p):
    '''InterfaceModifierS: InterfaceModifier InterfaceModifierS
                         | empty'''
    p[0] = tuple(["InterfaceModifierS"]+p[1:])

def p_AnnotationTypeBody(p):
    '''AnnotationTypeBody:  LBRACE AnnotationTypeMemberDeclarationS RBRACE'''
    p[0] = tuple(["AnnotationTypeBody"]+p[1:])

def AnnotationTypeMemberDeclarationS(p):
    '''AnnotationTypeMemberDeclarationS: AnnotationTypeMemberDeclaration AnnotationTypeMemberDeclarationS
                         | empty'''
    p[0] = tuple(["AnnotationTypeMemberDeclarationS"]+p[1:])

def p_AnnotationTypeMemberDeclaration(p):
    '''AnnotationTypeMemberDeclaration: AnnotationTypeElementDeclaration
                                        | ConstantDeclaration
                                        | ClassDeclaration
                                        | InterfaceDeclaration
                                        | SEMICOLON'''
    p[0] = tuple(["AnnotationTypeMemberDeclaration"]+p[1:])

def p_AnnotationTypeElementDeclaration(p):
    '''AnnotationTypeElementDeclaration:  AnnotationTypeElementModifierS UnannType IDENT LPAREN RPAREN ZooDims ZooDefaultValue SEMICOLON'''
    p[0] = tuple(["AnnotationTypeElementDeclaration"]+p[1:])

def p_ZooDims(p):
    '''ZooDims: Dims
              | empty'''
    p[0] = tuple(["ZooDims"]+p[1:])

def p_ZooDefaultValue(p):
    '''ZooDefaultValue: DefaultValue
              | empty'''
    p[0] = tuple(["ZooDefaultValue"]+p[1:])


def p_AnnotationTypeElementModifierS(p):
    '''AnnotationTypeElementModifierS: AnnotationTypeElementModifier AnnotationTypeElementModifierS
                                      | empty'''
    p[0] = tuple(["AnnotationTypeElementModifierS"]+p[1:])

def p_AnnotationTypeElementModifier(p):
    '''AnnotationTypeElementModifier: Annotation
                                     | PUBLIC
                                     | ABSTRACT'''
    p[0] = tuple(["AnnotationTypeElementModifier"]+p[1:])

def p_DefaultValue(p):
    '''DefaultValue: DEFAULT ElementValue'''
    p[0] = tuple(["DefaultValue"]+p[1:])

def p_Annotation(p):
    '''Annotation: NormalAnnotation
                  | MarkerAnnotation
                  | SingleElementAnnotation'''
    p[0] = tuple(["Annotation"]+p[1:])

def p_NormalAnnotation(p):
    '''NormalAnnotation: ATRATE TypeName LPAREN ZooElementValuePairList RPAREN '''
    p[0] = tuple(["NormalAnnotation"]+p[1:])


def p_ZooElementValuePairList(p):
    '''ZooElementValuePairList: ElementValuePairList
              | empty'''
    p[0] = tuple(["ZooElementValuePairList"]+p[1:])


def p_ElementValuePairList(p):
    '''ElementValuePairList: ElementValuePairList COMMAElementValuePairS'''
    p[0] = tuple(["ElementValuePairList"]+p[1:])

def p_COMMAElementValuePairS(p):
    '''COMMAElementValuePairS: COMMA ElementValuePair COMMAElementValuePairS
                              | empty'''
    p[0] = tuple(["COMMAElementValuePairS"]+p[1:])

def p_ElementValuePair(p):
    '''ElementValuePair: IDENT ASSIGN ElementValue'''
    p[0] = tuple(["ElementValuePair"]+p[1:])

def p_ElementValue(p):
    '''ElementValue: ConditionalExpression
                    | ElementValueArrayInitializer
                    | Annotation '''
    p[0] = tuple(["ElementValue"]+p[1:])

def p_ElementValueArrayInitializer(p):
    '''ElementValueArrayInitializer: LBRACE ZooElementValueList ZooCOMMA RBRACE '''
    p[0] = tuple(["ElementValueArrayInitializer"]+p[1:])


def p_ZooElementValueList(p):
    '''ZooElementValueList: ElementValueList
                          | empty '''
    p[0] = tuple(["ZooElementValueList"]+p[1:])

def p_ZooCOMMA(p):
    '''ZooCOMMA: COMMA
               | empty '''
    p[0] = tuple(["ZooCOMMA"]+p[1:])

def p_ElementValueList(p):
    '''ElementValueList: ElementValue  COMMAElementValueS'''
    p[0] = tuple(["ElementValueList"]+p[1:])

def p_COMMAElementValueS(p):
    '''COMMAElementValueS: COMMA ElementValue COMMAElementValueS
                         | empty '''
    p[0] = tuple(["COMMAElementValueS"]+p[1:])

def p_MarkerAnnotation(p):
    '''MarkerAnnotation: ATRATE TypeName'''
    p[0] = tuple(["MarkerAnnotation"]+p[1:])

def p_SingleElementAnnotation(p):
    '''SingleElementAnnotation: ATRATE TypeName LPAREN ElementValue RPAREN'''
    p[0] = tuple(["SingleElementAnnotation"]+p[1:])

#</editor-fold>############################################

#<editor-fold Section 10: Arrays #########################
################################################
### Section 10: Arrays
################################################
def p_ArrayInitializer(p):
    '''ArrayInitializer: LBRACE ZooVariableInitializerList ZooCOMMA RBRACE '''
    p[0] = tuple(["ArrayInitializer"]+p[1:])


def p_ZooVariableInitializerList(p):
    '''ZooVariableInitializerList: VariableInitializerList
                                 | empty'''
    p[0] = tuple(["ZooVariableInitializerList"]+p[1:])

def p_VariableInitializerList(p):
    '''VariableInitializerList: VariableInitializer COMMMAVariableInitializerS'''
    p[0] = tuple([""]+p[1:])

def p_COMMMAVariableInitializerS(p):
    '''COMMMAVariableInitializerS: COMMMAVariableInitializer COMMMAVariableInitializerS
                                 | empty'''
    p[0] = tuple(["COMMMAVariableInitializerS"]+p[1:])

#</editor-fold>############################################

#<editor-fold Section 15: Expressions #########################
################################################
### Section 15: Expressions
################################################

def p_Primary(p):
    '''Primary: PrimaryNoNewArray
              | ArrayCreationExpression '''
    p[0] = tuple(["Primary"]+p[1:])

def p_PrimaryNoNewArray(p):
    '''PrimaryNoNewArray: Literal
                        | ClassLiteral
                        | THIS
                        | TypeName PERIOD THIS
                        | LPAREN Expression RPAREN
                        | ClassInstanceCreationExpression
                        | FieldAccess
                        | ArrayAccess
                        | MethodInvocation
                        | MethodReference'''
    p[0] = tuple([""]+p[1:])

def p_ClassLiteral(p):
    '''ClassLiteral: TypeName LBRACKRBRACKS PERIOD CLASS
                   | NumericType LBRACKRBRACKS PERIOD CLASS
                   | BOOLEAN LBRACKRBRACKS PERIOD CLASS
                   | VOID PERIOD CLASS '''
    p[0] = tuple(["ClassLiteral"]+p[1:])

def p_LBRACKRBRACKS(p):
    '''LBRACKRBRACKS: LBRACK RBRACK LBRACKRBRACKS
                    | empty'''
    p[0] = tuple(["LBRACKRBRACKS"]+p[1:])

def p_ClassInstanceCreationExpression(p):
    '''ClassInstanceCreationExpression: UnqualifiedClassInstanceCreationExpression
                                      | ExpressionName PERIOD UnqualifiedClassInstanceCreationExpression
                                      | Primary PERIOD UnqualifiedClassInstanceCreationExpression'''
    p[0] = tuple(["ClassInstanceCreationExpression"]+p[1:])

def p_UnqualifiedClassInstanceCreationExpression(p):
    '''UnqualifiedClassInstanceCreationExpression: NEW ZooTypeArguments ClassOrInterfaceTypeToInstantiate LPAREN ZooArgumentList RPAREN ZooClassBody '''
    p[0] = tuple(["UnqualifiedClassInstanceCreationExpression"]+p[1:])

def p_ZooTypeArguments(p):
    '''ZooTypeArguments: TypeArguments
                       | empty'''
    p[0] = tuple(["ZooTypeArguments"]+p[1:])

def p_ZooArgumentList(p):
    '''ZooArgumentList: ArgumentList
                       | empty'''
    p[0] = tuple(["ZooArgumentList"]+p[1:])

def p_ZooClassBody(p):
    '''ZooClassBody: ClassBody
                       | empty'''
    p[0] = tuple(["ZooClassBody"]+p[1:])

def p_ClassOrInterfaceTypeToInstantiate(p):
    '''ClassOrInterfaceTypeToInstantiate: AnnotationS IDENT PERIODAnnotationSIDENTS ZooTypeArgumentsOrDiamond'''
    p[0] = tuple(["ClassOrInterfaceTypeToInstantiate"]+p[1:])

def p_AnnotationS(p):
    '''AnnotationS: Annotation AnnotationS
                  | empty'''
    p[0] = tuple(["AnnotationS"]+p[1:])

def p_ZooTypeArgumentsOrDiamond(p):
    '''ZooTypeArgumentsOrDiamond: TypeArgumentsOrDiamond
                                | empty'''
    p[0] = tuple(["ZooTypeArgumentsOrDiamond"]+p[1:])

def PERIODAnnotationSIDENTS(p):
    '''PERIODAnnotationSIDENTS: PERIOD AnnotationS IDENT PERIODAnnotationSIDENTS
                              | empty'''
    p[0] = tuple(["PERIODAnnotationSIDENTS"]+p[1:])

# TODO fix function name of Zoo and ...S(p); also in general
# TODO fix ''' in next line

def p_TypeArgumentsOrDiamond(p):
    '''TypeArgumentsOrDiamond: TypeArguments
                             | LSS GTR'''
    p[0] = tuple(["TypeArgumentsOrDiamond"]+p[1:])

def p_FieldAccess(p):
    '''FieldAccess: Primary PERIOD IDENT
                  | SUPER PERIOD IDENT
                  | TypeName PERIOD SUPER PERIOD IDENT'''
    p[0] = tuple(["FieldAccess"]+p[1:])


def p_ArrayAccess(p):
    '''ArrayAccess: ExpressionName LBRACK Expression RBRACK
                  | PrimaryNoNewArray LBRACK Expression RBRACK'''
    p[0] = tuple(["ArrayAccess"]+p[1:])

def p_MethodInvocation(p):
    '''MethodInvocation: MethodName LPAREN ZooArgumentList RPAREN
                       | TypeName PERIOD ZooTypeArguments IDENT LPAREN ZooArgumentList RPAREN
                       | ExpressionName PERIOD ZooTypeArguments IDENT LPAREN ZooArgumentList RPAREN
                       | Primary PERIOD ZooTypeArguments IDENT LPAREN ZooArgumentList RPAREN
                       | SUPER PERIOD ZooTypeArguments IDENT LPAREN ZooArgumentList RPAREN
                       | TypeName PERIOD SUPER PERIOD ZooTypeArguments IDENT LPAREN ZooArgumentList RPAREN '''
    p[0] = tuple(["MethodInvocation"]+p[1:])


def p_ArgumentList(p):
    '''ArgumentList: Expression COMMAExpressionS'''
    p[0] = tuple(["ArgumentList"]+p[1:])

def p_COMMAExpressionS(p):
    '''COMMAExpressionS: COMMA Expression COMMAExpressionS
                       | empty'''
    p[0] = tuple(["COMMAExpressionS"]+p[1:])

def p_MethodReference(p):
    '''MethodReference: ExpressionName COLON_SEP ZooTypeArguments IDENT
                      | ReferenceType COLON_SEP ZooTypeArguments IDENT
                      | Primary COLON_SEP ZooTypeArguments IDENT
                      | SUPER COLON_SEP ZooTypeArguments IDENT
                      | TypeName PERIOD SUPER COLON_SEP ZooTypeArguments IDENT
                      | ClassType COLON_SEP ZooTypeArguments NEW
                      | ArrayType COLON_SEP NEW'''
    p[0] = tuple(["MethodReference"]+p[1:])

def p_ArrayCreationExpression: (p):
    '''ArrayCreationExpression: NEW PrimitiveType DimExprs ZooDims
                              | NEW ClassOrInterfaceType DimExprs ZooDims
                              | NEW PrimitiveType Dims ArrayInitializer
                              | NEW ClassOrInterfaceType Dims ArrayInitializer'''
    p[0] = tuple(["ArrayCreationExpression: "]+p[1:])



def p_DimExprs(p):
    '''DimExprs: DimExprs DimExprS'''
    p[0] = tuple(["DimExprs"]+p[1:])

def p_DimExprS(p):
    '''DimExprS: DimExpr DimExprS
               | empty'''
    p[0] = tuple(["DimExprS"]+p[1:])

def p_DimExpr(p):
    '''DimExpr: AnnotationS LBRACK Expression RBRACK'''
    p[0] = tuple(["DimExpr"]+p[1:])

def p_Expression(p):
    '''Expression: LambdaExpression
                 | AssignmentExpression'''
    p[0] = tuple(["Expression"]+p[1:])

def p_LambdaExpression(p):
    '''LambdaExpression: LambdaParameters ARROW LambdaBody'''
    p[0] = tuple(["LambdaExpression"]+p[1:])


def p_LambdaParameters(p):
    '''LambdaParameters: IDENT
                       | LPAREN ZooFormalParameterList RPAREN
                       | LPAREN InferredFormalParameterList RPAREN'''
    p[0] = tuple(["LambdaParameters"]+p[1:])

def p_ZooFormalParameterList(p):
    '''ZooFormalParameterList: FormalParameterList
                       | empty'''
    p[0] = tuple(["ZooFormalParameterList"]+p[1:])


def p_InferredFormalParameterList(p):
    '''InferredFormalParameterList: IDENT COMMAIDENTS'''
    p[0] = tuple(["InferredFormalParameterList"]+p[1:])

def p_COMMAIDENTS(p):
    '''COMMAIDENTS: COMMA IDENT COMMAIDENTS
                  | empty'''
    p[0] = tuple(["COMMAIDENTS"]+p[1:])

def p_LambdaBody(p):
    '''LambdaBody: Expression
                 | Block'''
    p[0] = tuple(["LambdaBody"]+p[1:])

def p_AssignmentExpression(p):
    '''AssignmentExpression: ConditionalExpression
                           | Assignment'''
    p[0] = tuple(["AssignmentExpression"]+p[1:])

def p_Assignment(p):
    '''Assignment: LeftHandSide AssignmentOperator Expression'''
    p[0] = tuple(["Assignment"]+p[1:])

def p_LeftHandSide(p):
    '''LeftHandSide: ExpressionName
                   | FieldAccess
                   | ArrayAccess'''
    p[0] = tuple(["LeftHandSide"]+p[1:])

def p_AssignmentOperator(p):
    '''AssignmentOperator: ASSIGN
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
    p[0] = tuple(["AssignmentOperator"]+p[1:])

def p_ConditionalExpression(p):
    '''ConditionalExpression: ConditionalOrExpression
                            | ConditionalOrExpression QUES Expression COLON ConditionalExpression
                            | ConditionalOrExpression QUES Expression COLON LambdaExpression '''
    p[0] = tuple(["ConditionalExpression"]+p[1:])

def p_ConditionalOrExpression(p):
    '''ConditionalOrExpression: ConditionalAndExpression
                              | ConditionalOrExpression LOR ConditionalAndExpression'''
    p[0] = tuple(["ConditionalOrExpression"]+p[1:])

def p_ConditionalAndExpression(p):
    '''ConditionalAndExpression: InclusiveOrExpression
                               | ConditionalAndExpression LAND InclusiveOrExpression'''
    p[0] = tuple(["ConditionalAndExpression"]+p[1:])

def p_InclusiveOrExpression(p):
    '''InclusiveOrExpression: ExclusiveOrExpression
                            | InclusiveOrExpression OR ExclusiveOrExpression'''
    p[0] = tuple(["InclusiveOrExpression"]+p[1:])

def p_ExclusiveOrExpression(p):
    '''ExclusiveOrExpression: AndExpression
                            | ExclusiveOrExpression XOR AndExpression'''
    p[0] = tuple(["ExclusiveOrExpression"]+p[1:])

def p_AndExpression(p):
    '''AndExpression: EqualityExpression
                    | AndExpression AND EqualityExpression'''
    p[0] = tuple(["AndExpression"]+p[1:])

def p_EqualityExpression(p):
    '''EqualityExpression: RelationalExpression
                         | EqualityExpression EQL RelationalExpression
                         | EqualityExpression NEQ RelationalExpression'''
    p[0] = tuple(["EqualityExpression"]+p[1:])

def p_RelationalExpression(p):
    '''RelationalExpression: ShiftExpression
                           | RelationalExpression LSS ShiftExpression
                           | RelationalExpression GTR ShiftExpression
                           | RelationalExpression LEQ ShiftExpression
                           | RelationalExpression GEQ ShiftExpression
                           | RelationalExpression INSTANCEOF ReferenceType'''
    p[0] = tuple(["RelationalExpression"]+p[1:])

def p_ShiftExpression(p):
    '''ShiftExpression: AdditiveExpression
                      | ShiftExpression SHL AdditiveExpression
                      | ShiftExpression SHR AdditiveExpression
                      | ShiftExpression SHR_UN AdditiveExpression'''
    p[0] = tuple(["ShiftExpression"]+p[1:])

def p_AdditiveExpression(p):
    '''AdditiveExpression: MultiplicativeExpression
                         | AdditiveExpression ADD MultiplicativeExpression
                         | AdditiveExpression SUB MultiplicativeExpression'''
    p[0] = tuple(["AdditiveExpression"]+p[1:])

def p_MultiplicativeExpression(p):
    '''MultiplicativeExpression: UnaryExpression
                               | MultiplicativeExpression MUL UnaryExpression
                               | MultiplicativeExpression QUO UnaryExpression
                               | MultiplicativeExpression REM UnaryExpression'''
    p[0] = tuple(["MultiplicativeExpression"]+p[1:])

def p_UnaryExpression(p):
    '''UnaryExpression: PreIncrementExpression
                      | PreDecrementExpression
                      | ADD UnaryExpression
                      | SUB UnaryExpression
                      | UnaryExpressionNotPlusMinus'''
    p[0] = tuple(["UnaryExpression"]+p[1:])

def p_PreIncrementExpression(p):
    '''PreIncrementExpression: INC UnaryExpression'''
    p[0] = tuple(["PreIncrementExpression"]+p[1:])

def p_PreDecrementExpression(p):
    '''PreDecrementExpression: DEC UnaryExpression'''
    p[0] = tuple(["PreDecrementExpression"]+p[1:])


def p_UnaryExpressionNotPlusMinus(p):
    '''UnaryExpressionNotPlusMinus: PostfixExpression
                                   | LNOT UnaryExpression
                                   | NOT UnaryExpression
                                   | CastExpression'''
    p[0] = tuple(["UnaryExpressionNotPlusMinus"]+p[1:])

def p_PostfixExpression(p):
    '''PostfixExpression: Primary
                        | ExpressionName
                        | PostIncrementExpression
                        | PostDecrementExpression'''
    p[0] = tuple(["PostfixExpression"]+p[1:])

def p_PostIncrementExpression(p):
    '''PostIncrementExpression: PostfixExpression INC'''
    p[0] = tuple(["PostIncrementExpression"]+p[1:])

def PostDecrementExpression(p):
    '''PostDecrementExpression: PostfixExpression DEC'''
    p[0] = tuple(["PostDecrementExpression"]+p[1:])

def p_CastExpression(p):
    '''CastExpression: LPAREN PrimitiveType RPAREN UnaryExpression
                     | LPAREN ReferenceType AdditionalBoundS RPAREN UnaryExpressionNotPlusMinus
                     | LPAREN ReferenceType AdditionalBoundS RPAREN LambdaExpression'''
    p[0] = tuple(["CastExpression"]+p[1:])

def p_AdditionalBoundS(p):
    '''AdditionalBoundS: AdditionalBound AdditionalBoundS
                       | empty'''
    p[0] = tuple(["AdditionalBoundS"]+p[1:])

def p_ConstantExpression(p):
    '''ConstantExpression: Expression'''
    p[0] = tuple(["ConstantExpression"]+p[1:])

#</editor-fold>############################################

#<editor-fold Section 7: Packages #########################
################################################
### Section 7: Packages
################################################
def p_CompilationUnit(p):
    '''CompilationUnit: ZooPackageDeclaration ImportDeclarationS TypeDeclarationS'''
    p[0] = tuple(["CompilationUnit"]+p[1:])

def p_ZooPackageDeclaration(p):
    '''ZooPackageDeclaration:  PackageDeclaration
                             | empty'''
    p[0] = tuple(["ZooPackageDeclaration"]+p[1:])

def p_ImportDeclarationS(p):
    '''ImportDeclarationS: ImportDeclaration ImportDeclarationS
                          | empty'''
    p[0] = tuple(["ImportDeclarationS"]+p[1:])

def p_TypeDeclarationS(p):
    '''TypeDeclarationS: TypeDeclaration TypeDeclarationS
                          | empty'''
    p[0] = tuple(["TypeDeclarationS"]+p[1:])

def p_PackageDeclaration(p):
    '''PackageDeclaration: PackageModifierS PACKAGE IDENT PERIODIDENTS SEMICOLON'''
    p[0] = tuple(["PackageDeclaration"]+p[1:])

def p_PERIODIDENTS(p):
    '''PERIODIDENTS: PERIOD IDENT PERIODIDENTS
                   | empty'''
    p[0] = tuple(["PERIODIDENTS"]+p[1:])

def p_PackageModifier(p):
    '''PackageModifier: Annotation'''
    p[0] = tuple(["PackageModifier"]+p[1:])

def p_ImportDeclaration(p):
    '''ImportDeclaration: SingleTypeImportDeclaration
                        | TypeImportOnDemandDeclaration
                        | SingleStaticImportDeclaration
                        | StaticImportOnDemandDeclaration'''
    p[0] = tuple(["ImportDeclaration"]+p[1:])

def p_SingleTypeImportDeclaration(p):
    '''SingleTypeImportDeclaration: IMPORT TypeName SEMICOLON'''
    p[0] = tuple(["SingleTypeImportDeclaration"]+p[1:])

def p_TypeImportOnDemandDeclaration(p):
    '''TypeImportOnDemandDeclaration: IMPORT PackageOrTypeName PERIOD MUL SEMICOLON'''
    p[0] = tuple(["TypeImportOnDemandDeclaration"]+p[1:])

def p_SingleStaticImportDeclaration(p):
    '''SingleStaticImportDeclaration: IMPORT STATIC TypeName PERIOD Identifier SEMICOLON'''
    p[0] = tuple(["SingleStaticImportDeclaration"]+p[1:])

def p_StaticImportOnDemandDeclaration(p):
    '''StaticImportOnDemandDeclaration: IMPORT STATIC TypeName PERIOD MUL SEMICOLON'''
    p[0] = tuple(["StaticImportOnDemandDeclaration"]+p[1:])

def p_TypeDeclaration(p):
    '''TypeDeclaration: ClassDeclaration
                      | InterfaceDeclaration
                      | SEMICOLON'''
    p[0] = tuple(["TypeDeclaration"]+p[1:])

#</editor-fold>############################################


def p_(p):
    ''' '''
    p[0] = tuple([""]+p[1:])

def p_(p):
    ''' '''
    p[0] = tuple([""]+p[1:])

def p_(p):
    ''' '''
    p[0] = tuple([""]+p[1:])

def p_(p):
    ''' '''
    p[0] = tuple([""]+p[1:])

def p_(p):
    ''' '''
    p[0] = tuple([""]+p[1:])

def p_(p):
    ''' '''
    p[0] = tuple([""]+p[1:])
