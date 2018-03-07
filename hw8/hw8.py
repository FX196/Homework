#################################################
# Zhuqing Yang (zhuqingy) Section E 
# Hw8
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
# Hw8 problems
#################################################

'''
def slow1(lst): # N is the length of the list lst
    assert(len(lst) >= 2)
    a = lst.pop()
    b = lst.pop(0)
    lst.insert(0, a)
    lst.append(b)
    
    A.this function is to exchange the first and the last element in a string 
    has length more than 2.
    B.see above.


def slow2(lst): # N is the length of the list lst
    counter = 0
    for i in range(len(lst)):
        if lst[i] not in lst[:i]:
            counter += 1
    return counter

import string
def slow3(s): # N is the length of the string s
    maxLetter = ""
    maxCount = 0
    for c in s:
        for letter in string.ascii_lowercase:
            if c == letter:
                if s.count(c) > maxCount or \
                   s.count(c) == maxCount and c < maxLetter:
                    maxCount = s.count(c)
                    maxLetter = c
    return maxLetter
'''



def instrumentedLinearSearch(lst,item):
    result = []
    if item not in lst:
        return None
    for i in range(len(lst)):
        if lst[i] != item:
            result.append(i)
        elif lst[i] == item:
            result.append(i)
            break
    return result

def instrumentedBinarySearch(lst,item):
    result = []
    lst = sorted(lst)
    find = False
    i = (len(lst)-1)//2
    if item not in lst:
        return None
    while find == False:
        result.append(i)
        if lst[i] == item:
            find = True
        elif lst[i] < item:
            i += (len(lst)-i-1)//2
        elif lst[i] > item:
            i = (len(lst)-i-1)//2
    return result

def containsPythagoreanTriple(a):
    count = 0
    for i in range(len(a)):
        for j in range(1,len(a)):
            for k in range(2,len(a)):
                if isPythagoreanTriple(a[i],a[j],a[k]):
                    count += 1
    if count >= 1:
        return True
    return False

    
def isPythagoreanTriple(a,b,c):
    if a**2+b**2==c**2 or a**2+c**2==b**2 or b**2+c**2==a**2:
        return True
    return False

def movieAwards(oscarResults):
    d = dict()
    movieList = []
    for i in oscarResults:
        movieList.append(i[1])
    movieSet = set(movieList)
    for movie in movieSet:
        awards = []
        for award in oscarResults:
            if movie in award[1]:
                awards.append(award[0])
                d[movie] = set(awards)
    anotherd = dict()
    for i in oscarResults:
        anotherd[i[1]] = i[0]
    anotherd.update(d)
    return anotherd

def friendsOfFriends(d):
    names = []
    matchedFriends = []
    fOF = []
    newd = dict()
    for name in d:
        names.append(name)
        matchedFriends.append(d[name])
    for i in range(len(names)):
        friends = []
        for j in range(len(names)):
            if names[j] in d[names[i]]:
                friends += d[names[j]]
        fOF.append(friends)
    FOF = []
    for i in fOF:
        FOF.append(set(i))
    for i in range(len(FOF)):
        FOF[i].discard(names[i])
        FOF[i] = FOF[i]-matchedFriends[i]
        newd[names[i]] = FOF[i]
    #print(names)
    #print(matchedFriends)
    #print(FOF)
    #print(fOF)
    return newd
    
    



#################################################
# Hw8 Test Functions
#################################################
def testInstrumentedLinearSearch():
    print("Testing instrumentedLinearSearch()...", end="")
    assert(instrumentedLinearSearch([2, 4, 6, 8, 10, 12], 8) == [0,1,2,3])
    assert(instrumentedLinearSearch([2, 4, 6, 8, 10, 12], 6) == [0,1,2])
    assert(instrumentedLinearSearch([1,4,7,8,5,15,12,3], 5) == [0,1,2,3,4])
    assert(instrumentedLinearSearch([2, 4, 6, 8, 10, 12], 9) == None)
    print("Passed!")

