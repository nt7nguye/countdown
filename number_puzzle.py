from random import shuffle, randint
from typing import List

class Expr:
    def __init__(self, value: int=0, target: int=0, lhs: 'Expr'=None, rhs:'Expr'=None, op: str=''):
        self.value = value
        self.target = target
        self.lhs = lhs
        self.rhs = rhs
        self.op = op
        self.str = str(self)

    def __str__(self):
        if self.op != '':
            expr_str = "{} {} {}".format(self.lhs.str, self.op, self.rhs.str)
            if self.op in ['+', '-']:
                return "({})".format(expr_str)
            return expr_str
        else:
            return str(self.value)

    def __repr__(self):
        return self.str
    
    def __lt__(self, other: 'Expr'):
        if abs(self.value - self.target) != abs(other.value - self.target):
            return abs(self.value - self.target) < abs(other.value - self.target)
        
        return len(self.str) < len(other.str)

class NumberPuzzle: 
    def __init__(self, 
                target: int = randint(100, 999),
                numBigOnes: int = 4,
                totalNums: int = 6,
                acceptibleDiff: int = 10,
                bigOnes: List[int] = [25, 50, 75, 100], 
                smallOnes: List[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9] * 2):
        self.target = target
        self.acceptableDiff = acceptibleDiff
        self.numList = []
        self.solutions = []
        self.memoized = set()
        self.solutionCount = 100
        self.exprEvaluated = 0

        shuffle(smallOnes)
        shuffle(bigOnes)

        for i in range(numBigOnes):
            self.numList.append(bigOnes[i])

        for i in range(totalNums - numBigOnes):
            self.numList.append(smallOnes[i])     
        
        self.numList.sort(reverse=True)

    def addMemoized(self, exprList: List[Expr]):
        memoized_str = ",".join([str(expr.value) for expr in exprList])
        if memoized_str in self.memoized:
            return False
        self.memoized.add(memoized_str)
        return True

    def solveRecursive(self, exprList: List[Expr]):
        self.exprEvaluated += 1
        n = len(exprList)
        for i in range(n - 1):
            for j in range(i + 1, n):
                for op in ['+', '-', '*', '/']:
                    expr = Expr(target=self.target, lhs=exprList[i], rhs=exprList[j], op=op)
                    if op == '+':
                        expr.value = expr.lhs.value + expr.rhs.value
                    elif op == '-':
                        expr.value = expr.lhs.value - expr.rhs.value
                    elif op == '*':
                        expr.value = expr.lhs.value * expr.rhs.value
                    elif op == '/':
                        if expr.rhs.value == 0:
                            continue
                        if expr.lhs.value % expr.rhs.value != 0:
                            continue
                        expr.value = expr.lhs.value / expr.rhs.value
                        
                    if abs(expr.value - self.target) <= self.acceptableDiff:
                        self.solutions.append(expr)

                    if n > 2:
                        exprListCopy = []
                        currAdded = False
                        for k in range(n):
                            if k != i and k != j:
                                if exprList[k].value < expr.value and not currAdded:
                                    exprListCopy.append(expr)
                                    currAdded = True
                                exprListCopy.append(exprList[k])
                        if not currAdded:
                            exprListCopy.append(expr)
                        if self.addMemoized(exprListCopy):
                            self.solveRecursive(exprListCopy)
    
    def solve(self, solutionCount:int = 10):
        exprList = [Expr(value=num, target=self.target) for num in self.numList]
        for expr in exprList:
            if expr.value == self.target:
                self.solutions.append(expr)
        self.solveRecursive(exprList)
        self.solutions.sort()
        i = 1
        while i < len(self.solutions):
            if self.solutions[i].str == self.solutions[i - 1].str:
                del self.solutions[i]
            else:
                i += 1
        return self.solutions[:solutionCount]