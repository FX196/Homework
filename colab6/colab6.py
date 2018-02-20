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
    data.board = [[]*15]
    data.piecesColor = [ "red", "yellow", "magenta", "pink", "cyan",
    "green", "orange" ]
    data.fallingPiece = []
    data.fallingPieceColor = []

def keyPressed(event,data):
    pass


def mousePressed(event,data):
    pass



def timerFired(data):
    pass

def playTeris(rows=15,cols=10):
    pass

def drawBoard(canvas,data):
    canvas.create_rectangle(0,0,data.width,data.height,fill="orange")
    for row in range(data.rows):
        data.board.append([])
        for col in range(data.cols):
            if col==0 and row==0:
                data.board[row].append("red")
            elif row==0 and col==data.cols-1:
                data.board[row].append("white")
            elif row==data.rows-1 and col==0:
                data.board[row].append("green")
            elif row==data.rows-1 and col==data.cols-1:
                data.board[row].append("gray")
            else:
                data.board[row].append(data.emptyColor)
            drawCell(canvas,data,row,col,data.board[row][col])
    
def drawCell(canvas,data,row,col,color):
    canvas.create_rectangle(data.margin+col*data.cellSize,
    data.margin+row*data.cellSize,data.margin+(col+1)*data.cellSize,
    data.margin+(row+1)*data.cellSize,
    fill=color,width=3,outline = "black")

def newFallingPiece(data):
    iPiece = [[  True,  True,  True,  True ]]
    jPiece = [[  True, False, False ],[  True,  True,  True ]]
    lPiece = [[ False, False,  True ],[  True,  True,  True ]]
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
    

def drawFallingPiece(canvas,data):
    newFallingPiece(data)
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
        pass
    else:
        data.fallingPiece[1] -=drow
        data.fallingPiece[2] -=dcol
    
def fallingPiecesLegal(data):
    return True
    
def rotateFallingPiece():
    pass
    
def placeFallingPiece():
    pass
    
def removeFullRows():
    pass


def redrawAll(canvas,data):
    drawBoard(canvas,data)
    drawFallingPiece(canvas,data)













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