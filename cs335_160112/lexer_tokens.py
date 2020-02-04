reserved = {
    'abstract': 	'ABSTRACT',
    'assert':       'ASSERT',
    'boolean':      'BOOLEAN',
    'break':    	'BREAK',
    'byte':         'BYTE',
    'case': 	    'CASE',
    'catch':        'CATCH',
    'char':         'CHAR',
    'class':        'CLASS',
    'const': 	    'CONST',
    'continue': 	'CONTINUE',
    'default': 	    'DEFAULT',
    'do':           'DO',
    'double':       'DOUBLE',
    'else': 	    'ELSE',
    'enum':         'ENUM',
    'extends':      'EXTENDS',
    'final':        'FINAL',
    'finally':      'FINALLY',
    'float':        'FLOAT',
    'for':	     	'FOR',
    'if': 	       	'IF',
    'goto':		    'GOTO',
    'implements':   'IMPLEMENTS',
    'import':   	'IMPORT',
    'instanceof':   'INSTANCEOF',
    'int':          'INT',
    'interface': 	'INTERFACE',
    'long':         'LONG',
    'native':       'NATIVE',
    'new':          'NEW',
    'package':  	'PACKAGE',
    'private':      'PRIVATE',
    'protected':    'PROTECTED',
    'public':       'PUBLIC',
    'return': 	    'RETURN',
    'short':        'SHORT',
    'static':       'STATIC',
    'strictfp':     'STRICTFP',
    'super':        'SUPER',
    'switch': 	    'SWITCH',
    'synchronized': 'SYNCHRONIZED',
    'this':         'THIS',
    'throw':        'THROW',
    'throws':       'THROWS',
    'transient':    'TRANSIENT',
    'try':          'TRY',
    'void':         'VOID',
    'volatile':     'VOLATILE',
    'while':        'WHILE'
}

literals_ = ['BOOL_LIT', 'NULL_LIT', 'DECIMAL_LIT', 'HEX_LIT', 'OCTAL_LIT', 'BINARY_LIT', 'FLOAT_DEC_LIT', 'FLOAT_HEX_LIT', 'STRING_LIT', 'CHAR_LIT'] ## Add int, float, character, strong, null

separators = ['LPAREN', 'LBRACK', 'LBRACE', 'RPAREN', 'RBRACK', 'RBRACE', 'COMMA', 'PERIOD', 'SEMICOLON', 'ELLIPSIS', 'ATRATE', 'COLON_SEP']

operators = ['ADD', 'SUB', 'MUL', 'QUO', 'REM', 'AND', 'OR', 'XOR','SHL', 'SHR', 'ADD_ASSIGN', 'SUB_ASSIGN', 'MUL_ASSIGN','QUO_ASSIGN', 'REM_ASSIGN', 'AND_ASSIGN', 'OR_ASSIGN','XOR_ASSIGN', 'SHL_ASSIGN', 'SHR_ASSIGN', 'LAND', 'LOR','ARROW', 'INC', 'DEC', 'EQL', 'LSS', 'GTR', 'ASSIGN', 'NOT', 'NEQ', 'LEQ', 'GEQ','LNOT', 'QUES', 'COLON', 'SHR_UN', 'SHR_UN_ASSIGN']

misc = ['IDENT', 'COMMENT']

err = ['UNCLOSED_CHAR', 'UNCLOSED_STR']

tokens = separators + literals_ + operators + list(reserved.values()) + misc + err


t_HEX_LIT = r'0[xX][0-9a-fA-F]([_]*[0-9a-fA-F])*[lL]?'
t_OCTAL_LIT = r'0[_]*[1-8]([_]*[0-8])*[lL]?'
t_BINARY_LIT = r'0[bB][0-1]([_]*[0-1])*[lL]?'
t_DECIMAL_LIT = r'0[lL]?|([1-9]([_]*[0-9])*)[lL]?'

