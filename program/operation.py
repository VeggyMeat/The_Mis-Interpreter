from program.expression import Expression
from program.expression_type import ExpressionType
from program.operator import Operator


class Operation(Expression):
    operator: Operator
    left_operand: Expression
    right_operand: Expression
    def __init__(self, operator: str, left: Expression, right: Expression) -> None:
        super().__init__()
        self.expression_type = ExpressionType.OPERATION
        self.operator = Operation.parse_operator(operator)
        self.left_operand = left
        self.right_operand = right

    @staticmethod
    def parse_operator(op_str: str) -> Operator:
        if op_str == "+":
            return Operator.ADD
        elif op_str == "-":
            return Operator.SUBTRACT
        elif op_str == ">>":
            return Operator.SHIFT_RIGHT
        elif op_str == "<<":
            return Operator.SHIFT_LEFT
        elif op_str == "<":
            return Operator.LESS_THAN
        elif op_str == ">":
            return Operator.GREATER_THAN
        elif op_str == "==":
            return Operator.EQUALS
        elif op_str == "!=":
            return Operator.NOT_EQUALS
        else:
            raise ValueError(f"Unknown operator: {op_str}")
