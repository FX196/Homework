#################################################
# Zhuqing Yang (zhuqingy) Section E 
# Hw11
#################################################

import decimal
import random


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
# Hw11 problem: OOPy Frogger
#################################################

# Updated Animation Starter Code

from tkinter import *


class Frog(object):
    def __init__(self, x, y):
        # position and size of frog in Frog. 
        self.x = x
        self.y = y
        self.froR = 15

    def move(self, event, data):
        # control the movement of the frog in the grid, but can't go beyong
        # the limit.
        if event.keysym == 'Up' and self.y > data.margin + self.froR:
            self.y -= data.size
        elif event.keysym == 'Down' and \
                self.y < data.margin + (data.rows - 1) * data.size + self.froR:
            self.y += data.size
        elif event.keysym == 'Right' and \
                self.x < data.margin + (data.cols - 1) * data.size + self.froR:
            self.x += data.size
        elif event.keysym == 'Left' and self.x > data.margin + self.froR:
            self.x -= data.size

    def draw(self, canvas):
        # draw the frog. 
        canvas.create_polygon((self.x - self.froR, self.y),
                              (self.x, self.y + self.froR), (self.x + self.froR, self.y),
                              (self.x, self.y - self.froR), fill='brown')


class Vehicle(object):
    # position, size, and moving direction of vehicle object. 
    def __init__(self, x, y, size, direction):
        self.x = x
        self.y = y
        self.size = size
        self.direction = direction

    # control the movement of the vehicles. 
    def move(self, data):
        if self.direction == 1:
            # if self.x < (data.cols-1)*data.size+data.margin:
            self.x += data.size
        else:
            # if self.x > data.margin:
            self.x -= data.size

    def collidesWithFrog(self, data):
        # get the position of current frog. 
        fx, fy = data.frP.x, data.frP.y
        # check whether vehicles and frog are meeting. 
        for vehicle in data.vehicles:
            if (fx - data.size / 2 == vehicle.x or \
                fx - data.size / 2 == vehicle.x + self.size / 2) and \
                    fy - data.size / 2 == vehicle.y:
                # minus one life, and set the frog back to its 
                # initial position. 
                data.lives -= 1
                data.frP = Frog(data.margin + (roundHalfUp(data.cols / 2) - 1) \
                                * data.size + 15, data.margin + (data.rows - 1) * data.size + 15)


class Car(Vehicle):
    def __init__(self, x, y, size, direction):
        super().__init__(x, y, size, direction)

    def draw(self, canvas, data):
        # draw all cars that within the board. 
        if self.x >= data.margin and self.x <= data.margin + data.size * (data.cols - 1):
            canvas.create_oval(self.x, self.y, self.x + 2 * self.size, self.y + 2 * self.size,
                               outline='black', fill='blue')


class Truck(Vehicle):
    def __init__(self, x, y, size, direction):
        super().__init__(x, y, size, direction)

    def draw(self, canvas, data):
        # draw all trucks that within the board, and half of the truck when 
        # half of it is out of the board. 
        if self.x >= data.margin and self.x <= data.margin + (data.cols - 2) * data.size:
            canvas.create_rectangle(self.x, self.y, self.x + self.size,
                                    self.y + self.size / 2, outline='black', fill='red')
        elif self.x < data.margin and self.x >= data.margin - data.size:
            canvas.create_rectangle(self.x + data.size, self.y, self.x + self.size,
                                    self.y + self.size / 2, outline='black', fill='red')
        elif self.x > data.margin + (data.cols - 2) * data.size and \
                self.x <= data.margin + (data.cols - 1) * data.size:
            canvas.create_rectangle(self.x, self.y, self.x + data.size,
                                    self.y + data.size, outline='black', fill='red')


def init(data):
    # load data.xyz as appropriate
    data.margin = 20
    data.size = 30
    data.rows = (data.height - 2 * data.margin) // data.size
    data.cols = (data.width - 2 * data.margin) // data.size
    data.frP = Frog(data.margin + (roundHalfUp(data.cols / 2) - 1) * data.size + 15,
                    data.margin + (data.rows - 1) * data.size + 15)
    data.directions = randomDirection(data)
    data.freq = randomFrequency(data)
    data.vehicles = []
    data.lives = 3
    # a time separator for later use, with the combination of frequency. 
    data.tsep = 0
    data.isGameOver = False
    initVehicle(data)


# generate random vehicles' moving frequencies for vehicles in each row.
def randomFrequency(data):
    lst = []
    for i in range(data.rows):
        lst.append(random.randint(3, 8))
    return lst


