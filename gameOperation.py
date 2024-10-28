"""
- Create 4x4 matrix
- Pick two random points in the matrix:
    - Generate 2's in those spots in th matrix
- Each turn:
    - nextMove = Call Player's move
    - if left (moveLeft Funct - returns new matrix and score)
        - test all cells with their partner to the left. if the cell to the left is same value then combine them
    - if right (moveRight Funct)
        - test all cells with their partner to the right. if the cell to the right is same value then combine them
    - if up (moveUp Funct)
        - test all cells with their partner above. if the cell above is same value then combine them
    - if down (moveDown Funct)
        - test all cells with their partner below. if the cell below is same value then combine them

    ^^^Score counter: add the valu of combined cells to score

    - Find all empty cells
    - choose at random one of the empty cells
    - flip a coin: populate chosen cell with 2 if heads, 4 if false

    Tester if game is over:
    - if all no empty cells (val 0): 
        - are there any neighboring cells with the same value: NOT DONE
        - else: GAME OVER, return GAME OVER and Score
"""
import random
import playerMove

def flipCoin( p ):
    r = random.random()
    return r < p

def fillNextCell (gameMatrix, chanceOfTwo):
    """
    This function takes a gameMatrix in its current state, 
    finds the empty cells, chooses a random empty cell to be filled,
    then fills it with 2 at a prob of chanceOfTwo and 4 otherwise
    """
    #Looking for all "empty" cells
    emptyCells = []
    for row in range(4):
        for col in range(4):
            if gameMatrix[row][col]==0:
                emptyCells += [(row,col)]

    #pick one of the emptyCells to be filled, at random
    cellToFill = random.choice(emptyCells)            

    #True means new cell will be 2, false is 4
    isItTwo = flipCoin(chanceOfTwo)
    if isItTwo:
        newVal = 2
    else:
        newVal = 4

    #filling cell
    gameMatrix[cellToFill[0]][cellToFill[1]] = newVal
    return

def printCurrGame(gameMatrix, numRows, numCols):

    for row in range(numRows):
        print("|",end="")
        for col in range(numCols):
            print(gameMatrix[row][col],end="|")
        print()

    print()
    return

def shiftCellsLeft(gameMatrix, row, numCol):
    """
    Will go through row of gameMatrix and shift all valued cells to the left
    
    """
    for col in range(numCol):
        firstVal = col

        while gameMatrix[row][firstVal]==0:
            if firstVal == numCol-1:
                return
            firstVal+=1
        
        #here i is the col num of first non-zero val or func has returned bc rest of row is 0
        i = 0 
        for colShift in range(firstVal,numCol):
            #print("firstval=",firstVal,"colShift=",colShift,"col+i=",col+i)
            #printCurrGame(gameMatrix,4,4)
            gameMatrix[row][col+i] = gameMatrix[row][colShift]
            if firstVal != col:
                gameMatrix[row][colShift] = 0

            i+=1
    
    return #only reach this return if there is never a trailing line of 
    
def shiftCellsRight(gameMatrix, row, numCol):
    """
    Will go through row of gameMatrix and shift all valued cells to the left
    
    """
    for col in range(numCol):
        currCol = (numCol-1)-col
        firstVal = currCol

        while gameMatrix[row][firstVal]==0:
            if firstVal == 0:
                return
            firstVal-=1
        
        #here i is the col num of first non-zero val or func has returned bc rest of row is 0
        i = 0
        #here we have col val of first nonzero from right
        #we want to shift right 
        for i in range(firstVal+1): #0101
            gameMatrix[row][currCol-i] = gameMatrix[row][firstVal-i]
            if firstVal!=currCol:
                gameMatrix[row][firstVal-i] = 0
    
    return #only reach this return if there is never a trailing line of zeros

def shiftCellsUp(gameMatrix, col, numRow):
    """
    Will go through row of gameMatrix and shift all valued cells to the left
    
    """
    for row in range(numRow):
        firstVal = row

        while gameMatrix[firstVal][col]==0:
            if firstVal == numRow-1:
                return
            firstVal+=1
        
        #here i is the col num of first non-zero val or func has returned bc rest of row is 0
        i = 0 
        for rowShift in range(firstVal,numRow):
            #print("firstval=",firstVal,"colShift=",colShift,"col+i=",col+i)
            #printCurrGame(gameMatrix,4,4)
            gameMatrix[row+i][col] = gameMatrix[rowShift][col]
            if firstVal != row:
                gameMatrix[rowShift][col] = 0

            i+=1
    
    return #only reach this return if there is never a trailing line of 
        
