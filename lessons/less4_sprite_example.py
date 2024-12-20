import pygame
import sys
from random import randint
from sprite import Sprite


# Ініціалізація
pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("PyGame TBS v0.1")

clock = pygame.time.Clock()
FPS = 60

move_left, move_right, move_up, move_down = False, False, False, False
hero_sprite = Sprite(screen, "images/hero1.png", (100, 100))
hero_sprite.add_animation('Default', 3, 250)
hero_sprite.add_animation('Walk', 4, 300)
hero_sprite.scale(4)


#Основний цикл програми

runnig = True
while runnig:
    for event in pygame.event.get(): # Обробка подій
        if event.type == pygame.QUIT:
            runnig = False 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_left = True
            if event.key == pygame.K_RIGHT:
                move_right = True
            if event.key == pygame.K_UP:
                move_up = True
            if event.key == pygame.K_DOWN:
                move_down = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            if event.key == pygame.K_RIGHT:
                move_right = False
            if event.key == pygame.K_UP:
                move_up = False
            if event.key == pygame.K_DOWN:
                move_down = False

    if move_down or move_up or move_left or move_right:
        hero_sprite.set_animation('Walk')
    else:
        hero_sprite.set_animation('Default')

    if move_left:
        hero_sprite.move_by_vector(-5, 0)
        hero_sprite.set_mirrored(True)
    if move_right:
        hero_sprite.move_by_vector(5, 0)
        hero_sprite.set_mirrored(False)
    if move_up:
        hero_sprite.move_by_vector(0, -5)
    if move_down:
        hero_sprite.move_by_vector(0, 5)
    screen.fill((255, 255, 255))
    hero_sprite.draw()

    pygame.display.flip() # Малюємо наступний кадр
    clock.tick(FPS)


#Завершення програми
pygame.quit()
sys.exit()