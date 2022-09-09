import random
from turtle import forward
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

PLAYER = 1
AI = 2

def createBoard():
    board = np.zeros((NUM_OF_ROWS, NUM_OF_COLS))
    return board

def validMove(board, position):
    for row in range(NUM_OF_ROWS):
        if board[row, position] == 0:
            return True
    return False

def getValidMoves(board):
    valid_moves = []
    for col_pos in range(NUM_OF_COLS):
        if validMove(board, col_pos):
            valid_moves.append(col_pos)
    return valid_moves

def getDiscRow(board, col_pos):
    play_index = NUM_OF_ROWS - 1
    for row in range(NUM_OF_ROWS):
        if board[row][col_pos] != 0:
            play_index = row - 1
            break
    return play_index

def playMove(board, col_pos, player):
    row_pos = getDiscRow(board, col_pos)
    board[row_pos, col_pos] = player
    return board


# def gameOver(board, row_index, col_index, player):
#     if np.all(board):
#         return True, 0
#     # check down
#     seq_length = 0
#     temp_row_index = row_index
#     while temp_row_index < NUM_OF_ROWS:
#         if board[temp_row_index, col_index] == player:
#             seq_length += 1
#             temp_row_index += 1
#         else:
#             break
#     if seq_length == 4:
#         return True, player

#     # check row
#     seq_length = 0
#     temp_col_index = col_index
#     while temp_col_index < NUM_OF_COLS:
#         if board[row_index, temp_col_index] == player:
#             seq_length += 1
#             temp_col_index += 1
#         else:
#             break
    
#     temp_col_index = col_index
#     while temp_col_index >= 0:
#         if board[row_index, temp_col_index] == player:
#             seq_length += 1
#             temp_col_index -= 1
#         else:
#             break
    
#     seq_length -= 1
#     if seq_length >= 4:
#         return True, player
    
#     # check left diagonal
#     seq_length = 0
#     temp_row_index = row_index
#     temp_col_index = col_index
#     while temp_col_index < NUM_OF_COLS and temp_row_index >= 0:
#         if board[temp_row_index, temp_col_index] == player:
#             seq_length += 1
#             temp_row_index -= 1
#             temp_col_index += 1
#         else:
#             break
    
#     temp_row_index = row_index
#     temp_col_index = col_index
#     while temp_col_index >= 0 and temp_row_index < NUM_OF_ROWS:
#         if board[temp_row_index, temp_col_index] == player:
#             seq_length += 1
#             temp_row_index += 1
#             temp_col_index -= 1
#         else:
#             break
    
#     seq_length -= 1
#     if seq_length >= 4:
#         return True, player

#     # check right diagonal
#     seq_length = 0
#     temp_row_index = row_index
#     temp_col_index = col_index
#     while temp_col_index >= 0 and temp_row_index >= 0:
#         if board[temp_row_index, temp_col_index] == player:
#             seq_length += 1
#             temp_row_index -= 1
#             temp_col_index -= 1
#         else:
#             break
    
#     temp_row_index = row_index
#     temp_col_index = col_index
#     while temp_col_index < NUM_OF_COLS and temp_row_index < NUM_OF_ROWS:
#         if board[temp_row_index, temp_col_index] == player:
#             seq_length += 1
#             temp_row_index += 1
#             temp_col_index += 1
#         else:
#             break

#     seq_length -= 1
#     if seq_length >= 4:
#         return True, player
    
#     return False, 0

def winningMove(board, player):
    for row in board:
        for c in range(len(row) - 3):
            window = list(row[c:c+4])
            if window.count(player) == 4:
                return True
    # Vertical
    for col in range(NUM_OF_COLS):
        for row in range(NUM_OF_ROWS - 3):
            window = list(board[temp_row][col] for temp_row in range(row, row + 4))
            if window.count(player) == 4:
                return True

    # forward diagonal /
    for row in range(3, NUM_OF_ROWS):
        for col in range(NUM_OF_COLS - 3):
            temp_row = row
            temp_col = col
            window = []
            for _ in range(4):
                window.append(board[temp_row,temp_col])
                temp_row -= 1
                temp_col += 1
            if window.count(player) == 4:
                return True

    # backward diagonal \
    for row in range(NUM_OF_ROWS - 3):
        for col in range(NUM_OF_COLS - 3):
            temp_row = row
            temp_col = col
            window = []
            for _ in range(4):
                window.append(board[temp_row,temp_col])
                temp_row += 1
                temp_col += 1
            if window.count(player) == 4:
                return True
    return False

def gameOver(board):
    return winningMove(board, PLAYER) or winningMove(board, AI) or len(getValidMoves(board)) == 0

