import pygame
import sys
import random

dt = 0.01

class Enemy():
    last_spawn = 0
    velocity_abs = 3
    
    def __init__(self, target_x, target_y):
        side = random.choice(["top", "bottom", "left", "right"])
        self.hp = 10

        if side == "top":
            self.x = random.randint(0, screen_width)
            self.y = -100

        if side == "bottom":
            self.x = random.randint(0, screen_width)
            self.y = screen_height + 100

        if side == "left":
            self.x = -100
            self.y = random.randint(0, screen_height)
            
        if side == "right":
            self.x = screen_width + 100
            self.y = random.randint(0, screen_height)
        
        self.direction_vector = pygame.math.Vector2(target_x - self.x, target_y - self.y)
        self.velocity_vector = self.direction_vector.copy()
        self.velocity_vector.scale_to_length(self.velocity_abs)
        self.sprite = pygame.transform.rotate(pygame.image.load("enemy.png"), self.direction_vector.angle_to((0, 1)))

    def draw(self, screen):
        self.rect = self.sprite.get_rect()
        self.rect.center = self.x, self.y
        screen.blit(self.sprite, self.rect)
        # hpbar_rect = pygame.Rect((0, 0), (self.hp, 10))
        # hpbar_rect.center = (self.get_rect().centerx, self.get_rect().centery + 80)
        # pygame.draw.rect(screen, (0, 255, 0), hpbar_rect)

    def update(self):
        self.x += self.velocity_vector.x
        self.y += self.velocity_vector.y

    def handle_event(self, event):
        pass

    def is_on_screen(self, screen_width, screen_height):
        return (-100 < self.x < screen_width + 100) and (-100 < self.y < screen_height + 100)

class Rocket:
    def __init__(self, start_x, start_y, direction_vector):
        self.x, self.y = start_x, start_y
        self.velocity_vector = direction_vector.copy()
        self.velocity = 3
        self.velocity_vector.scale_to_length(self.velocity)
        self.sprite = pygame.transform.rotate(pygame.image.load("bullet.png"), direction_vector.angle_to((0, -1)))

    def handle_event(self, event):
        pass

    def draw(self, screen):
        rect = self.sprite.get_rect()
        rect.center = self.x, self.y
        screen.blit(self.sprite, rect)

    def update(self):
        self.x += self.velocity_vector.x
        self.y += self.velocity_vector.y

    def is_on_screen(self, screen_width, screen_height):
        return (-100 < self.x < screen_width + 100) and (-100 < self.y < screen_height + 100)
        
class Player:
    def __init__(self, start_x, start_y):
        self.x, self.y = start_x, start_y
        self.hp = 100
        
        self.acceleration_abs = 200
        self.angle = 0
        self.move = False

        self.last_shot_time = 0
        self.shot_cooldown = 500

        self.direction_vector = pygame.math.Vector2(1, 0)
        self.velocity_vector = pygame.math.Vector2(0, 0)
        self.acceleration_vector = pygame.math.Vector2(0, 0)

        self.sprite = pygame.image.load("ship.png")
    
    def draw(self, screen):
        current_sprite = pygame.transform.rotate(self.sprite, self.angle)
        rect = current_sprite.get_rect()
        rect.center = self.x, self.y
        screen.blit(current_sprite, rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            self.direction_vector = pygame.math.Vector2(mouse_x - self.x, mouse_y - self.y)
            self.direction_vector.scale_to_length(1)
            self.angle = self.direction_vector.angle_to((0, -1)) # кут з напрямком вертикально вгору
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.move = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.move = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                now = pygame.time.get_ticks()
                if now - self.last_shot_time >= self.shot_cooldown:
                    objects.append(Rocket(self.x + self.direction_vector.x * 60, 
                                        self.y + self.direction_vector.y * 60, 
                                        self.direction_vector))
                    self.last_shot_time = now
                
    def update(self):
        if self.move:
            self.acceleration_vector = self.direction_vector.copy()
            self.acceleration_vector.scale_to_length(self.acceleration_abs)
        else:
            self.acceleration_vector = pygame.math.Vector2(0, 0)

        self.velocity_vector += self.acceleration_vector * dt
        self.x += self.velocity_vector.x * dt
        self.y += self.velocity_vector.y * dt


# Ініціалізація
pygame.init()

screen_width, screen_height = 800, 600
FPS = 60
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
pygame.display.set_caption("PyGame TBS v0.1")

player = Player(screen_width // 2, screen_height // 2)

objects = [player]

#Основний цикл програми
runnig = True
while runnig:
    for event in pygame.event.get(): # Обробка подій
        if event.type == pygame.QUIT:
            runnig = False 
        for obj in objects:
            obj.handle_event(event)
    
    screen.fill((0,0,0))
    
    now = pygame.time.get_ticks()
    if now - Enemy.last_spawn >= 1000:
        objects.append(Enemy(player.x, player.y))
        Enemy.last_spawn = now

    next_frame_objects = [player]

    for obj in objects:
        obj.update()
        obj.draw(screen)

        if isinstance(obj, (Rocket, Enemy)):
            if obj.is_on_screen(screen_width, screen_height):
                next_frame_objects.append(obj)

    pygame.display.flip() # Малюємо наступний кадр
    clock.tick(FPS)

    objects = next_frame_objects


#Завершення програми
pygame.quit()
sys.exit()