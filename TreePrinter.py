import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


class TreePrinter:
    @addToClass(AST.Node)
    def printTree(self):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.BinExpr)
    def printTree(self):
        pass

    @addToClass(AST.Program)
    def printTree(self, indent=""):
        self.constructions.printTree(indent)

    @addToClass(AST.Construction)
    def printTree(self, indent):
        self.code.printTree(indent)

    @addToClass(AST.Declaration)
    def printTree(self, indent=""):
        print(indent + "DECL")
        self.value.printTree(indent + " | ")

    @addToClass(AST.Init)
    def printTree(self, indent=""):
        print(indent + " = ")
        print(indent + " | " + self.ID)
        self.expr.printTree(indent + " | ")

    @addToClass(AST.ExpressionList)
    @addToClass(AST.DeclarationList)
    @addToClass(AST.ConstructionList)
    @addToClass(AST.InitList)
    @addToClass(AST.InstructionList)
    @addToClass(AST.ArgList)
    def printTree(self, indent=""):
        if len(self.list) > 0:
            for i in self.list:
                i.printTree(indent)

    @addToClass(AST.Instruction)
    def printTree(self, indent=""):
        self.instruction.printTree(indent)

    @addToClass(AST.LabeledInstr)
    def printTree(self, indent=""):
        print(indent + " : ")
        print(indent + " | " + self.id)
        self.instruction.printTree(indent + " | ")

    @addToClass(AST.Assignment)
    def printTree(self, indent=""):
        print(indent + " = ")
        print(indent + " | " + self.id)
        self.expression.printTree(indent + " | ")

    @addToClass(AST.ChoiceInstr)
    def printTree(self, indent=""):
        print(indent + "IF")
        self.condition.printTree(indent + " | ")
        self.instruction.printTree(indent + " | ")
        if self.instruction_else is not None:
            print(indent + "ELSE")
            self.instruction_else.printTree(indent + " | ")

    @addToClass(AST.WhileInstr)
    def printTree(self, indent=""):
        print(indent + "WHILE")
        self.condition.printTree(indent + " | ")
        self.instruction.printTree(indent + " | ")

    @addToClass(AST.RepeatInstr)
    def printTree(self, indent=""):
        print(indent + "REPEAT")
        self.instructions.printTree(indent + " | ")
        print(indent + "UNTIL")
        self.condition.printTree(indent + " | ")

    @addToClass(AST.PrintInstr)
    def printTree(self, indent=""):
        print(indent + "PRINT")
        self.expression.printTree(indent + " | ")

    @addToClass(AST.ReturnInstr)
    def printTree(self, indent=""):
        print(indent + "RETURN")
        self.expression.printTree(indent + " | ")

    @addToClass(AST.ContinueInstr)
    def printTree(self, indent=""):
        print(indent + "CONTINUE")

    @addToClass(AST.BreakInstr)
    def printTree(self, indent=""):
        print(indent + "BREAK")

    @addToClass(AST.CompoundInstr)
    def printTree(self, indent=""):
        self.declarations.printTree(indent)
        self.instructions.printTree(indent)

    @addToClass(AST.Condition)
    def printTree(self, indent=""):
        self.expression.printTree(indent)

    @addToClass(AST.Expression)
    def printTree(self, indent=""):
        if self.expression is not None:
            if type(self.expression) == str:
                print(indent + self.expression)
            else:
                self.expression.printTree(indent)

        if self.left is not None:
            if hasattr(self.left, "printTree"):
                self.left.printTree(indent + " | ")
            else:
                print(indent + " | " + self.left)

        if self.right is not None:
            if hasattr(self.right, "printTree"):
                self.right.printTree(indent + " | ")
            else:
                print(indent + " | " + self.right)

    @addToClass(AST.Float)
    @addToClass(AST.String)
    @addToClass(AST.Integer)
    @addToClass(AST.Const)
    def printTree(self, indent=""):
        print(indent + self.value)

    @addToClass(AST.Variable)
    def printTree(self, indent=""):
        print(indent + self.name)

    @addToClass(AST.Fundef)
    def printTree(self, indent=""):
        print(indent + "FUNDEF")
        print(indent + " | " + self.id)
        print(indent + " | " + "RET " + self.type)
        self.args.printTree(indent + " | ")
        self.instr.printTree(indent + " | ")

    @addToClass(AST.Funcall)
    def printTree(self, indent=""):
        print(indent + "FUNCALL")
        print(indent + " | " + self.id)
        self.args.printTree(indent + " | ")

    @addToClass(AST.Arg)
    def printTree(self, indent=""):
        print(indent + "ARG " + self.name)
