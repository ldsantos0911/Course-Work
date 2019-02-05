#include <iostream>
using namespace std;

/**
 * @brief A class representing the board of a sudoku game. Also contains
 * functions and variables essential to the execution of a full game.
 */
class Grid
{
    private:
        char grid[9][9]; /**<The board*/
        char moves[9][9]; /**<Distinguishes user moves from game board*/
        void loadBoard(const char *filename);
        bool checkSquare(int x, int y, char val);
        string checkValid(int x, int y, char val);
        string checkUndo(int x, int y);
    public:
        Grid(const char *filename);
        ~Grid();
        bool isComplete();
        string writeNum(int x, int y, char val);
        string undoNum(int x, int y);
        void display();
};
