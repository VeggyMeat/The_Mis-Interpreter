from typing import Any

from program.assignment import Assignment
from program.command import Command
from program.command_type import CommandType
from program.condition import Condition
from program.output import Output


class CodeBlock(Command):
    commands: list[Command] = []

    def __init__(self, c_code: list[str]) -> None:
        self.commands = self._load_from_c(c_code)
        self.command_type = CommandType.CODE_BLOCK

    def _load_from_c(self, c_code: list[Any]) -> list[Command]:
        i = 0
        commands = []
        while i < len(c_code):
            cmd_str = c_code[i]
            if isinstance(cmd_str, list):
                code_block = CodeBlock(cmd_str)
                commands.append(code_block)
            else:
                if cmd_str.startswith("char"):
                    cmd_str = cmd_str.split(" ", 1)[1]
                    commands.append(Assignment(cmd_str))
                elif cmd_str.startswith("if"):
                    cmd_str = cmd_str[2:]
                    if i + 2 < len(c_code) and c_code[i + 2].startswith("else"):
                        commands.append(Condition(cmd_str, CodeBlock(c_code[i + 1]), CodeBlock(c_code[i + 3])))
                        i += 3
                    else:
                        commands.append(Condition(cmd_str, CodeBlock(c_code[i + 1]), CodeBlock([])))
                        i += 1
                elif cmd_str.startswith("printf("):
                    cmd_str = cmd_str[cmd_str.rindex("\"")+2:-1]

                    commands.append(Output(cmd_str))
            i += 1

        return commands
