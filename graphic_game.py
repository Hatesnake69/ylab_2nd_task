import pygame
import sys
import random
from typing import Union


def check_five(example_list: list[Union[int, str]]) -> bool:
    """this function checks if where are any of 5 same elements in a row"""
    fst_elem = example_list[0]
    counter = 1
    for index in range(1, len(example_list)):
        if example_list[index] == fst_elem:
            counter += 1
            if counter == 5:
                return True
        else:
            counter = 1
            fst_elem = example_list[index]
    return False


def check_win(mas: list[list[Union[int, str]]], sign: str) -> Union[bool, str]:
    """this function checks whether the winner or loser is found"""
    counter = 0
    for col in mas:
        for elem in col:
            if check_five(col):
                return sign
            if str(elem).isdigit():
                counter += 1
    for row in range(len(mas)):
        if check_five([mas[i_col][row] for i_col in range(len(mas))]):
            return sign
    if check_five([mas[index][index] for index in range(len(mas))]):
        return sign
    if check_five([mas[len(mas)-index-1][index] for index in range(len(mas))]):
        return sign
    if counter == 0:
        return 'peace'
    return False


def main():
    """this part of code initializes app and configuration parameters for the game"""
    pygame.init()
    margin = 15
    size_block = 50
    width = height = size_block * 10 + margin * 11
    size_window = (width, height)
    screen = pygame.display.set_mode(size_window)
    pygame.display.set_caption('Крестики-нолики')
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    white = (255, 255, 255)
    query = 0
    number = 10
    mas: list[list[Union[int, str]]] = [[i for i in range(j, j + number)] for j in range(1, number ** 2, number)]
    game_over: Union[bool, str] = False
    while True:
        for event in pygame.event.get():
            """this cycle processes incoming events"""
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif query % 2 == 0 and event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                """this part of code runs when user clicks on an empty cell of the board on the screen"""
                x_mouse, y_mouse = pygame.mouse.get_pos()
                col = x_mouse // (size_block + margin)
                row = y_mouse // (size_block + margin)
                try:
                    if str(mas[col][row]).isdigit():
                        mas[col][row] = 'x'
                        query += 1
                except IndexError:
                    pass
            elif query % 2 == 1 and not game_over:
                """this part of code runs after user makes his move and it does computer turn"""
                list_of_possible_moves = [j_elem for i_line in mas for j_elem in i_line if str(j_elem).isdigit()]
                random_number = random.choice(list_of_possible_moves)
                for i_index, i_list in enumerate(mas):
                    for j_index, j_value in enumerate(i_list):
                        if j_value == random_number:
                            mas[i_index][j_index] = 'o'
                query += 1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                """this part of code resets the game after it was finished by pressing SPACE"""
                game_over = False
                mas = [[i for i in range(j, j + number)] for j in range(1, number ** 2, number)]
                query = 0
                screen.fill(black)
        if not game_over:
            for row in range(10):
                """this cycle checks list mas where all marks for the game is stored and marks screen cells"""
                for col in range(10):
                    if mas[col][row] == 'x':
                        color = red
                    elif mas[col][row] == 'o':
                        color = green
                    else:
                        color = white
                    x = col * size_block + (col+1) * margin
                    y = row * size_block + (row+1) * margin
                    pygame.draw.rect(screen, color, (x, y, size_block, size_block))
                    if color == red:
                        pygame.draw.line(screen, white, (x, y), (x + size_block, y + size_block), 3)
                        pygame.draw.line(screen, white, (x + size_block, y), (x, y + size_block), 3)
                    elif color == green:
                        pygame.draw.circle(screen, white, (x + size_block / 2, y + size_block / 2), size_block//2, 3)
        if (query - 1) % 2 == 0:
            game_over = check_win(mas, 'o')
        else:
            game_over = check_win(mas, 'x')
        if game_over:
            """this part of code raises window with a winner"""
            screen.fill(black)
            font = pygame.font.SysFont('stxingkai', 30)
            text1 = font.render(f'Победил {"computer" if game_over == "o" else "игрок"}', True, white)
            text_rect = text1.get_rect()
            text_x = screen.get_width() / 2 - text_rect.width / 2
            text_y = screen.get_height() / 2 - text_rect.height / 2
            screen.blit(text1, [text_x, text_y])
            text2 = font.render('Нажмите пробел, чтобы продолжить', True, white)
            screen.blit(text2, [text_x-80, text_y+20])

        pygame.display.update()


if __name__ == '__main__':
    main()

