
import AST
import SymbolTable
from Memory import *
from Exceptions import *
from visit import *
import sys

sys.setrecursionlimit(10000)

class Interpreter(object):
    memory_stack_global = MemoryStack(Memory('global'))
    memory_stack_local = MemoryStack()
    op = {'+': lambda x, y: x + y,
          '-': lambda x, y: x - y,
          '*': lambda x, y: x * y,
          '/': lambda x, y: x / y,
          '%': lambda x, y: x % y,
          '>>': lambda x, y: x >> y,
          '<<': lambda x, y: x << y,
          '|': lambda x, y: x | y,
          '&': lambda x, y: x & y,
          '^': lambda x, y: x ^ y,
          '>': lambda x, y: x > y,
          '>=': lambda x, y: x >= y,
          '<': lambda x, y: x < y,
          '<=': lambda x, y: x <= y,
          '==': lambda x, y: x == y,
          '!=': lambda x, y: x != y
          }

    @on('node')
    def visit(self, node):
        pass

    @when(AST.Program)
    def visit(self, node):
        for child in node.children:
            self.visit(child)

    @when(AST.BinExpr)
    def visit(self, node):
        r1 = self.visit(node.left)
        r2 = self.visit(node.right)
        ret_val = self.op[node.op](r1, r2)
        return ret_val
      #  return eval(str(r1) + ' ' + node.op + ' ' + str(r2))

    @when(AST.Assignment)
    def visit(self, node):
        value = self.visit(node.expression)
        val_memory = self.memory_stack_local.get(node.id)
        if val_memory is None:
            self.memory_stack_global.set(node.id, value)
        else:
            self.memory_stack_local.set(node.id, value)

    @when(AST.Const)
    def visit(self, node):
        return node.value

    @when(AST.RepeatInstr)
    def visit(self, node):
        try:
            while(True):
                try:
                    self.visit(node.instructions)
                except ContinueException as ce:
                    if not self.visit(node.condition):
                        self.visit(node)
                if self.visit(node.condition):
                    break
        # TODO: Break - check scopes
        except BreakException as be:
            return

    @when(AST.WhileInstr)
    def visit(self, node):
        # _len = len(self.memory_stack_local.memory)
        try:
            while self.visit(node.condition):
                try:
                    self.visit(node.instruction)
                except ContinueException as ce:
                    #self.visit(node)
                    continue
        except BreakException as be:
            # self.memory_stack_local.memory = self.memory_stack_local.memory[:_len-1]
            return

    @when(AST.Condition)
    def visit(self, node):
        return self.visit(node.expression)

    @when(AST.ChoiceInstr)
    def visit(self, node):
        if self.visit(node.condition):
            self.visit(node.instruction)
        else:
            self.visit(node.instruction_else)

    @when(AST.Fundef)
    def visit(self, node):
        self.memory_stack_global.insert(node.id, (node.args, node.instr))

    @when(AST.Funcall)
    def visit(self, node):
        try:
            fun = self.memory_stack_global.get(node.id)
            arg_calls = []
            for arg_call in node.args.list:
                arg_calls.append(self.visit(arg_call))
            self.memory_stack_local.push(Memory(node.id))
            for arg_def, arg_call in zip(fun[0].list, arg_calls):
                self.memory_stack_local.insert(arg_def.name, arg_call)

            self.visit(fun[1], True)
        except ReturnValueException as e:
            while self.memory_stack_local.memory[-1].name != node.id:
                self.memory_stack_local.pop()
            self.memory_stack_local.pop()
            return e.value

    @when(AST.ReturnInstr)
    def visit(self, node):
        raise ReturnValueException(self.visit(node.expression))

    @when(AST.BreakInstr)
    def visit(self, node):
        raise BreakException()

    @when(AST.ContinueInstr)
    def visit(self, node):
        raise ContinueException()

    @when(AST.PrintInstr)
    def visit(self, node):
        print(self.visit(node.expression))

    @when(AST.Init)
    def visit(self, node):
        if len(self.memory_stack_local.memory) > 0:
            self.memory_stack_local.insert(node.ID, self.visit(node.expr))
        else:
            self.memory_stack_global.insert(node.ID, self.visit(node.expr))

    @when(AST.Integer)
    def visit(self, node):
        return int(node.value)

    @when(AST.Float)
    def visit(self, node):
        return float(node.value)

    @when(AST.String)
    def visit(self, node):
        return str(node.value[1:-1])

    @when(AST.Variable)
    def visit(self, node):
        val = self.memory_stack_local.get(node.name)
        if val is not None:
            return val
        else:
            return self.memory_stack_global.get(node.name)

    @when(AST.Node)
    def visit(self, node):
        for child in node.children:
            self.visit(child)


    @when(AST.ConstructionList)
    def visit(self, node):
        for child in node.children:
            self.visit(child)

    @when(AST.CompoundInstr)
    def visit(self, node, fundef=False):
        if not fundef:
            try:
                self.memory_stack_local.push(Memory('while'))
                # print('|' + str(node.line))
                self.visit(node.declarations)
                self.visit(node.instructions)
                self.memory_stack_local.pop()
                # print('\\' + str(node.line))
            except (BreakException, ContinueException):
                self.memory_stack_local.pop()
                # print('/' + str(node.line))
                raise
        else:
            self.visit(node.declarations)
            self.visit(node.instructions)

