# Zhuqing Yang (zhuqingy) Section E #############
# Colab9
# Partner: Shuyuan Ding (shuyuand)###############

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
# Colab9 problems
########################

class Book(object):
    def __init__(self, title, author, numPages):
        self.title = title
        self.author = author
        self.numPages = numPages
        self.bookPage = 1
        self.bookmarkedPage = None

    def getHashables(self):
        return (self.title, self.author, self.numPages)  # return a tuple of hashables

    def __hash__(self):
        return hash(self.getHashables())

    def __eq__(self, other):
        return (isinstance(other, Book) and (self.title == other.title) \
                and (self.author == other.author) \
                and (self.numPages == other.numPages) \
                and (self.bookPage == other.bookPage) \
                and (self.bookmarkedPage == other.bookmarkedPage))

    def __repr__(self):
        if self.bookmarkedPage == None:
            if self.numPages > 1:
                return "Book<%s by %s: %d pages, currently on page %d>" % \
                       (self.title, self.author, self.numPages, self.bookPage)
            else:
                return "Book<%s by %s: %d page, currently on page %d>" % \
                       (self.title, self.author, self.numPages, self.bookPage)
        else:
            if self.numPages > 1:
                return ("Book<%s by %s: %d pages"
                        % (self.title, self.author, self.numPages) +
                        "currently on page %d, page %d bookmarked>" %
                        (self.bookPage, self.bookmarkedPage))
            else:
                return "Book<%s by %s: %d page, currently on page %d, page %d bookmarked>" % (self.title, self.author,
                                                                                              self.numPages,
                                                                                              self.bookPage,
                                                                                              self.bookmarkedPage)

    def turnPage(self, n):
        if self.bookPage + n < 1:
            self.bookPage = 1
        elif self.bookPage + n > self.numPages:
            self.bookPage = self.numPages
        else:
            self.bookPage += n

    def getCurrentPage(self):
        return self.bookPage

    def placeBookmark(self):
        self.bookmarkedPage = self.bookPage

    def getBookmarkedPage(self):
        return self.bookmarkedPage

    def turnToBookmark(self):
        if self.bookmarkedPage != None:
            self.bookPage = self.bookmarkedPage

    def removeBookmark(self):
        self.bookmarkedPage = None


class Bird(object):
    def __init__(self, bird):
        self.bird = bird
        self.numEggs = 0

    def __repr__(self):
        if self.numEggs == 1:
            return "%s has %d egg" % (self.bird, self.numEggs)
        else:
            return "%s has %d eggs" % (self.bird, self.numEggs)

    def fly(self):
        return "I can fly!"

    def layEgg(self):
        self.numEggs += 1

    def countEggs(self):
        return self.numEggs


class Penguin(Bird):
    def fly(self):
        return "No flying for me."

    def swim(self):
        return "I can swim!"


class MessengerBird(Bird):
    def __init__(self, bird, message=None):
        super().__init__(bird)
        if message != None:
            self.message = message
        else:
            self.message = None

    def deliverMessage(self):
        if self.message != None:
            return self.message
        else:
            return ""


def alternatingSum(lst):
    # specialize the case when the list is empty.
    if len(lst) == 0:
        return 0
    # when the list has even length, just simply take every pair of difference.
    elif len(lst) % 2 == 0:
        return lst[0] - lst[1] + alternatingSum(lst[2:])
    # when the list has odd length, plus the last element first, then turn to 
    # the case when it has even length.
    elif len(lst) % 2 != 0:
        return lst[len(lst) - 1] + alternatingSum(lst[:len(lst) - 1])


def powersOf3ToN(n, res=None):
    # eliminate all cases when n is less than one. (since the result won't be 
    # positive)
    if n < 1:
        return None
    # add the element 1 to the list first, since 1 must appear in every answer
    # if n is larger than 1, then base on the first element 1, we could do 
    # further calculation. 
    elif n >= 1 and res == None:
        return powersOf3ToN(n, [1])
    # use the simple method to determine whether the next power of 3 is less 
    # than n. 
    elif n >= 1 and res != None:
        if 3 * res[-1] <= n:
            # everytime change the last element, so the last element could be 
            # used in next round.
            res.append(3 * res[-1])
            return powersOf3ToN(n, res)
        elif 3 * res[-1] > n:
            return res


#################################################
# Colab9 Test Functions
#################################################    

