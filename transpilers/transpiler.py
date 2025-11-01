from program.code_block import CodeBlock


class Transpiler:
    def __init__(self, code_block : CodeBlock):
        self.code = code_block

    def run_in(self) -> None:
        ...
    
    def run_out(self, output: int) -> None:
        ...
