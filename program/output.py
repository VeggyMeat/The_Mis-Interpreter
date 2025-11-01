from program.command import Command
from program.command_type import CommandType
from program.expression import Expression
from program.parser import parse_expression_string


class Output(Command):
    expression: Expression
    def __init__(self, cmd_str: str) -> None:
        super().__init__()
        self.expression = parse_expression_string(cmd_str)
        self.command_type = CommandType.OUTPUT
