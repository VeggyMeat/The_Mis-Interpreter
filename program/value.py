from program.expression import Expression
from program.expression_type import ExpressionType


class Value(Expression):
    value: int
    def __init__(self, value: int) -> None:
        super().__init__()
        self.expression_type = ExpressionType.VALUE
        self.value = value