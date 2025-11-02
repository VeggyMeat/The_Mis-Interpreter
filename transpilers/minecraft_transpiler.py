from program.assignment import Assignment
from program.code_block import CodeBlock
from program.condition import Condition
from program.operation import Operation
from program.operator import Operator
from program.output import Output
from program.value import Value
from program.variable import Variable
from transpilers.transpiler import Transpiler

import pygetwindow as gw
import time
import keyboard

DELAY = 0.03
TIME_HELD = 3

class MinecraftTranspiler(Transpiler):
    def __init__(self, code_block: CodeBlock):
        super().__init__(code_block)
        self.variables = set()
        self.temp_var_count = 0

    def _code_block_to_commands(self, code_block: CodeBlock) -> list[str]:
        commands = []
        for cmd in code_block.commands:
            if isinstance(cmd, Assignment):
                expression = self._expression_to_commands(cmd.expression)
                commands += expression[:-1]
                commands.append(f"scoreboard players operation {cmd.variable.name} vars = {expression[-1]} vars")
            elif isinstance(cmd, Condition):
                true_code_block = self._code_block_to_commands(cmd.true_code_block)
                false_code_block = self._code_block_to_commands(cmd.false_code_block)
                expression = self._expression_to_commands(cmd.expression)
                commands += expression[:-1]
                true_code_block = [f"execute unless score {expression[-1]} vars matches 0 run " + line for line in true_code_block]
                false_code_block = [f"execute if score {expression[-1]} vars matches 0 run " + line for line in false_code_block]
                commands += true_code_block
                commands += false_code_block
            elif isinstance(cmd, Output):
                expression = self._expression_to_commands(cmd.expression)
                commands += expression[:-1]
                commands.append(f'title @a title [{{"text":"Output: "}},{{"score":{{"name":"{expression[-1]}","objective":"vars"}}}}]')
            elif isinstance(cmd, CodeBlock):
                commands += self._code_block_to_commands(cmd)
        return commands

    def _operator_to_minecraft(self, operator: Operator) -> str:
        if operator == Operator.ADD:
            return "+="
        elif operator == Operator.SUBTRACT:
            return "-="
        elif operator == Operator.MULTIPLY:
            return "*="
        elif operator == Operator.EQUALS:
            return "=="
        elif operator == Operator.NOT_EQUALS:
            return "!="
        elif operator == Operator.LESS_THAN:
            return "<"
        elif operator == Operator.GREATER_THAN:
            return ">"
        raise ValueError(f"Unknown operator: {operator}")

    def _expression_to_commands(self, expression) -> list[str]:
        if isinstance(expression, Value):
            out = [f"scoreboard players set temp{self.temp_var_count} vars {expression.value}", f"temp{self.temp_var_count}"]
            self.temp_var_count += 1
            return out
        elif isinstance(expression, Variable):
            self.variables.add(expression.name)
            return [f"{expression.name}"]
        elif isinstance(expression, Operation):
            out = []
            left_expression = self._expression_to_commands(expression.left_operand)
            out += left_expression[:-1]
            right_expression = self._expression_to_commands(expression.right_operand)
            out += right_expression[:-1]
            out.append(f"scoreboard players operation temp{self.temp_var_count} vars = {left_expression[-1]} vars")
            out.append(f"scoreboard players operation temp{self.temp_var_count} vars {self._operator_to_minecraft(expression.operator)} {right_expression[-1]} vars")
            out.append(f"temp{self.temp_var_count}")
            self.temp_var_count += 1
            return out
        raise ValueError(f"Unknown expression type: {expression}")

    def run_in(self) -> None:
        commands = self._code_block_to_commands(self.code_block)
        setup = ["scoreboard objectives add vars dummy", "scoreboard objectives setdisplay sidebar vars"]
        commands = setup + commands
        windows = [w for w in gw.getWindowsWithTitle('Minecraft 1.21.10 - Singleplayer') if w.title]
        if windows:
            win = windows[0]
            win.restore()  # un-minimize
            win.activate()  # bring to front
        
        time.sleep(1)
        keyboard.press_and_release('escape')
        for command in commands:
            keyboard.press_and_release('/')
            time.sleep(0.05)
            words = command.split(' ')
            for i, word in enumerate(words):
                if i != 0:
                    keyboard.write(' ' + word)
                else:
                    keyboard.write(word)
                time.sleep(DELAY)
            keyboard.press_and_release('enter')
        
        time.sleep(TIME_HELD)
    
    def run_out(self) -> None:
        windows = [w for w in gw.getWindowsWithTitle('Minecraft 1.21.10 - Singleplayer') if w.title]
        if windows:
            win = windows[0]
            win.restore()  # un-minimize
            win.activate()  # bring to front
            keyboard.press_and_release('/')
            time.sleep(0.05)
            keyboard.write('scoreboard objectives remove vars')
            keyboard.press_and_release('enter')
            time.sleep(DELAY)
            win.minimize()  # minimize after running
