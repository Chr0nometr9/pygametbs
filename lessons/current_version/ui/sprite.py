import pygame

class Animation:
    def __init__(self, folder_name : str, count : int, frame_duration : int, loop : bool = True):
        self.frames = [pygame.image.load(f"images/{folder_name}/{i}.png") for i in range(1, count + 1)]
        self.frame_duration = frame_duration
        self.loop = loop
        self.count = count
        self.last_update = None
        self.current_frame = 0

    def get_current_frame(self):
        now = pygame.time.get_ticks()
        if self.last_update is None:
            self.last_update = now
        
        if now - self.last_update >= self.frame_duration:
            if self.loop:
                self.current_frame += 1
                self.current_frame %= self.count
            else:
                if self.current_frame != self.count - 1:
                    self.current_frame += 1
            self.last_update = now

        return self.frames[self.current_frame]


class Sprite:
    def __init__(self, screen_surface : pygame.Surface, file : str, start_position : list = [0, 0]):
        self.original_image = pygame.image.load(file)
        self.screen_surface = screen_surface
        self.position = start_position
        self.__size = list(self.original_image.get_size())

        self.mirrored = False
        self.animations = {}
        self.current_animation_name = 'Default'

        self.current_image = self.original_image

    def rect(self):
        return self.current_image.get_rect()

    def draw(self):
        if self.current_animation_name != "Default":
            self.current_image = self.animations[self.current_animation_name].get_current_frame()
        else:
            self.current_image = self.original_image
    
        self.current_image = pygame.transform.scale(self.current_image, self.__size)
        if self.mirrored:
            self.current_image = pygame.transform.flip(self.current_image, True, False)
        rect = self.rect()
        rect.center = self.position
        self.screen_surface.blit(self.current_image, rect)

    def resize(self, new_width, new_height):
        self.__size = (new_width, new_height)

    def scale(self, scale_coeff):
        self.resize(self.__size[0] * scale_coeff, self.__size[1] * scale_coeff)

    def set_position(self, new_x, new_y):
        self.position = [new_x, new_y]

    def move_by_vector(self, move_x, move_y):
        self.set_position(self.position[0] + move_x, self.position[1] + move_y)

    def set_mirrored(self, state : bool):
        self.mirrored = state

    def add_animation(self, animation_name : str, count : int, 
                    frame_duration : int, loop : bool = True):
        self.animations[animation_name] = Animation(animation_name, count, frame_duration, loop)

    def set_animation(self, animation_name : str):
        self.current_animation_name = animation_name
