###################################
# Section 4
# #################################
 
def p_Type(p):
    '''Type : PrimitiveType
            | ReferenceType'''

#

def p_PrimitiveType(p):
    '''PrimitiveType : AnnotationS NumericType
                     | AnnotationS boolean'''

def p_AnnotationS(p):
    '''AnnotationS : Annotation AnnotationS
                       | empty '''

#

def p_NumericType(p):
    '''NumericType : IntegralType 
                   | FloatingPointType'''

#

def p_IntegralType(p):
    '''IntegralType : BYTE
                    | SHORT
                    | INT
                    | LONG
                    | CHAR'''

#

def p_FloatingPointType(p):
    '''FloatingPointType : FLOAT
                         | DOUBLE'''

#

def p_ReferenceType(p):
    '''ReferenceType : ClassOrInterfaceType 
                     | TypeVariable 
                     | ArrayType'''

#

def p_ClassOrInterfaceType(p):
    '''ClassOrInterfaceType : ClassType 
                            | InterfaceType'''

#

def p_ClassType(p):
    '''ClassType : AnnotationS IDENT ZooTypeArguments 
                 | ClassOrInterfaceType PERIOD AnnotationS IDENT ZooTypeArguments '''

def p_ZooTypeArguments(p):
    '''ZooTypeArguments : TypeArguments
                        | empty '''

#

def p_InterfaceType(p):
    '''InterfaceType : ClassType'''

#

def p_TypeVariable(p):
    '''TypeVariable : AnnotationS IDENT'''

#

def p_ArrayType(p):
    '''ArrayType :  PrimitiveType Dims 
                 |  ClassOrInterfaceType Dims 
                 |  TypeVariable Dims '''

#

def p_Dims(p):
    '''Dims : AnnotationS LBRACE RBRACE AnnotationSLBRACERBRACES'''

def p_AnnotationSLBRACERBRACES(p):
    '''AnnotationSLBRACERBRACES : AnnotationS LBRACE RBRACE AnnotationLBRACERBRACES
                                | empty '''

#

def p_TypeParameter(p):
    '''TypeParameter :  TypeParameterModifierS IDENT ZooTypeBound '''

def p_TypeParameterModifierS(p):
    '''TypeParameterModifierS : TypeParameterModifier TypeParameterModifiers
                              | empty '''

def p_ZooTypeBound(p):
    '''ZooTypeBound : TypeBound
                    | empty '''

#


def p_TypeParameterModifier(p):
    '''TypeParameterModifier : Annotation '''

#

def p_TypeBound(p)::
    '''TypeBound : EXTENDS TypeVariable
                 | EXTENDS ClassOrInterfaceType AdditionalBoundS'''

def p_AdditionalBoundS(p):
    '''AdditionalBounds : AdditionalBound AdditionalBounds
                        | empty '''

#

def p_AdditionalBound(p):
    '''AdditionalBound : AND InterfaceType '''

#

def p_TypeArguments(p):
    '''TypeArguments : LSS TypeArgumentList GTR '''

#

def p_TypeArgumentList(p):
    '''TypeArgumentList : TypeArgument COMMATypeArgumentS'''

def p_COMMATypeArgumentS(p):
    '''COMMATypeArgumentS : COMMA TypeArgument COMMATypeArgumentS
                          | empty '''

#

def p_TypeArgument(p):
    '''TypeArgument : ReferenceType
                    | Wildcard '''

#

def p_Wildcard(p):
    '''Wildcard : AnnotationS QUES ZooWildcardBounds'''

def p_ZooWildcardBounds(p):
    '''ZooWildcardBounds : WildcardBounds
                         | empty '''

#

def p_WildcardBounds(p):
    '''WildcardBounds : EXTENDS ReferenceType
                      | SUPER ReferenceType'''
                      
#

###################################
# Section 14
# #################################
 
 
def p_Block(p):
	'''Block : LBRACE ZooBlockStatements RBRACE
'''

def p_ZooBlockStatements(p):
'''ZooBlockStatements : BlockStatements 
| empty'''

def p_BlockStatements(p):
	'''BlockStatements : BlockStatement BlockStatementS
'''
def p_BlockStatementS(p):
'''BlockStatementS : BlockStatement BlockStatementS
| empty'''

