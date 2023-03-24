# -*- coding: utf-8 -*-

"""Calculator module for scientific calculator application
"""

from __future__ import print_function

import re
import math

from collections import namedtuple
from enum import Enum


class Associativity(Enum):
    """Represent operators associativity
    """
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class LexType(Enum):
    """Lex token types
    """
    BEGIN = "BEGIN"
    LEFT_PARENTHESIS = "LEFT_PARENTHESIS"
    RIGHT_PARENTHESIS = "RIGHT_PARENTHESIS"
    OPERATOR = "OPERATOR"
    EQUAL = "EQUAL"
    FUNCTION = "FUNCTION"
    NUMBER = "NUMBER"
    VARIABLE = "VARIABLE"


class LexTag(Enum):
    """Lex token tags/names
    """
    LEFT_PARENTHESIS = "LEFT_PARENTHESIS"
    RIGHT_PARENTHESIS = "RIGHT_PARENTHESIS"
    ADDITION = "ADDITION"
    UNARY_SUBTRACTION = "UNARY_SUBTRACTION"
    SUBTRACTION = "SUBTRACTION"
    MULTIPLICATION = "MULTIPLICATION"
    DIVISION = "DIVISION",
    EXPONENTIATION = "EXPONENTIATION"
    EQUAL = "EQUAL"
    SQRT = "SQRT"
    LOG = "LOG"
    SIN = "SIN"
    COS = "COS"
    NUMBER = "NUMBER"
    VARIABLE = "VARIABLE"


LEX_TOKENS = [
    (r"[ \n\t]+", None, None),
    (r"#[^\n]*", None, None),
    (r"\(", LexType.LEFT_PARENTHESIS, LexTag.LEFT_PARENTHESIS),
    (r"\)", LexType.RIGHT_PARENTHESIS, LexTag.RIGHT_PARENTHESIS),
    (r"\+", LexType.OPERATOR, LexTag.ADDITION),
    (r"-", LexType.OPERATOR, LexTag.SUBTRACTION),
    (r"\*", LexType.OPERATOR, LexTag.MULTIPLICATION),
    (r"/", LexType.OPERATOR, LexTag.DIVISION),
    (r"\^", LexType.OPERATOR, LexTag.EXPONENTIATION),
    (r"=", LexType.EQUAL, LexTag.EQUAL),
    (r"sqrt", LexType.FUNCTION, LexTag.SQRT),
    (r"log", LexType.FUNCTION, LexTag.LOG),
    (r"sin", LexType.FUNCTION, LexTag.SIN),
    (r"cos", LexType.FUNCTION, LexTag.COS),
    (r"[0-9.]+", LexType.NUMBER, LexTag.NUMBER),
    (r"x", LexType.VARIABLE, LexTag.VARIABLE),
]

Operator = namedtuple("Operator", ["precedence", "associativity"])

OPERATOR_TABLE = {
    LexTag.EXPONENTIATION: Operator(5, Associativity.RIGHT),
    LexTag.UNARY_SUBTRACTION: Operator(4, Associativity.RIGHT),
    LexTag.MULTIPLICATION: Operator(3, Associativity.LEFT),
    LexTag.DIVISION: Operator(3, Associativity.LEFT),
    LexTag.ADDITION:  Operator(2, Associativity.LEFT),
    LexTag.SUBTRACTION: Operator(2, Associativity.LEFT),
}

COMPUTE = {
    LexTag.EXPONENTIATION: lambda a, b: a**b,
    LexTag.MULTIPLICATION: lambda a, b: a*b,
    LexTag.DIVISION: lambda a, b: a/b,
    LexTag.ADDITION: lambda a, b: a+b,
    LexTag.SUBTRACTION: lambda a, b: a-b,
    LexTag.UNARY_SUBTRACTION: lambda a: -a,
    LexTag.SQRT: math.sqrt,
    LexTag.LOG: math.log,
    LexTag.SIN: math.sin,
    LexTag.COS: math.cos,
}

