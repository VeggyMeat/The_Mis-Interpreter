import os
import time
from typing import cast
from program.code_block import CodeBlock
from program.expression import Expression
from program.expression_type import ExpressionType
from program.operation import Operation
from program.operator import Operator
from program.output import Output
from program.variable import Variable
from transpilers.transpiler import Transpiler
from program.command_type import CommandType
from program.assignment import Assignment
from program.condition import Condition
from program.value import Value
import bisect

import keyboard
import mouse
import subprocess

import pygetwindow as gw
import sys

class Scratch(Transpiler):
    variables: list[str] = ["my variable"]
    variables_list_offset : int = 34
    variables_menu_offset : int = 30
    expressions_area_offset: int = 60
    program_x : int = 580
    program_y : int = 250
    expressions_area = (550,700)
    mouse_delay = 0.1
    scroll_delay = 0.15

    tabs: dict[str, tuple[int, int]] = {"variables":(240,550), "operators":(240,500),"control":(240,410),"looks":(240,275),"events":(240,360)}
    def _get_variable(self, variable_name : str, location: tuple[int,int]) -> None:
        mouse.move(self.tabs["variables"][0], self.tabs["variables"][1],absolute=True)
        mouse.click()
        time.sleep(self.scroll_delay)
        if variable_name not in self.variables:
            raise ValueError(f"Variable {variable_name} not found")
        i = self.variables.index(variable_name)
        mouse.move(310,300 + self.variables_list_offset * i, absolute=True)
        time.sleep(self.mouse_delay)
        mouse.press()
        mouse.move(location[0]-2,location[1],absolute=True)
        mouse.release()
        time.sleep(self.mouse_delay)
        
    
    def _get_block(self, block : str, location: tuple[int,int]) -> None:
        match block:
            case "START":
                mouse.move(self.tabs["events"][0], self.tabs["events"][1],absolute=True)
                mouse.click()
                time.sleep(self.scroll_delay)
                mouse.move(285,290,absolute=True)
            case "SET":
                mouse.move(self.tabs["variables"][0], self.tabs["variables"][1],absolute=True)
                mouse.click()
                time.sleep(self.scroll_delay)
                mouse.move(285,306+self.variables_list_offset*len(self.variables),absolute=True)
            case "ADD":
                mouse.move(self.tabs["operators"][0], self.tabs["operators"][1],absolute=True)
                mouse.click()
                time.sleep(self.scroll_delay)
                mouse.move(285,265,absolute=True)
            case "SUBTRACT":
                mouse.move(self.tabs["operators"][0], self.tabs["operators"][1],absolute=True)
                mouse.click()
                time.sleep(self.scroll_delay)
                mouse.move(285,300,absolute=True)
            case "MULTIPLY":
                mouse.move(self.tabs["operators"][0], self.tabs["operators"][1],absolute=True)
                mouse.click()
                time.sleep(self.scroll_delay)
                mouse.move(285,335,absolute=True)
            case "EQUALS":
                mouse.move(self.tabs["operators"][0], self.tabs["operators"][1],absolute=True)
                mouse.click()
                time.sleep(self.scroll_delay)
                mouse.move(285,545,absolute=True)
            case "NOT_EQUALS" :
                mouse.move(self.tabs["operators"][0], self.tabs["operators"][1],absolute=True)
                mouse.click()
                time.sleep(self.scroll_delay)
                mouse.move(285,670,absolute=True)
            case "LESS_THAN":
                mouse.move(self.tabs["operators"][0], self.tabs["operators"][1],absolute=True)
                mouse.click()
                time.sleep(self.scroll_delay)
                mouse.move(285,510,absolute=True)
            case "GREATER_THAN":
                mouse.move(self.tabs["operators"][0], self.tabs["operators"][1],absolute=True)
                mouse.click()
                time.sleep(self.scroll_delay)
                mouse.move(285,475,absolute=True)
            case "IF":
                mouse.move(self.tabs["control"][0], self.tabs["control"][1],absolute=True)
                mouse.click()
                time.sleep(self.scroll_delay)
                mouse.move(285,590,absolute=True)
            case "SAY":
                mouse.move(self.tabs["looks"][0], self.tabs["looks"][1],absolute=True)
                mouse.click()
                time.sleep(self.scroll_delay)
                mouse.move(285,310,absolute=True)
            case _:
                raise ValueError(f"Unknown block: {block}")
            
        time.sleep(self.mouse_delay)
        mouse.press()
        mouse.move(location[0],location[1],absolute=True)
        mouse.release()
        time.sleep(self.mouse_delay)

    def _parse_expression(self, expression : Expression, result_location: tuple[int,int]) -> None:
        match expression.expression_type:
            case ExpressionType.VALUE:
                expression = cast(Value, expression)
                self._get_block("ADD", result_location)
                mouse.move(58,0,absolute=False)
                mouse.click()
                time.sleep(self.mouse_delay)
                keyboard.write(str(expression.value))
                mouse.move(-58,0,absolute=False)
                time.sleep(self.mouse_delay)
            
            case ExpressionType.VARIABLE:
                expression = cast(Variable, expression)
                self._get_variable(expression.name, result_location)

            case ExpressionType.OPERATION:
                expression = cast(Operation, expression)

                match expression.operator:
                    case Operator.ADD:
                        self._get_block("ADD", result_location)
                        
                        self._parse_expression(expression.right_operand, (result_location[0], result_location[1] + self.expressions_area_offset))
                        mouse.press()
                        mouse.move(58,-self.expressions_area_offset,absolute=False)
                        mouse.release()
                        time.sleep(self.mouse_delay)

                        self._parse_expression(expression.left_operand, (result_location[0], result_location[1] + self.expressions_area_offset))
                        mouse.press()
                        mouse.move(13,-self.expressions_area_offset,absolute=False)
                        mouse.release()
                        time.sleep(self.mouse_delay)


                    case Operator.SUBTRACT:
                        self._get_block("SUBTRACT", result_location)

                        self._parse_expression(expression.right_operand, (result_location[0], result_location[1] + self.expressions_area_offset))
                        mouse.press()
                        mouse.move(58,-self.expressions_area_offset,absolute=False)
                        mouse.release()
                        time.sleep(self.mouse_delay)

                        self._parse_expression(expression.left_operand, (result_location[0], result_location[1] + self.expressions_area_offset))
                        mouse.press()
                        mouse.move(13,-self.expressions_area_offset,absolute=False)
                        mouse.release()
                        time.sleep(self.mouse_delay)
                    
                    case Operator.MULTIPLY:
                        self._get_block("MULTIPLY", result_location)

                        self._parse_expression(expression.right_operand, (result_location[0], result_location[1] + self.expressions_area_offset))
                        mouse.press()
                        mouse.move(58,-self.expressions_area_offset,absolute=False)
                        mouse.release()
                        time.sleep(self.mouse_delay)

                        self._parse_expression(expression.left_operand, (result_location[0], result_location[1] + self.expressions_area_offset))
                        mouse.press()
                        mouse.move(13,-self.expressions_area_offset,absolute=False)
                        mouse.release()
                        time.sleep(self.mouse_delay)
                    
                    case Operator.EQUALS:
                        self._get_block("EQUALS", result_location)

                        self._parse_expression(expression.right_operand, (result_location[0], result_location[1] + self.expressions_area_offset))
                        mouse.press()
                        mouse.move(68,-self.expressions_area_offset,absolute=False)
                        mouse.release()
                        time.sleep(self.mouse_delay)

                        self._parse_expression(expression.left_operand, (result_location[0], result_location[1] + self.expressions_area_offset))
                        mouse.press()
                        mouse.move(20,-self.expressions_area_offset,absolute=False)
                        mouse.release()
                        time.sleep(self.mouse_delay)

                    case Operator.NOT_EQUALS:
                        self._get_block("NOT_EQUALS", result_location)

                        negated = Operation("==", expression.left_operand, expression.right_operand)
                        self._parse_expression(negated, (result_location[0], result_location[1] + self.expressions_area_offset))
                        mouse.press()
                        mouse.move(40,-self.expressions_area_offset,absolute=False)
                        mouse.release()
                        time.sleep(self.mouse_delay)
                    case Operator.LESS_THAN:
                        self._get_block("LESS_THAN", result_location)

                        self._parse_expression(expression.right_operand, (result_location[0], result_location[1] + self.expressions_area_offset))
                        mouse.press()
                        mouse.move(68,-self.expressions_area_offset,absolute=False)
                        mouse.release()
                        time.sleep(self.mouse_delay)

                        self._parse_expression(expression.left_operand, (result_location[0], result_location[1] + self.expressions_area_offset))
                        mouse.press()
                        mouse.move(20,-self.expressions_area_offset,absolute=False)
                        mouse.release()
                        time.sleep(self.mouse_delay)
                    
                    case Operator.GREATER_THAN:
                        self._get_block("GREATER_THAN", result_location)

                        self._parse_expression(expression.right_operand, (result_location[0], result_location[1] + self.expressions_area_offset))
                        mouse.press()
                        mouse.move(68,-self.expressions_area_offset,absolute=False)
                        mouse.release()
                        time.sleep(self.mouse_delay)

                        self._parse_expression(expression.left_operand, (result_location[0], result_location[1] + self.expressions_area_offset))
                        mouse.press()
                        mouse.move(20,-self.expressions_area_offset,absolute=False)
                        mouse.release()
                        time.sleep(self.mouse_delay)
                        
                
        # mouse.move(result_location[0]-10, result_location[1], absolute=True)
        mouse.move(result_location[0]-2, result_location[1]+2, absolute=True)
        if expression.expression_type != ExpressionType.OPERATION or expression.operator not in [Operator.ADD, Operator.SUBTRACT, Operator.MULTIPLY]:
            mouse.move(5, 3, absolute=False)
        time.sleep(self.mouse_delay)
        return

    def _parse_code_block(self, code_block : CodeBlock) -> None:
        for command in code_block.commands:
            if command.command_type == CommandType.CONDITION:
                command = cast(Condition, command)
                
                self._get_block("IF", (self.program_x, self.program_y))
                self._parse_expression(command.expression, self.expressions_area)
                mouse.press()
                mouse.move(self.program_x + 45, self.program_y)
                mouse.release()
                time.sleep(self.mouse_delay)

                self.program_x += 15
                self.program_y += 30
                self._parse_code_block(command.true_code_block)
                self.program_y += 35
                self._parse_code_block(command.false_code_block)
                self.program_y += 35
                self.program_x -= 15

            if command.command_type == CommandType.ASSIGNMENT:
                command = cast(Assignment, command)

                self._parse_expression(command.expression, self.expressions_area)

                if command.variable.name not in self.variables:
                    bisect.insort(self.variables,command.variable.name)

                    mouse.move(self.tabs["variables"][0], self.tabs["variables"][1],absolute=True)
                    mouse.click()
                    time.sleep(self.scroll_delay)

                    mouse.move(360,260)
                    mouse.click()
                    time.sleep(self.mouse_delay)
                    keyboard.write(command.variable.name)
                    time.sleep(self.mouse_delay)
                    keyboard.press_and_release('enter')
                    time.sleep(self.scroll_delay)
                    
                i = self.variables.index(command.variable.name)

                self._get_block("SET", (self.program_x, self.program_y))
                mouse.move(45,0,absolute=False)
                time.sleep(self.mouse_delay)
                mouse.click()
                time.sleep(self.scroll_delay)
                mouse.move(0,45 + self.variables_list_offset * i,absolute=False)
                mouse.click()
                time.sleep(self.mouse_delay)

                mouse.move(self.expressions_area[0]-2, self.expressions_area[1]+1, absolute=True)
                mouse.press()
                mouse.move(self.program_x+90, self.program_y, absolute=True)
                mouse.release()
                time.sleep(self.mouse_delay)

                self.program_y += 36
            
            if command.command_type == CommandType.OUTPUT:
                command = cast(Output, command)

                self._parse_expression(command.expression, self.expressions_area)
                
                self._get_block("SAY", (self.program_x, self.program_y))
                mouse.move(self.expressions_area[0]-2, self.expressions_area[1]+1, absolute=True)
                mouse.press()
                mouse.move(self.program_x+45,self.program_y,absolute=True)
                mouse.release()
                time.sleep(self.mouse_delay)

                self.program_y += 38

    def run_in(self) -> None:
        keyboard.add_hotkey('a', lambda: os._exit(0))

        windows = [w for w in gw.getWindowsWithTitle('Scratch 3.29.1') if w.title]
        if windows:
            win = windows[0]
            win.restore()  # un-minimize
            win.activate()  # bring to front

            time.sleep(1)
            self._get_block("START", (self.program_x, self.program_y-5))
            self.program_y += 10
            self._parse_code_block(self.code_block)
    
    def run_out(self):
        time.sleep(1)
        windows = [w for w in gw.getWindowsWithTitle('Scratch 3.29.1') if w.title]
        if windows:
            win = windows[0]
            win.restore()  # un-minimize
            win.activate()  # bring to front

            time.sleep(1)
        
            mouse.move(1020,190,absolute=True)
            mouse.click()
            time.sleep(3)

            mouse.move(380,142)
            mouse.click()
            time.sleep(self.mouse_delay)
            mouse.move(400,187)
            mouse.click()
            time.sleep(self.mouse_delay)
            mouse.move(916,520)
            mouse.click()

            time.sleep(self.mouse_delay)
            win.minimize()
