
import AST
import SymbolTable
from Memory import *
from Exceptions import  *
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
          '>': lambda x, y: x % y,
          '>=': lambda x, y: x % y,
          '<': lambda x, y: x % y,
          '<=': lambda x, y: x % y,
          '==': lambda x, y: x % y,
          '!=': lambda x, y: x % y
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
        r1 = node.left.visit(self)
        r2 = node.right.visit(self)
        return self.op[node.op](r1, r2)

    @when(AST.Assignment)
    def visit(self, node):
        id = self.memory_stack_local.get(node.id)
        if id is not None:
            self.memory_stack_local.set(node.id, self.visit(node.expression))
        else:
            self.memory_stack_global.set(node.id, self.visit(node.expression))

    @when(AST.Const)
    def visit(self, node):
        return node.value

    # simplistic while loop interpretation
    @when(AST.WhileInstr)
    def visit(self, node):
        r = None
        while node.cond.accept(self):
            r = node.body.accept(self)
        return r

    @when(AST.Fundef)
    def visit(self, node):
        self.memory_stack_global.insert(node.id, (node.args, node.instr))

    @when(AST.Funcall)
    def visit(self, node):
        fun = self.memory_stack_global.get(node.id)
        self.memory_stack_local.push(node.id)
        for arg_def, arg_call in zip(fun[0], node.args):
            self.memory_stack_local.insert(arg_def.name, self.visit(arg_call))
        ret = self.visit(fun[1])
        self.memory_stack_local.pop()
        return ret
