#!/usr/bin/python

class Symbol(object):
    pass


class VariableSymbol(Symbol):

    def __init__(self, name, type):
        pass
    #


class FunError(object):
    pass


class SymbolTable(object):

    def __init__(self, parent, name): # parent scope and symbol table name
        self.symbols = {}
        self.name = name
        self.parent = parent
    #

    def put(self, name, symbol): # put variable symbol or fundef under <name> entry
        global_scope = self
        while global_scope.getParentScope() is not None:
            global_scope = global_scope.getParentScope()
        if global_scope.shallowGet(name) is None or isinstance(global_scope.shallowGet(name), str):
            if self.shallowGet(name) is None:
                self.symbols[name] = symbol
            else:
                raise ValueError
        else:
            raise NameError

    def shallowGet(self, name):
        return self.symbols.get(name, None)

    def get(self, name): # get variable symbol or fundef from <name> entry
        if name in self.symbols:
            return self.symbols[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise ValueError

    def getParentScope(self):
        return self.parent

    def pushScope(self, name):
        return SymbolTable(self, name)

    def popScope(self):
        return self.parent

