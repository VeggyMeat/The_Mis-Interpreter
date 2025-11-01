from enum import StrEnum


class ExpressionType(StrEnum):
    VALUE = "VALUE"
    VARIABLE = "VARIABLE"
    OPERATION = "OPERATION"
