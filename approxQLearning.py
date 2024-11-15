"""
Features: 
- average value of a block (prob not going to be good)
- number of zeros 
- difference in avg value of half grid vs other
- monotonicity?
- max tile location from corner

What is a state? Need a generalization
    - a binary representation of the game matrix before the random 2/4 is added where 1 is a tile with a val, 0 is a tile with no val

- want to code args for the feature weights


Q(s,a)=w_1*f_1(s,a)+w_2*f_2(s,a)+...+w_n*f_n(s,a)
w_i<-w_i + alpha*[difference]*f_i(s,a)
difference = [r + gamma*maxQ(s',a')]-Q(s,a)
"""
import util
import gameOperation
import playerMove
import random

def initApproxLearning():
    weights = util.Counter() 
    qVals = util.Counter()
    return       

def howManyZeros(gameMatrix, numRow, numCol):
    """
    returns avg value of blocks projected in the matrix
    """
    numZeros = 0
    for row in range(numRow):
        for col in range(numCol):
            if gameMatrix[row][col]==0:
                numZeros+=1
    
    return numZeros

def diffInMatrixDistribution(gameMatrix,numRow,numCol):
    """
    Determines the ratio of weights in how many tiles are value versus empty in bottom:top
    favors a game that is heavier on the bottom in tile distribution
    """
    topHalf=0
    bottomHalf=0
    for row in [0,1]:
        for col in range(numCol):
            topHalf+=gameMatrix[row][col]
    for row in [2,3]:
        for col in range(numCol):
            bottomHalf+=gameMatrix[row][col]

    return (bottomHalf+0.1)/(topHalf+0.1)

def maxLocation(gameMatrix, numRow,numCol):
    """
    returns values with varying value depending on where the max tile is located. Below is the order in increasing rank of ideal:
    1. [1,1] or [1,2] (returns 1)
    2. [2,1] or [2,2] (returns 2)
    3. [0,1] or [0,2] or [1,0] or [1,3] (returns 4)
    4. [0,0] or [0,3] (returns 5)
    5. [2,0] or [2,3] or [3,1] or [3,2] (returns 7)
    6. [3,0] or [3,3] (returns 9)

    a tie for highest tile will just go to the last tile of that valued looked at

    this method favors max tiles being on the outer edge, specifically in ccrners and in the bottom half of the board
    """
    #finding max tile
    maxLoc = (-1,-1)
    maxTile=-1
    for row in range(numRow):
        for col in range(numCol):
            if gameMatrix[row][col]>=maxTile:
                maxTile = gameMatrix[row][col]
                maxLoc = (row,col)

    #returning feature val based on location
    if maxLoc==(1,1) or maxLoc==(1,2):
        return 1
    if maxLoc==(2,1) or maxLoc==(2,2):
        return 2
    if maxLoc==(0,1) or maxLoc==(0,2) or maxLoc==(1,0) or maxLoc==(1,3):
        return 4
    if maxLoc==(0,0) or maxLoc==(0,3):
        return 5
    if maxLoc==(2,0) or maxLoc==(2,3) or maxLoc==(3,1) or maxLoc==(3,2):
        return 7
    if maxLoc==(3,0) or maxLoc==(3,3):
        return 9

def tileDifference(gameMatrix, numRow, numCol):
    """
    This function calculates the sum of the differences between tiles moving in a snake pattern starting at the bottom left corner 

    looking to favor lower differences in values

    does not count difference when one of the blocks is a 0 since that could unfavorably penalty large values near empty tiles
    """
    totalDiff = 0
    for col in range(numCol-1):
        if (gameMatrix[3][col]!=0) and (gameMatrix[3][col+1]!=0):
            totalDiff+=abs(gameMatrix[3][col]-gameMatrix[3][col+1])
          
    if (gameMatrix[3][3]!=0) and (gameMatrix[2][3]!=0):
        totalDiff+=abs(gameMatrix[3][3]-gameMatrix[2][3])
   
    for col in range(numCol-1):
        if (gameMatrix[2][3-col]!=0) and (gameMatrix[2][2-col]!=0):
            totalDiff+=abs(gameMatrix[2][3-col]-gameMatrix[2][2-col])
    
    if (gameMatrix[2][0]!=0) and (gameMatrix[1][0]!=0):
        totalDiff+=abs(gameMatrix[2][0]-gameMatrix[1][0])
    
    for col in range(numCol-1):
        if (gameMatrix[1][col]!=0) and (gameMatrix[1][col+1]!=0):
            totalDiff+=abs(gameMatrix[1][col]-gameMatrix[1][col+1])
     
    if (gameMatrix[1][3]!=0) and (gameMatrix[0][3]!=0):
        totalDiff+=abs(gameMatrix[1][3]-gameMatrix[0][3])
        
    for col in range(numCol-1):
        if (gameMatrix[0][3-col]!=0) and (gameMatrix[0][2-col]!=0):
            totalDiff+=abs(gameMatrix[0][3-col]-gameMatrix[0][2-col])
           
    return -totalDiff

