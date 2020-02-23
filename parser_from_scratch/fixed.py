###################################
# Section 4
# #################################
 
def p_Type(p):
    '''Type : PrimitiveType
            | ReferenceType'''
	p[0]=tuple(["Type"]+p[1:])

#

def p_PrimitiveType(p):
    '''PrimitiveType : AnnotationS NumericType
                     | AnnotationS boolean'''
	p[0]=tuple(["PrimitiveType"]+p[1:])

def p_AnnotationS(p):
    '''AnnotationS : Annotation AnnotationS
                       | empty '''
	p[0]=tuple(["AnnotationS"]+p[1:])

#

def p_NumericType(p):
    '''NumericType : IntegralType 
                   | FloatingPointType'''
	p[0]=tuple(["NumericType"]+p[1:])

#

def p_IntegralType(p):
    '''IntegralType : BYTE
                    | SHORT
                    | INT
                    | LONG
                    | CHAR'''
	p[0]=tuple(["IntegralType"]+p[1:])

#

def p_FloatingPointType(p):
    '''FloatingPointType : FLOAT
                         | DOUBLE'''
	p[0]=tuple(["FloatingPointType"]+p[1:])

#

def p_ReferenceType(p):
    '''ReferenceType : ClassOrInterfaceType 
                     | TypeVariable 
                     | ArrayType'''
	p[0]=tuple(["ReferenceType"]+p[1:])

#

def p_ClassOrInterfaceType(p):
    '''ClassOrInterfaceType : ClassType 
                            | InterfaceType'''
	p[0]=tuple(["ClassOrInterfaceType"]+p[1:])

#

def p_ClassType(p):
    '''ClassType : AnnotationS IDENT ZooTypeArguments 
                 | ClassOrInterfaceType PERIOD AnnotationS IDENT ZooTypeArguments '''
	p[0]=tuple(["ClassType"]+p[1:])

def p_ZooTypeArguments(p):
    '''ZooTypeArguments : TypeArguments
                        | empty '''
	p[0]=tuple(["ZooTypeArguments"]+p[1:])

#

def p_InterfaceType(p):
    '''InterfaceType : ClassType'''
	p[0]=tuple(["InterfaceType"]+p[1:])

#

def p_TypeVariable(p):
    '''TypeVariable : AnnotationS IDENT'''
	p[0]=tuple(["TypeVariable"]+p[1:])

#

def p_ArrayType(p):
    '''ArrayType :  PrimitiveType Dims 
                 |  ClassOrInterfaceType Dims 
                 |  TypeVariable Dims '''
	p[0]=tuple(["ArrayType"]+p[1:])

#

def p_Dims(p):
    '''Dims : AnnotationS LBRACE RBRACE AnnotationSLBRACERBRACES'''
	p[0]=tuple(["Dims"]+p[1:])

def p_AnnotationSLBRACERBRACES(p):
    '''AnnotationSLBRACERBRACES : AnnotationS LBRACE RBRACE AnnotationLBRACERBRACES
                                | empty '''
	p[0]=tuple(["AnnotationSLBRACERBRACES"]+p[1:])

#

def p_TypeParameter(p):
    '''TypeParameter :  TypeParameterModifierS IDENT ZooTypeBound '''
	p[0]=tuple(["TypeParameter"]+p[1:])

def p_TypeParameterModifierS(p):
    '''TypeParameterModifierS : TypeParameterModifier TypeParameterModifiers
                              | empty '''
	p[0]=tuple(["TypeParameterModifierS"]+p[1:])

def p_ZooTypeBound(p):
    '''ZooTypeBound : TypeBound
                    | empty '''
	p[0]=tuple(["ZooTypeBound"]+p[1:])

#


def p_TypeParameterModifier(p):
    '''TypeParameterModifier : Annotation '''
	p[0]=tuple(["TypeParameterModifier"]+p[1:])

#

