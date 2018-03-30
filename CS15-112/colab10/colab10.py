# Zhuqing Yang (zhuqingy) Section E #############
# Colab10
# Partner: Shuyuan Ding (shuyuand)###############

import os

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

def areLegalValues(values):
    if len(values)**0.5-int(len(values)**0.5)!=0 or len(values)==0:
        return False
    for i in range(len(values)):
        if values[i]!=0 and values.count(values[i])>1:
            return False
        elif int(values[i]) > len(values):
            return False
    return True

def isLegalRow(board, row):
    if row >= len(board):
        return False
    rowValues = board[row]
    return areLegalValues(rowValues)

def isLegalCol(board, col):
    if col >= len(board):
        return False
    colValues = []
    for row in range(len(board)):
        colValues.append(board[row][col])
    return areLegalValues(colValues)

def isLegalBlock(board, block):
    if block >= len(board):
        return False
    bloValues = []
    singleBlo = []
    n = int(len(board)**0.5)
    for row in range(int(block-(block+n)%n),int(block-(block+n)%n+n)):
        bloValues.append(board[row][n*(block%n):n*(block%n)+n])
    for i in range(len(bloValues)):
        singleBlo += bloValues[i] 
    return areLegalValues(singleBlo)

def isLegalSudoku(board):
    if len(board) == 0:
        return False
    for i in range(len(board)):
        if isLegalRow(board,i)!=True:
            return False
        if isLegalCol(board,i)!=True:
            return False
        if isLegalBlock(board,i)!=True:
            return False
    return True

#################################################
# Colab10 problems
########################

def evalAns(lst,sym):
    if sym == "+":
        return lst[0]+lst[1]
    elif sym == "-":
        return lst[0]-lst[1]
    elif sym == "*":
        return lst[0]*lst[1]
    elif sym == "/":
        return lst[0]/lst[1]

def evalPrefixNotation(lst):
    if not isinstance(lst [0], int):
        sym = lst.pop(0)
        return evalAns([evalPrefixNotation(lst),evalPrefixNotation(lst)], sym)
    else:
        return lst.pop(0)

def getLargestFile(path):
    if os.path.isdir(path):
        contents = os.listdir(path)
        if contents:
            max = ('',0)
            for name in contents:
                if 'DS' in name:
                    pass
                else:
                    temp = getLargestFile(path+'/'+name)
                    if temp[1] >= max[1]:
                        max = temp
            return max
        else:
            return ('',0)
    else:
        return (path,os.path.getsize(path))

def findLargestFile(path):
    ans = getLargestFile(path)
    return ans[0]


from itertools import product


def solveSudoku(grid):
    boxR, boxC = 3, 3
    board_size = boxR * boxC
    X = ([("rc", rc) for rc in product(range(board_size), range(board_size))] +
         [("rn", rn) for rn in product(range(board_size), range(1, board_size + 1))] +
         [("cn", cn) for cn in product(range(board_size), range(1, board_size + 1))] +
         [("bn", bn) for bn in product(range(board_size), range(1, board_size + 1))])
    Y = dict()
    for r, c, n in product(range(board_size), range(board_size), range(1, board_size + 1)):
        b = (r // boxR) * boxR + (c // boxC)  # Box number
        Y[(r, c, n)] = [
            ("rc", (r, c)),
            ("rn", (r, n)),
            ("cn", (c, n)),
            ("bn", (b, n))]
    X, Y = exact_cover(X, Y)
    for i, row in enumerate(grid):
        for j, n in enumerate(row):
            if n:
                select(X, Y, (i, j, n))
    for solution in solve(X, Y, []):
        for (r, c, n) in solution:
            grid[r][c] = n
    return grid


def exact_cover(X, Y):
    X = {j: set() for j in X}
    for i, row in Y.items():
        for j in row:
            X[j].add(i)
    return X, Y


def solve(X, Y, solution):
    if not X:
        yield list(solution)
    else:
        c = min(X, key=lambda c: len(X[c]))
        for r in list(X[c]):
            solution.append(r)
            cols = select(X, Y, r)
            for s in solve(X, Y, solution):
                yield s
            deselect(X, Y, r, cols)
            solution.pop()


def select(X, Y, r):
    cols = []
    for j in Y[r]:
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].remove(i)
        cols.append(X.pop(j))
    return cols


