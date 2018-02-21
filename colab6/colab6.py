# Zhuqing Yang (zhuqingy) Section E #############
# Colab6
# Partner: Shuyuan Ding (shuyuand)###############

import math
import string
import copy
import random

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
# Colab6 problems
########################

from tkinter import * 

def init(data):
    data.cellSize = 20
    data.margin = 25
    data.rows = 15
    data.cols = 10
    data.emptyColor = "blue"
    data.board = getBoard(data)
    data.piecesColor = [ "red", "yellow", "magenta", "pink", "cyan",
    "green", "orange" ]
    data.gameOver = False
    data.fallingPiece = []
    data.fallingPieceColor = []
    newFallingPiece(data)

def getBoard(data):
    board = [[]*data.rows]
    for row in range(data.rows):
        board.append([])
        for col in range(data.cols):
            if col==0 and row==0:
                board[row].append("red")
            elif row==0 and col==data.cols-1:
                board[row].append("white")
            elif row==data.rows-1 and col==0:
                board[row].append("green")
            elif row==data.rows-1 and col==data.cols-1:
                board[row].append("gray")
            else:
                board[row].append(data.emptyColor)
    return board

def keyPressed(event,data):
    if event.keysym == "r":
        init(data)
    elif data.gameOver:
        return
    if event.keysym == "Up":
        rotateFallingPiece(data)
    elif event.keysym == "Down":
        moveFallingPiece(data, +1, 0)
    elif event.keysym == "Left":
        moveFallingPiece(data, 0, -1)
    elif event.keysym == "Right":
        moveFallingPiece(data, 0, +1)
    if event.char == "b":
        newFallingPiece(data)


def mousePressed(event,data):
    pass


def timerFired(data):
    if data.gameOver:
        return
    moved = moveFallingPiece(data, 1, 0)
    if not moved:
        placeFallingPiece(data)


def playTeris(rows=15,cols=10):
    pass


def drawBoard(canvas,data):
    canvas.create_rectangle(0,0,data.width,data.height,fill="orange")
    for row in range(data.rows):
        for col in range(data.cols):
            drawCell(canvas,data,row,col,data.board[row][col])


def drawCell(canvas,data,row,col,color):
    canvas.create_rectangle(data.margin+col*data.cellSize,
    data.margin+row*data.cellSize,data.margin+(col+1)*data.cellSize,
    data.margin+(row+1)*data.cellSize,
    fill=color,width=3,outline = "black")


def newFallingPiece(data):
    iPiece = [[True,  True,  True,  True]]
    jPiece = [[True, False, False],[True,  True,  True]]
    lPiece = [[ False, False,  True ],[True,  True,  True]]
    oPiece = [[  True,  True ],[  True,  True ]]
    sPiece = [[ False,  True,  True ],[  True,  True, False ]]
    tPiece = [[ False,  True, False ],[  True,  True,  True ]]
    zPiece = [[  True,  True, False ],[ False,  True,  True ]]
    tetrisPieces = [ iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece ]
    randomInd = random.randint(0, len(tetrisPieces) - 1)
    if tetrisPieces[randomInd] == iPiece:
        fallRow,fallCol = (0,3)
    else:
        fallRow,fallCol = (0,4) 
    data.fallingPiece = [tetrisPieces[randomInd],fallRow,fallCol]
    data.fallingPieceColor = [data.piecesColor[randomInd]]

    if not fallingPiecesLegal(data):
        data.gameOver = True


def drawFallingPiece(canvas,data):
    piece = data.fallingPiece[0]
    frow = data.fallingPiece[1]
    fcol = data.fallingPiece[2]
    for row in range(len(piece)):
        for col in range(len(piece[0])):
            if piece[row][col] == True:
                drawCell(canvas,data,row+frow,col+fcol,data.fallingPieceColor)


def moveFallingPiece(data,drow,dcol):
    data.fallingPiece[1] += drow
    data.fallingPiece[2] += dcol
    if fallingPiecesLegal(data):
        return True
    else:
        data.fallingPiece[1] -=drow
        data.fallingPiece[2] -=dcol
        return False


def fallingPiecesLegal(data, *piece):
    if not piece:
        piece = data.fallingPiece
    else:
        piece = piece[0]
    shape, rPiece, cPiece = piece
    if rPiece < 0 or cPiece < 0:
        return False
    elif rPiece > data.rows-len(shape) or \
            cPiece > data.cols-len(shape[0]):
        return False
    else:
        for row in range(len(shape)):
            for col in range(len(shape[0])):
                if shape[row][col] and data.board[row+rPiece][col+cPiece] != data.emptyColor:
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
    shape, r, c = data.fallingPiece

    for row in range(len(shape)):
        for col in range(len(shape[0])):
            if shape[row][col]:
                data.board[row+r][col+c] = data.fallingPieceColor

    newFallingPiece(data)

def checkGameOver(canvas, data):
    if data.gameOver:
        canvas.create_rectangle(data.margin, data.height / 4, data.width - data.margin,
                            data.height / 2, fill="black")
        canvas.create_text(data.width / 2, data.height / 3, text="Game Over!!",
                       font="Arial " + str(int(data.cellSize * 1.5)) + " bold", fill="yellow")


def removeFullRows():
    pass


def redrawAll(canvas, data):
    drawBoard(canvas, data)
    drawFallingPiece(canvas, data)
    checkGameOver(canvas, data)









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

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 1000 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(250, 350)













#################################################
# Colab5 Test Functions
#########################################################################



#################################################
# Colab5 Main
################################################

#def testAll():

#def main():
#    testAll()

#if __name__ == '__main__':
#    main()
