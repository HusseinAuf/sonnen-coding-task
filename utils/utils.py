import math

def is_equal(a, b, tol=1e-6):
    return math.isclose(a, b, abs_tol=tol)

def less_than(a, b, tol=1e-6):
    return a < b - tol

def less_equal(a, b, tol=1e-6):
    return a <= b + tol

def greater_than(a, b, tol=1e-6):
    return a > b + tol

def greater_equal(a, b, tol=1e-6):
    return a >= b - tol