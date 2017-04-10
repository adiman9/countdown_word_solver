#!/usr/bin/env python

numbers = [50,75,8,5,4,1]
target = 937

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

    def check_order(self, target):
        total = 0
        skip = 0
        next_op = '+'
        for i, op in enumerate(self.operations):
            # skip = skip - 1
            # if(op.op == ')' or skip > 0):
            #     continue
            # if(op.op == '('):
            #     for y, ops in enumerate(self.operations[i:]):
            #         if(ops.op == ')'):
            #             print('herere')
            #             print(self.operations, i)
            #             parsed = self.parse_brackets(self.operations[i+1:y+1])
            #             total = OPS[next_op](total, parsed[0])
            #             next_op = parsed[1]
            #             ops.num = next_op
            #             skip = y + 1
            #     continue
            # if (next_op == '-' or next_op == '/') and op.num > total:
            #     self.operations = self.swap(i)
            #     return self.check_order(target)
            total = OPS[next_op](total, op.num)
            next_op = op.op
        assert total == target

    # def parse_brackets(self, list):
    #     total = list[0].num
    #     for i in range(1, len(list)):
    #         print(list[i])
    #         total = OPS[list[i-1].op](total, list[i].num)

    #     op = list[-1].op
    #     list[-1].op = ''

    #     return [total, op]

    # def swap(self, index):
    #     list_copy = self.operations[:]
    #     temp_op = self.operations[index].op
    #     self.operations[index].op = self.operations[index-1].op
    #     self.operations[index-1].op = temp_op

    #     start = self.operations[index:index+1]
    #     to_move = self.operations[:index]
    #     to_move.insert(0, CalcOperation(None, '('))
    #     to_move.insert(len(to_move), CalcOperation(None, ')'))
    #     end = self.operations[index+1:]
    #     start.extend(to_move)
    #     start.extend(end)
    #     return start

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
        # self.numbers = sorted(numbers)
        self.numbers = sorted(numbers, reverse=True)
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
                                operations.check_order(self.target)
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