def p_TypeBound(p)::
    '''TypeBound : EXTENDS TypeVariable
                 | EXTENDS ClassOrInterfaceType AdditionalBoundS'''
	p[0]=tuple(["TypeBound"]+p[1:])

def p_AdditionalBoundS(p):
    '''AdditionalBounds : AdditionalBound AdditionalBounds
                        | empty '''
	p[0]=tuple(["AdditionalBoundS"]+p[1:])

#

def p_AdditionalBound(p):
    '''AdditionalBound : AND InterfaceType '''
	p[0]=tuple(["AdditionalBound"]+p[1:])

#

def p_TypeArguments(p):
    '''TypeArguments : LSS TypeArgumentList GTR '''
	p[0]=tuple(["TypeArguments"]+p[1:])

#

def p_TypeArgumentList(p):
    '''TypeArgumentList : TypeArgument COMMATypeArgumentS'''
	p[0]=tuple(["TypeArgumentList"]+p[1:])

def p_COMMATypeArgumentS(p):
    '''COMMATypeArgumentS : COMMA TypeArgument COMMATypeArgumentS
                          | empty '''
	p[0]=tuple(["COMMATypeArgumentS"]+p[1:])

#

def p_TypeArgument(p):
    '''TypeArgument : ReferenceType
                    | Wildcard '''
	p[0]=tuple(["TypeArgument"]+p[1:])

#

def p_Wildcard(p):
    '''Wildcard : AnnotationS QUES ZooWildcardBounds'''
	p[0]=tuple(["Wildcard"]+p[1:])

def p_ZooWildcardBounds(p):
    '''ZooWildcardBounds : WildcardBounds
                         | empty '''
	p[0]=tuple(["ZooWildcardBounds"]+p[1:])

#

def p_WildcardBounds(p):
    '''WildcardBounds : EXTENDS ReferenceType
                      | SUPER ReferenceType'''
	p[0]=tuple(["WildcardBounds"]+p[1:])
                      
#

###################################
# Section 14
# #################################
 
 
def p_Block(p):
	'''Block : LBRACE ZooBlockStatements RBRACE
'''
	p[0]=tuple(["Block"]+p[1:])

def p_ZooBlockStatements(p):
'''ZooBlockStatements : BlockStatements 
| empty'''
	p[0]=tuple(["ZooBlockStatements"]+p[1:])

def p_BlockStatements(p):
	'''BlockStatements : BlockStatement BlockStatementS
'''
	p[0]=tuple(["BlockStatements"]+p[1:])
def p_BlockStatementS(p):
'''BlockStatementS : BlockStatement BlockStatementS
| empty'''
	p[0]=tuple(["BlockStatementS"]+p[1:])

def p_BlockStatement(p):
	'''BlockStatement : LocalVariableDeclarationStatement
| ClassDeclaration
| Statement
'''
	p[0]=tuple(["BlockStatement"]+p[1:])

def p_LocalVariableDeclarationStatement(p):
	'''LocalVariableDeclarationStatement : LocalVariableDeclaration SEMICOLON
'''
	p[0]=tuple(["LocalVariableDeclarationStatement"]+p[1:])

def p_LocalVariableDeclaration(p):
	'''LocalVariableDeclaration : VariableModifierS UnannType VariableDeclaratorList
'''
	p[0]=tuple(["LocalVariableDeclaration"]+p[1:])
def p_VariableModifierS(p):
'''VariableModifierS : VariableModifier VariableModifierS
| empty'''
	p[0]=tuple(["VariableModifierS"]+p[1:])

def p_Statement(p):
	'''Statement : StatementWithoutTrailingSubstatement
| LabeledStatement
| IfThenStatement
| IfThenElseStatement
| WhileStatement
| ForStatement
'''
	p[0]=tuple(["Statement"]+p[1:])

