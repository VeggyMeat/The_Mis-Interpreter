import time

from program.code_block import CodeBlock
from program.assignment import Assignment
from program.condition import Condition
from program.output import Output
from program.variable import Variable
from program.value import Value
from program.operation import Operation
from program.operator import Operator
from transpilers.transpiler import Transpiler

import xlwings as xw

DELAY = 0.03
TIME_HELD = 3


class ExcelTranspiler(Transpiler):
    """Transpiles C-like intermediate representation into Excel formulas/code."""

    def __init__(self, code_block: CodeBlock):
        super().__init__(code_block)
        self.last_cell = {}
        self.row = 1
        self.run_cell = "G2"
    
    def _write_cell_char_by_char(self, cell, text):
        print(text)
        self.sheet.range(cell).value = ""
        if text and text[0] == "=":
            self.sheet.range(cell).value = text
            time.sleep(DELAY*len(text))
        else:
            for i in range(0, len(text), 1):
                self.sheet.range(cell).value = text[:i+1]
                time.sleep(DELAY)

    def _generate_excel_file(self) -> None:
        self.app = xw.App(visible=True,add_book=False)
        self.wb = self.app.books.add()
        self.sheet = self.wb.sheets[0]

        for i, column_name in enumerate(["Type", "Variable", "Expression", "Run?", "Result", "Variable Set", "Run Cell"]):
            self._write_cell_char_by_char(f"{'ABCDEFG'[i]}{self.row}", column_name)
        self.row += 1
        self._write_block_to_sheet(self.code_block)
    
    def _convert_expression(self, expr) -> str:
        if isinstance(expr, Value):
            return str(expr.value)
        elif isinstance(expr, Variable):
            return expr.name
        elif isinstance(expr, Operation):
            left = self._convert_expression(expr.left_operand)
            right = self._convert_expression(expr.right_operand)
            op = self._convert_operator(expr.operator)
            return f"({left}{op}{right})"
        else:
            raise ValueError(f"Unknown expression type: {expr}")
    
    def _convert_expression_actual(self, expr) -> str:
        if isinstance(expr, Value):
            return str(expr.value)
        elif isinstance(expr, Variable):
            return f"LOOKUP(\"{expr.name}\", F2:F{self.row - 1}, E2:E{self.row - 1})"
        elif isinstance(expr, Operation):
            left = self._convert_expression_actual(expr.left_operand)
            right = self._convert_expression_actual(expr.right_operand)
            op = self._convert_operator(expr.operator)
            return f"({left}{op}{right})"
        else:
            raise ValueError(f"Unknown expression type: {expr}")

    def _convert_operator(self, op: Operator) -> str:
        mapping = {
            Operator.ADD: "+",
            Operator.SUBTRACT: "-",
            Operator.LEFT_SHIFT: "<<",
            Operator.RIGHT_SHIFT: ">>",
            Operator.EQUALS: "=",
            Operator.NOT_EQUALS: "<>",
            Operator.LESS_THAN: "<",
            Operator.GREATER_THAN: ">"
        }
        return mapping[op]

    def _write_block_to_sheet(self, code_block: CodeBlock):
        for cmd in code_block.commands:
            if isinstance(cmd, Assignment):
                var_name = cmd.variable.name
                expr = self._convert_expression(cmd.expression)
                self._write_cell_char_by_char(f"A{self.row}", "Assignment")
                self._write_cell_char_by_char(f"B{self.row}", var_name)
                self._write_cell_char_by_char(f"C{self.row}", expr)
                self._write_cell_char_by_char(f"D{self.row}", f"=D{self.row - 1}" if self.row > 2 else f"={self.run_cell}")
                expr_actual = self._convert_expression_actual(cmd.expression)
                self._write_cell_char_by_char(f"E{self.row}", f"=IF(D{self.row}, {expr_actual}, \"\")")
                self._write_cell_char_by_char(f"F{self.row}", f"=IF(D{self.row}, \"{var_name}\", \"\")")
                self.row += 1
            elif isinstance(cmd, Condition):
                expr = self._convert_expression(cmd.expression)
                self._write_cell_char_by_char(f"A{self.row}", "Condition")
                self._write_cell_char_by_char(f"C{self.row}", expr)
                expr_actual = self._convert_expression_actual(cmd.expression)
                self._write_cell_char_by_char(f"D{self.row}", f"=IF({f"D{self.row - 1}" if self.row > 2 else self.run_cell}, IF({expr_actual}, TRUE, FALSE), 0)")
                expression_row = self.row
                self.row += 1
                self._write_block_to_sheet(cmd.true_code_block)
                if getattr(cmd, "false_code_block", None) and cmd.false_code_block.commands:
                    self._write_cell_char_by_char(f"A{self.row}", "Condition")
                    self._write_cell_char_by_char(f"C{self.row}", f"NOT({expr})")
                    self._write_cell_char_by_char(f"D{self.row}", f"=IF(D{expression_row}=0, 0, IF(D{expression_row}=TRUE, FALSE, TRUE))")
                    self.row += 1
                    self._write_block_to_sheet(cmd.false_code_block)
            elif isinstance(cmd, Output):
                expr = self._convert_expression(cmd.expression)
                self._write_cell_char_by_char(f"A{self.row}", "Output")
                self._write_cell_char_by_char(f"C{self.row}", expr)
                self._write_cell_char_by_char(f"D{self.row}", f"=D{self.row - 1}" if self.row > 2 else f"={self.run_cell}")
                expr_actual = self._convert_expression_actual(cmd.expression)
                self._write_cell_char_by_char(f"E{self.row}", f"=IF(D{self.row}, {expr_actual}, \"\")")
                self.row += 1

    def run_in(self) -> None:
        """Generate Excel code from code block and open it as popup."""
        self._generate_excel_file()

    def run_out(self) -> None:
        self._write_cell_char_by_char(self.run_cell, "TRUE")
        time.sleep(TIME_HELD)
