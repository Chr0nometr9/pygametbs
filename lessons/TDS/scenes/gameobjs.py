import pygame
import random

dt = 0.01

class Bar:
    def __init__(self, max_width, max_value, height, color, background_color):
        self.max_width = max_width
        self.max_value = max_value
        self.height = height
        self.color = color
        self.background_color = background_color

    def draw(self, screen, value, x, y):
        bar_background_rect = pygame.Rect(x - self.max_width // 2, y - self.height // 2, self.max_width, self.height)
        bar_rect = pygame.Rect(x - self.max_width // 2, y - self.height // 2, int(self.max_width * value / self.max_value), self.height)
        pygame.draw.rect(screen, self.background_color, bar_background_rect)
        pygame.draw.rect(screen, self.color, bar_rect)


class Explosion:
    def __init__(self, x, y, scale_factor=1.5, sound_volume=0.1):
        self.frames = [pygame.transform.scale_by(pygame.image.load(f"explosion_animation/{i}.png"), scale_factor) for i in range(25)]
        self.frame_duration = 50
        self.last_update = pygame.time.get_ticks()
        self.current_frame_idx = 0
        self.end = False
        self.x, self.y = x, y

        sound = pygame.mixer.Sound(file='8-bit-explosion_F.wav')
        sound.set_volume(sound_volume)
        pygame.mixer.Sound.play(sound)

    def handle_event(self, event, **kwargs):
        pass

    def update(self):
        pass

    def draw(self, screen):
        now = pygame.time.get_ticks()
        current_frame = self.frames[self.current_frame_idx]
        current_frame_rect = current_frame.get_rect()
        current_frame_rect.center = self.x, self.y
        screen.blit(current_frame, current_frame_rect)
        if now - self.last_update >= self.frame_duration:
            self.last_update = now
            if self.current_frame_idx < len(self.frames) - 1:
                self.current_frame_idx += 1
            else:
                self.end = True


class Heal:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.sprite = pygame.transform.scale_by(pygame.image.load("heal.png"), 0.5)
        self.mask = pygame.mask.from_surface(self.sprite)
        
    def get_rect(self):
        rect = self.sprite.get_rect()
        rect.center = self.x, self.y
        return rect

    def draw(self, screen):
        screen.blit(self.sprite, self.get_rect())

    def destroy(self):
        self.x = -1000

    def update(self):
        pass

    def handle_event(self, event, **kwargs):
        pass

    def is_on_screen(self, screen):
        return (-100 < self.x < screen.get_width() + 100) and (-100 < self.y < screen.get_height() + 100)


class Enemy:
    last_spawn = None
    velocity_abs = 3
    spawn_duration = 2000
    
    def __init__(self, target_x, target_y, screen):
        side = random.choice(["top", "bottom", "left", "right"])
        self.hp = 30
        self.hp_bar = Bar(120, 30, 10, (0, 255, 0), (0, 80, 0))

        if side == "top":
            self.x = random.randint(0, screen.get_width())
            self.y = -100 # спавнимо ворога на 100 пікселів вище верхньої межі ігрового рівня

        if side == "bottom":
            self.x = random.randint(0, screen.get_width())
            self.y = screen.get_height() + 100

        if side == "left":
            self.x = -100
            self.y = random.randint(0, screen.get_height())
            
        if side == "right":
            self.x = screen.get_width() + 100
            self.y = random.randint(0, screen.get_height())
        
        self.direction_vector = pygame.math.Vector2(target_x - self.x, target_y - self.y)
        self.velocity_vector = self.direction_vector.copy()
        self.velocity_vector.scale_to_length(self.velocity_abs)
        self.sprite = pygame.transform.rotate(pygame.image.load("enemy.png"), self.direction_vector.angle_to((0, 1)))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, screen):
        self.rect = self.sprite.get_rect()
        self.rect.center = self.x, self.y
        screen.blit(self.sprite, self.rect)
        self.hp_bar.draw(screen, self.hp, self.x, self.y + 100)
        # hpbar_rect = pygame.Rect((0, 0), (self.hp, 10))
        # hpbar_rect.center = (self.get_rect().centerx, self.get_rect().centery + 80)
        # pygame.draw.rect(screen, (0, 255, 0), hpbar_rect)

    def update(self):
        self.x += self.velocity_vector.x
        self.y += self.velocity_vector.y

    def handle_event(self, event, **kwargs):
        pass

    def is_on_screen(self, screen):
        return (-100 < self.x < screen.get_width() + 100) and (-100 < self.y < screen.get_height() + 100)
    
    def get_rect(self):
        return self.sprite.get_rect(center = (self.x, self.y))
    
    def destroy(self):
        self.x = -1000


class Rocket:
    def __init__(self, start_x, start_y, direction_vector):
        self.x, self.y = start_x, start_y
        self.velocity_vector = direction_vector.copy()
        self.velocity_abs = 6
        self.velocity_vector.scale_to_length(self.velocity_abs)
        self.sprite = pygame.transform.rotate(pygame.image.load("bullet.png"), direction_vector.angle_to((0, -1)))
        self.mask = pygame.mask.from_surface(self.sprite)

    def handle_event(self, event, **kwargs):
        pass

    def draw(self, screen):
        rect = self.sprite.get_rect()
        rect.center = self.x, self.y
        screen.blit(self.sprite, rect)

    def update(self):
        self.x += self.velocity_vector.x
        self.y += self.velocity_vector.y

    def is_on_screen(self, screen):
        return (-100 < self.x < screen.get_width() + 100) and (-100 < self.y < screen.get_height() + 100)
    
    def get_rect(self):
        return self.sprite.get_rect(center = (self.x, self.y))
    
    def destroy(self):
        self.x = -1000


class Player:
    def __init__(self, start_x, start_y):
        self.x, self.y = start_x, start_y
        self.hp = 100
        self.hp_bar = Bar(600, 100, 25, (255, 0, 0), (80, 0, 0))
        
        self.acceleration_abs = 200
        self.angle = 0
        self.move = False
        self.explosion_movement = False

        self.last_shot_time = 0
        self.shot_cooldown = 500

        self.direction_vector = pygame.math.Vector2(1, 0)
        self.velocity_vector = pygame.math.Vector2(0, 0)
        self.acceleration_vector = pygame.math.Vector2(0, 0)

        self.sprite = pygame.image.load("ship.png")
        self.current_sprite = self.sprite
    
    def get_mask(self):
        return pygame.mask.from_surface(self.current_sprite)

    def get_rect(self):
        return self.current_sprite.get_rect(center = (self.x, self.y))

    def draw(self, screen):
        screen.blit(self.current_sprite, self.get_rect())
        self.hp_bar.draw(screen, self.hp, screen.get_width() // 2, screen.get_height() - 80)

    def explosion_impulse(self, enemy_x, enemy_y):
        self.explosion_movement = True
        self.direction_vector = pygame.math.Vector2(self.x - enemy_x, self.y - enemy_y)

    def handle_event(self, event, **kwargs):
        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos

            new_direction_vector = pygame.math.Vector2(mouse_x - self.x, mouse_y - self.y)
            if new_direction_vector.length(): #захист від багу "нульового вектора"
                self.direction_vector = new_direction_vector

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

                    # вектори зміщення для лівої і правої ракети

                    left_rocket_pos_vector = pygame.math.Vector2(-35, 0).rotate(90 - self.direction_vector.angle_to((1, 0)))
                    right_rocket_pos_vector = pygame.math.Vector2(35, 0).rotate(90 - self.direction_vector.angle_to((1, 0)))

                    # додаємо дві ракети (ліворуч і праворуч)
                    
                    kwargs['objects'].extend([Rocket(self.x + right_rocket_pos_vector.x + self.direction_vector.x * 60, 
                                        self.y + right_rocket_pos_vector.y + self.direction_vector.y * 60,

                                        self.direction_vector),
                                    Rocket(self.x + left_rocket_pos_vector.x + self.direction_vector.x * 60, 
                                        self.y + left_rocket_pos_vector.y + self.direction_vector.y * 60, 

                                        self.direction_vector)])
                    
                    self.last_shot_time = now
                
    def update(self):
        self.current_sprite = pygame.transform.rotate(self.sprite, self.angle)
        if self.move or self.explosion_movement:
            self.acceleration_vector = self.direction_vector.copy()
            if self.explosion_movement:
                self.acceleration_vector.scale_to_length(10000) #  ТИДИЩ!!!!!!
            else:
                self.acceleration_vector.scale_to_length(self.acceleration_abs)
            self.explosion_movement = False
        else:
            self.acceleration_vector = pygame.math.Vector2(0, 0)

        self.velocity_vector += self.acceleration_vector * dt
        self.x += self.velocity_vector.x * dt
        self.y += self.velocity_vector.y * dt
