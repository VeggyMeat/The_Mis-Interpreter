from program.expression import Expression
from program.expression_type import ExpressionType


class Value(Expression):
    value: str
    def __init__(self, value: str) -> None:
        super().__init__()
        self.expression_type = ExpressionType.VALUE
        self.value = value