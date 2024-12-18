import pygame
import sys
from random import randint

# Ініціалізація
pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("PyGame TBS v0.1")

clock = pygame.time.Clock()
FPS = 60

hero_right = pygame.image.load("images/hero1.png") # Завантажуємо зображення, повертає Surface 
hero_size = hero_right.get_size() # Отримуємо розміри
hero_right = pygame.transform.scale(hero_right, (hero_size[0]*4, hero_size[1]*4)) # Збільшуємо в 4 рази
hero_left = pygame.transform.flip(hero_right, True, False) # Створюємо віддзеркалену копію

hero_image = hero_right # Відпочатку дивимось праворуч
hero_rect = hero_image.get_rect() # Отримуємо прямокутник, який містить наш спрайт

move_left, move_right = False, False

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
            if event.key == pygame.K_SPACE:
                hero_rect.center = (randint(0, screen_width), randint(0, screen_height))
                # По натисканню пробілу переміщуємо героя у випадкову позицію на екрані
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            if event.key == pygame.K_RIGHT:
                move_right = False

    if move_left:
        hero_rect.centerx -= 5
        hero_image = hero_left # Якщо йдемо ліворуч, то відображаємо віддзеркалений спрайт
    if move_right:
        hero_rect.centerx += 5
        hero_image = hero_right # Якщо праворуч, то повертаємо оригінал
    
    screen.fill((230, 230, 230))
    #Замалювати прямокутну область героя зеленим кольором
    #pygame.draw.rect(screen, (0, 255, 0), hero_rect)
    screen.blit(hero_image, hero_rect)
    pygame.display.flip() # Малюємо наступний кадр
    clock.tick(60)

#Завершення програми
pygame.quit()
sys.exit()