import pygame
import sys
from random import randint

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
circle_x, circle_y = 300, 300

#Основний цикл програми
runnig = True
while runnig:
    for event in pygame.event.get(): # Обробка подій
        if event.type == pygame.QUIT:
            runnig = False 


    screen.fill((0, 0, 0))

    circle_x += 1
    circle_y += 1

    pygame.draw.circle(screen, (255, 255, 255), (circle_x, circle_y), 30)

    pygame.display.flip() # Малюємо наступний кадр
    clock.tick(FPS)


#Завершення програми
pygame.quit()
sys.exit()