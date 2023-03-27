# -*- coding: utf-8 -*-

"""Minimal web interface for scientific calculator

    AngulrJS with Flask
"""

from __future__ import print_function

import json
from flask import Flask, request, render_template

import calculator as Calc


application = Flask(__name__)


@application.route('/')
def calculator():
    """Main route
    """
    return render_template('calculator.html')


# compute expression
@application.route('/calculate', methods=['POST'])
def calculate():
    """Calculate an expression and return result ready to display
    """
    rq_data = json.loads(request.data)
    print("rq data %s" % rq_data)
    calc = Calc.Calculator(rq_data["expression"])
    rez = {}
    try:
        value = calc.solve()
        if calc.is_equation:
            value = "x = %s" % value
        rez = {
            "status": "OK!",
            "value": value,
            "is_equation": calc.is_equation
        }
    except Calc.CalculatorError as error:
        if error.position:
            message = "%s at position %s" % (error.message, error.position)
        else:
            message = error.message
        rez = {
            "status": "ERROR!",
            "message": message,
            "position": error.position
        }

    rez["expression"] = rq_data["expression"]
    return json.dumps(rez)


if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=False)
