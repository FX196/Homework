#################################################
# Zhuqing Yang (zhuqingy) Section E 
# Hw9
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
# Hw9 problems
#################################################

class VendingMachine(object):
    def __init__(self, numBottles, bottlePrice):
        self.numBottles = numBottles
        self.cent = 100
        self.bottlePrice = bottlePrice / self.cent
        self.pricePaid = 0

    def getHashables(self):
        return (self.numBottles, self.bottlePrice)  # return a tuple of hashables

    def __hash__(self):
        return hash(self.getHashables())

    def __eq__(self, other):
        return (isinstance(other, VendingMachine) \
                and (self.numBottles == other.numBottles) \
                and (self.bottlePrice == other.bottlePrice) \
                and (self.pricePaid == other.pricePaid))

    def __repr__(self):
        if self.numBottles != 1:
            if self.pricePaid == 0:
                return "Vending Machine:<%d bottles; $%0.2f each; $%d paid>" \
                       % (self.numBottles, self.bottlePrice, self.pricePaid)
            else:
                return "Vending Machine:<%d bottles; $%0.2f each; $%0.2f paid>" \
                       % (self.numBottles, self.bottlePrice, self.pricePaid)
        else:
            return "Vending Machine:<%d bottle; $%0.2f each; $%d paid>" % \
                   (self.numBottles, self.bottlePrice, self.pricePaid)

    def isEmpty(self):
        if self.numBottles > 0:
            return False
        else:
            return True

    def getBottleCount(self):
        return self.numBottles

    def stillOwe(self):
        return int((self.bottlePrice - self.pricePaid) * self.cent)

    def insertMoney(self, n):
        if self.numBottles == 0:
            return ("Machine is empty", n)
        else:
            self.pricePaid += n / self.cent
            if self.pricePaid >= self.bottlePrice:
                self.numBottles -= 1
                change = int(100 * (self.pricePaid - self.bottlePrice))
                self.pricePaid = 0
                return ("Got a bottle!", change)
            else:
                if int(self.bottlePrice - self.pricePaid) - \
                        (self.bottlePrice - self.pricePaid) == 0:
                    return ("Still owe $%d" % \
                            (self.bottlePrice - self.pricePaid), 0)
                else:
                    return ("Still owe $%0.2f" % \
                            (self.bottlePrice - self.pricePaid), 0)

    def stockMachine(self, n):
        self.numBottles += n


class Gate(object):
    def __init__(self):
        self.boo0 = None
        self.boo1 = None
        self.numInput = 2
        self.bootup = (self.boo0, self.boo1)

    def __str__(self):
        return type(self).__name__ + str(self.bootup)

    def numberOfInputs(self):
        return self.numInput

    def setInput(self, n, boo):
        if n == 0:
            self.boo0 = boo
        elif n == 1:
            self.boo1 = boo
        self.bootup = (self.boo0, self.boo1)


class AndGate(Gate):
    def getOutput(self):
        if self.boo0 and self.boo1:
            return True
        else:
            return False


class OrGate(Gate):
    def getOutput(self):
        if self.boo0 or self.boo1:
            return True
        elif self.boo0 == False and self.boo1 == False:
            return False


class NotGate(Gate):
    def getOutput(self):
        self.boo0 = not self.boo0
        return self.boo0

    def numberOfInputs(self):
        self.numInput = 1
        return self.numInput


and1 = AndGate()
print(type(and1))
print(isinstance(and1, Gate))
print(and1.numberOfInputs())
and1.setInput(0, True)
and1.setInput(1, False)
print(str(and1))
print(and1.getOutput())
and1.setInput(1, True)
print(and1.getOutput())
print(str(and1))


def powerSum(n, k):
    if n <= 0 or k < 0:
        return 0
    else:
        return n ** k + powerSum(n - 1, k)


def generateLetterString(s):
    if len(s) != 2 or s[0] == s[1] or s.isalpha() == False:
        return ''
    elif s[0] < s[1]:
        return s[0] + generateLetterString(chr(ord(s[0]) + 1) + s[1])
    elif s[0] > s[1]:
        return s[0] + generateLetterString(chr(ord(s[0]) - 1) + s[1])


#################################################
# Hw8 Test Functions
#################################################

