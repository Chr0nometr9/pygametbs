import pygame
import sys
from random import randint

# Ініціалізація
pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("PyGame TBS v0.1")

for i in range(1, 6):
    color = randint(0,255), randint(0,255), randint(0,255)
    circ = pygame.draw.circle(screen, color, (i*50, i*50), i*5) # намалювати коло
    print(circ.center)

#Основний цикл програми
runnig = True
while runnig:
    for event in pygame.event.get(): # Обробка подій
        if event.type == pygame.QUIT:
            runnig = False 

    pygame.display.flip() # Малюємо наступний кадр


#Завершення програми
pygame.quit()
sys.exit()