import pygame
import sys

from battle.battle import Battle
from battle.units import Hero
from battle.units import Enemy
from ui.sprite import Sprite
from ui.button import Button

# Ініціалізація
pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("PyGame TBS v0.1")

clock = pygame.time.Clock()
FPS = 60

font = pygame.font.Font("BF_Mnemonika_Regular.ttf", 32)

battle = Battle(
    heroes=[Hero("Герой 1", 20, 8, 10), Hero("Герой 2", 15, 8, 12)],
    enemies=[Enemy("Ворог 1", 15, 5), Enemy("Ворог 2", 10, 4)]
)

units_view = []

button1 = Button("Закінчити хід!", 
                font,
                position=(300, 500), 
                callback = lambda: battle.process_command({"com": "end"}))

for id, hero in enumerate(battle.heroes):
    hero_view_dict = {}
    hero_view_dict['type'] = 'hero'
    hero_view_dict['id'] = id
    hero_view_dict['sprite'] = Sprite(screen, "sprites/hero1/idle.png", [200, int(600*((id+1)/(len(battle.heroes)+1)))])
    hero_view_dict['sprite'].add_animation('Attack', 'sprites/hero1/Attack', 4, 250, False)
    hero_view_dict['sprite'].scale(3)
    hero_view_dict['name_text'] = font.render(hero.name, True, (0, 0, 0))
    hero_view_dict['hp_value'] = hero.hp

    units_view.append(hero_view_dict)

for id, enemy in enumerate(battle.enemies):
    enemy_view_dict = {}
    enemy_view_dict['type'] = 'enemy'
    enemy_view_dict['id'] = id
    enemy_view_dict['sprite'] = Sprite(screen, "sprites/enemy1/idle.png", [600, int(600*((id+1)/(len(battle.enemies)+1)))])
    enemy_view_dict['sprite'].scale(2)
    enemy_view_dict['sprite'].set_mirrored(True)
    enemy_view_dict['name_text'] = font.render(enemy.name, True, (0, 0, 0))
    enemy_view_dict['hp_value'] = enemy.hp

    units_view.append(enemy_view_dict)

#Основний цикл програми
runnig = True
while runnig:
    for event in pygame.event.get(): # Обробка подій
        if event.type == pygame.QUIT:
            runnig = False
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for unit_view in units_view:
                if unit_view['type'] == 'enemy':
                    if unit_view['sprite'].get_rect().collidepoint(event.pos) and battle.state == "HERO_TURN":
                        battle.process_command({"com":"attack", "target_id":unit_view['id']})

        button1.handle(event)

    screen.fill((100, 100, 100))

    while battle.result_cmds_queue:
        current_com = battle.result_cmds_queue.pop(0)
        for unit_view in units_view:
            if unit_view['type'] == current_com['type'] and unit_view['id'] == current_com['id']:
                if current_com['com'] == 'update_hp':
                    unit_view['hp_value'] = current_com['new_hp']
                if current_com['com'] == 'play_animation':
                    unit_view['sprite'].set_animation(current_com['animation'])

    for unit_view in units_view:
        unit_view['sprite'].draw()
        unit_x, unit_y = unit_view['sprite'].position
        unit_hp_text = font.render("HP: " + str(unit_view['hp_value']).replace("0", "O"), True, (0, 0, 0))
        screen.blit(unit_view['name_text'], (unit_x - 30, unit_y + 70))
        screen.blit(unit_hp_text, (unit_x - 30, unit_y + 110))

    button1.render(screen)

    if battle.state == "ENEMY_TURN":
        battle.process_enemy_turn()

    pygame.display.flip() # Малюємо наступний кадр
    clock.tick(FPS)


#Завершення програми
pygame.quit()
sys.exit()