from random import choice
from json import loads

class Battle():
    def __init__(self, heroes : list, enemies : list):
        self.heroes = heroes
        self.enemies = enemies
        self.index_turn = 0
        self.state = "HERO_TURN"
        self.result_cmds_queue = []

    def add_cmd_to_queue(self, command):
        self.result_cmds_queue.append(command)

    def print_state(self):
        for hero in self.heroes:
            print(hero)
        for enemy in self.enemies:
            print(enemy)

    def get_current_unit(self):
        if self.state == "HERO_TURN":
            return self.heroes[self.index_turn]
        elif self.state == "ENEMY_TURN":
            return self.enemies[self.index_turn]

    def process_command(self, command):
        com = command['com']
        current_hero = self.heroes[self.index_turn]
        if com == "attack":
            if current_hero.ap >= 5:
                target_enemy_id = command['target_id']
                target_enemy = self.enemies[target_enemy_id]
                if target_enemy.hp > 0:
                    current_hero.attack(target_enemy)
                    current_hero.ap -= 5

                    self.add_cmd_to_queue({"com":"play_animation",
                                            "type":"hero", 
                                            "id":self.index_turn,
                                            "animation":"Attack"})

                    self.add_cmd_to_queue({"com":"update_hp",
                                            "type":"enemy", 
                                            "id":target_enemy_id,
                                            "new_hp":target_enemy.hp})
                    
                    

        elif com == "def":
            if current_hero.ap >= 3:
                current_hero.defense = True
                current_hero.ap -= 3
        elif com == "end":
            self.next_state()

    def process_enemy_turn(self):
        current_enemy = self.enemies[self.index_turn]
        alive_heroes = [hero for hero in self.heroes if hero.hp > 0]
        target_hero = choice(alive_heroes)
        target_hero_id = self.heroes.index(target_hero)
        current_enemy.attack(target_hero)

        self.add_cmd_to_queue({"com":"update_hp",
                                            "type":"hero", 
                                            "id":target_hero_id,
                                            "new_hp":target_hero.hp})
        
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

        elif self.state == "ENEMY_TURN":
            if self.index_turn == len(self.enemies) - 1:
                self.state = "HERO_TURN"
                self.index_turn = 0
            else:
                self.index_turn += 1

        if self.get_current_unit().hp <= 0:
            self.next_state()
        else:
            print(f"Зараз ходить {self.get_current_unit().name}")



