# -*- coding: utf-8 -*-

from __future__ import print_function

import nose
from nose.tools import raises

import calculator as Calc

# test Variable class

def test_variable_init_none():
    var = Calc.Variable()
    assert var.type == None


def test_variable_init_number():
    token = Calc.Token('24.67', Calc.LexType.NUMBER, Calc.LexTag.NUMBER, 12)
    var = Calc.Variable(token)
    assert var.a == 0
    assert var.b == 24.67
    assert var.type == Calc.LexType.NUMBER
    assert var.position == 12


def test_variable_init_variable():
    token = Calc.Token('x', Calc.LexType.VARIABLE, Calc.LexTag.VARIABLE, 12)
    var = Calc.Variable(token)
    assert var.a == 1.0
    assert var.b == 0.0
    assert var.type == Calc.LexType.VARIABLE
    assert var.position == 12


def test_variable_init_float():
    token = Calc.Token('24.67', Calc.LexType.NUMBER, Calc.LexTag.NUMBER, 12)
    var = Calc.Variable(token)
    assert float(var) == 24.67

    token = Calc.Token('x', Calc.LexType.VARIABLE, Calc.LexTag.VARIABLE, 12)
    var = Calc.Variable(token)
    var.a = 2
    var.b = 1
    assert float(var) == -0.5


def test_variable_init_neg():
    token = Calc.Token('24.67', Calc.LexType.NUMBER, Calc.LexTag.NUMBER, 12)
    var = Calc.Variable(token)
    var = -var
    assert var.a == 0
    assert var.b == -24.67

    token = Calc.Token('x', Calc.LexType.VARIABLE, Calc.LexTag.VARIABLE, 12)
    var = Calc.Variable(token)
    var.a = 2
    var.b = 1
    var = -var
    assert var.a == -2
    assert var.b == -1


def test_variable_init_add():
    token = Calc.Token('24.67', Calc.LexType.NUMBER, Calc.LexTag.NUMBER, 12)
    var1 = Calc.Variable(token)
    token = Calc.Token('10.12', Calc.LexType.NUMBER, Calc.LexTag.NUMBER, 12)
    var2 = Calc.Variable(token)
    var3 = var1+var2
    assert var3.a == 0
    assert var3.b == 34.79

    token = Calc.Token('x', Calc.LexType.VARIABLE, Calc.LexTag.VARIABLE, 12)
    var2 = Calc.Variable(token)
    var2.a = 2
    var2.b = 1

    var3 = var1+var2
    assert var3.a == 2
    assert var3.b == 25.67


def test_variable_init_sub():
    token = Calc.Token('25.50', Calc.LexType.NUMBER, Calc.LexTag.NUMBER, 12)
    var1 = Calc.Variable(token)
    token = Calc.Token('10.10', Calc.LexType.NUMBER, Calc.LexTag.NUMBER, 12)
    var2 = Calc.Variable(token)
    var3 = var1-var2
    assert var3.a == 0
    assert var3.b == 15.4

    token = Calc.Token('x', Calc.LexType.VARIABLE, Calc.LexTag.VARIABLE, 12)
    var2 = Calc.Variable(token)
    var2.a = 2
    var2.b = 1

    var3 = var1-var2

    assert var3.a == -2
    assert var3.b == 24.5


@raises(Calc.CalculatorError)
def test_variable_init_mul_var_var():
    token = Calc.Token('x', Calc.LexType.VARIABLE, Calc.LexTag.VARIABLE, 12)
    var1 = Calc.Variable(token)
    var1.a = 2
    var1.b = 1

    token = Calc.Token('x', Calc.LexType.VARIABLE, Calc.LexTag.VARIABLE, 12)
    var2 = Calc.Variable(token)
    var2.a = 2
    var2.b = 1

    var3 = var1 * var2


def test_variable_init_mul_num_num():
    token = Calc.Token('7', Calc.LexType.NUMBER, Calc.LexTag.NUMBER, 12)
    var1 = Calc.Variable(token)
    token = Calc.Token('3.1', Calc.LexType.NUMBER, Calc.LexTag.NUMBER, 12)
    var2 = Calc.Variable(token)
    var3 = var1*var2

    assert var3.a == 0
    assert var3.b == 21.7
    assert var3.type == Calc.LexType.NUMBER


