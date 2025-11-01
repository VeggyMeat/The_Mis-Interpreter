
from program.code_block import CodeBlock


class ITranspiler:
    def __init__(self, code_block : CodeBlock):
        self.code_block = code_block

    def transpile(self) -> None:
        ...
