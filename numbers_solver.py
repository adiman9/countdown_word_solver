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

OPS = [
    {
        'op': 'x',
        'fn': mult
    },
    {
        'op': '/',
        'fn': divide
    },
    {
        'op': '+',
        'fn': add
    },
    {
        'op': '-',
        'fn': sub
    }
]

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

def solve(numbers, target, best=0, operations=None, used=[False for num in numbers], current=0, level=0):

    if not operations:
        operations = []

    used = [True if used[i] else False for (i, num) in enumerate(numbers)]
    # print(used)

    numbers.sort()

    for i, val in enumerate(numbers):
        if used[i]:
            continue

        if current > 0:
            # print('GO CURRENT', current)
            for op in OPS:

                combo = sorted([current, val], reverse=True)
                result = op['fn'](combo[0], combo[1])
                # print(combo[0], op['op'], combo[1], ' = ', result)
                # print(level)

                if find_abs_diff(result, target) < find_abs_diff(best, target):
                    # print('NEW BEST')
                    best = result

                    if best == target:
                        return NumberSolution(operations, best, target)

                used[i] = True
                solve(numbers, target, best, operations, used, result, level+1)
        else:
            # print('NO CURRENT')
            used[i] = True
            solve(numbers, target, best, operations, used, val, level+1)

def find_abs_diff(x, y):
    return abs(x - y)

solution = solve(numbers, target)
print(solution)