def shiftCellsDown(gameMatrix, col, numRow):
    """
    Will go through row of gameMatrix and shift all valued cells to the left
    
    """
    for row in range(numRow):
        currRow = (numRow-1)-row
        firstVal = currRow

        while gameMatrix[firstVal][col]==0:
            if firstVal == 0:
                return
            firstVal-=1
        
        #here i is the col num of first non-zero val or func has returned bc rest of row is 0
        i = 0
        #here we have col val of first nonzero from right
        #we want to shift right 
        for i in range(firstVal+1): #0101
            gameMatrix[currRow-i][col] = gameMatrix[firstVal-i][col]
            if firstVal!=currRow:
                gameMatrix[firstVal-i][col] = 0
    
    return #only reach this return if there is never a trailing line of zeros
            
def matrixUpdate(gameMatrix,moveMade,gameScore,numCol,numRow):

    if moveMade == "left":
        for row in range(numRow):
            #this collapses all non-zero cells to the left
            shiftCellsLeft(gameMatrix,row,numCol)
            #this part combines cells of same value 
            for col in range(numCol-1):
                if gameMatrix[row][col] == gameMatrix[row][col+1]:
                    newCell = 2*gameMatrix[row][col]
                    gameScore += newCell
                    gameMatrix[row][col] = newCell
                    gameMatrix[row][col+1] = 0

                    shiftCellsLeft(gameMatrix,row,numCol)
    if moveMade == "right":
        for row in range(numRow):
            #this collapses all non-zero cells to the left
            shiftCellsRight(gameMatrix,row,numCol)
            #this part combines cells of same value 
            for col in range(numCol-1):
                currCol = (numCol-1)-col
                if gameMatrix[row][currCol] == gameMatrix[row][currCol-1]:
                    newCell = 2*gameMatrix[row][currCol]
                    gameScore += newCell
                    gameMatrix[row][currCol] = newCell
                    gameMatrix[row][currCol-1] = 0

                    shiftCellsRight(gameMatrix,row,numCol)

    if moveMade == "up":
        for col in range(numCol):
            #this collapses all non-zero cells to the left
            shiftCellsUp(gameMatrix,col,numRow)
            #this part combines cells of same value 
            for row in range(numRow-1):
                if gameMatrix[row][col] == gameMatrix[row+1][col]:
                    newCell = 2*gameMatrix[row][col]
                    gameScore += newCell
                    gameMatrix[row][col] = newCell
                    gameMatrix[row+1][col] = 0

                    shiftCellsUp(gameMatrix,col,numRow)  

    if moveMade == "down":
        for col in range(numCol):
            #this collapses all non-zero cells to the left
            shiftCellsDown(gameMatrix,col,numRow)
            #this part combines cells of same value 
            for row in range(numRow-1):
                currRow = (numRow-1)-row
                if gameMatrix[currRow][col] == gameMatrix[currRow-1][col]:
                    newCell = 2*gameMatrix[currRow][col]
                    gameScore += newCell
                    gameMatrix[currRow][col] = newCell
                    gameMatrix[currRow-1][col] = 0

                    shiftCellsDown(gameMatrix,col,numRow)              
    return gameScore

def isGameOver(gameMatrix,numRow,numCol):
    """
    Checks if there are any empty cells left (to be run after a matrix update);
    If there are no empties there, then it will return True for gameOver, otherwise it will return False    
    """
    for row in range(numRow):
        for col in range(numCol):
            if gameMatrix[row][col]==0:
                return False 
    
    return True

"""
    Running Game
"""
gameMatrix = [[0 for row in range(4)] for col in range(4)]

#game starts with 2 random cells having val 2
fillNextCell(gameMatrix,1)
fillNextCell(gameMatrix,1)

print("first fills")
printCurrGame(gameMatrix,4,4)


moveType = "randomMove"

playerScore = 0
moveCount = 0
gameIsOver = False

nextMove = playerMove.nextMove(moveType)
print("going",nextMove)
playerScore = matrixUpdate(gameMatrix,nextMove,playerScore,4,4)

while not gameIsOver:

    fillNextCell(gameMatrix,0.75)
    moveCount+=1

    printCurrGame(gameMatrix,4,4)
    print("score=",playerScore,"move #", moveCount)
    print()

    nextMove = playerMove.nextMove(moveType)
    print("going",nextMove)
    playerScore = matrixUpdate(gameMatrix,nextMove,playerScore,4,4)

    gameIsOver = isGameOver(gameMatrix,4,4)
