#################################################
# Zhuqing Yang (zhuqingy) Section E 
# Hw10
#################################################

import decimal


#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10 ** -7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)


def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))


#################################################
# Hw10 problems
#################################################

def flatten(lst):
    if len(lst) == 0:
        return []
    elif isinstance(lst[0], list) == False:
        return [lst[0]] + flatten(lst[1:])
    else:
        return flatten(lst[0]) + flatten(lst[1:])


def collectPos(atp, board):
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == chr(ord(atp) - 1):
                pos = (row, col)
                r, c = pos[0], pos[1]
    possiblelst = [(r - 1, c - 1), (r - 1, c), (r - 1, c + 1), (r, c + 1), (r + 1, c + 1), (r + 1, c), (r + 1, c - 1),
                   (r, c - 1)]
    return possiblelst


def solveABC(constraints, aLocation, sol=None, atp='B'):
    rows, cols, diags = constraints['rows'], constraints['cols'], constraints['diags']
    if atp == 'Z':
        return sol
    if sol == None:
        sol = []
        for i in range(5): sol += [['Z'] * 5]
        sol[aLocation[0]][aLocation[1]] = 'A'
    possiblelst = collectPos(atp, sol)
    for possiblePos in possiblelst:
        prow, pcol = possiblePos[0], possiblePos[1]
        if prow >= len(sol) or prow < 0 or pcol >= len(sol) or pcol < 0:
            continue
        elif sol[prow][pcol] == 'Z':
            sol[prow][pcol] = atp
        else:
            continue
        if (atp in rows[prow]) or (atp in cols[pcol]) or ((prow == pcol) and ((atp in
                                                                               diags['left'])) or (
                                                                  (prow + pcol == 4) and atp in diags['right'])):
            tempsol = solveABC(constraints, aLocation, sol, chr(ord(atp) + 1))
            if tempsol != None:
                return sol
        sol[prow][pcol] = 'Z'


con = {
    "rows": {0: ["I", "L"],
             1: ["M", "F"],
             2: ["Y", "N"],
             3: ["D", "U"],
             4: ["Q", "R"]},
    "cols": {0: ["H", "T"],
             1: ["J", "W"],
             2: ["X", "K"],
             3: ["B", "E"],
             4: ["O", "P"]},
    "diags": {"left": ["C", "G"],
              "right": ["V", "S"]}}
aLo = (0, 4)

######################################################################
# ignore_rest: The autograder will ignore all code below here
######################################################################

from tkinter import *


def init(data):
    data.level = 1


def teddyFace(canvas, xc, yc, r):
    eyeR = r / 8
    mouR = r / 2
    earR = r / 2
    # face
    canvas.create_oval(xc - r, yc - r, xc + r, yc + r, fill='brown', outline='black',
                       width=r / 20)
    # yellow area
    canvas.create_oval(xc - mouR, yc + mouR * 0.5 - mouR, xc + mouR, yc + mouR * 0.5 + mouR,
                       fill='pink', outline='black', width=mouR / 10)
    # left eye
    canvas.create_oval(xc - 0.6 * mouR - eyeR, yc - mouR - eyeR, xc - 0.6 * mouR + eyeR,
                       yc - mouR + eyeR, fill='black')
    # right eye
    canvas.create_oval(xc + 0.6 * mouR - eyeR, yc - mouR - eyeR, xc + 0.6 * mouR + eyeR,
                       yc - mouR + eyeR, fill='black')
    # nose
    canvas.create_oval(xc - eyeR, yc + 0.1 * r - eyeR, xc + eyeR, yc + 0.1 * r + eyeR,
                       fill='black')
    # mouth
    # canvas.create_arc()


def fractalTeddy(canvas, xc, yc, r, level):
    if level == 1:
        teddyFace(canvas, xc, yc, r)
    else:
        fractalTeddy(canvas, xc, yc, r, level - 1)
        fractalTeddy(canvas, xc - 1.05 * r, yc - 1.05 * r, r / 2, level - 1)
        fractalTeddy(canvas, xc + 1.05 * r, yc - 1.05 * r, r / 2, level - 1)


def keyPressed(event, data):
    if (event.keysym in ["Up", "Right"]):
        data.level += 1
    elif ((event.keysym in ["Down", "Left"]) and (data.level > 1)):
        data.level -= 1


def redrawAll(canvas, data):
    r = data.width / 6
    xc = data.width / 2
    yc = 0.7 * data.height
    fractalTeddy(canvas, xc, yc, r, data.level)
    canvas.create_text(data.width / 2, data.width / 20,
                       text="Level %d Bear Face" % (data.level),
                       font="Arial 26 bold")
    canvas.create_text(data.width / 2, data.height / 6,
                       text="Use arrows to change level",
                       font="Arial 10")


def mousePressed(event, data): pass


def timerFired(data): pass


def runTeddyFractalViewer(width=500, height=300):
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
    data.timerDelay = 100  # milliseconds
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
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")


# runTeddyFractalViewer()


#################################################
# Hw10 Test Functions
#################################################


def testFlatten():
    print("Testing flatten()...", end="")
    assert (flatten([1, [2]]) == [1, 2])
    assert (flatten([1, 2, [3, [4, 5], 6], 7]) == [1, 2, 3, 4, 5, 6, 7])
    assert (flatten(['wow', [2, [[]]], [True]]) == ['wow', 2, True])
    assert (flatten([]) == [])
    assert (flatten([[]]) == [])
    print("Passed!")


#################################################
# Hw10 Main
#################################################

def testAll():
    testFlatten()
    solveABC(con, aLo)


def main():
    testAll()


if __name__ == '__main__':
    main()
