from tkinter import *
import random
black = '#000000'
box_size =7
class GOL_board:
    '''
    A GOL_board will be responsible for the graphics in Conway's Game of Life.
    It will consist of small rectangles whose color will be set appropriately.
    '''

    def __init__(self, x=1000, y=1000, init_str=None, fname=None):
        self.board = []
        self.board_bin = []
        self.root = Tk()
        self.root.geometry(str(x) + 'x' + str(y))
        self.board_canvas = Canvas(self.root, width=x, height=y)
        self.board_canvas.pack()

        for i in range(x // box_size):
            temp_row = []
            temp_row_bin = []
            for j in range(y // box_size):
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
        for i in range(5000):
            y = box_size * random.randint(0, len(self.board_bin) - 1)
            x = box_size * random.randint(0, len(self.board_bin[0]) - 1)
            self.board[int(y / box_size)][int(x / box_size)] = \
                    self.board_canvas.create_rectangle(x, y, \
                    x + box_size, y + box_size, fill=random_color())
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
                    i * box_size, (j + 1) * box_size, (i + 1) * box_size, fill=random_color())
        self.root.update()

def random_color():
    '''
    Returns a string containing 6 hexadecimal digits which represents a color.
    '''
    color = '#'
    digits = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'a', 'b', 'c', 'd', 'e', 'f']
    for i in range(6):
        color += str(random.choice(digits))
    return color
