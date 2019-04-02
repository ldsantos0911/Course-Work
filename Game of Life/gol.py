from board import *
import time

def play(**kwargs):
    game_board = GOL_board()
    while True:
        game_board.update(update(game_board.get_rects_binary()))
        time.sleep(.0001)

def update(board_bin):
    ret_board = board_bin.copy()
    for y, row in enumerate(board_bin):
        for x, col in enumerate(row):
            alive = (col == 1)
            neighbors = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y - 1),
                         (x, y + 1), (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]
            living_neigh = 0
            for i, tup in enumerate(neighbors):
                if tup[0] < len(row) and tup[0] >= 0 and \
                tup[1] < len(board_bin) and tup[1] >= 0 and \
                board_bin[tup[1]][tup[0]] == 1:
                   living_neigh += 1

            if alive and (living_neigh < 2 or living_neigh > 3):
                ret_board[y][x] = 0
            if alive and (living_neigh == 2 or living_neigh == 3):
                ret_board[y][x] = 1
            if not alive and (living_neigh == 3):
                ret_board[y][x] = 1
    return ret_board


if __name__== '__main__':
    play()
