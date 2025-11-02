from program.assignment import Assignment
from program.code_block import CodeBlock
from program.condition import Condition
from program.expression import Expression
from program.operation import Operation
from program.operator import Operator
from program.output import Output
from program.value import Value
from program.variable import Variable
from transpilers.transpiler import Transpiler

import mouse
import time

HOLD_TIME = 3


class MindustryTranspiler(Transpiler):
    def __init__(self, code_block: CodeBlock):
        super().__init__(code_block)
        self.variables = set()
        self.line = 0
        self.temp_var_count = 0
    
    def _code_block_to_commands(self, code_block: CodeBlock) -> list[str]:
        commands = []
        for cmd in code_block.commands:
            if isinstance(cmd, Assignment):
                expression = self._expression_to_commands(cmd.expression)
                commands += expression[:-1]
                commands.append(f"set {cmd.variable.name} {expression[-1]}")
                self.line += 1
            elif isinstance(cmd, Condition):
                self.line += 1 # for the jump line
                expression = self._expression_to_commands(cmd.expression)
                true_code_block = self._code_block_to_commands(cmd.true_code_block)
                self.line += 1 # placeholder for jump out
                line = self.line
                false_code_block = self._code_block_to_commands(cmd.false_code_block)
                commands += expression[:-1]
                commands.append(f"jump {line} equal {expression[-1]} 0")
                commands += true_code_block
                commands.append(f"jump {self.line} equal true true")
                commands += false_code_block
            elif isinstance(cmd, Output):
                expression = self._expression_to_commands(cmd.expression)
                commands += expression[:-1]
                commands.append(f"print {expression[-1]}")
                commands.append("printflush message1")
                self.line += 2
            elif isinstance(cmd, CodeBlock):
                commands += self._code_block_to_commands(cmd)
        return commands

    def _operator_to_mindustry(self, operator: Operator) -> str:
        if operator == Operator.ADD:
            return 'add'
        elif operator == Operator.SUBTRACT:
            return 'sub'
        elif operator == Operator.EQUALS:
            return 'equal'
        elif operator == Operator.NOT_EQUALS:
            return 'notEqual'
        elif operator == Operator.LESS_THAN:
            return 'lessThan'
        elif operator == Operator.GREATER_THAN:
            return 'greaterThan'
        else:
            raise ValueError(f"Unsupported operator: {operator}")
    
    def _expression_to_commands(self, expression: Expression) -> list[str]:
        if isinstance(expression, Value):
            out = [f"set temp{self.temp_var_count} {expression.value}", f"temp{self.temp_var_count}"]
            self.line += 1
            self.temp_var_count += 1
            return out
        elif isinstance(expression, Variable):
            self.variables.add(expression.name)
            return [expression.name]
        elif isinstance(expression, Operation):
            out = []
            left_expression = self._expression_to_commands(expression.left_operand)
            out += left_expression[:-1]
            right_expression = self._expression_to_commands(expression.right_operand)
            out += right_expression[:-1]
            out.append(f"op {self._operator_to_mindustry(expression.operator)} temp{self.temp_var_count} {left_expression[-1]} {right_expression[-1]}")
            self.line += 1
            out.append(f"temp{self.temp_var_count}")
            self.temp_var_count += 1
            return out
        else:
            raise ValueError("Unknown expression type")
    
    def run_in(self) -> None:
        commands = self._code_block_to_commands(self.code_block)
        commands.append("end")
        print('\n'.join([f"{i}: {command}" for i, command in enumerate(commands)]))
        print('\n'.join(commands))
        windows = [w for w in gw.getWindowsWithTitle('Mindustry') if w.title]
        if windows:
            win = windows[0]
            win.restore()  # un-minimize
            win.activate()  # bring to front
        time.sleep(HOLD_TIME)

    def run_out(self) -> None:
        windows = [w for w in gw.getWindowsWithTitle('Mindustry') if w.title]
        if windows:
            win = windows[0]
            win.restore()  # un-minimize
            win.activate()  # bring to front
            # hover over the message
            time.sleep(HOLD_TIME)
            win.minimize()  # minimize after running
