# -*- coding: utf-8 -*-

from __future__ import print_function

import nose
from nose.tools import raises

import calculator as Calc

# test Calculator class

def test_calculator_init_none():
    solver = Calc.Calculator("s")
    assert solver.string == "s"


def test_calculator_bad():
    bad_expr_list = [
        ("", "Empty expression"),
        ("()", "Unexpected token: ')'"),
        ("-", "Unexpected end of expression after '-u'"),
        ("*", "Unexpected token: '*'"),
        ("2--", "Unexpected token: '-'"),
        ("2**", "Unexpected token: '*'"),
        ("2+sin", "Unexpected end of expression after '+'"),
        ("2+sin(", "There are mismatched parentheses"),
        ("2+sin)", "Unexpected token: ')'"),
        ("2+2=", "Equation needs both a variable and an equal sign"),
        ("2+x=", "Equation needs value after equal"),
        ("2+x=()", "Unexpected token: ')'"),
        ("2+sin^", "Unexpected token: '^'"),
        ("2+sin(^", "Unexpected token: '^'"),
        ("2+sin(x)", "Equation needs both a variable and an equal sign"),
        ("2+sin(x)=0", "Function 'sin' applied to variable is not supported"),
    ]

    for bad_expr in bad_expr_list:
        solver = Calc.Calculator(bad_expr[0])
        try:
            print("try expression: %s" % bad_expr[0])
            value = solver.solve()
            assert False
        except Calc.CalculatorError as error:
            print("tried expression: %s" % bad_expr[0])
            print("catch error %s" % error)
            assert error.message == bad_expr[1]


def test_calculator_good():
    expr_list = [
        ("(3+(4-1))*5", 30),
        ("2 * x + 0.5 = 1", 0.25),
        ("cos(5+4*3) + 2 * 3", 5.7248366619484035),
        ("-(1 + 2) * 3", -9),
        ("(1-2)/3.0 + 0.0000", -0.3333333333333333),
        ("1.0 / 3 * 6", 2),
        ("x=4/2+8*4-(5+2)/3", 31.666666666666668),
    ]

    for expr in expr_list:
        solver = Calc.Calculator(expr[0])
        value = solver.solve()
        if value != expr[1]:
            print("tried expression: %s -> %s" % (expr[0], repr(expr[1])))
            print("got result %s" % repr(value))
            assert False

