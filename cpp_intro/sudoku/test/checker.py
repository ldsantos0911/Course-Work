import re
successes = 0
tests = ["test/test2.out",
         "test/test1.out",
         "test/test3.out",
         "test/test4.out",
         "test/test5.out",
         "test/test6.out",
         "test/test7.out",
         "test/test8.out",
         
        ]
codes = [0, 1, 2, 3, 4, 5, 6, 7]
regex = re.compile('[^a-zA-Z ]')

print "\nRUNNING ", len(tests), " TESTS..."

def success(s):
    print "SUCCESS: " + s;
def failure(s):
    print "FAIL: " + s;

def simpleMoves(file):
    '''
    This test files in the top row of testFileEasy.in with values
    and checks that they all get entered.
    '''
    s = "| 2 6 8 | 4 1 3 | 5 7 9 | "
    t = ''.join(s.split()).lower()
    for f in file:
        if (''.join(f.split()).lower() == t):
            success("simpleMoves test")
            global successes
            successes += 1
            return
    failure("simpleMoves test")


def modifyGiven(file):
    '''
    This test checks whether the user can undo a cell value that was 
    inially given in the puzzle. You should not be able to undo 
    puzzle cells that were given. But you should be able to undo moves that 
    you added.
    '''
    s = "ERROR"
    for f in file:
        f = regex.sub('', f)
        if (s in f.upper().split()):
            success("modifyGiven test")
            global successes
            successes += 1
            return
    failure("modifyGiven test")

def badRowCol(file):
    '''
    This test checks for incorrect row and column inputs
    1 <= row <= 9
    1 <= col <= 9
    Code should inform user of error :
    "ERROR: Row and column numbers should be 1-9"
    Then prompt the same board for another move
    '''
    num = 0
    s = "ERROR"
    for f in file:
        f = regex.sub('', f)
        if (s in f.upper().split()):
            num += 1
    if (num == 4):
        success("badRowCol test")
        global successes
        successes += 1
        return
    else:
        failure("badRowCol test")

def badBoxEntry(file):
    '''
    This test checks whether the inputed number violates the 
    condition that no number can be repeated in a 3x3 segment of
    the board.
    '''
    num = 0
    s = "ERROR"
    for f in file:
        f = regex.sub('', f)
        if (s in f.upper().split()):
            num += 1
    if (num == 1):
        success("badBoxEntry test")
        global successes
        successes += 1
        return
    else:
        failure("badBoxEntry test")

def badRowEntry(file):
    '''
    This test checks whether the inputed number violates the 
    condition that no number can be repeated in a row segment of
    the board.
    '''
    num = 0
    s = "ERROR"
    for f in file:
        f = regex.sub('', f)
        if (s in f.upper().split()):
            num += 1
    if (num == 1):
        success("badRowEntry test")
        global successes
        successes += 1
        return
    else:
        failure("badRowEntry test")

def badColEntry(file):
    '''
    This test checks whether the inputed number violates the 
    condition that no number can be repeated in a column segment of
    the board.
    '''
    num = 0
    s = "ERROR"
    for f in file:
        f = regex.sub('', f)
        if (s in f.upper().split()):
            num += 1
    if (num == 1):
        success("badColEntry test")
        global successes
        successes += 1
        return
    else:
        failure("badColEntry test")        

def winCondition(file):
    '''
    Inputs a correct solution to the testFileEasy puzzle.
    Checks that the program says you solved the puzzle.
    Checks the win condition of the game.
    '''
    num = 0
    s = "SOLVED"
    for f in file:
        f = regex.sub('', f)
        if (s in f.upper().split()):
            num += 1
    if (num == 1):
        success("winCondition test")
        global successes
        successes += 1
        return
    else:
        failure("winCondition test")

def combinedTest(file):
    '''
    This tests checks each of the above situations in one program run.
    '''
    err = 0
    sov = 0
    s = "SOLVED"
    t = "ERROR"
    for f in file:
        f = regex.sub('', f)
        if (s in f.upper().split()):
            sov += 1
        if (t in f.upper().split()):
            err += 1
    if (err == 8 and sov == 1):
        success("combinedTest test")
        global successes
        successes += 1
        return
    else:
        failure("combinedTest test")


options = {
    0 : simpleMoves,
    1 : modifyGiven,
    2 : badRowCol, 
    3 : badBoxEntry,
    4 : badRowEntry,
    5 : badColEntry,
    6 : winCondition,
    7 : combinedTest,
}

for filename, code in zip(tests, codes):
    file = open(filename, "r")
    options[code](file);
    file.close()

print "OVERALL : ", successes, " / ", len(tests)