def p_StatementNoShortIf(p):
	'''StatementNoShortIf : StatementWithoutTrailingSubstatement
| LabeledStatementNoShortIf
| IfThenElseStatementNoShortIf
| WhileStatementNoShortIf
| ForStatementNoShortIf
'''
	p[0]=tuple(["StatementNoShortIf"]+p[1:])

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
	p[0]=tuple(["StatementWithoutTrailingSubstatement"]+p[1:])

def p_EmptyStatement(p):
	'''EmptyStatement : SEMICOLON
'''
	p[0]=tuple(["EmptyStatement"]+p[1:])

def p_LabeledStatement(p):
	'''LabeledStatement : Identifier  COLON  Statement
'''
	p[0]=tuple(["LabeledStatement"]+p[1:])

def p_LabeledStatementNoShortIf(p):
	'''LabeledStatementNoShortIf : Identifier  COLON  StatementNoShortIf
'''
	p[0]=tuple(["LabeledStatementNoShortIf"]+p[1:])

def p_ExpressionStatement(p):
	'''ExpressionStatement : StatementExpression SEMICOLON
'''
	p[0]=tuple(["ExpressionStatement"]+p[1:])

def p_StatementExpression(p):
	'''StatementExpression : Assignment
| PreIncrementExpression
| PreDecrementExpression
| PostIncrementExpression
| PostDecrementExpression
| MethodInvocation
| ClassInstanceCreationExpression
'''
	p[0]=tuple(["StatementExpression"]+p[1:])

def p_IfThenStatement(p):
	'''IfThenStatement : IF LPAREN Expression RPAREN Statement
'''
	p[0]=tuple(["IfThenStatement"]+p[1:])

def p_IfThenElseStatement(p):
	'''IfThenElseStatement : IF LPAREN Expression RPAREN StatementNoShortIf ELSE Statement
'''
	p[0]=tuple(["IfThenElseStatement"]+p[1:])

def p_IfThenElseStatementNoShortIf(p):
	'''IfThenElseStatementNoShortIf : IF LPAREN Expression RPAREN StatementNoShortIf ELSE StatementNoShortIf
'''
	p[0]=tuple(["IfThenElseStatementNoShortIf"]+p[1:])

def p_AssertStatement(p):
	'''AssertStatement : ASSERT Expression SEMICOLON
| ASSERT Expression  COLON  Expression SEMICOLON
'''
	p[0]=tuple(["AssertStatement"]+p[1:])

def p_SwitchStatement(p):
	'''SwitchStatement : SWITCH LPAREN Expression RPAREN SwitchBlock
'''
	p[0]=tuple(["SwitchStatement"]+p[1:])

def p_SwitchBlock(p):
	'''SwitchBlock : LBRACE SwitchBlockStatementGroupS SwitchLabelS RBRACE
'''
	p[0]=tuple(["SwitchBlock"]+p[1:])
def p_SwitchBlockStatementGroupS(p):
'''SwitchBlockStatementGroupS : SwitchBlockStatementGroup SwitchBlockStatementGroupS
| empty'''
	p[0]=tuple(["SwitchBlockStatementGroupS"]+p[1:])

def p_SwitchBlockStatementGroupS(p):
'''SwitchBlockStatementGroupS : SwitchBlockStatementGroup SwitchBlockStatementGroupS
| empty'''
	p[0]=tuple(["SwitchBlockStatementGroupS"]+p[1:])

def p_SwitchBlockStatementGroup(p):
	'''SwitchBlockStatementGroup : SwitchLabels BlockStatements
'''
	p[0]=tuple(["SwitchBlockStatementGroup"]+p[1:])

def p_SwitchLabels(p):
	'''SwitchLabels : SwitchLabel SwitchLabelS
'''
	p[0]=tuple(["SwitchLabels"]+p[1:])
def p_SwitchLabelS(p):
'''SwitchLabelS : SwitchLabel SwitchLabelS
| empty'''
	p[0]=tuple(["SwitchLabelS"]+p[1:])

