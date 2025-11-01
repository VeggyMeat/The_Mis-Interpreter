# imports
import transpiler
import subprocess
import sys
import tempfile

from program.command_type import CommandType
from program.assignment import Assignment
from program.condition import Condition
from program.output import Output
from program.variable import Variable
from program.value import Value
from program.operation import Operation
from program.operator import Operator


class C_Python:
    def __init__(self, code_block):
        self.code = code_block

    def convert(self, code_block=None, indent=0):
        if code_block is None:
            code_block = self.code

        code = ""
        # 4 spaces per indent
        indent_str = "    " * indent  

        for cmd in code_block.commands:
            if cmd.command_type == CommandType.ASSIGNMENT:
                line = self._convert_assignment(cmd)
                code += f"{indent_str}{line}\n"

            elif cmd.command_type == CommandType.CONDITION:
                line = self._convert_condition(cmd, indent)
                code += line

            elif cmd.command_type == CommandType.OUTPUT:
                line = self._convert_output(cmd)
                code += f"{indent_str}{line}\n"

        return code

    def _convert_assignment(self, assignment: Assignment) -> str:
        var_name = assignment.variable.name
        expr = self._convert_expression(assignment.expression)
        return f"{var_name} = {expr}"

    def _convert_condition(self, condition: Condition, indent: int) -> str:
        expr = self._convert_expression(condition.expression)
        code = f"{'    '*indent}if {expr}:\n"
        code += self.convert(condition.true_code_block, indent + 1)

        # Handle the optional else block
        if getattr(condition, "false_code_block", None) and condition.false_code_block.commands:
            code += f"{'    '*indent}else:\n"
            code += self.convert(condition.false_code_block, indent + 1)

        return code

    def _convert_output(self, output: Output) -> str:
        expr = self._convert_expression(output.expression)
        return f"print({expr})"

    def _convert_expression(self, expr):
        if isinstance(expr, Value):
            return str(expr.value)
        elif isinstance(expr, Variable):
            return expr.name
        elif isinstance(expr, Operation):
            left = self._convert_expression(expr.left_operand)
            right = self._convert_expression(expr.right_operand)
            op = self._convert_operator(expr.operator)
            return f"({left} {op} {right})"
        else:
            raise ValueError(f"Unknown expression type: {expr}")

    def _convert_operator(self, op: Operator) -> str:
        mapping = {
            Operator.ADD: "+",
            Operator.SUBTRACT: "-",
            Operator.LEFT_SHIFT: "<<",
            Operator.RIGHT_SHIFT: ">>",
            Operator.EQUALS: "==",
            Operator.NOT_EQUALS: "!=",
            Operator.LESS_THAN: "<",
            Operator.GREATER_THAN: ">"
        }
        return mapping[op]

    
    def run_in(self, code_to_display):
        """
        Displays the given code (or the transpiled code) in a new IDLE window
        with a smooth character-by-character typing animation.
        """
        # If no custom string was passed, use the transpiled code
        if code_to_display is None:
            code_to_display = self.convert()

        # Escape newlines and quotes properly for embedding in a Python string
        code_to_display = code_to_display.replace("\\", "\\\\").replace('"', '\\"')

        delay_seconds = 0.02  # typing speed

        # Python code that will animate the text in IDLE
        code_runner = f'''
import time
text = """{code_to_display}"""
for char in text:
    print(char, end="", flush=True)
    time.sleep({delay_seconds})
print()  # move to a new line at the end
'''

        # Write this animation code into a temporary file
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".py") as tmp:
            tmp.write(code_runner)
            tmp_path = tmp.name

        # Open a new IDLE window to display it
        subprocess.Popen([sys.executable, "-m", "idlelib", "-r", tmp_path])

    
    # def run_out(self, output) -> None:

    #     # run_out to animate
    #     to_print = output

    #     # delay between letters
    #     delay_seconds = 0.02  

    #     # code for temporary script
    #     code_to_run = f"""
    #     import time
    #     text = "{to_print}"
    #     for char in text:
    #         print(char, end="", flush=True)
    #         time.sleep({delay_seconds})
    #     print()  # move to a new line at the end
    #     """

    #     # temp script file
    #     with tempfile.NamedTemporaryFile("w", delete=False, suffix=".py") as tmp:
    #         tmp.write(code_to_run)
    #         tmp_path = tmp.name

    #     # launch IDLE run temp script
    #     subprocess.Popen([sys.executable, "-m", "idlelib", "-r", tmp_path])