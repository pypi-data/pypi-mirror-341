# operations.py

def add(a, b):
    return a + b

def average(a, b):
    return (a + b) / 2

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b != 0:
        return a / b
    else:
        return "Cannot divide by zero"