def drawWindow(board, mouse_pos, player):
    WIN.fill(BLUE)
    drawBoard(board)
    if player != None:
        if mouse_pos != None:
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
    WIN.blit(winner_text, ((WIDTH - winner_text.get_width())// 2,0))
    pygame.display.update()
    pygame.time.delay(2000)

def evaluate_window(window,player):
    opp_player = 1 if player == 2 else 2
    score = 0
    if window.count(player) == 4:
        score += 100
    elif window.count(player) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(player) == 2 and window.count(0) == 2:
        score += 2
    
    if window.count(opp_player) == 3 and window.count(0) == 1:
        score -= 4
    # elif window.count(opp_player) == 2 and window.count(0) == 2:
    #     score -= 5
    return score

def scorePosition(board, player):
    score = 0
    # Horizontal
    center_array = [value for value in list(board[:, NUM_OF_COLS // 2])]
    center_count = center_array.count(player)
    score += center_count * 3
    for row in board:
        for c in range(len(row) - 3):
            window = list(row[c:c+4])
            score += evaluate_window(window,player)
    # Vertical
    for col in range(NUM_OF_COLS):
        for row in range(NUM_OF_ROWS - 3):
            window = list(board[temp_row][col] for temp_row in range(row, row + 4))
            score += evaluate_window(window,player)

    # forward diagonal /
    for row in range(3, NUM_OF_ROWS):
        for col in range(NUM_OF_COLS - 3):
            temp_row = row
            temp_col = col
            window = []
            for _ in range(4):
                window.append(board[temp_row,temp_col])
                temp_row -= 1
                temp_col += 1
            score += evaluate_window(window,player)

    # backward diagonal \
    for row in range(NUM_OF_ROWS - 3):
        for col in range(NUM_OF_COLS - 3):
            temp_row = row
            temp_col = col
            window = []
            for _ in range(4):
                window.append(board[temp_row,temp_col])
                temp_row += 1
                temp_col += 1
            score += evaluate_window(window,player)

    return score

def pickBestMove(board, player):
    best_score = 0
    valid_moves = getValidMoves(board)
    best_col = random.choice(valid_moves)
    for col_pos in valid_moves:
        temp_board = board.copy()
        row_pos = getDiscRow(board, col_pos)
        temp_board = playMove(temp_board, row_pos, col_pos, player)
        score = scorePosition(temp_board, player)
        # print(col_pos, score)
        if score > best_score:
            best_score = score
            best_col = col_pos

    return best_col
            

def minimax(board, depth, alpha, beta, maximisingPlayer):
    if depth == 0 or gameOver(board):
        if gameOver(board):
            if winningMove(board, PLAYER):
                return None, -1000000
            elif winningMove(board, AI):
                return None, 1000000
            else:
                return None, 0
        else:
            return None, scorePosition(board, AI)
    valid_locations = getValidMoves(board)
    best_col = random.choice(valid_locations)
    if maximisingPlayer:
        score = - math.inf
        for col in valid_locations:
            new_board = board.copy()
            new_board = playMove(new_board, col, AI)
            new_score = minimax(new_board, depth - 1, alpha, beta, False)[1]
            if new_score > score:
                score = new_score
                best_col = col
            alpha = max(alpha, score)
            if alpha > beta:
                break
        return best_col, score
    else:
        score = math.inf
        for col in valid_locations:
            new_board = board.copy()
            new_board = playMove(new_board, col, PLAYER)
            new_score = minimax(new_board, depth - 1, alpha, beta, True)[1]
            if new_score < score:
                score = new_score
                best_col = col
            beta = min(beta, score)
            if alpha > beta:
                break
        return best_col, score

    

def main():
    board = createBoard()
    current_player = random.randint(1,2)
    run = True

    while run:
        # print(current_player)
        if current_player == 1:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    disc_pos = mouse_pos[0] // SQUARE_HEIGHT
                    if validMove(board, disc_pos):
                        board = playMove(board, disc_pos, current_player)
                        drawWindow(board, None, None)

                        if gameOver(board):
                            winner = 0
                            if winningMove(board, PLAYER):
                                winner = 1
                            elif winningMove(board, AI):
                                winner = 2
                            draw_winner(winner)
                            # print('game over')
                            run = False
                            break
                        current_player = 2
                        # drawWindow(board, None, None)
                        # pygame.time.delay(500)

        elif current_player == 2:
            # disc_pos = random.randint(0,NUM_OF_COLS - 1)
            # disc_pos = pickBestMove(board, current_player)
            disc_pos = minimax(board, 4, -math.inf, math.inf, True)[0]
            mouse_pos = None
            if validMove(board, disc_pos):
                board = playMove(board, disc_pos, current_player)
                drawWindow(board, mouse_pos, current_player)

                if gameOver(board):
                    winner = 0
                    if winningMove(board, PLAYER):
                        winner = 1
                    elif winningMove(board, AI):
                        winner = 2
                    draw_winner(winner)
                    # print('game over')
                    run = False
                    break
                current_player = 1 
            
                    

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