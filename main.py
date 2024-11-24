"""
NAME: Taylor McManus, Isaac Heim

Code Documentation: I used chatgpt to help with basic coding structures, debugging, and brainstorming for why the learning method wasnt worked (https://chatgpt.com/share/67429b19-08b0-8009-98c1-c1653e7cfe60). I also got help from Lt Kenworthy in EI. He suggested I implement epsilon exploration and training games to see if the method would improve. 

Date: 11/23/2025

This will be the main file where code is run

In the configuration it is in right now, it is designed to run multiple games and send result data to an excel
"""
import gameOperation
import approxQLearning
import playerMove
import util
import pandas

#weights = util.Counter()
discount = 0.99
alpha = 0.5
depths = [0,1,2,3,4,5] #here, any q value investigation will evaluate based on a tree that looks at q(s,a) for state s of n steps forward; ie. a traditional method would require a depth of 0
epsilon=0.5
varyingDepth = [['Depth', 'EndScores']] #header in excel

moveType = "approxQLearning"
numTrainingGames = 0

#iterating through varying depth values
for i in range(len(depths)):
    playerScores = [0 for k in range(30)] #array of score values to be sent to excel
    print("beginning testing for depth",depths[i])

    #run 30 games for each depth to get average of end scores
    for j in range(30):
        print("Round Number ", j)

        weights = util.Counter()

        for m in range(numTrainingGames+1):    

            playerScore = 0
            moveCount = 0
            gameIsOver = False

            gameMatrix = [[0 for row in range(4)] for col in range(4)]

            #game starts with 2 random cells having val 2
            gameOperation.fillNextCell(gameMatrix,1)
            gameOperation.fillNextCell(gameMatrix,1)

            #print("first fills")
            #gameOperation.printCurrGame(gameMatrix,4,4)
                
            """
            if m < numTrainingGames[i]:
                epsilon = 0
            else:
                epsilon = 0.5
            """    

            while not gameIsOver:
                
                nextMove = playerMove.nextMove(moveType,gameMatrix,playerScore,weights,epsilon,depths[i])
                
                if nextMove=="Exceeded QValue lower limit":
                    gameIsOver = True
                    continue

                #make the move
                #print("going ",nextMove[0])
                scoreBeforeMove = playerScore

                playerScore = gameOperation.matrixUpdate(gameMatrix,nextMove[0],playerScore,4,4)
                
                reward = playerScore-scoreBeforeMove
                moveCount+=1

                #fill the random cell for next move 
                gameOperation.fillNextCell(gameMatrix,0.75)
                
                if moveType == "approxQLearning":
                #update the weights
                    update = approxQLearning.update(gameMatrix, reward, playerScore,discount,weights,alpha,nextMove[2],nextMove[1],depths[i])
                    if update == "Exceeded QValue lower limit":
                        gameIsOver = True
                        #print("Exceeded QVal Lower Limit!")
                        continue
                        
                #display game state
                #gameOperation.printCurrGame(gameMatrix,4,4)
                
                #print("score=",playerScore,"move #", moveCount)
                #print()
                
                gameIsOver = gameOperation.isGameOver(gameMatrix,4,4)

                #if gameIsOver:
                    #print("score=",playerScore,"move #", moveCount)
                    #print()
        print("end score:",playerScore)
        playerScores[j] = playerScore            
    varyingDepth = varyingDepth + [[depths[i]]+playerScores]

#Printing findings to a output excel file using pandas
fileName = "varyingDepthDiscount99.xlsx"
df = pandas.DataFrame(varyingDepth)
df.to_excel(fileName,index=False)
print("Data written to ", fileName)