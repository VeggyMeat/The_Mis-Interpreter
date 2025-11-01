from program.expression import Expression
from program.operator import Operator


class Operation(Expression):
    operator: Operator
    left_operand: Expression
    right_operand: Expression