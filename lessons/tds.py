import pygame
import sys
import random

class Bullet():
    def __init__(self, x, y, dir_vector):
        self.x = x
        self.y = y
        self.dir = dir_vector.copy()
        self.dir.scale_to_length(4)
        self.bullet_sprite = pygame.image.load("bullet.png")
        self.bullet_sprite = pygame.transform.scale(self.bullet_sprite, (self.bullet_sprite.get_width() // 1.5, self.bullet_sprite.get_height() // 1.5))
        self.img = self.bullet_sprite
        self.bullet_rect = self.img.get_rect()

    def draw(self, screen):
        self.img = pygame.transform.rotate(self.bullet_sprite, self.dir.angle_to((0, -1)))
        self.bullet_rect = self.img.get_rect()
        self.bullet_rect.center = (self.x, self.y)
        screen.blit(self.img, self.bullet_rect)

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
        self.hp = 100

        if side == "top":
            self.x = random.randint(0, screen_width)
            self.y = 0

        if side == "bottom":
            self.x = random.randint(0, screen_width)
            self.y = screen_height - 100

        if side == "left":
            self.x = 0
            self.y = random.randint(0, screen_height)
            
        if side == "right":
            self.x = screen_width - 100
            self.y = random.randint(0, screen_height)
        
        self.dir = pygame.math.Vector2(target_x - self.x, target_y - self.y)
        self.dir.scale_to_length(2)
        self.img = pygame.transform.rotate(enemy_img, self.dir.angle_to((0, 1)))

    def get_rect(self):
        rect = self.img.get_rect()
        rect.topleft = (self.x, self.y)
        return rect

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))
        hpbar_rect = pygame.Rect((0, 0), (self.hp, 10))
        hpbar_rect.center = (self.get_rect().centerx, self.get_rect().centery + 80)
        pygame.draw.rect(screen, (0, 255, 0), hpbar_rect)

    def move(self, factor=1):
        self.x += self.dir.x * factor
        self.y += self.dir.y * factor

    def out_of_bounce(self, screen_width, screen_height):
        if self.x < 0 or self.x > screen_width or self.y < 0 or self.y > screen_height:
            return True
        else:
            return False

class ExplosionAnimation():
    def __init__(self, x, y):
        self.frames = [pygame.image.load(f"expl/{i}.png") for i in range(6)]
        self.frame_duration = 150
        self.last_update = pygame.time.get_ticks()
        self.current_frame_idx = 0
        self.end = False
        self.x, self.y = x, y

    def draw(self, screen):
        now = pygame.time.get_ticks()
        current_frame = self.frames[self.current_frame_idx]
        current_frame_rect = current_frame.get_rect()
        current_frame_rect.center = self.x, self.y
        screen.blit(current_frame, current_frame_rect)
        if now - self.last_update >= self.frame_duration:
            self.last_update = now
            if self.current_frame_idx < 5:
                self.current_frame_idx += 1
            else:
                self.end = True

# Ініціалізація
pygame.init()

screen_width, screen_height = 1920, 1080
# screen_width, screen_height = 1366, 768
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
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
ship = pygame.image.load("ship.png")
rotated_ship = ship
enemy_img = pygame.image.load("enemy.png")
big_rect = ship.get_rect()
small_rect = pygame.draw.circle(screen, (255, 255, 0), (x_rand, y_rand), 5)

font = pygame.font.Font(None, 32)
score = 0
bullets = []
enemies = []
expl_animations = []
hp = 100
damage = 10
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
                left_bullet_vector = pygame.math.Vector2(-45, 0).rotate(90 - dir_vector.angle_to((1, 0)))
                right_bullet_vector = pygame.math.Vector2(45, 0).rotate(90 - dir_vector.angle_to((1, 0)))
                new_bullet = Bullet(x+left_bullet_vector.x, y+left_bullet_vector.y, dir_vector)
                new_bullet.move(10)
                bullets.append(new_bullet)
                new_bullet = Bullet(x+right_bullet_vector.x, y+right_bullet_vector.y, dir_vector)
                new_bullet.move(10)
                bullets.append(new_bullet)
    if big_rect.colliderect(small_rect):
        score = score + 1
        x_rand = random.randint(5, 795)
        y_rand = random.randint(5, 595)

    screen_width, screen_height = screen.get_size()
    hero_mask = pygame.mask.from_surface(rotated_ship)

    for bullet in bullets:
        for enemy in enemies:
            if bullet.bullet_rect.colliderect(enemy.get_rect()):
                bullet.x = -10000
                enemy.hp -= damage
                if enemy.hp <= 0:
                    expl_animations.append(ExplosionAnimation(*enemy.get_rect().center))
                    enemy.x = -10000

    for enemy in enemies:
        enemy_mask = pygame.mask.from_surface(enemy.img)
        offset = big_rect.x - enemy.get_rect().x, big_rect.y - enemy.get_rect().y
        if enemy_mask.overlap(hero_mask, offset):
            hp -= 20
            expl_animations.append(ExplosionAnimation(*enemy.get_rect().center))
            enemy.x = -10000

    if hp <= 0:
        print("You lose")
        runnig = False

    dir_vector = pygame.math.Vector2(mouse_x - x, mouse_y - y)
    a = dir_vector.copy()
    a.scale_to_length(200)

    if move:
        a_x, a_y = a.xy
    else:
        a_x, a_y = 0, 0

    v_x += a_x * dt
    v_y += a_y * dt
    x += v_x * dt
    y += v_y * dt

    now = pygame.time.get_ticks()
    if now - last_create_enemy >= 3000:
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

    hpbar_rect = pygame.Rect((0, 0), (hp * 5, 25))
    hpbar_rect.center = (screen_width // 2, screen_height - 60)
    pygame.draw.rect(screen, (255, 0, 0), hpbar_rect)

    screen.blit(scoretext, (0, 0))
    screen.blit(rotated_ship, big_rect)

    for bullet in bullets:
        bullet.move()
        bullet.draw(screen)

    for expl in expl_animations:
        expl.draw(screen)
    
    bullets = [b for b in bullets if not b.out_of_bounce(screen_width, screen_height)]
    expl_animations = [expl for expl in expl_animations if not expl.end]

    pygame.display.flip() # Малюємо наступний кадрa
    clock.tick(60)
    

pygame.quit()
sys.exit()