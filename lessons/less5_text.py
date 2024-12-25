import pygame
from multiline import MultilineText
from button import Button

pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
font = pygame.font.Font("BF_Mnemonika_Regular.ttf", 32)

text = """Це приклад багаторядкового тексту, який підтримує перенесення по словам. Також він 
        підтримує символи переносу рядку \n \n Всі слова, які не вміщаються на Surface - обрізаються"""

max_width = 400
max_height = 300

text1 = MultilineText(
    text=text,
    font=font,
    max_width=max_width,
    max_height=max_height,
    text_color=(255, 255, 255),
    bg_color=(50, 50, 50),
    typing_effect=True,
    typing_speed=50
)

button1 = Button("Fight!", font)
mouse_x, mouse_y = 0, 0


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos

    screen.fill((30, 30, 30))
    
    text1_surf = text1.render()
    screen.blit(text1_surf, (50, 50))
    button1_surf = button1.render(mouse_x, mouse_y)
    screen.blit(button1_surf, (500, 100))


    pygame.display.flip()

pygame.quit()