"""
Designed to use the q operations by looking a down a depth of n and returning maxes all the way up
"""
import approxQLearning
import gameOperation
import random

def getBestQValue(gameMatrix, gameScore, epsilon, currDepth, depth, weights):
    actions = ['left', 'right','up','down']
    QVal = [0,0,0,0]
    features = [0,0,0,0]
    testingScore = gameScore

    for i in range(len(actions)):
        testingMatrix = [row[:] for row in gameMatrix]
        currDepth+=1

        if depth == currDepth:
            nodeQVal = approxQLearning.bestMove(testingMatrix,testingScore,weights,0)
            
        else:
            testingScore = gameOperation.matrixUpdate(testingMatrix,actions[i], testingScore, 4, 4)
            gameOperation.fillNextCell(testingMatrix,0.75)

            gameIsOver = gameOperation.isGameOver(testingMatrix,4,4)
            if gameIsOver:
                nodeQVal = [0,0,approxQLearning.featExtractor(testingMatrix,actions[i],testingScore)]
            nodeQVal = getBestQValue(testingMatrix,testingScore,0,currDepth,depth,weights)

        QVal[i] = nodeQVal[1]
        features[i] = nodeQVal[2]

    if depth==1:
        takeRandom = gameOperation.flipCoin(epsilon)
        if takeRandom:
            actionIndex = random.choice([0,1,2,3])
            return [actions[i],QVal[i],features[i]]
    
    bestQ = -1000
    maxIndex = -1
    for i in range(len(actions)):
        if QVal[i]>bestQ:
            bestQ = QVal[i]
            bestMove = actions[i]
            maxIndex = i

    return [bestMove,bestQ,actions[i]]

def treeupdate(gameMatrix, reward, gameScore, discount, weights, alpha, features, prevQVal):
        """
        Should update your weights based on transition

        w_i<-w_i + alpha*[difference]*f_i(s,a)
        difference = [r + gamma*maxQ(s',a')]-Q(s,a)
        """ 

        projectedMaxOptimalAction = bestMove(gameMatrix, gameScore, weights,0)
        if projectedMaxOptimalAction=="Exceeded QValue lower limit":
            return "Exceeded QValue lower limit"
        #print("projectedMaxOptimal = ", projectedMaxOptimalAction)
        #print("prevQVal = ", prevQVal)

        difference = (reward + discount*projectedMaxOptimalAction[1]) - prevQVal 

        #print("difference = [",reward,"+",discount,"*",projectedMaxOptimalAction[1],"] - ",prevQVal,"=   ",difference)

        for i in range(7):
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