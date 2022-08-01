from random import randint

def skillRoll(modifier = 0):
    return randint(-9, 10) + modifier

def roll(diceAmount, diceType, modifier = 0):
    return sum([randint(1, diceType) for dice in range(diceAmount)]) + modifier