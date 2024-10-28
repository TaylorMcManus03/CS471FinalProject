"""
Player action file:
NextMove
    - given a move argument, it will call the correct type of policy choice
RandomMove: picks random move of left, right, up, and down

"""
import random 


def makeRandomMove():
    moves = ["up","down","left","right"]
    return random.choice(moves)


def nextMove(typeOfAgent):
    if typeOfAgent=="randomMove":
        return makeRandomMove()
    
    return "up"
