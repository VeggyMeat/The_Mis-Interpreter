from program.command import Command
from program.command_type import CommandType
from program.expression import Expression
from program.parser import parse_expression_string
from program.variable import Variable


class Assignment(Command):
    expression: Expression
    variable: Variable

    def __init__(self, string: str):
        parts = string.split("=")
        self.variable = Variable(parts[0])
        self.expression = parse_expression_string(parts[1])
        self.command_type = CommandType.ASSIGNMENT