def featExtractor(gameMatrix, action, gameScore, moveCount):
    """ 
    will take the gameMatrix and return a vector of feature values

    these are the following features in order:
    0. how many zeros
    1. difference in the total value of top half of the grid vs the bottom
    2. Max value tile's location     
    3. New score
    4. Sum of the difference between tiles 

    """
    testingMatrix = [row[:] for row in gameMatrix]
    initScore = gameScore
    newScore = gameOperation.matrixUpdate(testingMatrix,action,initScore,4,4)

    features = [0 for row in range(5)]
    features[0] = howManyZeros(testingMatrix,4,4)
    features[1] = diffInMatrixDistribution(testingMatrix,4,4)
    features[2] = maxLocation(testingMatrix,4,4)
    features[3] = moveCount
    features[4] = tileDifference(testingMatrix,4,4)

    """
    #normalize features
    sumOfFeats = 0
    for i in range(5):
        sumOfFeats+=features[i]

    for i in range(5):
        features[i]=features[i]/sumOfFeats
    #for i in range(5):
        #print("feature ",i,":",features[i])
    """    

    return features

def getQValue(gameMatrix,action,gameScore,weights,moveCount):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
                
        features = featExtractor(gameMatrix,action,gameScore,moveCount)
        QVal = 0

        for i in range(len(features)):
            QVal += weights[i]*features[i]
                
        return [QVal,features]

def bestMove(gameMatrix, gameScore,weights,moveCount):
    """
    will look at the q val for each (s,a) pair and then deteremine the max and return that action

    tie breaking: will return a random move amongst max moves   
    """

    actions = ['left','right','up','down']

    bestQ = -1000
    bestActionIndices=[]
    bestFeatures = []
    
    for i in range(len(actions)):
        qValandFeat = getQValue(gameMatrix,actions[i],gameScore,weights,moveCount)
                
        if qValandFeat[0]>bestQ:
            bestActionIndices = [i]
            bestQ=qValandFeat[0]
            bestFeatures = [qValandFeat[1]]
        elif qValandFeat[0]==bestQ:
            bestActionIndices = bestActionIndices + [i]
            bestFeatures=bestFeatures+[qValandFeat[1]]
                       
    if len(bestActionIndices)==1:
        bestMove = actions[bestActionIndices[0]]
        featureSet = bestFeatures[0]       
    elif len(bestActionIndices)>1:
        moveIndex = random.choice(bestActionIndices)
        print(moveIndex)
        for i in range(len(bestActionIndices)):
            if bestActionIndices[i]==moveIndex:
                featureSet = bestFeatures[i]

        bestMove = actions[moveIndex]        
    else:
        featureSet = []
        bestMove = "noBestActionChosen"

    return [bestMove,bestQ,featureSet]

def update(gameMatrix, reward, gameScore, discount, weights, alpha, features, prevQVal,moveCount):
        """
        Should update your weights based on transition

        w_i<-w_i + alpha*[difference]*f_i(s,a)
        difference = [r + gamma*maxQ(s',a')]-Q(s,a)
        """ 

        projectedMaxOptimalAction = bestMove(gameMatrix, gameScore, weights,moveCount)
        print("projectedMaxOptimal = ", projectedMaxOptimalAction)
        print("prevQVal = ", prevQVal)

        difference = (reward + discount*projectedMaxOptimalAction[1]) - prevQVal 

        print("difference = [",reward,"+",discount,"*",projectedMaxOptimalAction[1],"] - ",prevQVal,"=   ",difference)

        for i in range(5):
            weights[i] += alpha*difference*features[i]
            print("weight ",i,"=","prev weight +",alpha,"*",difference,"*",features[i],"=   ",weights[i])

        return 
