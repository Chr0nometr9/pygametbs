import pygame
import sys
from scenes.game import GameScene
from scenes.death import DeathScreen
from scenes.menu import Menu
from scenes.pause import Pause
from random import choice

# Ініціалізація
pygame.init()

screen_width, screen_height = 1920, 1080
FPS = 60
screen = pygame.display.set_mode((screen_width, screen_height), flags=pygame.FULLSCREEN)
clock = pygame.time.Clock()
pygame.display.set_caption("PyGame TBS v0.1")
pygame.mixer.init()

timecodes = [0, 240, 480, 714, 955, 1147, 1344, 1504, 1745, 1898, 2138, 2375, 2584, 2771, 2873, 2971, 3166, 3267, 3479]

pygame.mixer.music.load(filename='ost.ogg')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(loops=-1, start=choice(timecodes), fade_ms=500)

class SceneManager:
    def __init__(self):
        self.scenes = {}
        self.current_scene_name = "menu"
        self.running = True
        self.background_surface = None
        
    def update_and_draw(self, events):
        self.scenes[self.current_scene_name].update_and_draw(events)

    def set_scene(self, scene_name):
        self.current_scene_name = scene_name
    
    def add_scene(self, scene, scene_name):
        self.scenes[scene_name] = scene

    def reset_game(self):
        self.scenes['game'].reset()

    def exit_game(self):
        self.running = False

scene_manager = SceneManager()

scene_manager.add_scene(GameScene(screen, scene_manager), "game")
scene_manager.add_scene(DeathScreen(screen, scene_manager), "death")
scene_manager.add_scene(Menu(screen, scene_manager), "menu")
scene_manager.add_scene(Pause(screen, scene_manager), "pause")

#Основний цикл програми

while scene_manager.running:
    scene_manager.update_and_draw(pygame.event.get())
    pygame.display.flip() # Малюємо наступний кадр
    clock.tick(FPS)

#Завершення програми
pygame.quit()
sys.exit()