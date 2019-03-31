from tkinter import *
black = '#000000'
class GOL_board:
    '''
    A GOL_board will be responsible for the graphics in Conway's Game of Life.
    It will consist of small rectangles whose color will be set appropriately.
    '''

    def __init__(self, x=0, y=0, init_str=None):
        self.board = []
        self.board_bin = []
        self.root = Tk()
        root.geometry(str(x) + 'x' + str(y))
        self.board_canvas = Canvas(root, width=x, height=y)
        board_canvas.pack()

        for i in range(x // 10):
            temp_row = []
            temp_row_bin = []
            for j in range(y // 10):
                temp_row.append(board_canvas.create_rectangle(j * 10, \
                i * 10, (j + 1) * 10, (i + 1) * 10, fill=black, outline=black))
                temp_row_bin.append(0)
            board.append(temp_row)
            board_bin.append(temp_row_bin)

        if init_str != None:
            self.update(self.string_to_board(init_str))


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
        finally:
            f.close()


    def update(self, _board):
        # Update rectangle colors based on binary list
        for i, row in enumerate(_board):
            for j, col in enumerate(row):
                self.board_canvas.delete(self.board[i][j])
                if col == 0:
                    self.board_bin[i][j] = 0
                    self.board[i][j] = board_canvas.create_rectangle(j * 10, \
                    i * 10, (j + 1) * 10, (i + 1) * 10, fill=black, outline=black)
                else:
                    self.board_bin[i][j] = 1
                    self.board[i][j] = board_canvas.create_rectangle(j * 10, \
                    i * 10, (j + 1) * 10, (i + 1) * 10, fill=random_color(),
                    outline=random_color())

def random_color():
    '''
    Returns a string containing 6 hexadecimal digits which represents a color.
    '''
    color = '#'
    digits = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'a', 'b', 'c', 'd', 'e', 'f']
    for i in range(6):
        color += str(random.choice(digits))
    return color
