#!/usr/bin/env python

"""
Usage:
    numbers_solver <numbers> <target>
"""
import sys
from docopt import docopt

OPS = {
    'x': lambda x,y: x*y,
    '/': lambda x,y: x/y,
    '+': lambda x,y: x+y,
    '-': lambda x,y: x-y
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
        if self.op == '(' or self.op == ')':
            if self.num:
                return str(self.op + ' ' + str(self.num) + ' ')
            else:
                return str(self.op + ' ')
        return '{num} {op} '.format(num=self.num, op=self.op)

    def __str__(self):
        return self.__repr__()

class OperationList(object):
    def __init__(self, size):
        self.size = size
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
                self.update_op(i, op='')
                self.operations = self.operations[:i+1]
                break

    def trim_copy(self):
        new_op = OperationList(self.size)

        for i,op in enumerate(self.operations):
            new_op.insert(op, i)

        new_op.trim()

        print(new_op)

        return new_op

    def check_order(self, target):
        total = 0
        skip = 0
        next_op = '+'
        for i, op in enumerate(self.operations):
            if op and next_op:
                total = OPS[next_op](total, op.num)
                next_op = op.op
        return total == target

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
            print('\nFound A Solution\n')
        else:
            print('Only managed to find a result of {result}, this is an error of {error}\n'.format(result=self.result, error=abs(self.target - self.result)))

        return self.operations.__repr__()

class NumberGameSolver(object):
    def __init__(self, numbers, target):
        self.numbers = sorted(numbers, reverse=True)
        self.target = target
        self.best = 0
        self.solution = None
        self.solutions = []

        self._solve()
        # print(self.solution)

    def __repr__(self):
        text = ''
        for sol in self.solutions:
            text += sol.__repr__() + '\n'
        return text
        # return self.solution.__repr__()

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

                    if result > 0 and find_abs_diff(result, self.target) <= find_abs_diff(self.best, self.target):
                        if type(result) is int or type(result) is float:

                            if operations.check_order(self.target):
                                self.best = result
                                self.solution = NumberSolution(operations.trim_copy(), self.best, self.target)

                                if self.best == self.target:
                                    self.solutions.append(NumberSolution(operations.trim_copy(), self.best, self.target))
                                    # operations.trim()

                    self._solve(
                                operations,
                                [True if used[j] or j == i else False for (j, num) in enumerate(self.numbers)],
                                result,
                                level+1)

            else:
                operations.insert(CalcOperation(val), level)
                self._solve(
                            operations,
                            [True if used[j] or j == i else False for (j, num) in enumerate(self.numbers)],
                            val,
                            level+1)


if '__main__' == __name__:
    args = docopt(__doc__, argv=sys.argv[1:])

    if ',' in args['<numbers>']:
        numbers = [int(num) for num in args['<numbers>'].split(',')]
    else:
        numbers = [int(num) for num in args['<numbers>'].split(' ')]

    solution = NumberGameSolver(numbers, int(args['<target>']))

