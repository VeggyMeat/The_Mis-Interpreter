from program.expression import Expression
from program.expression_type import ExpressionType


class Variable(Expression):
    name: str
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
        self.expression_type = ExpressionType.VARIABLE