EXPECTED_TOKEN = {
    LexType.BEGIN: [
        LexTag.LEFT_PARENTHESIS,
        LexTag.ADDITION, LexTag.SUBTRACTION, LexTag.UNARY_SUBTRACTION,
        LexTag.SQRT, LexTag.LOG, LexTag.SIN, LexTag.COS,
        LexTag.NUMBER, LexTag.VARIABLE],
    LexType.LEFT_PARENTHESIS: [
        LexTag.LEFT_PARENTHESIS,
        LexTag.ADDITION, LexTag.SUBTRACTION, LexTag.UNARY_SUBTRACTION,
        LexTag.SQRT, LexTag.LOG, LexTag.SIN, LexTag.COS,
        LexTag.NUMBER, LexTag.VARIABLE],
    LexType.RIGHT_PARENTHESIS: [
        LexTag.RIGHT_PARENTHESIS,
        LexTag.ADDITION, LexTag.SUBTRACTION,
        LexTag.MULTIPLICATION, LexTag.DIVISION, LexTag.EXPONENTIATION],
    LexType.OPERATOR: [
        LexTag.LEFT_PARENTHESIS,
        LexTag.SQRT, LexTag.LOG, LexTag.SIN, LexTag.COS,
        LexTag.NUMBER, LexTag.VARIABLE],
    LexType.FUNCTION: [
        LexTag.LEFT_PARENTHESIS],
    LexType.NUMBER: [
        LexTag.RIGHT_PARENTHESIS,
        LexTag.ADDITION, LexTag.SUBTRACTION,
        LexTag.MULTIPLICATION, LexTag.DIVISION, LexTag.EXPONENTIATION],
    LexType.VARIABLE: [
        LexTag.RIGHT_PARENTHESIS,
        LexTag.ADDITION, LexTag.SUBTRACTION,
        LexTag.MULTIPLICATION, LexTag.DIVISION, LexTag.EXPONENTIATION],
}

Token = namedtuple("Token", ["value", "type", "tag", "position"])


class CalculatorError(ValueError):
    """custom error class for Calculator
    """
    def __init__(self, *args):
        super(CalculatorError, self).__init__(*args)
        self.message = args[0]
        self.position = args[1]

    def __str__(self):
        return "%s at position %s" % (self.message, self.position)


class Variable(object):
    """Implement arithmetic operations for first degree polynomials

    Format is a*x+b

    """

    def __init__(self, token=None):
        if token is None:
            self.a = None
            self.b = None
            self.type = None
            self.position = None
            return
        self.type = token.type
        self.position = token.position
        if token.type == LexType.NUMBER:
            self.a = 0.0
            self.b = float(token.value)
        elif token.type == LexType.VARIABLE:
            self.a = 1.0
            self.b = 0.0

    def __str__(self):
        return "({0}*x {1})".format(self.a, self.b)

    def __repr__(self):
        return "({0}*x {1})".format(self.a, self.b)

    def __float__(self):
        if self.a == 0:
            return float(self.b)
        else:
            return float(-self.b)/float(self.a)

    def __neg__(self):
        var = Variable()
        var.a = -self.a
        var.b = -self.b
        var.type = self.type
        var.position = self.position
        return var

    def __add__(self, other):
        var = Variable()
        var.a = self.a + other.a
        var.b = self.b + other.b
        var.position = other.position
        if var.a == 0:
            var.type = LexType.NUMBER
        else:
            var.type = LexType.VARIABLE
        return var

    def __sub__(self, other):
        var = Variable()
        var.a = self.a - other.a
        var.b = self.b - other.b
        var.position = other.position
        if var.a == 0:
            var.type = LexType.NUMBER
        else:
            var.type = LexType.VARIABLE
        return var

    def __mul__(self, other):
        var = Variable()
        var.type = LexType.VARIABLE
        var.position = other.position

        if self.a == 0 and other.a == 0:
            var.a = 0
            var.b = self.b * other.b
            var.type = LexType.NUMBER
        elif self.a == 0 and other.a != 0:
            var.a = self.b * other.a
            var.b = self.b * other.b
        elif self.a != 0 and other.a == 0:
            var.a = self.a * other.b
            var.b = self.b * other.b
        elif self.a != 0 and other.a != 0:
            raise CalculatorError("Multiplication of two variables is not supported", other.position)
        return var

    def __div__(self, other):
        var = Variable()
        var.position = other.position
        if other.a != 0:
            raise CalculatorError("Division with a variable is not supported", other.position)

        if other.b == 0:
            raise CalculatorError("Division by zero", other.position)

        var.a = self.a / other.b
        var.b = self.b / other.b

        if self.a == 0:
            var.type = LexType.NUMBER
        elif self.a != 0:
            var.type = LexType.VARIABLE
        return var

    def __pow__(self, other):
        var = Variable()
        var.position = other.position
        var.type = LexType.NUMBER

        if self.a == 0 and other.a == 0:
            var.a = 0
            var.b = self.b ** other.b
        else:
            raise CalculatorError("Exponentiation with a variable is not supported", other.position)
        return var


