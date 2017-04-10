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

class NumberSolution(object):
    def __init__(self, operations, result, target):
        self.operations = operations
        self.result = result
        self.target = target

    def __repr__(self):
        if(self.result - self.target == 0):
            return 'Found A Solution'

        return 'Only managed to find a result of {result}, this is an error of {error}'.format(result=self.result, error=abs(self.target - self.result))

def solve(numbers, target, best=0, operations=None, used=None):

    if not operations:
        operations = []
    if not used:
        used = [False for num in numbers]

    numbers.sort()

    for i, val in enumerate(numbers):
        if used[i]:
            continue

        for j in range(i+1, len(numbers)):
            if used[j]:
                continue

            jval = numbers[j]

            combo = [val, jval]
            combo.sort(reverse=True)

            for op, fn in OPS.items():

                result = fn(combo[0], combo[1])

                if find_abs_diff(result, target) < find_abs_diff(best, target):
                    best = result

                    if best == target:
                        return NumberSolution(operations, best, target)
                    else:
                        used[i] = True
                        used[j] = True

    return NumberSolution(operations, best, target)


def find_abs_diff(x, y):
    return abs(x - y)

solution = solve(numbers, target)
print(solution)


