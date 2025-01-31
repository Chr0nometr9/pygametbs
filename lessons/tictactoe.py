import pygame
import sys


# Ініціалізація
pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("PyGame TBS v0.1")

font = pygame.font.Font(size=32)
x_win_text = font.render("Хрестики перемогли!", True, (0, 0, 0))
o_win_text = font.render("Ноліки перемогли!", True, (0, 0, 0))

screen.fill((255, 255, 255))

pygame.draw.line(screen, (0, 0, 0), (325, 75), (325, 525), 3)
pygame.draw.line(screen, (0, 0, 0), (475, 75), (475, 525), 3)
pygame.draw.line(screen, (0, 0, 0), (175, 225), (625, 225), 3)
pygame.draw.line(screen, (0, 0, 0), (175, 375), (625, 375), 3)

board_x, board_y = 175, 75


def draw_cross(cell_x, cell_y, screen : pygame.Surface):
    left_top_corner = (150 * cell_x + board_x + 20 , 150 * cell_y + board_y + 20)
    right_bottom_corner = (150 * (cell_x + 1) + board_x - 20, 150 * (cell_y + 1) + board_y - 20)
    left_bottom_corner = (150 * cell_x + board_x + 20, 150 * (cell_y + 1) + board_y - 20)
    right_up_corner = (150 * (cell_x + 1) + board_x - 20, 150 * cell_y + board_y + 20)

    pygame.draw.line(screen, (255, 0, 0), left_top_corner, right_bottom_corner, 3)
    pygame.draw.line(screen, (255, 0, 0), left_bottom_corner, right_up_corner, 3)


def draw_circle(cell_x, cell_y, screen : pygame.Surface):
    center_cell = (150 * cell_x + 75 + board_x, 150 * cell_y + 75 + board_y)
    pygame.draw.circle(screen, (0, 0, 255), center_cell, 55, 3)

def draw_victory_line(start_line, end_line, screen : pygame.Surface):
    pygame.draw.line(screen, (0, 255, 0), start_line, end_line, 3)

def check_victory(board, figure):
    for i in range(3): # перевіряємо чи десь стоять три фігури в ряд
        if board[i] == [figure] * 3:
            y = board_y + i * 150 + 75
            start_line = (board_x, y)
            end_line = (board_x + 450, y),
            draw_victory_line(start_line, end_line, screen)
            return True

    for i in range(3): # перевіряємо чи десь стоять три фігури в одному стовпчику
        column = [board[0][i], board[1][i], board[2][i]]
        if column == [figure] * 3:
            x = board_x + i * 150 + 75 
            start_line = (x, board_y)
            end_line = (x, board_y + 450),
            draw_victory_line(start_line, end_line, screen)
            return True

    main_diag = [board[0][0], board[1][1], board[2][2]]
    sub_diag = [board[0][2], board[1][1], board[2][0]]

    if main_diag == [figure] * 3:
        start_line = (board_x, board_y)
        end_line = (board_x + 450, board_y + 450),
        draw_victory_line(start_line, end_line, screen)
        return True
    
    if sub_diag == [figure] * 3:
        start_line = (board_x + 450, board_y)
        end_line = (board_x, board_y + 450),
        draw_victory_line(start_line, end_line, screen)
        return True

    return False

board = [
    ["_", "_", "_"],   #board[0]
    ["_", "_", "_"],   #board[1]
    ["_", "_", "_"]    #board[2]
]

tic_turn_flag = True
win = False

#Основний цикл програми
runnig = True
while runnig:
    for event in pygame.event.get(): # Обробка подій
        if event.type == pygame.QUIT:
            runnig = False
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                click_x, click_y = event.pos
                cell_x = (click_x - 175) // 150
                cell_y = (click_y - 75) // 150
                if 2 >= cell_x >= 0 and 2 >= cell_y >= 0:
                    if not win:
                        if board[cell_y][cell_x] == '_':
                            if tic_turn_flag:
                                board[cell_y][cell_x] = 'x'
                                draw_cross(cell_x, cell_y, screen)
                                if check_victory(board, 'x'):
                                    x_win_text_rect = x_win_text.get_rect()
                                    x_win_text_rect.center = (400, 565)
                                    screen.blit(x_win_text, x_win_text_rect)
                                    win = True
                            else:
                                board[cell_y][cell_x] = 'o'
                                draw_circle(cell_x, cell_y, screen)
                                if check_victory(board, 'o'):
                                    o_win_text_rect = o_win_text.get_rect()
                                    o_win_text_rect.center = (400, 565)
                                    screen.blit(o_win_text, o_win_text_rect)
                                    win = True

                            tic_turn_flag = not tic_turn_flag
                            print(board)

    pygame.display.flip() # Малюємо наступний кадр



#Завершення програми
pygame.quit()
sys.exit()