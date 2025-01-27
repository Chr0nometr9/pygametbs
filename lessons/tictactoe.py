import pygame
import sys


# Ініціалізація
pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("PyGame TBS v0.1")

screen.fill((255, 255, 255))

pygame.draw.line(screen, (0, 0, 0), (325, 75), (325, 525), 3)
pygame.draw.line(screen, (0, 0, 0), (475, 75), (475, 525), 3)
pygame.draw.line(screen, (0, 0, 0), (175, 225), (625, 225), 3)
pygame.draw.line(screen, (0, 0, 0), (175, 375), (625, 375), 3)

board = [
    ["_", "_", "_"],
    ["_", "_", "_"],
    ["_", "_", "_"]
]

#Основний цикл програми
runnig = True
while runnig:
    for event in pygame.event.get(): # Обробка подій
        if event.type == pygame.QUIT:
            runnig = False
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                click_x, click_y = event.pos
                cell_x = (click_x - 175) // 150
                cell_y = (click_y - 75) // 150
                if 2 >= cell_x >= 0 and 2 >= cell_y >= 0:
                    print(cell_x, cell_y)

    pygame.display.flip() # Малюємо наступний кадр


#Завершення програми
pygame.quit()
sys.exit()