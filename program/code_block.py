from program.command import Command


class CodeBlock:
    commands: list[Command] = []
    def __init__(self, cCode: str) -> None:
        self.cCode: str = cCode

    def _load_from_c(self) -> None:
        # Logic to load and parse C code
        ...