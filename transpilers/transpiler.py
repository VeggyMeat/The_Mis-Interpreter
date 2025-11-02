from program.code_block import CodeBlock


class Transpiler:
    def __init__(self, code_block : CodeBlock):
        self.code_block = code_block

    def run_in(self) -> None:
        ...
    
    def run_out(self) -> None:
        ...
