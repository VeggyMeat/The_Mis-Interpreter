import sys

from program.code_block import CodeBlock
from transpilers.c_to_python import C_Python

class ExecutionController:
    program: CodeBlock
    inputs: list[str]

    def __init__(self):
        self.file = sys.argv[1]
        self.inputs = self.take_inputs()
        self.program = self._load_program(self.file)

    def run_program(self) -> None:
        python_transpiler = C_Python(self.program)
        python_transpiler.run_in()
    
    def _load_program(self, c_code: str) -> CodeBlock:
        with open(self.file, 'r') as f:
            c_code = f.read()
        print(c_code)
        cleaned_code = self._clean_code(c_code)
        print(cleaned_code)
        stck = [[]]
        current_str = ""
        i = 0
        while i < len(cleaned_code):
            char = cleaned_code[i]
            if i + 6 < len(cleaned_code) and cleaned_code[i:i+5] == "argv[" and cleaned_code[i+5].isdigit() and cleaned_code[i+6] == "]":
                current_str += self.inputs[int(cleaned_code[i+5])]
                i += 6
            elif char == ';':
                stck[-1].append(current_str)
                current_str = ""
            elif char == '{':
                stck[-1].append(current_str)
                current_str = ""
                stck.append([])
            elif char == '}':
                if current_str:
                    stck[-1].append(current_str)
                    current_str = ""
                block = stck.pop()
                stck[-1].append(block)
            else:
                current_str += char
            i += 1
        if current_str:
            stck[0].append(current_str)
        print(stck)
        return CodeBlock(stck[0])

    def _clean_code(self, c_code: str) -> str:
        # get rid of int main(...) and whitespace
        c_code = c_code[c_code.index("{")+1:c_code.rindex("return 0;")]
        out = ""
        for i, char in enumerate(c_code):
            if char == '\n' or char == '\t' or char == '\r':
                continue

            if char == ' ' and (i < 4 or c_code[i-4:i] != "char") and (i < 6 or c_code[i-6:i] != "printf"):
                continue

            out += char

        return out

    def take_inputs(self) -> list[int]:
        inputs = []
        for arg in range(int(sys.argv[2])):
            inputs.append(sys.argv[arg+3])
        return inputs

if __name__ == "__main__":
    controller = ExecutionController()
    controller.run_program()
    pass
