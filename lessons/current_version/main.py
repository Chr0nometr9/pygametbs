import pygame
import sys

import pygame.tests
from battle.battle import Battle
from battle.units import Hero
from battle.units import Enemy
from ui.sprite import Sprite

# Ініціалізація
pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("PyGame TBS v0.1")

clock = pygame.time.Clock()
FPS = 60

font = pygame.font.Font("BF_Mnemonika_Regular.ttf", 32)

battle = Battle(
    heroes=[Hero("Герой 1", 1, 8, 10)],
    enemies=[Enemy("Ворог 1", 10, 5), Enemy("Ворог 2", 12, 4)]
)

heroes_sprites, enemies_sprites = [], []
heroes_names, enemies_names = [], []

for i, hero in enumerate(battle.heroes, 1):
    hero_sprite = Sprite(screen, "sprites/hero1/idle.png", [200, int(600*(i/(len(battle.heroes)+1)))])
    hero_sprite.scale(3)
    heroes_sprites.append(hero_sprite)
    hero_name = font.render(hero.name, True, (0, 0, 0))
    heroes_names.append(hero_name)

for i, enemy in enumerate(battle.enemies, 1):
    enemy_sprite = Sprite(screen, "sprites/enemy1/idle.png", [600, int(600*(i/(len(battle.enemies)+1)))])
    enemy_sprite.set_mirrored(True)
    enemy_sprite.scale(2)
    enemies_sprites.append(enemy_sprite)
    enemy_name = font.render(enemy.name, True, (0, 0, 0))
    enemies_names.append(enemy_name)

#Основний цикл програми
runnig = True
while runnig:
    for event in pygame.event.get(): # Обробка подій
        if event.type == pygame.QUIT:
            runnig = False
        '''if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for idx, enemy_sprite in enumerate(enemies_sprites):
                if enemy_sprite.rect().collidepoint(event.pos) and battle.state == "HERO_TURN":
                    battle.process_command()
                    battle.process_command('') '''
    screen.fill((150, 150, 150))
    
    for idx, hero_sprite in enumerate(heroes_sprites):
        hero_sprite.draw()
        hero_x, hero_y = hero_sprite.position
        screen.blit(heroes_names[idx], (hero_x - 30, hero_y + 70))
    for idx, enemy_sprite in enumerate(enemies_sprites):
        enemy_sprite.draw()
        enemy_x, enemy_y = enemy_sprite.position
        screen.blit(enemies_names[idx], (enemy_x - 30, enemy_y + 70))

    pygame.display.flip() # Малюємо наступний кадр
    clock.tick(FPS)


#Завершення програми
pygame.quit()
sys.exit()