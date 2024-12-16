import pygame
import sys
from random import randint
from math import cos, sin

import pygame.draw

# Ініціалізація
pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("PyGame TBS v0.1")

FPS = 60

'''for i in range(1, 6):
    color = randint(0,255), randint(0,255), randint(0,255)
    circ = pygame.draw.circle(screen, color, (i*50, i*50), i*5) # намалювати коло
    print(circ.center)'''

clock = pygame.time.Clock() # створюємо об'єкт для взаємодії з часом
group_surface_pos = [300, 300] # x, y
group_surface_speed = 5

move_left, move_right = False, False

group_surface = pygame.Surface((100, 400))

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
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            if event.key == pygame.K_RIGHT:
                move_right = False

    if move_left:
        group_surface_pos[0] -= group_surface_speed
    if move_right:
        group_surface_pos[0] += group_surface_speed

    screen.fill((0, 0, 0))
    pygame.draw.polygon(group_surface, (255, 0, 0), [(40, 60), (60, 20), (80, 60)])
    pygame.draw.circle(group_surface, (255, 255, 255), [60, 100], 20)
    pygame.draw.line(group_surface, (0, 255, 0), (60, 120), (20, 160), 5)
    pygame.draw.line(group_surface, (0, 255, 0), (60, 120), (100, 160), 5)
    pygame.draw.line(group_surface, (0, 0, 255), (60, 140), (30, 200), 5)
    pygame.draw.line(group_surface, (0, 0, 255), (60, 140), (90, 200), 5) 
    screen.blit(group_surface, group_surface_pos)


    pygame.display.flip() # Малюємо наступний кадр
    clock.tick(FPS)


#Завершення програми
pygame.quit()
sys.exit()