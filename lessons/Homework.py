import pygame
import random

pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Збирач кульок!")

FPS = 60
clock = pygame.time.Clock()

start_time = pygame.time.get_ticks()
time_limit = 30000  


player_radius = 20
player_speed = 5
player_pos = pygame.Rect(screen_width // 2, screen_height // 2, player_radius * 2, player_radius * 2)

move_left = move_right = move_up = move_down = False

circle_radius = 10
small_circle = pygame.Rect(
    random.randint(50, screen_width - 50), 
    random.randint(50, screen_height - 50), 
    circle_radius * 2, circle_radius * 2
)


def draw_player(screen, player):
    pygame.draw.circle(screen, (0, 0, 255), player.center, player_radius)

score = 0  

running = True
while running:
    screen.fill((0, 0, 0))  
    current_time = pygame.time.get_ticks()
    remaining_time = max(0, (time_limit - (current_time - start_time)) // 1000)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
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

    if move_left:
        player_pos.x -= player_speed
    if move_right:
        player_pos.x += player_speed
    if move_up:
        player_pos.y -= player_speed
    if move_down:
        player_pos.y += player_speed

    draw_player(screen, player_pos)

    if player_pos.colliderect(small_circle):
        score += 1
        small_circle.x = random.randint(50, screen_width - 50)
        small_circle.y = random.randint(50, screen_height - 50)

    pygame.draw.circle(screen, (255, 255, 0), small_circle.center, circle_radius)

    font = pygame.font.Font(None, 36)
    timer_text = font.render(f"Час: {remaining_time}", True, (255, 255, 255))
    screen.blit(timer_text, (screen_width - 120, 10))

    score_text = font.render(f"Рахунок: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    if remaining_time == 0:
        if score >= 10:
            print(f"Ви виграли! Ваш рахунок: {score}")
        else:
            print(f"Ви програли! Ваш рахунок: {score}")
        running = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
