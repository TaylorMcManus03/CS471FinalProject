"""
Player action file:
NextMove
    - given a move argument, it will call the correct type of policy choice
RandomMove: picks random move of left, right, up, and down

"""
import random 
import approxQLearning


def makeRandomMove():
    moves = ["up","down","left","right"]
    randomMove = random.choice(moves)
    return [randomMove]


def nextMove(typeOfAgent, gameMatrix, gameScore, weights,moveCount):
    if typeOfAgent=="randomMove":
        return makeRandomMove()
    if typeOfAgent=="approxQLearning":
        return approxQLearning.bestMove(gameMatrix,gameScore,weights,moveCount)
    
    
    return "up"
