from random import randint

class Unit():
    def __init__(self, name, hp, max_dmg, ):
                #sprite):
        self.name = name
        self.hp = hp
        self.max_dmg = max_dmg
        #self.sprite = sprite

    def attack(self, target_unit):
        current_damage = int((randint(75, 100)/100)*self.max_dmg)
        target_unit.was_attacked(current_damage)

    def was_attacked(self, dmg):
        self.hp -= dmg

    def __str__(self):
        return f"{self.name} {self.hp}"