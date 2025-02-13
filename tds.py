# import pygame
# import sys


# # Ініціалізація
# pygame.init()

# screen_width, screen_height = 800, 600
# screen = pygame.display.set_mode((screen_width, screen_height))
# pygame.display.set_caption("PyGame TBS v0.1")


# #Основний цикл програми
# runnig = True
# while runnig:
#     for event in pygame.event.get(): # Обробка подій
#         if event.type == pygame.QUIT:
#             runnig = False 
    
#     pygame.display.flip() # Малюємо наступний кадр


# #Завершення програми
# pygame.quit()
# sys.exit()
import pygame
import sys
import random

class Bullet():
    def __init__(self, x, y, mouse_x, mouse_y):
        self.x = x
        self.y = y
        self.dir = pygame.math.Vector2(mouse_x - x, mouse_y - y)
        self.dir.scale_to_length(5)

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 0, 255), (self.x, self.y), 5)

    def move(self, factor=1):
        self.x += self.dir.x * factor
        self.y += self.dir.y * factor

    def out_of_bounce(self, screen_width, screen_height):
        if self.x < 0 or self.x > screen_width or self.y < 0 or self.y > screen_height:
            return True
        else:
            return False
        
class Enemy():
    def __init__(self, target_x, target_y, enemy_img):
        side = random.choice(["top", "bottom", "left", "right"])

        if side == "top":
            self.x = random.randint(0, screen_width)
            self.y = 0
            print("top")

        if side == "bottom":
            self.x = random.randint(0, screen_width)
            self.y = screen_height - 100
            print("bottom")

        if side == "left":
            self.x = 0
            self.y = random.randint(0, screen_height)
            print("left")

        if side == "right":
            self.x = screen_width - 100
            self.y = random.randint(0, screen_height)
            print("right")
        
        self.dir = pygame.math.Vector2(target_x - self.x, target_y - self.y)
        self.dir.scale_to_length(2)
        self.img = pygame.transform.rotate(enemy_img, self.dir.angle_to((0, 1)))

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def move(self, factor=1):
        self.x += self.dir.x * factor
        self.y += self.dir.y * factor

    def out_of_bounce(self, screen_width, screen_height):
        if self.x < 0 or self.x > screen_width or self.y < 0 or self.y > screen_height:
            return True
        else:
            return False





# Ініціалізація
pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("PyGame TBS v0.1")

clock = pygame.time.Clock()

x = 400
y = 300

a_x, a_y = 0, 0
v_x, v_y = 0, 0

dt = 0.01

mouse_x, mouse_y = 0, 0

move = False
x_rand = random.randint(5, 795)
y_rand = random.randint(5, 595)
ship = pygame.image.load("C://Users//Artem Chistyakov//Downloads//Python//Repository//pygametbs//ship.png")
enemy_img = pygame.image.load("C://Users//Artem Chistyakov//Downloads//Python//Repository//pygametbs//enemy.png")
big_rect = ship.get_rect()
small_rect = pygame.draw.circle(screen, (255, 255, 0), (x_rand, y_rand), 5)



font = pygame.font.Font(None, 32)
score = 0
bullets = []
enemies = []

last_create_enemy = 0

#Основний цикл програми
runnig = True
while runnig:
    for event in pygame.event.get(): # Обробка подій
        if event.type == pygame.QUIT:
            runnig = False 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                move = True 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                move = False 
        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                new_bullet = Bullet(x, y, mouse_x, mouse_y)
                new_bullet.move(10)
                bullets.append(new_bullet)
    if big_rect.colliderect(small_rect):
        score = score+1
        x_rand = random.randint(5, 795)
        y_rand = random.randint(5, 595)

    dir_vector = pygame.math.Vector2(mouse_x - x, mouse_y - y)
    a = dir_vector.copy()
    a.scale_to_length(130)

    if move:
        a_x, a_y = a.xy

    v_x += a_x * dt
    v_y += a_y * dt
    x += v_x * dt
    y += v_y * dt

    now = pygame.time.get_ticks()
    if now - last_create_enemy >= 3000:
        print("TicTac!")
        enemies.append(Enemy(x, y, enemy_img))
        last_create_enemy = now


    enemies = [e for e in enemies if not e.out_of_bounce(screen_width, screen_height)]

    screen.fill((0,0,0))
    scoretext = font.render(str(score), True, (255, 255, 255))


    for enemy in enemies:
        enemy.move()
        enemy.draw(screen)

    rotated_ship = pygame.transform.rotate(ship, dir_vector.angle_to((0, -1)))
    
    big_rect = rotated_ship.get_rect()
    big_rect.center = (x, y)
    small_rect = pygame.draw.circle(screen, (255, 255, 0), (x_rand, y_rand), 5)

    screen.blit(scoretext, (0, 0))
    screen.blit(rotated_ship, big_rect)

    for bullet in bullets:
        bullet.move()
        bullet.draw(screen)
    
    bullets = [b for b in bullets if not b.out_of_bounce(screen_width, screen_height)]

    pygame.display.flip() # Малюємо наступний кадр
    clock.tick(60)
    

#Завершення програми
pygame.quit()
sys.exit()