def p_BlockStatement(p):
	'''BlockStatement : LocalVariableDeclarationStatement
| ClassDeclaration
| Statement
'''

def p_LocalVariableDeclarationStatement(p):
	'''LocalVariableDeclarationStatement : LocalVariableDeclaration SEMICOLON
'''

def p_LocalVariableDeclaration(p):
	'''LocalVariableDeclaration : VariableModifierS UnannType VariableDeclaratorList
'''
def p_VariableModifierS(p):
'''VariableModifierS : VariableModifier VariableModifierS
| empty'''

def p_Statement(p):
	'''Statement : StatementWithoutTrailingSubstatement
| LabeledStatement
| IfThenStatement
| IfThenElseStatement
| WhileStatement
| ForStatement
'''

def p_StatementNoShortIf(p):
	'''StatementNoShortIf : StatementWithoutTrailingSubstatement
| LabeledStatementNoShortIf
| IfThenElseStatementNoShortIf
| WhileStatementNoShortIf
| ForStatementNoShortIf
'''

def p_StatementWithoutTrailingSubstatement(p):
	'''StatementWithoutTrailingSubstatement : Block
| EmptyStatement
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

def p_EmptyStatement(p):
	'''EmptyStatement : SEMICOLON
'''

def p_LabeledStatement(p):
	'''LabeledStatement : Identifier  COLON  Statement
'''

def p_LabeledStatementNoShortIf(p):
	'''LabeledStatementNoShortIf : Identifier  COLON  StatementNoShortIf
'''

def p_ExpressionStatement(p):
	'''ExpressionStatement : StatementExpression SEMICOLON
'''

def p_StatementExpression(p):
	'''StatementExpression : Assignment
| PreIncrementExpression
| PreDecrementExpression
| PostIncrementExpression
| PostDecrementExpression
| MethodInvocation
| ClassInstanceCreationExpression
'''

def p_IfThenStatement(p):
	'''IfThenStatement : IF LPAREN Expression RPAREN Statement
'''

def p_IfThenElseStatement(p):
	'''IfThenElseStatement : IF LPAREN Expression RPAREN StatementNoShortIf ELSE Statement
'''

def p_IfThenElseStatementNoShortIf(p):
	'''IfThenElseStatementNoShortIf : IF LPAREN Expression RPAREN StatementNoShortIf ELSE StatementNoShortIf
'''

def p_AssertStatement(p):
	'''AssertStatement : ASSERT Expression SEMICOLON
| ASSERT Expression  COLON  Expression SEMICOLON
'''

def p_SwitchStatement(p):
	'''SwitchStatement : SWITCH LPAREN Expression RPAREN SwitchBlock
'''

def p_SwitchBlock(p):
	'''SwitchBlock : LBRACE SwitchBlockStatementGroupS SwitchLabelS RBRACE
'''
def p_SwitchBlockStatementGroupS(p):
'''SwitchBlockStatementGroupS : SwitchBlockStatementGroup SwitchBlockStatementGroupS
| empty'''

def p_SwitchBlockStatementGroupS(p):
'''SwitchBlockStatementGroupS : SwitchBlockStatementGroup SwitchBlockStatementGroupS
| empty'''

def p_SwitchBlockStatementGroup(p):
	'''SwitchBlockStatementGroup : SwitchLabels BlockStatements
'''

def p_SwitchLabels(p):
	'''SwitchLabels : SwitchLabel SwitchLabelS
'''
def p_SwitchLabelS(p):
'''SwitchLabelS : SwitchLabel SwitchLabelS
| empty'''

def p_SwitchLabel(p):
	'''SwitchLabel : CASE ConstantExpression  COLON
    | CASE EnumConstantName COLON
    | DEFAULT  COLON '''

def p_EnumConstantName(p):
	'''EnumConstantName : Identifier
'''

def p_WhileStatement(p):
	'''WhileStatement : WHILE LPAREN Expression RPAREN Statement
'''

def p_WhileStatementNoShortIf(p):
	'''WhileStatementNoShortIf : WHILE LPAREN Expression RPAREN StatementNoShortIf
'''

def p_DoStatement(p):
	'''DoStatement : DO Statement WHILE LPAREN Expression RPAREN SEMICOLON
'''

def p_ForStatement(p):
	'''ForStatement : BasicForStatement
