"""
This will be the main file where code is run

ideas for diff qlearning methods: 
- try updating weights before and after random fill has occured
- try different epsilon values
- try a round or two of training the weights before going and see it improves beginning performance and even performance over time
- dynamic learning rate?
"""
import gameOperation
import approxQLearning
import playerMove
import util

weights = [1,1,1,1,1]
discount = 3
alpha = 0.5

gameMatrix = [[0 for row in range(4)] for col in range(4)]

#game starts with 2 random cells having val 2
gameOperation.fillNextCell(gameMatrix,1)
gameOperation.fillNextCell(gameMatrix,1)

print("first fills")
gameOperation.printCurrGame(gameMatrix,4,4)

playerScore = 0
moveCount = 0
gameIsOver = False

moveType = "approxQLearning"


while not gameIsOver:
     
    nextMove = playerMove.nextMove(moveType,gameMatrix,playerScore,weights,moveCount)
    
    #make the move
    print("going ",nextMove[0])
    scoreBeforeMove = playerScore

    playerScore = gameOperation.matrixUpdate(gameMatrix,nextMove[0],playerScore,4,4)
     
    reward = playerScore-scoreBeforeMove
    
    if moveType == "approxQLearning":
    #update the weights
        approxQLearning.update(gameMatrix, reward, playerScore,discount,weights,alpha,nextMove[2],nextMove[1],moveCount)
    
    #fill the random cell for next move and update moveCount and the reward incurred
    gameOperation.fillNextCell(gameMatrix,0.75)

    moveCount+=1

    #display game state
    gameOperation.printCurrGame(gameMatrix,4,4)
    print("score=",playerScore,"move #", moveCount)
    print()
       
    gameIsOver = gameOperation.isGameOver(gameMatrix,4,4)