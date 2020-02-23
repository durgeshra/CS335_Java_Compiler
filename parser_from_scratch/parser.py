

def p_type_name(p):
    '''type_name : IDENT
                | package_or_type_name PERIOD IDENT '''
    p[0] = tuple(["type_name"]+p[1:])