def deselect(X, Y, r, cols):
    for j in reversed(Y[r]):
        X[j] = cols.pop()
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].add(i)
    
#################################################
# Colab10 Test Functions
#################################################    

def testEvalPrefixNotation():
    print("Testing evalPrefixNotation()...", end="")
    assert(evalPrefixNotation(['+',2,3]) == 5)
    assert(evalPrefixNotation(['+','*',2,3,'*',4,5]) == 26)
    assert(evalPrefixNotation(['*','+',2,'*',3,'-',8,7,'+','*',2,2,5]) == 45)
    print("Passed!")

def testFindLargestFile():
    print("Testing findLargestFile()...", end="")
    assert(findLargestFile("sampleFiles/folderA") == \
    "sampleFiles/folderA/folderC/giftwrap.txt")
    assert(findLargestFile("sampleFiles/folderB") == \
    "sampleFiles/folderB/folderH/driving.txt")
    assert(findLargestFile("sampleFiles/folderB/folderF") == "")
    print("Passed!")
def testSolveSudoku():
    print('Testing solveSudoku()...', end='')
    board1 = [
              [ 5, 3, 0, 0, 7, 0, 0, 0, 0 ],
              [ 6, 0, 0, 1, 9, 5, 0, 0, 0 ],
              [ 0, 9, 8, 0, 0, 0, 0, 6, 0 ],
              [ 8, 0, 0, 0, 6, 0, 0, 0, 3 ],
              [ 4, 0, 0, 8, 0, 3, 0, 0, 1 ],
              [ 7, 0, 0, 0, 2, 0, 0, 0, 6 ],
              [ 0, 6, 0, 0, 0, 0, 2, 8, 0 ],
              [ 0, 0, 0, 4, 1, 9, 0, 0, 5 ],
              [ 0, 0, 0, 0, 8, 0, 0, 7, 9 ]
            ]
    solved1 = solveSudoku(board1)
    solution1 = [
                [5, 3, 4, 6, 7, 8, 9, 1, 2], 
                [6, 7, 2, 1, 9, 5, 3, 4, 8], 
                [1, 9, 8, 3, 4, 2, 5, 6, 7], 
                [8, 5, 9, 7, 6, 1, 4, 2, 3], 
                [4, 2, 6, 8, 5, 3, 7, 9, 1], 
                [7, 1, 3, 9, 2, 4, 8, 5, 6], 
                [9, 6, 1, 5, 3, 7, 2, 8, 4], 
                [2, 8, 7, 4, 1, 9, 6, 3, 5], 
                [3, 4, 5, 2, 8, 6, 1, 7, 9]
               ]
    assert(solved1 == solution1)
    board2 = [
             [ 1, 2, 3, 4, 5, 6, 7, 8, 9],
             [ 5, 0, 8, 1, 3, 9, 6, 2, 4],
             [ 4, 9, 6, 8, 7, 2, 1, 5, 3],
             [ 9, 5, 2, 3, 8, 1, 4, 6, 7],
             [ 6, 4, 1, 2, 9, 7, 8, 3, 5],
             [ 3, 8, 7, 5, 6, 4, 0, 9, 1],
             [ 7, 1, 9, 6, 2, 3, 5, 4, 8],
             [ 8, 6, 4, 9, 1, 5, 3, 7, 2],
             [ 2, 3, 5, 7, 4, 8, 9, 1, 6]
            ]
    solved2 = solveSudoku(board2)
    solution2 = [
                [1, 2, 3, 4, 5, 6, 7, 8, 9],
                [5, 7, 8, 1, 3, 9, 6, 2, 4],
                [4, 9, 6, 8, 7, 2, 1, 5, 3],
                [9, 5, 2, 3, 8, 1, 4, 6, 7],
                [6, 4, 1, 2, 9, 7, 8, 3, 5],
                [3, 8, 7, 5, 6, 4, 2, 9, 1],
                [7, 1, 9, 6, 2, 3, 5, 4, 8],
                [8, 6, 4, 9, 1, 5, 3, 7, 2],
                [2, 3, 5, 7, 4, 8, 9, 1, 6],
                ]
    assert(solved2 == solution2)
    print('Passed!')

#################################################
# Colab10 Main
#################################################

def testAll():
    testSolveSudoku()

def main():
    testAll()

if __name__ == '__main__':
    main()