def testVendingMachineClass():
    print("Testing Vending Machine class...", end="")
    # Vending machines have three main properties: 
    # how many bottles they contain, the price of a bottle, and
    # how much money has been paid. A new vending machine starts with no
    # money paid.
    vm1 = VendingMachine(100, 125)
    assert (str(vm1) == "Vending Machine:<100 bottles; $1.25 each; $0 paid>")
    assert (vm1.isEmpty() == False)
    assert (vm1.getBottleCount() == 100)
    assert (vm1.stillOwe() == 125)

    # When the user inserts money, the machine returns a message about their
    # status and any change they need as a tuple.
    assert (vm1.insertMoney(20) == ("Still owe $1.05", 0))
    assert (str(vm1) == "Vending Machine:<100 bottles; $1.25 each; $0.20 paid>")
    assert (vm1.stillOwe() == 105)
    assert (vm1.getBottleCount() == 100)
    assert (vm1.insertMoney(5) == ("Still owe $1", 0))

    # When the user has paid enough money, they get a bottle and 
    # the money owed resets.
    assert (vm1.insertMoney(100) == ("Got a bottle!", 0))
    assert (vm1.getBottleCount() == 99)
    assert (vm1.stillOwe() == 125)
    assert (str(vm1) == "Vending Machine:<99 bottles; $1.25 each; $0 paid>")

    # If the user pays too much money, they get their change back with the
    # bottle.
    assert (vm1.insertMoney(500) == ("Got a bottle!", 375))
    assert (vm1.getBottleCount() == 98)
    assert (vm1.stillOwe() == 125)

    # Machines can become empty
    vm2 = VendingMachine(1, 120)
    assert (str(vm2) == "Vending Machine:<1 bottle; $1.20 each; $0 paid>")
    assert (vm2.isEmpty() == False)
    assert (vm2.insertMoney(120) == ("Got a bottle!", 0))
    assert (vm2.getBottleCount() == 0)
    assert (vm2.isEmpty() == True)

    # Once a machine is empty, it should not accept money until it is restocked.
    assert (str(vm2) == "Vending Machine:<0 bottles; $1.20 each; $0 paid>")
    assert (vm2.insertMoney(25) == ("Machine is empty", 25))
    assert (vm2.insertMoney(120) == ("Machine is empty", 120))
    assert (vm2.stillOwe() == 120)
    vm2.stockMachine(20)  # Does not return anything
    assert (vm2.getBottleCount() == 20)
    assert (vm2.isEmpty() == False)
    assert (str(vm2) == "Vending Machine:<20 bottles; $1.20 each; $0 paid>")
    assert (vm2.insertMoney(25) == ("Still owe $0.95", 0))
    assert (vm2.stillOwe() == 95)
    vm2.stockMachine(20)
    assert (vm2.getBottleCount() == 40)

    # We should be able to test machines for basic functionality
    vm3 = VendingMachine(50, 100)
    vm4 = VendingMachine(50, 100)
    vm5 = VendingMachine(20, 100)
    vm6 = VendingMachine(50, 200)
    vm7 = "Vending Machine"
    assert (vm3 == vm4)
    assert (vm3 != vm5)
    assert (vm3 != vm6)
    assert (vm3 != vm7)  # should not crash!
    s = set()
    assert (vm3 not in s)
    s.add(vm4)
    assert (vm3 in s)
    s.remove(vm4)
    assert (vm3 not in s)
    assert (vm4.insertMoney(50) == ("Still owe $0.50", 0))
    assert (vm3 != vm4)
    print("Done!")


def getLocalMethods(clss):
    import types
    # This is a helper function for the test function below.
    # It returns a sorted list of the names of the methods
    # defined in a class.
    result = []
    for var in clss.__dict__:
        val = clss.__dict__[var]
        if (isinstance(val, types.FunctionType)):
            result.append(var)
    return sorted(result)


def testGateClasses():
    print("Testing Gate Classes... ", end="")

    # require methods be written in appropriate classes
    assert (getLocalMethods(Gate) == ['__init__', '__str__',
                                      'numberOfInputs', 'setInput'])
    assert (getLocalMethods(AndGate) == ['getOutput'])
    assert (getLocalMethods(OrGate) == ['getOutput'])
    assert (getLocalMethods(NotGate) == ['getOutput', 'numberOfInputs'])

    # make a simple And gate
    and1 = AndGate()
    assert (type(and1) == AndGate)
    assert (isinstance(and1, Gate) == True)
    assert (and1.numberOfInputs() == 2)
    and1.setInput(0, True)
    and1.setInput(1, False)
    # Hint: to get the name of the class given an object obj,
    # you can do this:  type(obj).__name__
    # You might do this in the Gate.__str__ method...
    assert (str(and1) == "And(True,False)")
    assert (and1.getOutput() == False)
    and1.setInput(1, True)  # now both inputs are True
    assert (and1.getOutput() == True)
    assert (str(and1) == "And(True,True)")

    # make a simple Or gate
    or1 = OrGate()
    assert (type(or1) == OrGate)
    assert (isinstance(or1, Gate) == True)
    assert (or1.numberOfInputs() == 2)
    or1.setInput(0, False)
    or1.setInput(1, False)
    assert (or1.getOutput() == False)
    assert (str(or1) == "Or(False,False)")
    or1.setInput(1, True)
    assert (or1.getOutput() == True)
    assert (str(or1) == "Or(False,True)")

    # make a simple Not gate
    not1 = NotGate()
    assert (type(not1) == NotGate)
    assert (isinstance(not1, Gate) == True)
    assert (not1.numberOfInputs() == 1)
    not1.setInput(0, False)
    assert (not1.getOutput() == True)
    assert (str(not1) == "Not(False)")
    not1.setInput(0, True)
    assert (not1.getOutput() == False)
    assert (str(not1) == "Not(True)")

    print("Passed!")


def testPowerSum():
    print("Testing powerSum()...", end="")
    assert (powerSum(5, 2) == 55)
    assert (powerSum(2, 5) == 33)
    assert (powerSum(1, 0) == 1)
    assert (powerSum(-2, 1) == 0)
    assert (powerSum(2, -1) == 0)
    print("Passed!")

#################################################
# Hw8 Main
#################################################

# def testAll():
# testVendingMachineClass()
# testGateClasses()
# testPowerSum()

# def main():
#    testAll()

# if __name__ == '__main__':
#    main()
