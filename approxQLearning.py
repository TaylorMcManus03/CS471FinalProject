"""
Q(s,a)=w_1*f_1(s,a)+w_2*f_2(s,a)+...+w_n*f_n(s,a)
w_i<-w_i + alpha*[difference]*f_i(s,a)
difference = [r + gamma*maxQ(s',a')]-Q(s,a)
"""
import util
import gameOperation
import playerMove
import random

def initApproxLearning():
    #was not used
    weights = util.Counter() 
    qVals = util.Counter()
    return       

def howManyZeros(gameMatrix, numRow, numCol):
    """
    returns number of tiles with value zero
    """
    numZeros = 0
    for row in range(numRow):
        for col in range(numCol):
            if gameMatrix[row][col]==0:
                numZeros+=1
    
    return numZeros

def diffInMatrixDistribution(gameMatrix,numRow,numCol):
    """
    Determines the ratio of values in tiles on bottom to top
    higher value for a game that is heavier on the bottom in tile distribution
    """
    topHalf=0
    bottomHalf=0
    for row in [0,1]:
        for col in range(numCol):
            topHalf+=gameMatrix[row][col]
    for row in [2,3]:
        for col in range(numCol):
            bottomHalf+=gameMatrix[row][col]

    return (bottomHalf+0.1)/(topHalf+0.1) #adding 0.1 to avoid dividing by zero

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
           
    return -totalDiff #negative so more difference is lower value

def weightBiasedMatrixEvaluation(gameMatrix):
    """
    will sum the values in all of the tiles multiplied by weights that are larger in magnitude based on their location
    matrix of multipliers:
    |5|6|6|5|
    |3|4|4|3|
    |1|2|2|1|
    |0|1|1|0|
    """
    sum = 0
    sum+= gameMatrix[0][0]*5
    sum+= gameMatrix[0][3]*5
    sum+= gameMatrix[0][1]*6
    sum+= gameMatrix[0][2]*6
    sum+= gameMatrix[1][0]*3
    sum+= gameMatrix[1][3]*3
    sum+= gameMatrix[1][2]*4
    sum+= gameMatrix[1][3]*4
    sum+= gameMatrix[2][0]*1
    sum+= gameMatrix[2][3]*1
    sum+= gameMatrix[2][1]*2
    sum+= gameMatrix[2][2]*2
    sum+= gameMatrix[3][0]*0
    sum+= gameMatrix[3][3]*0
    sum+= gameMatrix[3][1]*1
    sum+= gameMatrix[3][2]*1

    return sum

def numMatchingTiles(gameMatrix, numRow, numCol):
    """
    returns how many tiles are the same value looking through the columns and rows at the same time
    """
    numMatches=0
    for col in range(numCol-1):
        for row in range(numRow-1):
            if gameMatrix[row][col]==gameMatrix[row+1][col]:
                numMatches+=1
            if gameMatrix[col][row]==gameMatrix[col][row+1]:
                numMatches+=1
    
    return numMatches

def featExtractor(gameMatrix, action, gameScore):
    """ 
    will take the gameMatrix and return a vector of feature values

    these are the following features in order:
    0. how many zeros
    1. difference in the total value of top half of the grid vs the bottom
    2. Max value tile's location     
    3. New score
    4. Sum of the difference between tiles 
    5. Gradient weighted sem of tile value
    6. Number of matching adjacent tiles

    """
    testingMatrix = [row[:] for row in gameMatrix]
    initScore = gameScore
    newScore = gameOperation.matrixUpdate(testingMatrix,action,initScore,4,4)
    #print("extracting features for going ", action)
    #gameOperation.printCurrGame(testingMatrix,4,4)

    features = [0 for row in range(7)]
    features[0] = howManyZeros(testingMatrix,4,4)
    features[1] = diffInMatrixDistribution(testingMatrix,4,4)
    features[2] = maxLocation(testingMatrix,4,4)
    features[3] = newScore-initScore
    features[4] = tileDifference(testingMatrix,4,4)
    features[5] = weightBiasedMatrixEvaluation(testingMatrix)
    features[6] = numMatchingTiles(testingMatrix, 4,4)

    """
    for i in range(5):
        print("feature ", i, ": ", features[i])
    """
    
    #normalize features
    sumOfFeats = 0
    for i in range(7):
        sumOfFeats+=features[i]

    if sumOfFeats==0: # to avoid dividing by zero
        sumOfFeats = 0.00000001

    for i in range(7):
        features[i]=features[i]/sumOfFeats
    #for i in range(5):
        #print("feature ",i,":",features[i])

    return features

def getQValue(gameMatrix,action,gameScore,weights):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
                
        features = featExtractor(gameMatrix,action,gameScore)
        QVal = 0

        for i in range(len(features)):
            QVal += weights[i]*features[i]
                
        return [QVal,features]

