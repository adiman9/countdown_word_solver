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
    '-': sub
}

def find_abs_diff(x, y):
    return abs(x - y)

class CalcOperation(object):
    def __init__(self, num, op=None):
        """
        The op arg is the operation that should be applied to the next
        value in the chain
        """
        self.num = num
        self.op = op
        self.next = None

    def update(self, op=None, next=None, num=None):
        if(num is not None):
            self.num = num
        if(op is not None):
            self.op = op
        if(next is not None):
            self.next = next

    def __repr__(self):
        return '{num} {op} '.format(num=self.num, op=self.op)

    def __str__(self):
        return self.__repr__()

class OperationList(object):
    def __init__(self, size):
        self.operations = [None for val in range(size)]

    def insert(self, operation, index):
        self.operations[index] = operation

    def get(self, index):
        return self.operations[index]

    def all(self):
        return self.operations

    def trim(self):
        for i, op in enumerate(self.operations):
            if op.op is None:
                self.operations = self.operations[:-1]
                self.update_op(i, op='')
                break

    def update_op(self, index, op=None, next=None, num=None):
        self.operations[index].update(op=op, next=next, num=num)

    def __repr__(self):
        text = ''
        for op in self.operations:
            text += str(op)

        return text

class NumberSolution(object):
    def __init__(self, operations, result, target):
        self.operations = operations
        self.result = result
        self.target = target

    def __repr__(self):
        if(self.result - self.target == 0):
            print('Found A Solution\n')
        else:
            print('Only managed to find a result of {result}, this is an error of {error}\n'.format(result=self.result, error=abs(self.target - self.result)))

        return self.operations.__repr__()

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
        if not operations:
            operations = OperationList(len(self.numbers))

        for i, val in enumerate(self.numbers):
            if used[i]:
                continue

            if current > 0:
                for op, fn in OPS.items():

                    combo = sorted([current, val], reverse=True)
                    result = fn(combo[0], combo[1])

                    operations.insert(CalcOperation(val), level)
                    operations.update_op(level - 1, op=op, next=operations.get(level))

                    if find_abs_diff(result, self.target) < find_abs_diff(self.best, self.target):
                        if type(result) is int:
                            self.best = result

                            self.solution = NumberSolution(operations, self.best, self.target)

                            if self.best == self.target:
                                operations.trim()
                                return self.solution

                    has_solution = self._solve(
                                                operations,
                                                [True if used[j] or j == i else False for (j, num) in enumerate(self.numbers)],
                                                result,
                                                level+1)
                    if has_solution:
                        return has_solution

            else:
                operations.insert(CalcOperation(val), level)
                has_solution = self._solve(
                            operations,
                            [True if used[j] or j == i else False for (j, num) in enumerate(self.numbers)],
                            val,
                            level+1)

                if has_solution:
                    return has_solution


solution = NumberGameSolver(numbers, target)