class Calculator(object):
    """Main calculator class
    """
    def __init__(self, string):
        self.string = string.lower()
        self.tokens = []
        self.rpn = []
        self.has_variable = False
        self.is_equation = False
        self.equal_index = None

    def lex(self, lex_tokens):
        """Lexer, transform inpout in tokens
        """
        position = 0
        self.tokens = []
        while position < len(self.string):
            match = None
            for token_expr in lex_tokens:
                pattern, token_type, tag = token_expr
                regex = re.compile(pattern)
                match = regex.match(self.string, position)
                if match:
                    text = match.group(0)
                    if tag:
                        if token_type == LexType.NUMBER:
                            token = Token(float(text), token_type, tag, position)
                        else:
                            token = Token(text, token_type, tag, position)

                        if token.type == LexType.VARIABLE:
                            self.has_variable = True
                        elif token.type == LexType.EQUAL:
                            self.is_equation = True
                            self.equal_index = len(self.tokens)

                        self.tokens.append(token)
                    break
            if not match:
                raise CalculatorError("Illegal character: '%s'" % self.string[position], position)
            else:
                position = match.end(0)
        if len(self.tokens) == 0:
            raise CalculatorError("Empty expression", position)

        return self.tokens

    def parse(self):
        """ Parser based on shunting_yard
        """
        self.rpn = []
        if not self.tokens:
            return

        stack = []
        token_index = 0
        last = Token(" ", LexType.BEGIN, None, None)

        # a While there are tokens to be read:
        while token_index < len(self.tokens):
            # a.1 Read a token.
            token = self.tokens[token_index]

            # check if we expect this token
            if token.tag not in EXPECTED_TOKEN[last.type]:
                raise CalculatorError("Unexpected token: '%s'" % token.value, token.position)

            # treat unary subtraction
            if token.tag == LexTag.SUBTRACTION and (last.type == LexType.BEGIN or last.tag == LexTag.LEFT_PARENTHESIS):
                self.tokens[token_index] = Token('-u', LexType.OPERATOR, LexTag.UNARY_SUBTRACTION, token.position)
                token = self.tokens[token_index]

            token_index += 1
            last = token

            # a.2 If the token is a number, then add it to the output queue.
            if (token.type == LexType.NUMBER) or (token.type == LexType.VARIABLE):
                self.rpn.append(token)
                continue

            # a.3 If the token is a function token, then push it onto the stack.
            if token.type == LexType.FUNCTION:
                stack.append(token)
                continue

            # a.4 If the token is a function argument separator (e.g., a comma):
            # not implemented, we accept only unary functions

            # a.5 If the token is an operator, o_1, then:
            if token.type == LexType.OPERATOR:
                while True:
                    if len(stack) == 0:
                        break

                    # a.5.1 while there is an operator token, o_2, at the top of the stack, and either o_1 is left-associative and its precedence is less than or equal to that of o_2, or o_1 if right associative, and has precedence less than that of o_2, then pop o_2 off the stack, onto the output queue;
                    if (stack[-1].type == LexType.OPERATOR) and (
                            ((OPERATOR_TABLE[token.tag].associativity == Associativity.LEFT) and (
                                OPERATOR_TABLE[token.tag].precedence <= OPERATOR_TABLE[stack[-1].tag].precedence)
                            ) or (
                                (OPERATOR_TABLE[token.tag].associativity == Associativity.RIGHT) and (
                                    OPERATOR_TABLE[token.tag].precedence < OPERATOR_TABLE[stack[-1].tag].precedence)
                            )):
                        self.rpn.append(stack.pop())
                    else:
                        break

                # a.5.2 push o_1 onto the stack.
                stack.append(token)
                continue

            # a.6 If the token is a left parenthesis, then push it onto the stack.
            if token.type == LexType.LEFT_PARENTHESIS:
                stack.append(token)
                continue

            # a.7 If the token is a right parenthesis:
            if token.type == LexType.RIGHT_PARENTHESIS:

                # a.7.1 Until the token at the top of the stack is a left parenthesis, pop operators off the stack onto the output queue.
                # a.7.2 Pop the left parenthesis from the stack, but not onto the output queue.
                # a.7.3 If the token at the top of the stack is a function token, pop it onto the output queue.
                # a.7.4 If the stack runs out without finding a left parenthesis, then there are mismatched parentheses.

                while True:

                    if len(stack) == 0:
                        raise CalculatorError("There are mismatched parentheses", token.position)

                    if stack[-1].type == LexType.LEFT_PARENTHESIS:
                        stack.pop()
                        if len(stack) > 0 and stack[-1].type == LexType.FUNCTION:
                            self.rpn.append(stack.pop())
                        break

                    else:
                        self.rpn.append(stack.pop())

        # b When there are no more tokens to read:

        # b.1 While there are still operator tokens in the stack:
        while len(stack) > 0:
            # b.1.1 If the operator token on the top of the stack is a parenthesis, then there are mismatched parentheses.
            if (stack[-1].type == LexType.LEFT_PARENTHESIS) or (stack[-1].type == LexType.RIGHT_PARENTHESIS):
                raise CalculatorError("There are mismatched parentheses", stack[-1].position)

            # b.1.2 Pop the operator onto the output queue.
            self.rpn.append(stack.pop())

        # c Exit.
        return self.rpn

    def rpn_eval(self):
        """ Simple RPN eval - uses Variable simple evaluator
        """
        stack = []

        for token in self.rpn:

            if token.type in [LexType.NUMBER, LexType.VARIABLE]:
                stack.append(Variable(token))
                continue

            if token.type == LexType.FUNCTION:
                try:
                    first_operand = stack.pop()
                except IndexError as error:
                    raise CalculatorError("Unexpected end of expression after '%s'" % token.value, token.position)

                if first_operand.type == LexType.VARIABLE:
                    raise CalculatorError("Function '%s' applied to variable is not supported" % token.value, token.position)
                try:
                    stack.append(Variable(Token(COMPUTE[token.tag](first_operand.b), first_operand.type, None, first_operand.position)))
                except ArithmeticError as error:
                    raise CalculatorError("ArithmeticError (%s)" % error, token.position)

                continue

            # treat unary subtraction
            if token.tag == LexTag.UNARY_SUBTRACTION:
                try:
                    first_operand = stack.pop()
                except IndexError as error:
                    raise CalculatorError("Unexpected end of expression after '%s'" % token.value, token.position)

                try:
                    stack.append(COMPUTE[token.tag](first_operand))
                except ArithmeticError as error:
                    raise CalculatorError("ArithmeticError (%s)" % error, token.position)
                continue

            # only binary operators left
            if token.type == LexType.OPERATOR:
                try:
                    second_operand = stack.pop()
                    first_operand = stack.pop()
                except IndexError as error:
                    raise CalculatorError("Unexpected end of expression after '%s'" % token.value, token.position)

                try:
                    stack.append(COMPUTE[token.tag](first_operand, second_operand))
                except ArithmeticError as error:
                    raise CalculatorError("ArithmeticError (%s)" % error, token.position)

                continue

            raise CalculatorError("Unexpected token '%s'" % token.value, token.position)

        value = stack.pop()
        return value


    def solve(self):
        """Solve n expresiion
            Transform equation if needed
        """
        self.lex(LEX_TOKENS)

        if self.is_equation and self.has_variable:
            if len(self.tokens[self.equal_index+1:]) == 0:
                raise CalculatorError("Equation needs value after equal", 0)
            # transform x+1=2 into x+1-(2)=0
            self.tokens = self.tokens[:self.equal_index] + [Token("-", LexType.OPERATOR, LexTag.SUBTRACTION, 0),
                Token("(", LexType.LEFT_PARENTHESIS, LexTag.LEFT_PARENTHESIS, 0)] +  self.tokens[self.equal_index+1:] + [Token("(", LexType.RIGHT_PARENTHESIS, LexTag.RIGHT_PARENTHESIS, 0)]
        elif self.is_equation or self.has_variable:
            raise CalculatorError("Equation needs both a variable and an equal sign", 0)

        self.parse()
        value = float(self.rpn_eval())

        # Return an integer type if the answer is an integer
        if int(value) == value:
            return int(value)

        # If Python made some silly precision error like x.99999999999996, just return x+1 as an integer
        epsilon = 0.0000000001
        if int(value + epsilon) != int(value):
            return int(value + epsilon)
        if int(value - epsilon) != int(value):
            return int(value)
        return value
