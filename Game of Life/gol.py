from board import *
import threading
import subprocess
from appscript import app, mactypes
from PIL import Image
import time
import sys

buffer = 1

def play(theme_str='', wallpaper=False):
    game_board = GOL_board(theme=theme_str)
    if wallpaper:
        try:
            game_board.root.withdraw()
            wallpapers(game_board)
        finally:
            subprocess.Popen('rm -f board[0-9]*', shell=True)
    else:
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

def wallpapers(game_board):
    for i in range(buffer):
        game_board.update(update(game_board.get_rects_binary()))
        save_board(game_board, fname='board{}'.format(i))
    start_save = buffer
    start_set = 0
    while True:
        set_papers(start_set, game_board)
        del_buff(start_save - buffer)
        gen_papers(start_save, game_board)
        start_save += buffer
        start_set += buffer

def gen_papers(start, game_board):
    for i in range(start, buffer + start):
        game_board.update(update(game_board.get_rects_binary()))
        save_board(game_board, fname='board{}'.format(i))

def set_papers(start, game_board):
    # Set the wallpaper repeatedly
    for i in range(start, buffer + start):
        filename = 'board{}.jpg'.format(i)
        app('Finder').desktop_picture.set(mactypes.File(filename))
        time.sleep(.0001)

def save_board(game_board, fname=''):
    game_board.board_canvas.postscript(file=(fname + '.eps'))
    img = Image.open((fname + '.eps'))
    img.save((fname + '.jpg'), 'jpeg')


def del_buff(start):
    for i in range(start, buffer + start):
        SCRIPT = """rm -f """ + 'board{}.jpg'.format(i)
        subprocess.Popen(SCRIPT, shell=True)
        SCRIPT = """rm -f """ + 'board{}.eps'.format(i)
        subprocess.Popen(SCRIPT, shell=True)

if __name__== '__main__':
    if len(sys.argv) >= 2:
        wallpaper_val = False
        if '-w' in sys.argv:
            wallpaper_val = True
        play(sys.argv[1], wallpaper=wallpaper_val)
    else:
        play()
