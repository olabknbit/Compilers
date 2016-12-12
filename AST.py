#!/usr/bin/python

class Node(object):
    def __str__(self):
        return self.printTree()

    def accept(self, visitor):
        return visitor.visit(self)

    def __init__(self):
        self.children = ()
        self.i = 0
        self.n = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.i < self.n:
            self.i += 1
            return self
        else:
            raise StopIteration()

class NodeList(Node):
    list = []

    def __init__(self, list=None):
        self.list = []
        self.children = ()
        self.add_to_list(list)

        self.i = 0
        self.n = len(self.list)


    def add_to_list(self, list):
        if list is not None:
            self.list.append(list)
            self.children = tuple(self.list)

    def __iter__(self):
        return self

    def __next__(self):
        if self.i < self.n:
            i = self.i
            self.i += 1
            return self.list.list[i]
        else:
            raise StopIteration()



class BinExpr(Node):
    def __init__(self, op, left, right, line, token=None):
        super().__init__()
        self.token = token
        self.op = op
        self.left = left
        self.right = right
        self.line = line

        # if you want to use somewhere generic_visit method instead of visit_XXX in visitor
        # definition of children field is required in each class from AST
        self.children = (left, right)



class Program(Node):
    def __init__(self, constructions):
        super().__init__()
        self.constructions = constructions
        self.children = tuple(constructions.list)


class ConstructionList(NodeList):
    def __init__(self, constructions=None):
        super().__init__(constructions)


class Construction(Node):
    def __init__(self, code):
        super().__init__()
        self.code = code
        self.children = tuple(code)


class DeclarationList(NodeList):
    def __init__(self, declarations=None):
        super().__init__(declarations)


class Declaration(Node):
    def __init__(self, type, value, line):
        super().__init__()
        self.type = type
        self.value = value
        self.line = line
        self.children = tuple(value.list)


class InitList(NodeList):
    def __init__(self, inits=None):
        super().__init__(inits)


class Init(Node):
    def __init__(self, ID, expr, line):
        super().__init__()
        self.ID = ID
        self.expr = expr
        self.line = line
        self.children = tuple(expr)


class InstructionList(NodeList):
    def __init__(self, instructions=None):
        super().__init__(instructions)


class Instruction(Node):
    def __init__(self, instruction):
        super().__init__()
        self.instruction = instruction
        self.children = tuple(instruction)


class PrintInstr(Node):
    def __init__(self, type, expression, line):
        super().__init__()
        self.expression = expression
        self.type = type
        self.line = line
        self.children = tuple(expression)


class LabeledInstr(Node):
    def __init__(self, id, instruction):
        super().__init__()
        self.id = id
        self.instruction = instruction
        self.children = tuple(instruction)


class Assignment(Node):
    def __init__(self, id, expression, line):
        super().__init__()
        self.expression = expression
        self.id = id
        self.line = line
        self.children = tuple(expression)



class ChoiceInstr(Node):
    def __init__(self, condition, instruction1, instruction2=None):
        super().__init__()
        self.condition = condition
        self.instruction = instruction1
        self.instruction_else = instruction2
        self.children = (instruction1, instruction2)


class WhileInstr(Node):
    def __init__(self, condition, instruction):
        super().__init__()
        self.condition = condition
        self.instruction = instruction
        self.children = (condition, instruction)


class RepeatInstr(Node):
    def __init__(self, instructions, condition, line):
        super().__init__()
        self.instructions = instructions
        self.line = line
        self.condition = condition


class ReturnInstr(Node):
    def __init__(self, expression, line):
        super().__init__()
        self.expression = expression
        self.line = line


class ContinueInstr(Node):
    def __init__(self, line):
        super().__init__()
        self.line = line


class BreakInstr(Node):
    def __init__(self, line):
        super().__init__()
        self.line = line


class CompoundInstr(Node):
    def __init__(self, declarations, instructions, line):
        super().__init__()
        self.declarations = declarations
        self.instructions = instructions
        self.line = line
        self.children = (declarations, instructions)


class Condition(Node):
    def __init__(self, expression):
        super().__init__()
        self.expression = expression
        self.children = tuple(expression)


class ExpressionList(NodeList):
    def __init__(self, expr=None):
        super().__init__(expr)


class Expression(Node):
    def __init__(self, left, expression, right, idE=None):
        super().__init__()
        self.left = left
        self.expression = expression
        self.right = right
        self.id = idE
        self.children = (left, expression, right)


class Const(Node):
    def __init__(self, value):
        super().__init__()
        self.value = value
        self.children = tuple(value)


class Integer(Const):
    def __init__(self, value, line):
        super().__init__(value)
        self.value = value
        self.line = line


class Float(Const):
    def __init__(self, value, line):
        super().__init__(value)
        self.value = value
        self.line = line


class String(Const):
    def __init__(self, value, line):
        super().__init__(value)
        self.value = value
        self.line = line
        self.children = tuple(value)


class Variable(Node):
    def __init__(self, name, line):
        super().__init__()
        self.name = name
        # self.children = tuple(name)
        self.line = line


class Fundef(Node):
    def __init__(self, id, args, instr, return_type, line):
        super().__init__()
        self.id = id
        self.args = args
        self.instr = instr
        self.type = return_type
        self.line = line
        self.children = (args, instr)


class Funcall(Node):
    def __init__(self, id, args, line):
        super().__init__()
        self.id = id
        self.args = args
        self.line = line


class ArgList(NodeList):
    def __init__(self, arg=None, line = None):
        super().__init__(arg)
        self.line = line


class Arg(Node):
    def __init__(self, name, type, line):
        self.name = name
        self.type = type
        self.line = line
