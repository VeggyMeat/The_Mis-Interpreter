from enum import StrEnum


class CommandType(StrEnum):
    CONDITION = "CONDITION"
    ASSIGNMENT = "ASSIGNMENT"
    CODE_BLOCK = "CODE_BLOCK"
    OUTPUT = "OUTPUT"
