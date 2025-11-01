from program.command import Command
from program.expression import Expression
from program.variable import Variable


class Assignment(Command):
    expression: Expression
    variable: Variable