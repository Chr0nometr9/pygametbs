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

class Hero(Unit):
    def __init__(self, name : str, hp : int, ap : int, max_dmg : int):
        super().__init__(name, hp, max_dmg)
        self.max_ap = ap
        self.ap = ap
        self.defense = False
        
    def attack(self, target_enemy):
        super().attack(target_enemy)
        self.ap -= 5
    
    def was_attacked(self, dmg):
        if self.defense:
            dmg //= 2
            self.defense = False
        self.hp -= dmg

    def rest(self):
        '''if self.ap >= 2:
            heal_amount = self.ap // 2
            self.hp += heal_amount'''
        self.ap = self.max_ap

class Enemy(Unit):
    pass