| EnhancedForStatement
'''

def p_ForStatementNoShortIf(p):
	'''ForStatementNoShortIf : BasicForStatementNoShortIf
| EnhancedForStatementNoShortIf
'''

def p_BasicForStatement(p):
	'''BasicForStatement : FOR LPAREN ZooForInit SEMICOLON ZooExpression SEMICOLON ZooForUpdate RPAREN Statement
'''

def p_ZooForUpdate(p):
'''ZooForUpdate : ForUpdate 
| empty'''

def p_ZooExpression(p):
'''ZooExpression : Expression 
| empty'''

def p_ZooForInit(p):
'''ZooForInit : ForInit 
| empty'''

def p_BasicForStatementNoShortIf(p):
	'''BasicForStatementNoShortIf : FOR LPAREN ZooForInit SEMICOLON ZooExpression SEMICOLON ZooForUpdate RPAREN StatementNoShortIf
'''

def p_ForInit(p):
	'''ForInit : StatementExpressionList
| LocalVariableDeclaration
'''

def p_ForUpdate(p):
	'''ForUpdate : StatementExpressionList
'''

def p_StatementExpressionList(p):
	'''StatementExpressionList : StatementExpression COMMAStatementExpressionS
'''


def p_COMMAStatementExpressionS(p):
    '''COMMAStatementExpressionS : COMMA StatementExpression COMMAStatementExpressionS
                    | empty'''



def p_EnhancedForStatement(p):
	'''EnhancedForStatement : FOR LPAREN VariableModifierS UnannType VariableDeclaratorId  COLON  Expression RPAREN Statement
'''

def p_EnhancedForStatementNoShortIf(p):
	'''EnhancedForStatementNoShortIf : FOR LPAREN VariableModifierS UnannType VariableDeclaratorId  COLON  Expression RPAREN StatementNoShortIf
'''

def p_BreakStatement(p):
	'''BreakStatement : BREAK ZooIdentifier SEMICOLON
'''
def p_ZooIdentifier(p):
'''ZooIdentifier : Identifier 
| empty'''

def p_ContinueStatement(p):
	'''ContinueStatement : CONTINUE ZooIdentifier SEMICOLON
'''

def p_ReturnStatement(p):
	'''ReturnStatement : RETURN ZooExpression SEMICOLON
'''
def p_ZooExpression(p):
'''ZooExpression : Expression 
| empty'''

def p_ThrowStatement(p):
	'''ThrowStatement : THROW Expression SEMICOLON
'''

def p_SynchronizedStatement(p):
	'''SynchronizedStatement : SYNCHRONIZED LPAREN Expression RPAREN Block
'''

def p_TryStatement(p):
	'''TryStatement : TRY Block Catches
| TRY Block ZooCatches Finally
| TryWithResourcesStatement
'''
def p_ZooCatches(p):
'''ZooCatches : Catches 
| empty'''

def p_Catches(p):
	'''Catches : CatchClause CatchClauseS
'''
def p_CatchClauseS(p):
'''CatchClauseS : CatchClause CatchClauseS
| empty'''

def p_CatchClause(p):
	'''CatchClause : CATCH LPAREN CatchFormalParameter RPAREN Block
'''

def p_CatchFormalParameter(p):
	'''CatchFormalParameter : VariableModifierS CatchType VariableDeclaratorId
'''

def p_CatchType(p):
	'''CatchType : UnannClassType ORClassTypeS
'''

def p_ORClassTypeS(p):
    '''ORClassTypeS : OR ClassType ORClassTypeS
                    | empty'''


def p_Finally(p):
	'''Finally : FINALLY Block
'''

def p_TryWithResourcesStatement(p):
	'''TryWithResourcesStatement : TRY ResourceSpecification Block ZooCatches ZooFinally
'''
def p_ZooFinally(p):
'''ZooFinally : Finally 
| empty'''

def p_ResourceSpecification(p):
	'''ResourceSpecification : LPAREN ResourceList ZooSEMICOLON RPAREN
'''

def p_ResourceList(p):
	'''ResourceList : Resource SEMICOLONResources
'''


def p_SEMICOLONResources(p):
    '''SEMICOLONResources : SEMICOLON Resources SEMICOLONResources
                    | empty'''



def p_Resource(p):
	'''Resource : VariableModifierS UnannType VariableDeclaratorId ASSIGN Expression'''
