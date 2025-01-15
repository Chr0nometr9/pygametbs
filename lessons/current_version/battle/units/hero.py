from units.unit import Unit

class Hero(Unit):
    def __init__(self, name : str, hp : int, ap : int, max_dmg : int):
        super().__init__(name, hp, max_dmg)
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
        if self.ap >= 2:
            heal_amount = self.ap // 2
            self.hp += heal_amount
