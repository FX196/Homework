# Zhuqing Yang (zhuqingy) Section E #############
# Colab6
# Partner: Shuyuan Ding (shuyuand)###############

import random


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
# Colab6 problems
########################

from tkinter import *


def init(data, width, height):
    data.width = width
    data.height = height
    data.timerDelay = 600  # milliseconds
    data.cellSize = 20
    data.margin = 25
    data.rows = int((height - data.margin * 2) / data.cellSize)
    data.cols = int((width - data.margin * 2) / data.cellSize)
    data.emptyColor = "blue"
    data.board = getBoard(data)
    data.piecesColor = ["red", "yellow", "magenta", "pink", "cyan",
                        "green", "orange"]
    data.fallingPiece = []
    data.fallingPieceColor = ""
    data.firstFallingPiece = newFallingPiece(data)
    data.score = 0
    data.isGameOver = False


def keyPressed(event, data):
    if event.char == "r":
        data.board = getBoard(data)
        data.isGameOver = False
    if data.isGameOver == False:
        if event.keysym == "Up":
            rotateFallingPiece(data)
        elif event.keysym == "Down":
            moveFallingPiece(data, +1, 0)
        elif event.keysym == "Left":
            moveFallingPiece(data, 0, -1)
        elif event.keysym == "Right":
            moveFallingPiece(data, 0, +1)


def timerFired(data):
    if data.isGameOver == False:
        moved = moveFallingPiece(data, 1, 0)
        if not moved:
            placeFallingPiece(data)
            newFallingPiece(data)
    # moveFallingPiece(data,+1,0)


def playTeris(rows=15, cols=10):
    cellSize = 20
    margin = 25
    run((margin * 2 + cellSize * cols), (margin * 2 + cellSize * rows))


def getBoard(data):
    board = []
    for row in range(data.rows):
        board.append([])
        for col in range(data.cols):
            board[row].append(data.emptyColor)
    return board


def drawBoard(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill="orange")
    for row in range(data.rows):
        for col in range(data.cols):
            drawCell(canvas, data, row, col, data.board[row][col])


def drawCell(canvas, data, row, col, color):
    canvas.create_rectangle(data.margin + col * data.cellSize,
                            data.margin + row * data.cellSize, data.margin + (col + 1) * data.cellSize,
                            data.margin + (row + 1) * data.cellSize,
                            fill=color, width=3, outline="black")


def newFallingPiece(data):
    iPiece = [[True, True, True, True]]
    jPiece = [[True, False, False], [True, True, True]]
    lPiece = [[False, False, True], [True, True, True]]
    oPiece = [[True, True], [True, True]]
    sPiece = [[False, True, True], [True, True, False]]
    tPiece = [[False, True, False], [True, True, True]]
    zPiece = [[True, True, False], [False, True, True]]
    tetrisPieces = [iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece]
    randomInd = random.randint(0, len(tetrisPieces) - 1)
    if tetrisPieces[randomInd] == iPiece:
        fallRow, fallCol = (0, 3)
    else:
        fallRow, fallCol = (0, 4)
    data.fallingPiece = [tetrisPieces[randomInd], fallRow, fallCol]
    data.fallingPieceColor = data.piecesColor[randomInd]
    if fallingPiecesLegal(data, data.fallingPiece):
        pass
    else:
        data.isGameOver = True


def drawFallingPiece(canvas, data):
    piece = data.fallingPiece[0]
    frow = data.fallingPiece[1]
    fcol = data.fallingPiece[2]
    for row in range(len(piece)):
        for col in range(len(piece[0])):
            if piece[row][col] == True:
                drawCell(canvas, data, row + frow, col + fcol, data.fallingPieceColor)


def moveFallingPiece(data, drow, dcol):
    data.fallingPiece[1] += drow
    data.fallingPiece[2] += dcol
    if fallingPiecesLegal(data, data.fallingPiece):
        return True
    else:
        data.fallingPiece[1] -= drow
        data.fallingPiece[2] -= dcol
        return False


def fallingPiecesLegal(data, piece):
    tpiece = piece[0]
    frow = piece[1]
    fcol = piece[2]
    if frow < 0 or fcol < 0:
        return False
    elif frow > data.rows - len(tpiece) or fcol > data.cols - len(tpiece[0]):
        return False
    else:
        for row in range(len(tpiece)):
            for col in range(len(tpiece[0])):
                if tpiece[row][col] == True and \
                        data.board[row + frow][col + fcol] != data.emptyColor:
                    return False
    return True


def rotateFallingPiece(data):
    oldPiece = data.fallingPiece[0]
    oldCenterRow = data.fallingPiece[1] + len(oldPiece) // 2
    oldCenterCol = data.fallingPiece[2] + len(oldPiece[0]) // 2
    newNumRows, newNumCols = len(oldPiece[0]), len(oldPiece)
    newRow = oldCenterRow - newNumRows // 2
    newCol = oldCenterCol - newNumCols // 2
    newPiece = []
    for col in range(len(oldPiece[0])):
        newPiece.append([])
        row = len(oldPiece) - 1
        while row >= 0:
            newPiece[col].append(oldPiece[row][col])
            row -= 1
    tnewPiece = [newPiece, newRow, newCol]
    if fallingPiecesLegal(data, tnewPiece):
        data.fallingPiece = [newPiece, newRow, newCol]
    else:
        pass


def placeFallingPiece(data):
    piece = data.fallingPiece[0]
    frow = data.fallingPiece[1]
    fcol = data.fallingPiece[2]
    color = data.fallingPieceColor
    for row in range(len(piece)):
        for col in range(len(piece[0])):
            if piece[row][col] == True:
                data.board[frow + row][fcol + col] = color
    removeFullRows(data)


def gameOver(canvas, data):
    canvas.create_rectangle(data.margin, data.height / 4, data.width - data.margin,
                            data.height / 2, fill="black")
    canvas.create_text(data.width / 2, data.height / 3, text="Game Over!!",
                       font="Arial " + str(int(data.cellSize * 1.5)) + " bold", fill="yellow")


def removeFullRows(data):
    count = 0
    ind = 0
    while ind < len(data.board):
        if data.emptyColor not in data.board[ind]:
            print()
            data.board.pop(ind)
            count += 1
        else:
            ind += 1
    while len(data.board) < data.rows:
        emptyRow = [data.emptyColor] * data.cols
        data.board.insert(0, emptyRow)
    data.score += count ** 2


def redrawAll(canvas, data):
    drawBoard(canvas, data)
    drawFallingPiece(canvas, data)
    if data.isGameOver == True:
        gameOver(canvas, data)
    canvas.create_text(data.width / 2, data.margin / 2, text="score: " + str(data.score),
                       font="Arials 13 bold")


def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

    # Set up data and call init
    class Struct(object): pass

    data = Struct()
    init(data, width, height)
    root = Tk()
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Key>", lambda event:
    keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")


if __name__ == "__main__":
    playTeris(15, 10)
