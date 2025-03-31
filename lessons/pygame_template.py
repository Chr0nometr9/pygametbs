import pygame
import sys
import socket
from json import loads

login = input("Введіть логін: ")

# Ініціалізація
pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("PyGame TBS v0.1")

clock = pygame.time.Clock()
SERVER_IP, SERVER_PORT = '26.159.171.202', 8001

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect((SERVER_IP, SERVER_PORT))
my_socket.sendall(login.encode())

move_left, move_right, move_up, move_down = False, False, False, False

my_socket.setblocking(False)

#Основний цикл програми
runnig = True
with my_socket:
    while runnig:
        for event in pygame.event.get(): # Обробка подій
            if event.type == pygame.QUIT:
                runnig = False
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
        
        screen.fill((0, 0, 0))

        if move_down:
            my_socket.sendall(b'down')
        if move_up:
            my_socket.sendall(b'up')
        if move_right:
            my_socket.sendall(b'right')
        if move_left:
            my_socket.sendall(b'left')

        try:
            data = my_socket.recv(1024).decode()
            try:
                players = loads(data)
            except:
                pass
            for player, coords in players.items():
                pygame.draw.rect(screen, (255, 255, 255), (*coords, 50, 50))
        except BlockingIOError:
            pass

        pygame.display.flip() # Малюємо наступний кадр
        clock.tick(60)


#Завершення програми
pygame.quit()
sys.exit()