def test_variable_init_mul_num_var():
    token = Calc.Token('7', Calc.LexType.NUMBER, Calc.LexTag.NUMBER, 12)
    var1 = Calc.Variable(token)
    token = Calc.Token('x', Calc.LexType.VARIABLE, Calc.LexTag.VARIABLE, 12)
    var2 = Calc.Variable(token)
    var2.a = 2
    var2.b = 1

    var3 = var1*var2

    assert var3.a == 14.0
    assert var3.b == 7.0
    assert var3.type == Calc.LexType.VARIABLE


def test_variable_init_mul_var_num():
    token = Calc.Token('7', Calc.LexType.NUMBER, Calc.LexTag.NUMBER, 12)
    var1 = Calc.Variable(token)
    token = Calc.Token('x', Calc.LexType.VARIABLE, Calc.LexTag.VARIABLE, 12)
    var2 = Calc.Variable(token)
    var2.a = 2
    var2.b = 1

    var3 = var2*var1

    assert var3.a == 14.0
    assert var3.b == 7.0
    assert var3.type == Calc.LexType.VARIABLE


@raises(Calc.CalculatorError)
def test_variable_init_div_x_var():
    token = Calc.Token('7', Calc.LexType.NUMBER, Calc.LexTag.NUMBER, 12)
    var1 = Calc.Variable(token)
    token = Calc.Token('x', Calc.LexType.VARIABLE, Calc.LexTag.VARIABLE, 12)
    var2 = Calc.Variable(token)
    var2.a = 2
    var2.b = 1
    var3 = var1/var2


@raises(Calc.CalculatorError)
def test_variable_init_div_x_zero():
    token = Calc.Token('7', Calc.LexType.NUMBER, Calc.LexTag.NUMBER, 12)
    var1 = Calc.Variable(token)
    token = Calc.Token('0', Calc.LexType.NUMBER, Calc.LexTag.NUMBER, 12)
    var2 = Calc.Variable(token)
    var3 = var1/var2


def test_variable_init_div_num_num():
    token = Calc.Token('18', Calc.LexType.NUMBER, Calc.LexTag.NUMBER, 12)
    var1 = Calc.Variable(token)

    token = Calc.Token('2', Calc.LexType.NUMBER, Calc.LexTag.NUMBER, 12)
    var2 = Calc.Variable(token)

    var3 = var1/var2
    print("=%s=" % repr(var3.a))

    assert var3.a == 0.0
    assert var3.b == 9.0
    assert var3.type == Calc.LexType.NUMBER


def test_variable_init_div_var_num():
    token = Calc.Token('x', Calc.LexType.VARIABLE, Calc.LexTag.VARIABLE, 12)
    var1 = Calc.Variable(token)
    var1.a = 10
    var1.b = 14

    token = Calc.Token('2', Calc.LexType.NUMBER, Calc.LexTag.NUMBER, 12)
    var2 = Calc.Variable(token)

    var3 = var1/var2
    assert var3.a == 5.0
    assert var3.b == 7.0
    assert var3.type == Calc.LexType.VARIABLE


def test_variable_init_exp_num_num():
    token = Calc.Token('2', Calc.LexType.NUMBER, Calc.LexTag.NUMBER, 12)
    var1 = Calc.Variable(token)
    token = Calc.Token('3', Calc.LexType.NUMBER, Calc.LexTag.NUMBER, 12)
    var2 = Calc.Variable(token)

    var3 = var1**var2
    assert var3.a == 0.0
    assert var3.b == 8.0
    assert var3.type == Calc.LexType.NUMBER


@raises(Calc.CalculatorError)
def test_variable_init_exp_num_var():
    token = Calc.Token('2', Calc.LexType.NUMBER, Calc.LexTag.NUMBER, 12)
    var1 = Calc.Variable(token)
    token = Calc.Token('x', Calc.LexType.VARIABLE, Calc.LexTag.VARIABLE, 12)
    var2 = Calc.Variable(token)

    var3 = var1**var2


@raises(Calc.CalculatorError)
def test_variable_init_exp_num_var():
    token = Calc.Token('2', Calc.LexType.NUMBER, Calc.LexTag.NUMBER, 12)
    var1 = Calc.Variable(token)
    token = Calc.Token('x', Calc.LexType.VARIABLE, Calc.LexTag.VARIABLE, 12)
    var2 = Calc.Variable(token)

    var3 = var2**var1
