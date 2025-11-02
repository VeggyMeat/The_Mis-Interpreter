# imports
import subprocess
import sys
import tempfile
import platform

import keyboard
import time

from program.assignment import Assignment
from program.condition import Condition
from program.output import Output
from program.variable import Variable
from program.value import Value
from program.operation import Operation
from program.operator import Operator
from transpilers.transpiler import Transpiler

import pygetwindow as gw


class PythonTranspiler(Transpiler):
    def __init__(self, code_block):
        super().__init__(code_block)

    def _convert(self, code_block=None, indent=0):
        if code_block is None:
            code_block = self.code_block

        code = ""
        indent_str = "    " * indent

        for cmd in code_block.commands:
            if isinstance(cmd, Assignment):
                code += f"{indent_str}{self._convert_assignment(cmd)}\n"
            elif isinstance(cmd, Condition):
                code += self._convert_condition(cmd, indent)
            elif isinstance(cmd, Output):
                code += f"{indent_str}{self._convert_output(cmd)}\n"

        return code

    def _convert_assignment(self, assignment: Assignment) -> str:
        var_name = assignment.variable.name
        expr = self._convert_expression(assignment.expression)
        return f"{var_name} = {expr}"

    def _convert_condition(self, condition: Condition, indent: int) -> str:
        expr = self._convert_expression(condition.expression)
        code = f"{'    '*indent}if {expr}:\n"
        code += self._convert(condition.true_code_block, indent + 1)

        if getattr(condition, "false_code_block", None) and condition.false_code_block.commands:
            code += f"{'    '*indent}else:\n"
            code += self._convert(condition.false_code_block, indent + 1)

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

    def run_in(self) -> None:
        """
        Displays the transpiled Python code in an IDLE window
        with a smooth typing animation.
        """
        code_to_display = self._convert()
        code_to_display = code_to_display.replace("\\", "\\\\").replace('"', '\\"')
        delay_seconds = 0.02

        system = platform.system()
        if system == "Darwin":
            subprocess.Popen(["open", "-a", "IDLE"])
        elif system == "Windows":
            subprocess.Popen([sys.executable, "-m", "idlelib"])
        else:
            subprocess.Popen([sys.executable, "-m", "idlelib"])
        
        time.sleep(2)
        
        code_to_display = 'def program():\n' + code_to_display
        keyboard.write(code_to_display, delay=delay_seconds)
        print()

    def run_out(self) -> None:
        windows = [w for w in gw.getWindowsWithTitle('') if w.title]
        if windows:
            win = windows[0]
            win.restore()  # un-minimize
            win.activate()  # bring to front
        
            time.sleep(1)

            keyboard.press_and_release('enter')
            keyboard.write('program()', delay=0.02)
            keyboard.press_and_release('enter')

            time.sleep(5)

            win.close()