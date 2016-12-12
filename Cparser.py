#!/usr/bin/python

from scanner import Scanner
import re
import AST


class Cparser(object):
    def __init__(self):
        self.scanner = Scanner()
        self.scanner.build()

    tokens = Scanner.tokens

    precedence = (
        ("nonassoc", 'IFX'),
        ("nonassoc", 'ELSE'),
        ("right", '='),
        ("left", 'OR'),
        ("left", 'AND'),
        ("left", '|'),
        ("left", '^'),
        ("left", '&'),
        ("nonassoc", '<', '>', 'EQ', 'NEQ', 'LE', 'GE'),
        ("left", 'SHL', 'SHR'),
        ("left", '+', '-'),
        ("left", '*', '/', '%'),
    )

    def p_error(self, p):
        if p:
            print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')"
                  .format(p.lineno, self.scanner.find_tok_column(p), p.type, p.value))
        else:
            print("Unexpected end of input")

    def p_program(self, p):
        """program : constructions
                   | """
        p[0] = AST.Program(p[1])

    def p_constructions(self, p):
        """constructions : constructions construction
                         | construction"""
        if len(p) > 1:
            if isinstance(p[1], AST.ConstructionList):
                p[1].add_to_list(p[2])
                p[0] = p[1]
            else:
                p[0] = AST.ConstructionList()
                p[0].add_to_list(p[1])

    def p_construction(self, p):
        """construction : declaration
                        | fundef
                        | instruction """
        p[0] = AST.Construction(p[1])

    def p_declarations(self, p):
        """declarations : declarations declaration
                       | """

        if len(p) > 1:
            if p[1] == None:
                p[1] = AST.DeclarationList()

            p[0] = p[1]
            if len(p) > 2:
                p[1].add_to_list(p[2])
        else:
            p[0] = AST.DeclarationList()


    def p_declaration(self, p):
        """declaration : TYPE inits ';'
                       | error ';' """
        p[0] = AST.Declaration(p[1], p[2], p.lineno(1))

    def p_inits(self, p):
        """inits : inits ',' init
                 | init """
        if len(p) > 2:
            if p[1] == None:
                p[0] = AST.InitList()
            else:
                p[0] = p[1]
            p[0].add_to_list(p[3])

        else:
            p[0] = AST.InitList()
            p[0].add_to_list(p[1])

    def p_init(self, p):
        """init : ID '=' expression
                """
        p[0] = AST.Init(p[1], p[3], p.lineno(1))

    def p_instructions(self, p):
        """instructions : instructions instruction
                        | instruction """
        if len(p) > 2:
            if p[1] == None:
                p[1] = AST.InstructionList()

            p[1].add_to_list(p[2])
            p[0] = p[1]
        else:
            p[0] = AST.InstructionList(p[1])

    def p_instruction(self, p):
        """instruction : print_instr
                       | labeled_instr
                       | assignment
                       | choice_instr
                       | while_instr
                       | repeat_instr
                       | return_instr
                       | break_instr
                       | continue_instr
                       | compound_instr
                       | expression ';' """
        p[0] = AST.Instruction(p[1])

    def p_print_instr(self, p):
        """print_instr : PRINT expression ';'
                       | PRINT error ';' """
        p[0] = AST.PrintInstr("PRINT", p[2], p.lineno(1))

    def p_labeled_instr(self, p):
        """labeled_instr : ID ':' instruction """
        p[0] = AST.LabeledInstr(p[1], p[3])

    def p_assignment(self, p):
        """assignment : ID '=' expression ';' """
        p[0] = AST.Assignment(p[1], p[3], p.lineno(1))

    def p_choice_instr(self, p):
        """choice_instr : IF '(' condition ')' instruction  %prec IFX
                        | IF '(' condition ')' instruction ELSE instruction
                        | IF '(' error ')' instruction  %prec IFX
                        | IF '(' error ')' instruction ELSE instruction """

        if len(p) == 6:
            p[0] = AST.ChoiceInstr(p[3], p[5])
        elif len(p) > 6:
            p[0] = AST.ChoiceInstr(p[3], p[5], p[7])

    def p_while_instr(self, p):
        """while_instr : WHILE '(' condition ')' instruction
                       | WHILE '(' error ')' instruction """
        p[0] = AST.WhileInstr(p[3], p[5])

    def p_repeat_instr(self, p):
        """repeat_instr : REPEAT instructions UNTIL condition ';' """
        p[0] = AST.RepeatInstr(p[2], p[4], p.lineno(1))

    def p_return_instr(self, p):
        """return_instr : RETURN expression ';' """
        p[0] = AST.ReturnInstr(p[2], p.lineno(1))

    def p_continue_instr(self, p):
        """continue_instr : CONTINUE ';' """
        p[0] = AST.ContinueInstr(p.lineno(1))

    def p_break_instr(self, p):
        """break_instr : BREAK ';' """
        p[0] = AST.BreakInstr(p.lineno(1))

    def p_compound_instr(self, p):
        """compound_instr : '{' declarations instructions '}' """
        p[0] = AST.CompoundInstr(p[2], p[3], p.lineno(4))

    def p_condition(self, p):
        """condition : expression"""
        p[0] = AST.Condition(p[1])

    def p_const(self, p):
        """const : INTEGER
                 | FLOAT
                 | STRING"""
        if re.match(r"\d+(\.\d*)|\.\d+", p[1]):
            p[0] = AST.Float(p[1], p.lineno(1))
        elif re.match(r"\d+", p[1]):
            p[0] = AST.Integer(p[1], p.lineno(1))
        elif re.match( r'\"([^\\\n]|(\\.))*?\"', p[1]):
            p[0] = AST.String(p[1], p.lineno(1))

    def p_expression_id(self, p):
        """expression_id : ID"""
        p[0] = AST.Variable(p[1], p.lineno(1))

    def p_expression(self, p):
        """expression : const
                      | expression_id
                      | expression '+' expression
                      | expression '-' expression
                      | expression '*' expression
                      | expression '/' expression
                      | expression '%' expression
                      | expression '|' expression
                      | expression '&' expression
                      | expression '^' expression
                      | expression AND expression
                      | expression OR expression
                      | expression SHL expression
                      | expression SHR expression
                      | expression EQ expression
                      | expression NEQ expression
                      | expression '>' expression
                      | expression '<' expression
                      | expression LE expression
                      | expression GE expression
                      | '(' expression ')'
                      | '(' error ')'
                      | ID '(' expr_list_or_empty ')'
                      | ID '(' error ')' """

        if len(p) == 2:
            p[0] = p[1]

        elif p[2] == "(" and p[1] != "(":
            p[0] = AST.Funcall(p[1], p[3], p.lineno(1))

        elif len(p) == 4:
            if p[1] != '(':
                p[0] = AST.BinExpr(p[2], p[1], p[3], p.lineno(2))
            else:
                p[0] = p[2]

    def p_expr_list_or_empty(self, p):
        """expr_list_or_empty : expr_list
                              | """
        p[0] = p[1] if len(p) >= 2 else AST.ExpressionList()

    def p_expr_list(self, p):
        """expr_list : expr_list ',' expression
                     | expression """
        if len(p) > 2:
            if p[1] is None:
                p[1] = AST.ExpressionList()
            p[0] = p[1]
            p[0].add_to_list(p[3])
        else:
            p[0] = AST.ExpressionList()
            p[0].add_to_list(p[1])

    def p_fundef(self, p):
        """fundef : TYPE ID '(' args_list_or_empty ')' compound_instr """
        p[0] = AST.Fundef(p[2], p[4], p[6], p[1], p.lineno(1))

    def p_args_list_or_empty(self, p):
        """args_list_or_empty : args_list
                              | """
        p[0] = p[1] if len(p) > 1 else AST.ArgList(line = p.lineno(0))

    def p_args_list(self, p):
        """args_list : args_list ',' arg
                     | arg """
        if len(p) > 2:
            if p[1] is None:
                p[1] = AST.ArgList()
            p[0] = p[1]
            p[0].add_to_list(p[3])
        else:
            p[0] = AST.ArgList()
            p[0].add_to_list(p[1])



    def p_arg(self, p):
        """arg : TYPE ID """
        p[0] = AST.Arg(p[2], p[1], p.lineno(2))

