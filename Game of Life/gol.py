from board import *

def play(**kwargs):
    pass

def update(board_bin):
    ret_board = board_bin.copy()
    for x, row in enumerate(board_bin):
        for y, col in enumerate(row):
            alive = (col == 1)
            neighbors = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y - 1),
                         (x, y + 1), (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]
            living_neigh =
                len([i for i in neighbors if (i[0] < len(board)) and (i[0] >= 0)
                                        and (i[1] < len(row)) and (i[1] >= 0)])
            if alive and (living_neigh < 2 or living_neigh > 3):
                ret_board[x][y] = 0
            elif alive and (living_neigh == 2 or living_neigh == 3):
                ret_board[x][y] = 1
            elif not alive and (living_neigh == 3):
                ret_board[x][y] = 1
    return ret_board


if __name__== '__main__':
    pass