def bestMove(gameMatrix, gameScore,weights,epsilon):
    """
    will look at the q val for each (s,a) pair and then deteremine the max and return that action

    tie breaking: will return a random move amongst max moves   
    """

    actions = ['left','right','up','down']

    bestQ = -1000
    bestActionIndices=[]
    bestFeatures = []

    #epsilon exploration
    takeRandomAct = gameOperation.flipCoin(epsilon)
    if takeRandomAct:
        #print("RANDOM ACT BEING TAKEN")
        randomMove = random.choice(actions)
        qValandFeat = getQValue(gameMatrix, randomMove, gameScore, weights)
        return [randomMove, qValandFeat[0], qValandFeat[1]]
    
    #finding max Q(s,a)
    for i in range(len(actions)):
        qValandFeat = getQValue(gameMatrix,actions[i],gameScore,weights)
                
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
        #print(moveIndex)
        for i in range(len(bestActionIndices)):
            if bestActionIndices[i]==moveIndex:
                featureSet = bestFeatures[i]

        bestMove = actions[moveIndex]        
    else: #if there is no best action (ie. all q values are more negative than the threshold bestQ initializer
        featureSet = []
        bestMove = "noBestActionChosen"
        return "Exceeded QValue lower limit"
    return [bestMove,bestQ,featureSet]

def getBest(gameMatrix, gameScore, epsilon, currDepth, depth, weights):
    """
    this is the recursive version of bestMove used when a tree search (ie depth>0) is being implemented

    it refers back to bestMove to get a Q val evaluation when it recurses down to the identified depth; then it goes all the way up returning max q vals
    """
    actions = ['left', 'right','up','down']
    QVal = [0,0,0,0]
    features = [0,0,0,0]
    testingScore = gameScore
    testingMatrix = [row[:] for row in gameMatrix]

    if depth == 0:
        return bestMove(testingMatrix,testingScore,weights,0)
    
    currDepth+=1

    for i in range(len(actions)):
        testingMatrix = [row[:] for row in gameMatrix]
        
        if depth == currDepth:
            nodeQVal = bestMove(testingMatrix,testingScore,weights,0)
            if nodeQVal == "Exceeded QValue lower limit":
                nodeQVal = [actions[i],-1000,[0,0,0,0,0,0,0,0.1]] #hopefully if a node ends in a really low qval, this will bound it at the lowest possible value the program will allow to keep it runnign and then other nodes will beat it out
            
        else:

            testingScore = gameOperation.matrixUpdate(testingMatrix,actions[i], testingScore, 4, 4)
            gameIsOver = gameOperation.isGameOver(testingMatrix,4,4)

            if gameIsOver:
                nodeQVal = [0,0,featExtractor(testingMatrix,actions[i],testingScore)]
            else:
                gameOperation.fillNextCell(testingMatrix,0.75)
                nodeQVal = getBest(testingMatrix,testingScore,0,currDepth,depth,weights)            

        QVal[i] = nodeQVal[1]
        features[i] = nodeQVal[2]

    if currDepth==1:
        takeRandom = gameOperation.flipCoin(epsilon)
        if takeRandom:
            actionIndex = random.choice([0,1,2,3])
            return [actions[i],QVal[i],features[i]]
    
    bestQ = -1000
    maxIndex = -1
    bestAction = "No Action Chosen"
    for i in range(len(actions)):
        if type(QVal[i])!=int:
            QVal[i] = 0
        if QVal[i]>bestQ:
            bestQ = QVal[i]
            bestAction = actions[i]
            maxIndex = i
    
    if bestAction == "No Action Chosen":
        return "Exceeded QValue lower limit"

    return [bestAction,bestQ,features[i]]

def update(gameMatrix, reward, gameScore, discount, weights, alpha, features, prevQVal, depth):
        """
        Should update your weights based on transition

        w_i<-w_i + alpha*[difference]*f_i(s,a)
        difference = [r + gamma*maxQ(s',a')]-Q(s,a)
        """ 
        if depth==0:
            projectedMaxOptimalAction = bestMove(gameMatrix,gameScore,weights,0)
        else:
            projectedMaxOptimalAction = getBest(gameMatrix,gameScore,0,0,depth,weights)
        
        
        if projectedMaxOptimalAction=="Exceeded QValue lower limit":
            return "Exceeded QValue lower limit"
        #print("projectedMaxOptimal = ", projectedMaxOptimalAction)
        #print("prevQVal = ", prevQVal)

        #print("difference = [",reward,"+",discount,"*",projectedMaxOptimalAction[1],"] - ",prevQVal)
        difference = (reward + discount*projectedMaxOptimalAction[1]) - prevQVal 

        #print("difference = [",reward,"+",discount,"*",projectedMaxOptimalAction[1],"] - ",prevQVal,"=   ",difference)

        for i in range(7):
            #print("weight ",i,"=",weights[i] ,"+",alpha,"*",difference,"*",features[i])
            weights[i] += alpha*difference*features[i]
            #print("weight ",i,"=","prev weight +",alpha,"*",difference,"*",features[i],"=   ",weights[i])

        """
        #trying to normalize weights
        sumOfWeights = 0
        for i in range(7):
            sumOfWeights+=weights[i]
        if sumOfWeights!=0:
            for i in range(7):
                weights[i]=weights[i]/sumOfWeights
        """
                
        return 

