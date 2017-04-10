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

def find_abs_diff(x, y):
    return abs(x - y)

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

class NumberGameSolver(object):
    def __init__(self, numbers, target):
        self.numbers = sorted(numbers)
        self.target = target
        self.best = 0

        self.solution = self._solve()
        print(self.solution)

    def __repr__(self):
        return self.solution.__repr__()

    def _solve(self, operations=[], used=[], current=0, level=0):
        if not used:
            used = [False for num in self.numbers]

        for i, val in enumerate(self.numbers):
            if used[i]:
                continue

            if current > 0:
                for op in OPS:

                    combo = sorted([current, val], reverse=True)
                    result = op['fn'](combo[0], combo[1])

                    has_solution = self._solve(
                                                operations,
                                                [True if used[j] or j == i else False for (j, num) in enumerate(self.numbers)],
                                                result,
                                                level+1)
                    if has_solution:
                        return has_solution

                    if find_abs_diff(result, self.target) < find_abs_diff(self.best, self.target):
                        if type(result) is int:
                            self.best = result
                            # print('NEW BEST')
                            # print(self.best)

                            if self.best == self.target:
                                self.solution = NumberSolution(operations, self.best, self.target)
                                return self.solution

            else:
                has_solution = self._solve(
                            operations,
                            [True if used[j] or j == i else False for (j, num) in enumerate(self.numbers)],
                            val,
                            level+1)

                if has_solution:
                    return has_solution


solution = NumberGameSolver(numbers, target)
