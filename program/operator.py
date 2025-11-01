from enum import StrEnum


class Operator(StrEnum):
    ADD = "ADD"
    SUBTRACT = "SUBTRACT"
    LEFT_SHIFT = "LEFT_SHIFT"
    RIGHT_SHIFT = "RIGHT_SHIFT"
    EQUALS = "EQUALS"
    NOT_EQUALS = "NOT_EQUALS"
    LESS_THAN = "LESS_THAN"
    GREATER_THAN = "GREATER_THAN"
