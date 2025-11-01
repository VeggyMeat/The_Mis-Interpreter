from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from program.code_block import CodeBlock
from program.command import Command
from program.expression import Expression


class Condition(Command):
    expression: Expression
    true_code_block: CodeBlock
    false_code_block: CodeBlock
