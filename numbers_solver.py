#!/usr/bin/env python

numbers = [25, 7, 9, 3, 1, 8]
target = 642
# target = 225

def mult(x, y):
    return x * y

def divide(x, y):
    if(x > y):
        return x / y
    else:
        return y / x

def add(x, y):
    return x + y

def sub(x, y):
    if(x > y):
        return x - y
    else:
        return y - x

OPS = {
    'x': mult,
    '/': divide,
    '+': add,
    '-': sub,
}

class NumOperation(object):
    def __init__(self, num, op=None):
        """
        The op arg is the operation that should be applied to the next
        value in the chain
        """
        self.num = num
        self.op = op
        self.next = None

def solve(numbers, target, best=0, operations=None, used=None):

    if not operations:
        operations = []
    if not used:
        used = [False for num in numbers]

    numbers.sort()

    for i, val in enumerate(numbers):
        if used[i]:
            continue
        used[i] = True

        for j in range(i+1, len(numbers)):
            if used[j]:
                print('USED', j)
                continue
            used[j] = True

            jval = numbers[j]

            for op, fn in OPS.items():

                result = fn(val, jval)

                if find_abs_diff(result, target) < find_abs_diff(best, target):
                    best = result

                    if best == target:
                        return operations

def find_abs_diff(x, y):
    return abs(x - y)

solution = solve(numbers, target)
print(solution)


