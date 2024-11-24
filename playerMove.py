"""
Player action file:
NextMove
    - given a move argument, it will call the correct type of policy choice
RandomMove: picks random move of left, right, up, and down

"""
import random 
import approxQLearning
import treeLearning

def flipCoin( p ):
    r = random.random()
    return r < p

def makeRandomMove():
    moves = ["up","down","left","right"]
    randomMove = random.choice(moves)
    return [randomMove]


def nextMove(typeOfAgent, gameMatrix, gameScore, weights,epsilon,depth):
    if typeOfAgent=="randomMove":
        return makeRandomMove()
    if typeOfAgent=="approxQLearning":
        return approxQLearning.getBest(gameMatrix, gameScore,epsilon,0,depth,weights)

    
    return "up"
