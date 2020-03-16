class SymbolTable():
    def __init__(self):
        self.name = ""
        self.var_dict = dict()              # dict of variables in current scope: key:name val:type
        self.method_dict = dict()           # dict of variables in current scope: key:name val:MethodObj
        self.class_dict = dict()            # dict of variables in current scope: key:name val:ClassObj
        self.parent = None                  # A scope maybe a subscope some other scope, thus there maybe a parent. The parent is the index of the parent_scope in the scope_stack
        self.extra = dict()                 # Any extra values required in the table goes here

    def look_up_var(self, name):
        return (name in self.var_dict)
    def look_up_method(self, name):
        return (name in self.method_dict)
    def look_up_class(self, name):
        return (name in self.class_dict)
    def look_up(self, name):
        if self.look_up_var(name):
            return True
        elif self.look_up_method(name):
            return True
        elif self.look_up_class(name):
            return True
        return False


    def get_info(self, name):
        if self.look_up_var(name):
            return ["var", self.var_dict[name]]
        elif self.look_up_method(name):
            return ["method", self.method_dict[name]]
        elif self.look_up_class(name):
            return ["class", self.class_dict[name]]
        else:
            raise KeyError("IDENT " + str(name) + " does not exist.")

    def get_var_type(self, name):
        if not self.look_up_var(name):
            raise KeyError("Variable " + str(name) + " does not exist.")
        return self.var_dict[name]
    def get_method(self, name):
        if not self.look_up_method(name):
            raise KeyError("Method " + str(name) + " does not exist.")
        return self.method_dict[name]
    def get_class(self, name):
        if not self.look_up_class(name):
            raise KeyError("Class " + str(name) + " does not exist.")
        return self.class_dict[name]

    def insert_var(self, name, type):
        if not self.look_up_var(name):
            self.var_dict[name] = type
        else:
            raise KeyError("Variable " + str(name) + " already exist!!")
    def insert_method(self, name, method_):
        if not self.look_up_method(name):
            self.method_dict[name] = method_
        else:
            raise KeyError("Method " + str(name) + " already exist!!")
    def insert_class(self, name, class_):
        if not self.look_up_class(name):
            self.class_dict[name] = class_
        else:
            raise KeyError("Class " + str(name) + " already exist!!")

    def update_var_type(self, name, type):
        if not self.look_up_var(name):
            raise KeyError("Variable " + str(name) + " does not exist.")
        else:
            self.var_dict[name] = type

    #TODO: Anay - do we need update for methods or classes?

    # TODO: Anay - Why do we need this?
    # def delete(self, name):
    #     if not self.look_up(name):
    #         raise KeyError("Symbol " + str(name) + " does not exist.")
    #     else:
    #         del self.table[name]

    def set_parent(self, parent):
        self.parent = parent;

    def add_extra(self, value, key):
        self.extra[key] = value

    def get_extra(self, key):
        return self.extra.get(key)

class MethodObj():
    # each class name x list of (parameters+is_optional+type)
    def __init__(self):
        self.name = ""
        self.param_list = []
        self.is_opt = []
        self.type = []
        self.return_type = "unknown"
        self.modifiers = []

    def __init__(self, name_):
        self.name = name_
        self.param_list = []
        self.is_opt = []
        self.type = []
        self.return_type = "unknown"
        self.modifiers = []

    def look_up(self, name):
        return (name in self.param_list)

    def look_up_ind(self, name, i):
        return (name == self.param_list[i])

    def insert(self, name_, is_opt_, type_):
        if not self.look_up(name_):
            self.param_list += [name_]
            self.is_opt += [is_opt_]
            self.type += [type_]
        else:
            raise KeyError("Paramter " + str(name) + " already in parameter list.")

    def update(self, name_, is_opt_, type_):
        if not self.look_up(name):
            raise KeyError("Paramter " + str(name) + " does not exist.")
        else:
            i = self.param_list.index(name_)
            self.param_list[i] = name_
            self.is_opt[i] = is_opt_
            self.type[i] = type_

    def get_info(self, name):
        if not self.look_up(name):
            raise KeyError("Paramter " + str(name) + " does not exist.")
        i = self.param_list.index(name_)
        return (name_, self.is_opt[i], self.type[i])

class ClassObj():
    # each class name x
    #           list of methods
    #           list of variables
    #           list of classes #TODO: anay - Ignored for now

    def __init__(self):
        self.name = ""
        self.var_dict = dict()         # dict of variables in current class: key:name val:type
        self.method_dict = dict()           # dict of variables in current class: key:name val:MethodObj
        self.class_dict = dict()            # dict of variables in current class: key:name val:ClassObj
        self.extends_class = ""
        self.modifiers = []

    def __init__(self, name_):
        self.name = name_
        self.var_dict = dict()         # dict of variables in current scope: key:name val:type
        self.method_dict = dict()           # dict of variables in current scope: key:name val:MethodObj
        self.class_dict = dict()            # dict of variables in current scope: key:name val:ClassObj
        self.extends_class = ""
        self.modifiers = []

    def look_up_var(self, name):
        return (name in self.var_dict)
    def look_up_method(self, name):
        return (name in self.method_dict)
    def look_up_class(self, name):
        return (name in self.class_dict)

    def get_var_type(self, name):
        if not self.look_up_var(name):
            raise KeyError("Variable " + str(name) + " does not exist.")
        return self.var_dict[name]
    def get_method(self, name):
        if not self.look_up_var(name):
            raise KeyError("Method " + str(name) + " does not exist.")
        return self.method_dict[name]
    def get_class(self, name):
        if not self.look_up_var(name):
            raise KeyError("Class " + str(name) + " does not exist.")
        return self.class_dict[name]

    def insert_var(self, name, type):
        if not self.look_up_var(name):
            self.var_dict[name] = type
        else:
            raise KeyError("Variable " + str(name) + " already exist!!")
    def insert_method(self, name, method_):
        if not self.look_up_method(name):
            self.method_dict[name] = method_
        else:
            raise KeyError("Method " + str(name) + " already exist!!")
    def insert_class(self, name, class_):
        if not self.look_up_class(name):
            assert(name == class_.name)
            self.class_dict[name] = class_
        else:
            raise KeyError("Class " + str(name) + " already exist!!")

    def update(self, name_, is_opt_, type_):
        if not self.look_up(name):
            raise KeyError("Paramter " + str(name) + " does not exist.")
        else:
            i = self.param_list.index(name_)
            self.param_list[i] = name_
            self.is_opt[i] = is_opt_
            self.type[i] = type_

class Node:
    def __init__(self):
        self.id_list = []       # List of identifier names. Usually it only has one element, but for example, in FormalParameterList we need a list of names.
        self.code = []          # For 3AC: A list of lists.
        self.type_list = []     # List of types (like int etc.). Usually it only has one element, but for example, in FormalParameterList we need a list of types.
        self.extra = {}         # Extra info in special cases like return type
        self.place_list = []  # For temporary variables ?? TODO (anay): Don't need this yet
