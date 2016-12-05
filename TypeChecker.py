#!/usr/bin/python
import AST
from SymbolTable import Symbol, SymbolTable, VariableSymbol, FunError


class NodeVisitor(object):
    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.

        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        elif node is not None:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node) or isinstance(child, AST.Const):
                    self.visit(child)

                    # simpler version of generic_visit, not so general
                    # def generic_visit(self, node):
                    #    for child in node.children:
                    #        self.visit(child)


class TypeChecker(NodeVisitor):
    ttype = {}
    isValid = True

    # operatory arytmetyczne i binarne
    ttype['+'] = {}
    ttype['+']['int'] = {'float': 'float', 'int': 'int'}
    ttype['+']['float'] = {'float': 'float', 'int': 'float'}
    ttype['+']['string'] = {'string': 'string'}

    ttype['-'] = {}
    ttype['-']['int'] = {'float': 'float', 'int': 'int'}
    ttype['-']['float'] = {'float': 'float', 'int': 'float'}

    ttype['/'] = {}
    ttype['/']['int'] = {'float': 'float', 'int': 'int'}
    ttype['/']['float'] = {'float': 'float', 'int': 'float'}

    ttype['*'] = {}
    ttype['*']['int'] = {'float': 'float', 'int': 'int'}
    ttype['*']['float'] = {'float': 'float', 'int': 'float'}
    ttype['*']['string'] = {'int': 'string'}

    ttype['%'] = {}
    ttype['%']['int'] = {'int': 'int'}

    ttype['<<'] = {}
    ttype['<<']['int'] = {'int': 'int'}

    ttype['>>'] = {}
    ttype['>>']['int'] = {'int': 'int'}

    ttype['|'] = {}
    ttype['|']['int'] = {'int': 'int'}

    ttype['&'] = {}
    ttype['&']['int'] = {'int': 'int'}

    ttype['^'] = {}
    ttype['^']['int'] = {'int': 'int'}

    # operatory porownania
    ttype['>'] = {}
    ttype['>']['int'] = {'float': 'float', 'int': 'int'}
    ttype['>']['float'] = {'float': 'float', 'int': 'float'}
    ttype['>']['string'] = {'string': 'string'}

    ttype['>='] = {}
    ttype['>=']['int'] = {'float': 'float', 'int': 'int'}
    ttype['>=']['float'] = {'float': 'float', 'int': 'float'}
    ttype['>=']['string'] = {'string': 'string'}

    ttype['<'] = {}
    ttype['<']['int'] = {'float': 'float', 'int': 'int'}
    ttype['<']['float'] = {'float': 'float', 'int': 'float'}
    ttype['<']['string'] = {'string': 'string'}

    ttype['<='] = {}
    ttype['<=']['int'] = {'float': 'float', 'int': 'int'}
    ttype['<=']['float'] = {'float': 'float', 'int': 'float'}
    ttype['<=']['string'] = {'string': 'string'}

    ttype['=='] = {}
    ttype['==']['int'] = {'float': 'float', 'int': 'int'}
    ttype['==']['float'] = {'float': 'float', 'int': 'float'}
    ttype['==']['string'] = {'string': 'string'}

    ttype['!='] = {}
    ttype['!=']['int'] = {'float': 'float', 'int': 'int'}
    ttype['!=']['float'] = {'float': 'float', 'int': 'float'}
    ttype['!=']['string'] = {'string': 'string'}

    def visit_BinExpr(self, node):
        # alternative usage,
        # requires definition of accept method in class Node
        type1 = self.visit(node.left)  # type1 = node.left.accept(self)
        type2 = self.visit(node.right)  # type2 = node.right.accept(self)

        op = node.op
        if op in self.ttype:
            if type1 in self.ttype[op]:
                if type2 in self.ttype[op][type1]:
                    return self.ttype[op][type1][type2]
        if type1 is not None and type2 is not None:
            print('Error: Illegal operation,', type1, op, type2, ': line', node.line)
            self.isValid = False

    def visit_Integer(self, node):
        return 'int'

    def visit_Float(self, node):
        return 'float'

    def visit_String(self, node):
        return 'string'

    def visit_Const(self, node):
        return self.symbols.get(node.value)

    def visit_Program(self, node):
        self.symbols = SymbolTable(None, 'global')
        self.generic_visit(node)

    def visit_Declaration(self, node):
        declaration_type = node.type
        if len(node.value.list) > 0:
            for init in node.value.list:
                init_type = self.visit(init.expr)
                if init_type != declaration_type:
                    if init_type is None or declaration_type is None:
                        pass
                    elif declaration_type == 'int' and init_type == 'float':
                        print('Warning: Assignment of', init_type, 'to', declaration_type, ', possible loss of accuracy: line',
                              node.line)
                    else:
                        print('Error: Assignment of', init_type, 'to', declaration_type, ': line', node.line)
                        self.isValid = False
                else:
                    try:
                        self.symbols.put(init.ID, declaration_type)
                    except ValueError:
                        print('Error: Variable \'' + init.ID + '\' already declared: line', node.line)
                        self.isValid = False
                    except NameError:
                        print('Error: Function identifier \'' + init.ID + '\' used as a variable: line', node.line)
                        self.isValid = False

    def visit_Variable(self, node):
        try:
            var = self.symbols.get(node.name)
            if isinstance(var, str):
                return var
            else:
                print('Error: Function identifier \'' + node.name + '\' used as a variable: line', node.line)
                self.isValid = False
        except ValueError:
            if self.symbols.name == 'global':
                print('Error: Usage of undeclared variable \'' + node.name + '\': line', node.line)
            else:
                print('Error: Variable \'' + node.name + '\' undefined in current scope: line', node.line)
            self.isValid = False
        except NameError:
            print('Err')
            self.isValid = False

    def visit_Expression(self, node):
        return self.visit_BinExpr(node.expression)

    def visit_Fundef(self, node):
        try:
            self.symbols.put(node.id, (node.type, node.args, False))
            self.symbols = self.symbols.pushScope(node.id)
            self.generic_visit(node)
            self.symbols = self.symbols.popScope()
            if self.symbols.get(node.id)[2] == False:
                print('Error: Missing return statement in function \'' + node.id + '\' returning', node.type + ': line',
                      str(node.instr.line))
                self.isValid = False
        except (ValueError, NameError):
            print ("Error: Redefinition of function '" + node.id + "': line " + str(node.line))
            self.isValid = False


    def visit_Arg(self, node):
        try:
            self.symbols.put(node.name, node.type)
        except ValueError:
            print('Error: Variable \'' + node.name + '\' already declared: line', node.line)
            self.isValid = False

    def visit_Funcall(self, node):
        fundef = None
        try:
            fundef = self.symbols.get(node.id)
        except ValueError:
            pass
        if fundef is None:
            print('Error: Call of undefined fun \'' + node.id + '\': line', node.line)
            self.isValid = False
        elif isinstance(fundef, str):
            print('Error: Variable identifier \'' + fundef + '\' used as function call', node.line)
            self.isValid = False
        elif fundef[1] == node.args:
            return fundef[0]
        elif len(fundef[1].list) != len(node.args.list):
            print('Error: Improper number of args in ' + node.id + ' call: line', node.line)
            self.isValid = False
            return fundef[0]
        else:
            try:
                for arg1, arg2  in zip(fundef[1].list, node.args.list) :
                    if arg1.type != self.visit(arg2):
                        raise ValueError
                return fundef[0]
            except ValueError:
                print('Error: Improper type of args in ' + node.id + ' call: line', node.line)
                self.isValid = False
                return fundef[0]


    def visit_ReapeatInstr(self, node):
        self.visit(node.condition)
        self.symbols.pushScope('repeat')
        self.visit(node.instructions)
        self.symbols.popScope()

    def visit_WhileInstr(self, node):
        self.visit(node.condition)
        self.symbols.pushScope('while')
        self.visit(node.instruction)
        self.symbols.popScope()

    def visit_ReturnInstr(self, node):
        if self.symbols.getParentScope() is None:
            print('Error: return instruction outside a function call: line', node.line)
        else:
            par_ret = self.symbols.getParentScope().get(self.symbols.name)[0]
            ret = self.visit(node.expression)
            fundef = self.symbols.getParentScope().get(self.symbols.name)
            self.symbols.getParentScope().symbols[self.symbols.name] = (fundef[0], fundef[1], True)

            if par_ret == ret:
                pass
            elif par_ret is not None and ret is not None:
                print('Error: Improper returned type, expected', par_ret, 'got', ret + ': line', node.line)
                self.isValid = False

    def visit_ContinueInstr(self, node):
        if self.symbols.name == 'repeat' or self.symbols.name == 'while':
            pass
        else:
            print('Error: continue instruction outside a loop: line', node.line)
            self.isValid = False

    def visit_BreakInstr(self, node):
        if self.symbols.name == 'repeat' or self.symbols.name == 'while':
            pass
        else:
            print('Error: break instruction outside a loop: line', node.line)
            self.isValid = False

    def visit_Assignment(self, node):
        try:

            id_type = self.symbols.get(node.id)
            expr_type = self.visit(node.expression)
            if isinstance(id_type, str):
                if expr_type == id_type:
                    pass
                elif expr_type is None or id_type is None:
                    pass
                elif expr_type == 'int' and id_type == 'float':
                    print('Warning: Assignment of', expr_type, 'to', id_type, ', possible loss of accuracy: line',
                          node.line)
                    self.isValid = False
                else:
                    print('Error: Assignment of', expr_type, 'to', id_type, ': line', node.line)
                    self.isValid = False
            else:
                print('Error: Undefined error: line', node.line)
                self.isValid = False
        except ValueError:
            if self.symbols.name == 'global':
                print('Error: Usage of undeclared variable \'' + node.id + '\': line', node.line)
            else:
                print('Error: Variable \'' + node.id + '\' undefined in current scope: line', node.line)
            self.isValid = False
            self.visit(node.expression)