# generate random vehicles' moving directions for vehicles in each row.
def randomDirection(data):
    lst = []
    for i in range(data.rows):
        # '1' represent right, '0' for the left. 
        lst.append(random.randint(0, 1))
    return lst


def mousePressed(event, data):
    # use event.x and event.y
    pass


def keyPressed(event, data):
    # use event.char and event.keysym
    if data.isGameOver == False:
        data.frP.move(event, data)


def timerFired(data):
    # all movings are performed when game isn't over. 
    if data.isGameOver == False:
        # a time separator for later use, with the combination of frequency. 
        data.tsep += 1
        # add new vehicles. 
        newVehicle(data)
        for vehicle in data.vehicles:
            # vehicles move. 
            vehicle.move(data)


def initVehicle(data):
    for row in range(1, data.rows - 1):
        if row % 2 != 0:
            x = random.randint(0, data.cols - 1)
            data.vehicles.append(Car(x * data.size + data.margin,
                                     row * data.size + data.margin, 15, data.directions[row]))
        else:
            x = random.randint(0, data.cols - 2)
            data.vehicles.append(Truck(x * data.size + data.margin,
                                       row * data.size + data.margin, 60, data.directions[row]))


def newVehicle(data):
    for row in range(1, data.rows - 1):
        if row % 2 != 0:
            if data.directions[row] == 1 and (data.tsep % data.freq[row] == 0):
                data.vehicles.append(Car(data.margin - data.size, row * data.size + data.margin, 15,
                                         data.directions[row]))
            elif data.directions[row] == 0 and (data.tsep % data.freq[row] == 0):
                data.vehicles.append(Car(data.margin + data.size * (data.cols),
                                         row * data.size + data.margin, 15, data.directions[row]))
        else:
            if data.directions[row] == 1 and (data.tsep % data.freq[row] == 0):
                data.vehicles.append(Truck(data.margin - 2 * data.size,
                                           row * data.size + data.margin, 60, data.directions[row]))
            elif data.directions[row] == 0 and (data.tsep % data.freq[row] == 0):
                data.vehicles.append(Truck(data.margin + data.size * (data.cols),
                                           row * data.size + data.margin, 60, data.directions[row]))


def inValidArrive(data):
    fx, fy = data.frP.x, data.frP.y
    row = (fy - data.margin - data.size / 2) / data.size
    col = (fx - data.margin - data.size / 2) / data.size
    if row == 0 and col % 2 != 0:
        data.lives -= 1
        data.frP = Frog(data.margin + (roundHalfUp(data.cols / 2) - 1) \
                        * data.size + 15, data.margin + (data.rows - 1) * data.size + 15)


def isGameEnd(canvas, data):
    if data.lives == 0:
        data.isGameOver = True
        canvas.create_rectangle(data.margin, data.margin,
                                data.margin + data.cols * data.size, data.margin + data.rows * data.size * (3 / 5),
                                fill='black')
        canvas.create_text(data.margin, data.margin, text='YOU LOSE!',
                           fill='yellow', anchor=NW, font='Times %s bold' % str(data.width // 6))
    row = (data.frP.y - data.margin - data.size / 2) / data.size
    col = (data.frP.x - data.margin - data.size / 2) / data.size
    if row == 0 and col % 2 == 0 and data.lives > 0:
        data.isGameOver = True
        canvas.create_rectangle(data.margin, data.margin,
                                data.margin + data.cols * data.size, data.margin + data.rows * data.size * (3 / 5),
                                fill='black')
        canvas.create_text(data.margin, data.margin, text='YOU WIN!',
                           fill='yellow', anchor=NW, font='Times %s bold' % str(data.width // 6))


def redrawAll(canvas, data):
    # draw in canvas
    for row in range(data.rows):
        for col in range(data.cols):
            if (row == 0 and col % 2 == 0) or row == data.rows - 1:
                color = 'green'
            elif row == 0 and col % 2 != 0:
                color = 'black'
            else:
                color = 'grey'
            canvas.create_rectangle(data.margin + col * data.size,
                                    data.margin + row * data.size, data.margin + (col + 1) * data.size,
                                    data.margin + (row + 1) * data.size, outline='black', fill=color)
    data.frP.draw(canvas)
    canvas.create_text(data.margin, data.margin + (data.rows - 1) * data.size,
                       text='Lives: %d' % data.lives, fill='red', anchor=NW, font='Times 20 bold')
    for vehicle in data.vehicles:
        vehicle.draw(canvas, data)
        if data.lives >= 0 and data.isGameOver == False:
            vehicle.collidesWithFrog(data)
    inValidArrive(data)
    isGameEnd(canvas, data)


####################################
# use the run function as-is
####################################

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
    data.timerDelay = 1000  # milliseconds
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


run(500, 500)
