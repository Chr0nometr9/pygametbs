from units.hero import Hero
from units.enemy import Enemy
from random import choice
from json import loads

class Battle():
    def __init__(self, heroes : list, enemies : list):
        self.heroes = heroes
        self.enemies = enemies
        self.index_turn = 0
        self.state = "HERO_TURN"
        #self.queue = []
    
    def print_state(self):
        for hero in self.heroes:
            print(hero)
        for enemy in self.enemies:
            print(enemy)

    def process_command(self, command):
        com = command['com']
        current_hero = self.heroes[self.index_turn]
        if com == "attack":
            if current_hero.ap >= 5:
                target_enemy_id = command['target_id']
                target_enemy = self.enemies[target_enemy_id]
                current_hero.attack(target_enemy)
                current_hero.ap -= 5
        elif com == "def":
            if current_hero.ap >= 3:
                current_hero.defense = True
                current_hero.ap -= 3
        elif com == "end":
            return com

    def process_turn(self):
        if self.state == "HERO_TURN":
            end_flag = False
            while not end_flag:
                command = loads(input())#self.queue.pop(0)
                result = self.process_command(command)
                if result == "end":
                    end_flag = True
        elif self.state == "ENEMY_TURN":
            current_enemy = self.enemies[self.index_turn]
            target_hero = choice(self.heroes)
            current_enemy.attack(target_hero)

        self.next_state()

    def next_state(self):
        self.print_state()
        if self.state == "HERO_TURN":
            if self.index_turn == len(self.heroes) - 1:
                self.state = "ENEMY_TURN"
                self.index_turn = 0
            else:
                self.index_turn += 1
                self.heroes[self.index_turn].rest()
        if self.state == "ENEMY_TURN":
            if self.index_turn == len(self.enemies) - 1:
                self.state = "HERO_TURN"
                self.index_turn = 0
            else:
                self.index_turn += 1

battle = Battle(
    heroes=[Hero("Герой 1", 10, 8, 10), Hero("Герой 2", 15, 5, 8)],
    enemies=[Enemy("Ворог 1", 10, 5), Enemy("Ворог 2", 12, 4)]
)

battle.process_turn()
battle.process_turn()