def testInstrumentedBinarySearch():
    print("Testing instrumentedBinarySearch()...", end="")
    assert(instrumentedBinarySearch([2, 4, 6, 8, 10, 12, 14], 12) == [3,5])
    assert(instrumentedBinarySearch([2, 4, 6, 8, 10, 12, 14], 4) == [3,1])
    assert(instrumentedBinarySearch([1, 4, 2, 3, 10, 7, 6, 8], 6) == [3,5,4])
    assert(instrumentedBinarySearch([2, 4, 6, 8, 10, 12, 14], 12) == [])
    print("Passed!")

def testContainsPythagoreanTriple():
    print("Testing containsPythagoreanTriple()...", end="")
    assert(containsPythagoreanTriple([1,3,6,2,5,1,4]) == True)
    assert(containsPythagoreanTriple([1,3,6,2,3,1,4]) == False)
    assert(containsPythagoreanTriple([1,13,6,12,5,1,4]) == True)
    assert(containsPythagoreanTriple([1,3,4,12,5,13,4]) == True)
    print("Passed!")

def testIsPythagoreanTriple():
    print("Testing isPythagoreanTriple()...", end="")
    assert(isPythagoreanTriple(3,4,5) == True)
    assert(isPythagoreanTriple(1,4,5) == False)
    assert(isPythagoreanTriple(5,12,13) == True)
    assert(isPythagoreanTriple(0,0,0,) == True)
    print("Passed!")


awards1 = { 
    ("Best Picture", "The Shape of Water"), 
    ("Best Actor", "Darkest Hour"),
    ("Best Actress", "Three Billboards Outside Ebbing, Missouri"),
    ("Best Director", "The Shape of Water")
  }
dicawards1 = { 
    "Darkest Hour" : { "Best Actor" },
    "Three Billboards Outside Ebbing, Missouri" : { "Best Actress" },
    "The Shape of Water" : { "Best Director", "Best Picture" }
  }

awards2 = { 
    ("Best Picture", "La La Land"), 
    ("Best Actor", "Manchester by the Sea"),
    ("Best Actress", "La La Land"),
    ("Best Director", "La La Land"),
    ("Best Music", "La La Land")
  }

dicawards2 = { 
    "La La Land" : {"Best Actress","Best Picture","Best Director","Best Music"},
    "Manchester by the Sea" : { "Best Actor" }
  }

def testMovieAwards():
    print("Testing movieAwards()...", end="")
    assert(movieAwards(awards1) == dicawards1)
    assert(movieAwards(awards2) == dicawards2)
    assert(movieAwards(dict()) == dict())
    print("Passed!")

a = { }
a["jon"] = set(["arya", "tyrion"])    
a["tyrion"] = set(["jon", "jaime", "pod"])
a["arya"] = set(["jon"])    
a["jaime"] = set(["tyrion", "brienne"])
a["brienne"] = set(["jaime", "pod"])
a["pod"] = set(["tyrion", "brienne", "jaime"])
a["ramsay"] = set()

a1 = {
 'tyrion': {'arya', 'brienne'}, 
 'pod': {'jon'}, 
 'brienne': {'tyrion'}, 
 'arya': {'tyrion'}, 
 'jon': {'pod', 'jaime'}, 
 'jaime': {'pod', 'jon'}, 
 'ramsay': set()
}

b = { }



def testFriendsOfFriends():
    print("Testing friendsOfFriends()...", end="")
    assert(a == a1)
    print("Passed!")



#################################################
# Hw3 Main
#################################################

def testAll():
    testInstrumentedLinearSearch()
    #testInstrumentedBinarySearch()
    testContainsPythagoreanTriple()
    testIsPythagoreanTriple()
    testMovieAwards()
    testFriendsOfFriends()

def main():
    testAll()

if __name__ == '__main__':
    main()
