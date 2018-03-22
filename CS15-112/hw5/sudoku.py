# Zhuqing Yang (zhuqingy) Section E #############
# Hw5
#################################################


#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10 ** -7):
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


####################################
# customize these functions
####################################

def init(data):
    # load data.xyz as appropriate
    # data.board = starterBoard()
    data.rows = 9
    data.cols = 9
    data.side = data.width / 9
    data.margin = 5
    data.selection = (-1, -1)
    # data.board = starterBoard()


# def starterBoard():


def pointInGrid(x, y, data):
    # return True if (x, y) is inside the grid defined by data.
    return ((data.margin <= x <= data.width - data.margin) and
            (data.margin <= y <= data.height - data.margin))


def drawBoard(canvas, data):
    for row in range(data.rows):
        for col in range(data.cols):
            (x0, y0, x1, y1) = getCellBounds(row, col, data)
            fill = "white" if (data.selection == (row, col)) else "pink"
            canvas.create_rectangle(x0, y0, x1, y1, fill=fill)


def getCell(x, y, data):
    # aka "viewToModel"
    # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
    if (not pointInGrid(x, y, data)):
        return (-1, -1)
    boardWidth = data.width - 2 * data.margin
    boardHeight = data.height - 2 * data.margin
    cellWidth = boardWidth / data.cols
    cellHeight = boardHeight / data.rows
    row = (y - data.margin) // cellHeight
    col = (x - data.margin) // cellWidth
    # triple-check that we are in bounds
    row = min(data.rows - 1, max(0, row))
    col = min(data.cols - 1, max(0, col))
    return (row, col)


def getCellBounds(row, col, data):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    boardWidth = data.width - 2 * data.margin
    boardHeight = data.height - 2 * data.margin
    sideWidth = boardWidth / data.cols
    sideHeight = boardHeight / data.rows
    x0 = data.margin + col * sideWidth
    x1 = data.margin + (col + 1) * sideWidth
    y0 = data.margin + row * sideHeight
    y1 = data.margin + (row + 1) * sideHeight
    return (x0, y0, x1, y1)


def mousePressed(event, data):
    (row, col) = getCell(event.x, event.y, data)
    # select this (row, col) unless it is selected
    if (data.selection == (row, col)):
        data.selection = (-1, -1)
    else:
        data.selection = (row, col)


def keyPressed(event, data):
    (row, col) = getCell(event.x, event.y, data)
    # use event.char and event.keysym
    if event.keysym == "Up":
        data.selection = (row, col)
    elif event.keysym == "Down":
        data.selection = (row - 1, col)
    elif event.keysym == "Left":
        data.selection = (row, col - 1)
    elif event.keysym == "Right":
        data.selection = (row, col + 1)


def redrawAll(canvas, data):
    drawBoard(canvas, data)


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


run(630, 630)


### Your lab5 functions below ###

def areLegalValues(a):
    if len(values) ** 0.5 - int(len(values) ** 0.5) != 0 or len(values) == 0:
        return False
    for i in range(len(values)):
        if values[i] != 0 and values.count(values[i]) > 1:
            return False
        elif values[i] > len(values):
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
    n = int(len(board) ** 0.5)
    for row in range(int(block - (block + n) % n), int(block - (block + n) % n + n)):
        bloValues.append(board[row][n * (block % n):n * (block % n) + n])
    for i in range(len(bloValues)):
        singleBlo += bloValues[i]
    return areLegalValues(singleBlo)


def isLegalSudoku(board):
    if len(board) == 0:
        return False
    for i in range(len(board)):
        if isLegalRow(board, i) != True:
            return False
        if isLegalCol(board, i) != True:
            return False
        if isLegalBlock(board, i) != True:
            return False
    return True
