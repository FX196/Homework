# Zhuqing Yang (zhuqingy) Section E #############
# Hw5
#################################################

import math
import string
import copy

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

#################################################
# Hw5 problems
#################################################

from tkinter import *

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

def init(data):
    # load data.xyz as appropriate
    #data.board = starterBoard()
    data.rows = 9
    data.cols = 9
    data.margin = 10
    data.side = (data.width-2*data.margin)/9
    data.selection = (-1, -1)
    data.board = starterBoard()
    data.tempBoard = copy.deepcopy(data.board)
    

def starterBoard():
    board = [
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
    return board
    

def pointInGrid(x, y, data):
    # return True if (x, y) is inside the grid defined by data.
    return ((data.margin <= x <= data.width-data.margin) and
            (data.margin <= y <= data.height-data.margin))

def drawBoard(canvas,data):
    tempBoard = copy.deepcopy(data.board)
    for row in range(data.rows):
        for col in range(data.cols):
            if data.selection == (row,col) and data.board[row][col]==0:
                fill="peach puff"
            elif data.selection==(row,col) and data.board[row][col]!=0:
                fill="salmon"
            elif data.board[row][col]!=0:
                fill="misty rose"
            else:
                fill="white"
            canvas.create_rectangle(data.margin+col*data.side,
            data.margin+row*data.side,data.margin+(col+1)*data.side,
            data.margin+(row+1)*data.side,fill=fill,width=2)
    for row in range(data.rows):
        for col in range(data.cols):
            if data.tempBoard[row][col] != 0:# and isLegalSudoku(data.tempBoard):
                canvas.create_text(data.margin+(col+1)*(data.side)-  
                data.side/2,data.margin+(row+1)*(data.side)-data.side/2,text = 
                data.tempBoard[row][col],font="bold 28")

def checkAndReturn(canvas,data):
    count = 0
    for row in range(data.rows):
        for col in range(data.cols):
            if data.tempBoard[row][col] == 0:
                count += 1
    #congHeight = data.side * 2
    if count == 0:
        canvas.create_rectangle(0,data.height/2-data.side,
        data.width,data.height/2+data.side,fill="rosy brown",width=0)
        canvas.create_text(data.width/2,data.height/2,text="恭喜，你赢了！",
        fill="red",font="Times 40 bold")

def getCell(x, y, data):
    # aka "viewToModel"
    # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
    if (not pointInGrid(x, y, data)):
        return (-1, -1)
    row = (y - data.margin) // data.side
    col = (x - data.margin) // data.side
    # triple-check that we are in bounds
    row = min(data.rows-1, max(0, row))
    col = min(data.cols-1, max(0, col))
    return (row, col)


def mousePressed(event, data):
    (row, col) = getCell(event.x, event.y, data)
    # select this (row, col) unless it is selected
    if (row,col) == (-1,-1):
        pass
    else:
        data.selection = (row, col)

def keyPressed(event, data):
    (row, col) = data.selection
    if event.keysym == "Up":
        data.selection = ((row-1)%data.rows, col)
    elif event.keysym == "Down":
        data.selection = ((row+1)%data.rows,col)
    elif event.keysym == "Left":
        data.selection = (row,(col-1)%data.cols)
    elif event.keysym == "Right":
        data.selection = (row,(col+1)%data.cols)

    elif data.tempBoard[int(row)][int(col)] == 0 and event.char in string.digits:
        num = event.char
        data.tempBoard[int(row)][int(col)] = int(num)
        if isLegalSudoku(data.tempBoard)!=True:
            data.tempBoard[int(row)][int(col)] = 0
    elif event.keysym == "BackSpace":
        if data.tempBoard[int(row)][int(col)]!=0 and \
        data.board[int(row)][int(col)]==0:
            data.tempBoard[int(row)][int(col)] = 0
        

def redrawAll(canvas, data):
    drawBoard(canvas,data)
    for row in range(data.rows//3):
        for col in range(data.cols//3):
            canvas.create_rectangle(data.margin+col*3*data.side,
            data.margin+row*3*data.side,data.margin+(col+1)*3*data.side,
            data.margin+(row+1)*3*data.side,width=5)
    checkAndReturn(canvas,data)
    
def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    redrawAll(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")
run(630,630)





#################################################
# Hw5 Main
#################################################

'''def testAll():
    

def main():
    testAll()

if __name__ == '__main__':
    main()'''
