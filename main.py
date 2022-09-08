import numpy as np
import pygame
import math
import sys
pygame.font.init()


DISC_RADIUS = 45
SQUARE_HEIGHT = 100

NUM_OF_ROWS, NUM_OF_COLS = 6, 7
WIDTH, HEIGHT =  SQUARE_HEIGHT * NUM_OF_COLS, SQUARE_HEIGHT * (NUM_OF_ROWS + 1)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

BLACK = (0,0,0)
WHITE = (255,255,255)
YELLOW = (255, 255,0)
RED = (255,0,0)
BLUE = (0,0,255)

WINNER_FONT = pygame.font.SysFont('comicsans', 75)

def createBoard():
    board = np.zeros((NUM_OF_ROWS, NUM_OF_COLS))
    return board

def valid(board, position):
    for row in range(NUM_OF_ROWS):
        if board[row, position] == 0:
            return True
    return False

def playMove(board, position, player):
    play_index = NUM_OF_ROWS - 1
    for row in range(NUM_OF_ROWS):
        if board[row][position] != 0:
            play_index = row - 1
            break
    board[play_index, position] = player
    return board, play_index


def gameOver(board, col_index, row_index, player):
    if np.all(board):
        return True, 0
    # check down
    seq_length = 0
    temp_row_index = row_index
    while temp_row_index < NUM_OF_ROWS:
        if board[temp_row_index, col_index] == player:
            seq_length += 1
            temp_row_index += 1
        else:
            break
    if seq_length == 4:
        return True, player

    # check row
    seq_length = 0
    temp_col_index = col_index
    while temp_col_index < NUM_OF_COLS:
        if board[row_index, temp_col_index] == player:
            seq_length += 1
            temp_col_index += 1
        else:
            break
    
    temp_col_index = col_index
    while temp_col_index >= 0:
        if board[row_index, temp_col_index] == player:
            seq_length += 1
            temp_col_index -= 1
        else:
            break
    
    seq_length -= 1
    if seq_length >= 4:
        return True, player
    
    # check left diagonal
    seq_length = 0
    temp_row_index = row_index
    temp_col_index = col_index
    while temp_col_index < NUM_OF_COLS and temp_row_index >= 0:
        if board[temp_row_index, temp_col_index] == player:
            seq_length += 1
            temp_row_index -= 1
            temp_col_index += 1
        else:
            break
    
    temp_row_index = row_index
    temp_col_index = col_index
    while temp_col_index >= 0 and temp_row_index < NUM_OF_ROWS:
        if board[temp_row_index, temp_col_index] == player:
            seq_length += 1
            temp_row_index += 1
            temp_col_index -= 1
        else:
            break
    
    seq_length -= 1
    if seq_length >= 4:
        return True, player

    # check right diagonal
    seq_length = 0
    temp_row_index = row_index
    temp_col_index = col_index
    while temp_col_index >= 0 and temp_row_index >= 0:
        if board[temp_row_index, temp_col_index] == player:
            seq_length += 1
            temp_row_index -= 1
            temp_col_index -= 1
        else:
            break
    
    temp_row_index = row_index
    temp_col_index = col_index
    while temp_col_index < NUM_OF_COLS and temp_row_index < NUM_OF_ROWS:
        if board[temp_row_index, temp_col_index] == player:
            seq_length += 1
            temp_row_index += 1
            temp_col_index += 1
        else:
            break

    seq_length -= 1
    if seq_length >= 4:
        return True, player
    
    return False, 0


def drawWindow(board, mouse_pos, player):
    WIN.fill(BLUE)
    drawBoard(board)
    current_disc_center = (mouse_pos[0], SQUARE_HEIGHT // 2)
    color = YELLOW if player == 1 else RED
    pygame.draw.circle(WIN, color, current_disc_center, DISC_RADIUS)
    pygame.display.update()

def drawBoard(board):
    top_rect = pygame.Rect((0,0), (WIDTH, SQUARE_HEIGHT))
    pygame.draw.rect(WIN, BLACK, top_rect)
    for row_index, row in enumerate(board):
        for col_index, square in enumerate(row):
            center = ((col_index + 0.5) * SQUARE_HEIGHT, (row_index + 1.5) * SQUARE_HEIGHT)
            if square == 0:
                pygame.draw.circle(WIN, BLACK, center, DISC_RADIUS)
                # print(square)
            elif square == 1:
                pygame.draw.circle(WIN, YELLOW, center, DISC_RADIUS)
            elif square == 2:
                pygame.draw.circle(WIN, RED, center, DISC_RADIUS)

def draw_winner(outcome):
    text = ''
    if outcome == 0:
        text = 'Draw'
    elif outcome == 1:
        text = 'YELLOW Wins!'
    elif outcome == 2:
        text = 'RED Wins!'
    winner_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(winner_text, ((WIDTH - winner_text.get_width())// 2, (HEIGHT -winner_text.get_height()) // 2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    board = createBoard()
    current_player = 1
    run = True

    while run:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                disc_pos = mouse_pos[0] // SQUARE_HEIGHT
                if valid(board, disc_pos):
                    board, row_index = playMove(board, disc_pos, current_player)
                    drawWindow(board, mouse_pos, current_player)

                    is_game_over, outcome = gameOver(board, disc_pos, row_index, current_player)
                    if is_game_over:
                        draw_winner(outcome)
                        # print('game over')
                        run = False
                        break
                    current_player = 1 if current_player == 2 else 2

        drawWindow(board, mouse_pos, current_player)

        # print(board)
        # print()
        # col_index = int(input('Where would you like to play? 0-6: '))
        # if valid(board, col_index):
        #     board, row_index = playMove(board, col_index, current_player)
        #     is_game_over, outcome = gameOver(board, col_index, row_index, current_player)
        #     if is_game_over:
        #         print(board)
        #         print()
        #         print(f'Winner is {outcome}')
        #         run = False
        #         break
        #     current_player = 1 if current_player == 2 else 2
    
    pygame.quit()

        


if __name__ == '__main__':
    main()