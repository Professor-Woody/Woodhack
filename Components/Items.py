from random import randint


class Item:
    melee = None
    ranged = None
    Defence = None
    Use = None

    def __init__(self, entity, name):
        self.entity = entity
        self.name = name


class Attack:
    def __init__(self, item, attackModifier, damageDice, damageBonus):
        self.item = item
        self.attackModifier = attackModifier
        self.dice = damageDice
        self.damageBonus = damageBonus

    def attack(self, attackModifier=0):
        return self.attackModifier + attackModifier + + randint(1,20)


    def damage(self, damageModifier=0):
        return self.damageBonus + sum([randint(1,dice) for dice in self.dice]) + damageModifier


class Defence:
    def __init__(self, item, defenceModifier):
        self.item = item
        self.defenceModifier = defenceModifier

    def defend(self, defenceModifier=0):
        return self.defenceModifier + defenceModifier

class Use:
    def use(self):
        print ("Nothing happens (this item can't be used")