def p_SwitchLabel(p):
	'''SwitchLabel : CASE ConstantExpression  COLON
    | CASE EnumConstantName COLON
    | DEFAULT  COLON '''
	p[0]=tuple(["SwitchLabel"]+p[1:])

def p_EnumConstantName(p):
	'''EnumConstantName : Identifier
'''
	p[0]=tuple(["EnumConstantName"]+p[1:])

def p_WhileStatement(p):
	'''WhileStatement : WHILE LPAREN Expression RPAREN Statement
'''
	p[0]=tuple(["WhileStatement"]+p[1:])

def p_WhileStatementNoShortIf(p):
	'''WhileStatementNoShortIf : WHILE LPAREN Expression RPAREN StatementNoShortIf
'''
	p[0]=tuple(["WhileStatementNoShortIf"]+p[1:])

def p_DoStatement(p):
	'''DoStatement : DO Statement WHILE LPAREN Expression RPAREN SEMICOLON
'''
	p[0]=tuple(["DoStatement"]+p[1:])

def p_ForStatement(p):
	'''ForStatement : BasicForStatement
| EnhancedForStatement
'''
	p[0]=tuple(["ForStatement"]+p[1:])

def p_ForStatementNoShortIf(p):
	'''ForStatementNoShortIf : BasicForStatementNoShortIf
| EnhancedForStatementNoShortIf
'''
	p[0]=tuple(["ForStatementNoShortIf"]+p[1:])

def p_BasicForStatement(p):
	'''BasicForStatement : FOR LPAREN ZooForInit SEMICOLON ZooExpression SEMICOLON ZooForUpdate RPAREN Statement
'''
	p[0]=tuple(["BasicForStatement"]+p[1:])

def p_ZooForUpdate(p):
'''ZooForUpdate : ForUpdate 
| empty'''
	p[0]=tuple(["ZooForUpdate"]+p[1:])

def p_ZooExpression(p):
'''ZooExpression : Expression 
| empty'''
	p[0]=tuple(["ZooExpression"]+p[1:])

def p_ZooForInit(p):
'''ZooForInit : ForInit 
| empty'''
	p[0]=tuple(["ZooForInit"]+p[1:])

def p_BasicForStatementNoShortIf(p):
	'''BasicForStatementNoShortIf : FOR LPAREN ZooForInit SEMICOLON ZooExpression SEMICOLON ZooForUpdate RPAREN StatementNoShortIf
'''
	p[0]=tuple(["BasicForStatementNoShortIf"]+p[1:])

def p_ForInit(p):
	'''ForInit : StatementExpressionList
| LocalVariableDeclaration
'''
	p[0]=tuple(["ForInit"]+p[1:])

def p_ForUpdate(p):
	'''ForUpdate : StatementExpressionList
'''
	p[0]=tuple(["ForUpdate"]+p[1:])

def p_StatementExpressionList(p):
	'''StatementExpressionList : StatementExpression COMMAStatementExpressionS
'''
	p[0]=tuple(["StatementExpressionList"]+p[1:])


def p_COMMAStatementExpressionS(p):
    '''COMMAStatementExpressionS : COMMA StatementExpression COMMAStatementExpressionS
                    | empty'''
	p[0]=tuple(["COMMAStatementExpressionS"]+p[1:])



def p_EnhancedForStatement(p):
	'''EnhancedForStatement : FOR LPAREN VariableModifierS UnannType VariableDeclaratorId  COLON  Expression RPAREN Statement
'''
	p[0]=tuple(["EnhancedForStatement"]+p[1:])

def p_EnhancedForStatementNoShortIf(p):
	'''EnhancedForStatementNoShortIf : FOR LPAREN VariableModifierS UnannType VariableDeclaratorId  COLON  Expression RPAREN StatementNoShortIf
'''
	p[0]=tuple(["EnhancedForStatementNoShortIf"]+p[1:])

