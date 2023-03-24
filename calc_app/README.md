# Simple scientific calculator

## Running the application

Application runs in a docker container on any platform supported by Docker. The following commands are for installation on a Linux machine.

Checkout the source code:
```
$ git clone git@git.toptal.com:Luis-Filipe/felix-enescu.git
$ cd felix-enescu
```

Build the application container:
```
$ docker docker build -t calculator .
```

Start application container, mapping application to port 8080 of the host machine:
```
$ docker run -d -p 8080:5000 calculator
```
Note the `container id` for future reference


## Overview:

The calculator has the following features:

- supports addition, subtraction, multiplication, division, exponentiation, square root, log, sin and cos on floating point numbers
- solve simple linear equations with a single variable (namely, x), only addition, subtraction and multiplication operations are allowed
- supports parentheses in both modes
- have a language parser
- uses only base modules, do not use any library that can accomplish any of the listed requirements
- handles all error cases properly (by carefully indicating the errors to the user)

### Examples:

input: `(3+(4-1))*5`
output: `30`

input: `2 * x + 0.5 = 1`
output: `x = 0.25`

input: `2*x + 1 = 2*(1-x)`
output: `x = 0.25`

