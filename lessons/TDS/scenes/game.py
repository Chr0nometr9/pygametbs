import pygame
from scenes.gameobjs import *


class GameScene:
    def __init__(self, screen, scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager
        self.player = Player(self.screen.get_width() // 2, self.screen.get_height() // 2)
        self.objects = [self.player]

    def reset(self):
        self.player = Player(self.screen.get_width() // 2, self.screen.get_height() // 2)
        self.objects = [self.player]
        Enemy.last_spawn = None

    def update_and_draw(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.scene_manager.exit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.scene_manager.background_surface = self.screen.copy()
                    self.scene_manager.background_surface.fill((50, 50, 50, 50), special_flags=pygame.BLEND_ADD)
                    self.scene_manager.set_scene("pause")
            for obj in self.objects:
                obj.handle_event(event, objects = self.objects)
    
        if Enemy.last_spawn is None:
            Enemy.last_spawn = pygame.time.get_ticks()

        self.screen.fill((0,0,0))
        
        now = pygame.time.get_ticks()
        if now - Enemy.last_spawn >= Enemy.spawn_duration:
            self.objects.append(Enemy(self.player.x, self.player.y, self.screen))
            Enemy.last_spawn = now

        rockets = [obj for obj in self.objects if isinstance(obj, Rocket)]
        enemies = [obj for obj in self.objects if isinstance(obj, Enemy)]
        heals = [obj for obj in self.objects if isinstance(obj, Heal)]

        for enemy in enemies:
            for rocket in rockets:
                offset = rocket.get_rect().x - enemy.get_rect().x, rocket.get_rect().y - enemy.get_rect().y 
                if enemy.mask.overlap(rocket.mask, offset):
                    self.objects.append(Explosion(rocket.x, rocket.y, scale_factor=0.8, sound_volume=0.05))
                    rocket.destroy()
                    enemy.hp -= 5
                    if enemy.hp <= 0:
                        if random.randint(1, 100) <= 50:
                            self.objects.append(Heal(enemy.x, enemy.y))
                        self.objects.append(Explosion(enemy.x, enemy.y))
                        enemy.destroy()

            offset = self.player.get_rect().x - enemy.get_rect().x, self.player.get_rect().y - enemy.get_rect().y 
            if enemy.mask.overlap(self.player.get_mask(), offset):
                self.objects.append(Explosion(enemy.x, enemy.y))
                self.player.explosion_impulse(enemy.x, enemy.y)
                self.player.hp -= 20
                enemy.destroy()

                if self.player.hp <= 0:
                    self.scene_manager.set_scene("death")

        for heal in heals:
            offset = self.player.get_rect().x - heal.get_rect().x, self.player.get_rect().y - heal.get_rect().y 
            if heal.mask.overlap(self.player.get_mask(), offset):
                heal.destroy()
                if self.player.hp <= 75:
                    self.player.hp += 25
                else:
                    self.player.hp = 100

        next_frame_objects = [self.player]

        for obj in self.objects:
            obj.update()
            obj.draw(self.screen)

            if isinstance(obj, (Rocket, Enemy, Heal)):
                if obj.is_on_screen(self.screen):
                    next_frame_objects.append(obj)

            if isinstance(obj, Explosion):
                if not obj.end:
                    next_frame_objects.append(obj)

            self.objects = next_frame_objects