def p_BreakStatement(p):
	'''BreakStatement : BREAK ZooIdentifier SEMICOLON
'''
	p[0]=tuple(["BreakStatement"]+p[1:])
def p_ZooIdentifier(p):
'''ZooIdentifier : Identifier 
| empty'''
	p[0]=tuple(["ZooIdentifier"]+p[1:])

def p_ContinueStatement(p):
	'''ContinueStatement : CONTINUE ZooIdentifier SEMICOLON
'''
	p[0]=tuple(["ContinueStatement"]+p[1:])

def p_ReturnStatement(p):
	'''ReturnStatement : RETURN ZooExpression SEMICOLON
'''
	p[0]=tuple(["ReturnStatement"]+p[1:])
def p_ZooExpression(p):
'''ZooExpression : Expression 
| empty'''
	p[0]=tuple(["ZooExpression"]+p[1:])

def p_ThrowStatement(p):
	'''ThrowStatement : THROW Expression SEMICOLON
'''
	p[0]=tuple(["ThrowStatement"]+p[1:])

def p_SynchronizedStatement(p):
	'''SynchronizedStatement : SYNCHRONIZED LPAREN Expression RPAREN Block
'''
	p[0]=tuple(["SynchronizedStatement"]+p[1:])

def p_TryStatement(p):
	'''TryStatement : TRY Block Catches
| TRY Block ZooCatches Finally
| TryWithResourcesStatement
'''
	p[0]=tuple(["TryStatement"]+p[1:])
def p_ZooCatches(p):
'''ZooCatches : Catches 
| empty'''
	p[0]=tuple(["ZooCatches"]+p[1:])

def p_Catches(p):
	'''Catches : CatchClause CatchClauseS
'''
	p[0]=tuple(["Catches"]+p[1:])
def p_CatchClauseS(p):
'''CatchClauseS : CatchClause CatchClauseS
| empty'''
	p[0]=tuple(["CatchClauseS"]+p[1:])

def p_CatchClause(p):
	'''CatchClause : CATCH LPAREN CatchFormalParameter RPAREN Block
'''
	p[0]=tuple(["CatchClause"]+p[1:])

def p_CatchFormalParameter(p):
	'''CatchFormalParameter : VariableModifierS CatchType VariableDeclaratorId
'''
	p[0]=tuple(["CatchFormalParameter"]+p[1:])

def p_CatchType(p):
	'''CatchType : UnannClassType ORClassTypeS
'''
	p[0]=tuple(["CatchType"]+p[1:])

def p_ORClassTypeS(p):
    '''ORClassTypeS : OR ClassType ORClassTypeS
                    | empty'''
	p[0]=tuple(["ORClassTypeS"]+p[1:])


def p_Finally(p):
	'''Finally : FINALLY Block
'''
	p[0]=tuple(["Finally"]+p[1:])

def p_TryWithResourcesStatement(p):
	'''TryWithResourcesStatement : TRY ResourceSpecification Block ZooCatches ZooFinally
'''
	p[0]=tuple(["TryWithResourcesStatement"]+p[1:])
def p_ZooFinally(p):
'''ZooFinally : Finally 
| empty'''
	p[0]=tuple(["ZooFinally"]+p[1:])

def p_ResourceSpecification(p):
	'''ResourceSpecification : LPAREN ResourceList ZooSEMICOLON RPAREN
'''
	p[0]=tuple(["ResourceSpecification"]+p[1:])

def p_ResourceList(p):
	'''ResourceList : Resource SEMICOLONResources
'''
	p[0]=tuple(["ResourceList"]+p[1:])


def p_SEMICOLONResources(p):
    '''SEMICOLONResources : SEMICOLON Resources SEMICOLONResources
                    | empty'''
	p[0]=tuple(["SEMICOLONResources"]+p[1:])



def p_Resource(p):
	'''Resource : VariableModifierS UnannType VariableDeclaratorId ASSIGN Expression'''
	p[0]=tuple(["Resource"]+p[1:])
