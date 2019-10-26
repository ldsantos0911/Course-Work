from tkinter import *
import random
black = '#000000'
box_size = 20
randoms = 800
x_board = 1500
y_board = 1000

class GOL_board:
    '''
    A GOL_board will be responsible for the graphics in Conway's Game of Life.
    It will consist of small rectangles whose color will be set appropriately.
    '''

    def __init__(self, x=x_board, y=y_board, init_str=None, fname=None, theme='', wallpaper=False):
        self.board = []
        self.board_bin = []
        self.root = Tk()
        self.root.geometry(str(x) + 'x' + str(y))
        self.board_canvas = Canvas(self.root, width=x, height=y)
        self.board_canvas.pack()
        self.board_canvas.config(background=black)
        self.theme = theme

        for i in range(y // box_size):
            temp_row = []
            temp_row_bin = []
            for j in range(x // box_size):
                temp_row.append(self.board_canvas.create_rectangle(j * box_size, \
                i * box_size, (j + 1) * box_size, (i + 1) * box_size, fill=black, outline=black))
                temp_row_bin.append(0)
            self.board.append(temp_row)
            self.board_bin.append(temp_row_bin)

        if init_str != None:
            self.update(self.string_to_board(init_str))

        if fname != None:
            self.update(self.from_file(fname))

        if init_str == None and fname == None:
            self.random_board()

        self.root.update()

    def get_rects_binary(self):
        return self.board_bin

    def string_to_board(self, _board_str):
        board_str = _board_str.split('\n')
        board_ret = []
        for row in board_str:
            row_lst = row.split(',')
            row_temp = []
            for col in row_lst:
                row_temp.append(int(col))
            board_ret.append(row_temp)
        return board_ret


    def from_file(self, fname):
        # Read board state from file in text format
        try:
            f = open(fname, 'w')
            board_ret = []
            for line in f:
                row_lst = line.split(',')
                row_temp = []
                for col in row_lst:
                    row_temp.append(int(col))
                board_ret.append(row_temp)
            return board_ret
        finally:
            f.close()

    def random_board(self):
        for i in range(randoms):
            y = box_size * random.randint(0, len(self.board_bin) - 1)
            x = box_size * random.randint(0, len(self.board_bin[0]) - 1)
            self.board[int(y / box_size)][int(x / box_size)] = \
                    self.board_canvas.create_rectangle(x, y, \
                    x + box_size, y + box_size, fill=random_color(self.theme))
            self.board_bin[int(y / box_size)][int(x / box_size)] = 1

    def update(self, _board):
        # Update rectangle colors based on binary list
        for i, row in enumerate(_board):
            for j, col in enumerate(row):
                self.board_canvas.delete(self.board[i][j])
                if col == 0:
                    self.board_bin[i][j] = 0
                    self.board[i][j] = self.board_canvas.create_rectangle(j * box_size, \
                    i * box_size, (j + 1) * box_size, (i + 1) * box_size, fill=black, outline=black)
                else:
                    self.board_bin[i][j] = 1
                    self.board[i][j] = self.board_canvas.create_rectangle(j * box_size, \
                    i * box_size, (j + 1) * box_size, (i + 1) * box_size, fill=random_color(self.theme))
        self.root.update()

def random_color(theme=''):
    '''
    Returns a string containing 6 hexadecimal digits which represents a color.
    '''
    color = '#'
    digits = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'a', 'b', 'c', 'd', 'e', 'f']

    if theme == 'warm':
        digits_0 = ['c', 'd', 'e', 'f']
        digits_1 = [0, 1, 2]
        color += str(random.choice(digits_0))
        for i in range(2):
            color += str(random.choice(digits))
        for i in range(3):
            color += str(random.choice(digits_1))
    elif theme == 'cool':
        digits_0 = [6, 7, 8, 9, 'a', 'b', 'c', 'd', 'e', 'f']
        digits_1 = [0, 1, 2, 3, 4]
        color += str(random.choice(digits_1))
        color += str(random.choice(digits))
        for i in range(2):
            color += str(random.choice(digits))
        color += str(random.choice(digits_0))
        color += str(random.choice(digits))
    elif theme == 'mono':
        color = '#FFFFFF'
    else:
        for i in range(6):
            color += str(random.choice(digits))
    return color
