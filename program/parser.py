import re

from program.expression import Expression
from program.operation import Operation
from program.value import Value
from program.variable import Variable


token_pattern = re.compile(r"\s*(==|!=|>>|<<|[+\-*/()<>]|[A-Za-z_]\w*|\d+)\s*")

def tokenize(s):
    return token_pattern.findall(s)

# --- Parser with precedence handling ---
class Parser:
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> str | None:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, expected=None) -> str:
        tok = self.peek()
        if expected and tok != expected:
            raise SyntaxError(f"Expected {expected} but got {tok}")
        self.pos += 1
        return tok

    # precedence levels:  >>,<<  <,>  ==,!=  +,-
    def parse_expression(self) -> Expression:
        return self.parse_add_sub()

    def parse_add_sub(self) -> Expression:
        node = self.parse_mul()
        while self.peek() in ('+', '-'):
            op = self.consume()
            right = self.parse_mul()
            node = Operation(op, node, right)
        return node
    
    def parse_mul(self):
        node = self.parse_compare()
        while self.peek() == '*':
            op = self.consume()
            right = self.parse_compare()
            node = Operation(op, node, right)
        return node

    def parse_compare(self):
        node = self.parse_term()
        while self.peek() in ('==', '!=', '<', '>'):
            op = self.consume()
            right = self.parse_term()
            node = Operation(op, node, right)
        return node

    def parse_term(self):
        tok = self.peek()
        if tok is None:
            raise SyntaxError("Unexpected end")
        if tok.isdigit():
            self.consume()
            return Value(int(tok))
        elif re.match(r"[A-Za-z_]\w*", tok):
            self.consume()
            return Variable(tok)
        elif tok == '(':
            self.consume('(')
            node = self.parse_expression()
            self.consume(')')
            return node
        else:
            raise SyntaxError(f"Unexpected token {tok}")

def parse_expression_string(s):
    tokens = tokenize(s)
    parser = Parser(tokens)
    result = parser.parse_expression()
    if parser.peek() is not None:
        raise SyntaxError("Extra input after expression")
    return result