t_FLOAT_HEX_LIT = r'((0[xX][0-9a-fA-F]([_]*[0-9a-fA-F])*[\.]?)|(0[xX]([0-9a-fA-F]([_]*[0-9a-fA-F])*)?\.[0-9a-fA-F]([_]*[0-9a-fA-F])*))[pP][\+\-]?[0-9]+'

# Explanation of regex (first two combined with ORs)
# 0[xX][0-9a-fA-F]([_]*[0-9a-fA-F])*[\.]?
# 0[xX]([0-9a-fA-F]([_]*[0-9a-fA-F])*)?\.[0-9a-fA-F]([_]*[0-9a-fA-F])*
# [pP][\+\-]?[0-9]+

# Tests
# 0x1.fffffffffffffp1023, 0x119_1.d2e39e3p-0000, 0x19__29_19__20.2___02_9p0,
# 0x21111.p-0, 0x0.p-0, 0x.0p-0


t_FLOAT_DEC_LIT = r'([0-9]+\.[0-9]* ([eE][\+\-]?[0-9]+)? [fFdD]?)|([0-9]*\.[0-9]+ ([eE][\+\-]?[0-9]+)? [fFdD]?)|([0-9]+ ([eE][\+\-]?[0-9]+) [fFdD]?)|([0-9]+ ([eE][\+\-]?[0-9]+)?[fFdD])'
# Explanation of regex (combined with ORs)
# [0-9]+\.[0-9]* ([eE][\+\-]?[0-9]+)? [fFdD]?
# [0-9]*\.[0-9]+ ([eE][\+\-]?[0-9]+)? [fFdD]?
# [0-9]+ ([eE][\+\-]?[0-9]+) [fFdD]?
# [0-9]+ ([eE][\+\-]?[0-9]+)? [fFdD]

# Tests
# 0f, 0F, 0.00, 00.00, 00.0000e-0, 0.0000e-0233, 0.0000e+0233,
# 2122.120e+0233, .2334, .2334e+29292f, 2e-1f, 2d, 3D

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t\f'

## Null literal
t_NULL_LIT = r'(null)'

## Boolean literals
t_BOOL_LIT = r'((true)|(false))'

## Operators
t_ADD = r'\+'
t_SUB = r'-'
t_MUL = r'\*'
t_QUO = r'/'
t_REM = r'%'

t_AND = r'&'
t_OR =  r'\|'
t_XOR = r'\^'
t_SHL = r'(<<)'
t_SHR = r'(>>)'

t_ADD_ASSIGN = r'(\+=)'
t_SUB_ASSIGN = r'(-=)'
t_MUL_ASSIGN = r'(\*=)'
t_QUO_ASSIGN = r'(/=)'
t_REM_ASSIGN = r'(%=)'

t_AND_ASSIGN = r'(&=)'
t_OR_ASSIGN = r'(\|=)'
t_XOR_ASSIGN = r'(\^=)'
t_SHL_ASSIGN = r'(<<=)'
t_SHR_ASSIGN = r'(>>=)'

t_LAND = r'(&&)'
t_LOR = r'(\|\|)'
t_ARROW = r'(->)'
t_INC = r'(\+\+)'
t_DEC = r'(--)'

t_EQL = r'(==)'
t_LSS = r'<'
t_GTR = r'>'
t_ASSIGN = r'='
t_NOT = r'!'

t_NEQ = r'(!=)'
t_LEQ = r'(<=)'
t_GEQ = r'(>=)'

t_LNOT = r'\~'
t_QUES = r'\?'
t_COLON = r'\:'
t_SHR_UN = r'(\>\>\>)'
t_SHR_UN_ASSIGN = r'(\>\>\>\=)'

## Separators
t_LPAREN = r'\('
t_LBRACK = r'\['
t_LBRACE = r'\{'
t_RPAREN = r'\)'
t_RBRACK = r'\]'
t_RBRACE = r'\}'

t_COMMA =  r','
t_PERIOD = r'\.'
t_SEMICOLON = r';'
t_ELLIPSIS = r'(\.\.\.)'
t_ATRATE = r'\@'
t_COLON_SEP = r'(\:\:)'
