# -*- coding: utf-8 -*-

from __future__ import print_function

import nose
from nose.tools import raises

import calculator as Calc

# test Calculator Error exception class

def test_calculator_error():
    calc_err = Calc.CalculatorError("some message", 12)

    assert calc_err.message == "some message"
    assert calc_err.position == 12
    assert "%s" % calc_err == "some message at position 12"