def testBookClass():
    print("Testing Book class...", end="")
    # A Book has a title, and author, and a number of pages.
    # It also has a current page, which always starts at 1. There is no page 0!
    book1 = Book("Harry Potter and the Sorcerer's Stone",
                 "J. K. Rowling", 309)
    assert (str(book1) == "Book<Harry Potter and the Sorcerer's Stone by " +
            "J. K. Rowling: 309 pages, currently on page 1>")
    book2 = Book("Carnegie Mellon Motto", "Andrew Carnegie", 1)
    assert (str(book2) == "Book<Carnegie Mellon Motto by Andrew Carnegie: " +
            "1 page, currently on page 1>")

    # You can turn pages in a book. Turning a positive number of pages moves
    # forward; turning a negative number moves backwards. You can't move past
    # the first page going backwards or the last page going forwards
    book1.turnPage(4)  # turning pages does not return
    assert (book1.getCurrentPage() == 5)
    book1.turnPage(-1)
    assert (book1.getCurrentPage() == 4)
    book1.turnPage(400)
    assert (book1.getCurrentPage() == 309)
    assert (str(book1) == "Book<Harry Potter and the Sorcerer's Stone by " +
            "J. K. Rowling: 309 pages, currently on page 309>")
    book2.turnPage(-1)
    assert (book2.getCurrentPage() == 1)
    book2.turnPage(1)
    assert (book2.getCurrentPage() == 1)

    # You can also put a bookmark on the current page. This lets you turn
    # back to it easily. The book starts out without a bookmark.
    book3 = Book("The Name of the Wind", "Patrick Rothfuss", 662)
    assert (str(book3) == "Book<The Name of the Wind by Patrick Rothfuss: " +
            "662 pages, currently on page 1>")
    assert (book3.getBookmarkedPage() == None)
    book3.turnPage(9)
    book3.placeBookmark()  # does not return
    assert (book3.getBookmarkedPage() == 10)
    book3.turnPage(7)
    assert (book3.getBookmarkedPage() == 10)
    assert (book3.getCurrentPage() == 17)
    assert (str(book3) == "Book<The Name of the Wind by Patrick Rothfuss: " +
            "662 pages, currently on page 17, page 10 bookmarked>")
    book3.turnToBookmark()
    assert (book3.getCurrentPage() == 10)
    book3.removeBookmark()
    assert (book3.getBookmarkedPage() == None)
    book3.turnPage(25)
    assert (book3.getCurrentPage() == 35)
    book3.turnToBookmark()  # if there's no bookmark, don't turn to a page
    assert (book3.getCurrentPage() == 35)
    assert (str(book3) == "Book<The Name of the Wind by Patrick Rothfuss: " + \
            "662 pages, currently on page 35>")

    # Finally, you should be able to compare two books directly and hash books
    book5 = Book("A Game of Thrones", "George R.R. Martin", 807)
    book6 = Book("A Game of Thrones", "George R.R. Martin", 807)
    book7 = Book("A Natural History of Dragons", "Marie Brennan", 334)
    book8 = Book("A Game of Spoofs", "George R.R. Martin", 807)
    assert (book5 == book6)
    assert (book5 != book7)
    assert (book5 != book8)
    s = set()
    assert (book5 not in s)
    s.add(book5)
    assert (book6 in s)
    assert (book7 not in s)
    s.remove(book6)
    assert (book5 not in s)
    book5.turnPage(1)
    assert (book5 != book6)
    book5.turnPage(-1)
    assert (book5 == book6)
    book6.placeBookmark()
    assert (book5 != book6)
    print("Done!")


def getLocalMethods(clss):
    import types
    # This is a helper function for the test function below.
    # It returns a sorted list of the names of the methods
    # defined in a class. It's okay if you don't fully understand it!
    result = []
    for var in clss.__dict__:
        val = clss.__dict__[var]
        if (isinstance(val, types.FunctionType)):
            result.append(var)
    return sorted(result)


def testBirdClasses():
    print("Testing Bird classes...", end="")
    # A basic Bird has a species name, can fly, and can lay eggs
    bird1 = Bird("Parrot")
    assert (type(bird1) == Bird)
    assert (isinstance(bird1, Bird))
    assert (bird1.fly() == "I can fly!")
    assert (bird1.countEggs() == 0)
    assert (str(bird1) == "Parrot has 0 eggs")
    bird1.layEgg()
    assert (bird1.countEggs() == 1)
    assert (str(bird1) == "Parrot has 1 egg")
    bird1.layEgg()
    assert (bird1.countEggs() == 2)
    assert (str(bird1) == "Parrot has 2 eggs")
    assert (getLocalMethods(Bird) == ['__init__', '__repr__', 'countEggs',
                                      'fly', 'layEgg'])

    # A Penguin is a Bird that cannot fly, but can swim
    bird2 = Penguin("Emperor Penguin")
    assert (type(bird2) == Penguin)
    assert (isinstance(bird2, Penguin))
    assert (isinstance(bird2, Bird))
    assert (bird2.fly() == "No flying for me.")
    assert (bird2.swim() == "I can swim!")
    bird2.layEgg()
    assert (bird2.countEggs() == 1)
    assert (str(bird2) == "Emperor Penguin has 1 egg")
    assert (getLocalMethods(Penguin) == ['fly', 'swim'])

    # A MessengerBird is a Bird that can optionally carry a message
    bird3 = MessengerBird("War Pigeon", message="Top-Secret Message!")
    assert (type(bird3) == MessengerBird)
    assert (isinstance(bird3, MessengerBird))
    assert (isinstance(bird3, Bird))
    assert (not isinstance(bird3, Penguin))
    assert (bird3.deliverMessage() == "Top-Secret Message!")
    assert (str(bird3) == "War Pigeon has 0 eggs")
    assert (bird3.fly() == "I can fly!")

    bird4 = MessengerBird("Homing Pigeon")
    assert (bird4.deliverMessage() == "")
    bird4.layEgg()
    assert (bird4.countEggs() == 1)
    assert (getLocalMethods(MessengerBird) == ['__init__', 'deliverMessage'])
    print("Done!")


def testAlternatingSum():
    print("Testing alternatingSum()...", end="")
    assert (alternatingSum([1, 2, 3, 4, 5]) == 3)
    assert (alternatingSum([1, 2, 3, 4]) == -2)
    assert (alternatingSum([2, 4, 6, 1, 5]) == 8)
    assert (alternatingSum([3, 10, 2, 7]) == -12)
    print("Passed!")


def testPowersOf3ToN():
    print("Testing powersOf3ToN()...", end="")
    assert (powersOf3ToN(10.5) == [1, 3, 9])
    assert (powersOf3ToN(0) == None)
    assert (powersOf3ToN(-3) == None)
    assert (powersOf3ToN(86.7) == [1, 3, 9, 27, 81])
    print("Passed!")


#################################################
# Colab9 Main
#################################################

def testAll():
    testBookClass()
    testBirdClasses()
    testAlternatingSum()
    testPowersOf3ToN()


def main():
    testAll()


if __name__ == '__main__':
    main()
