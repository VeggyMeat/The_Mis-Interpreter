from typing import TYPE_CHECKING

from program.command_type import CommandType
from program.parser import parse_expression_string

if TYPE_CHECKING:
    from program.code_block import CodeBlock
from program.command import Command
from program.expression import Expression


class Condition(Command):
    expression: Expression
    true_code_block: CodeBlock
    false_code_block: CodeBlock
    def __init__(self, expression: str, true_code_block: CodeBlock, false_code_block: CodeBlock) -> None:
        super().__init__()
        self.expression = parse_expression_string(expression)
        self.true_code_block = true_code_block
        self.false_code_block = false_code_block
        self.command_type = CommandType.CONDITION
