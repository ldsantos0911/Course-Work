#include "grid.hpp"
#include <iostream>
#include <fstream>
#include <cstdlib>


using namespace std;

Grid::Grid(const char *filename)
{
    loadBoard(filename);
}

Grid::~Grid()
{
    /**
     * @brief Called when a Grid object is destroyed.
     */
}

void Grid::loadBoard(const char *filename)
{
    /**
     * @brief Populates a 2-d array accordingly from the file given.
     * 
     * @param filename the path to the file to be read and used to
     * populate
     */
    ifstream file;
    string line;
    file.open(filename);
    while(!file.is_open()) // loops while the entered file is invalid
    {
        string tmp;
        cout << "Please enter a valid filepath: ";
        cin >> tmp;
        cout << endl;
        cin.ignore();
        filename = tmp.c_str();
        file.open(filename);
    }
    int line_num = 0;

    while(getline(file, line))
    {
        for(int i = 0; i < 9; i++)
        {
            grid[line_num][i] = line[i];
            if(line[i] != ' ')
            {
                /*
                 * if the board has a number at (line_num, i), 
                 * designate this in moves[][] with a '-' to prevent
                 * later modification.
                 */
                moves[line_num][i] = '-';
            }
            else
            {
                moves[line_num][i] = line[i];
            }
        }
        line_num++;
    }
    file.close();
}

bool Grid::isComplete()
{
    /**
     * @brief Checks if the board is full.
     * 
     * @return Returns true if full, false if otherwise.
     */
    for(int i = 0; i < 9; i++)
    {
        for (int y : grid[i])
        {
            if(y == ' ')
            {
                return false;
            }
        }
    }
    return true;
}


bool Grid::checkSquare(int x, int y, char val)
{
    /**
     * @brief Checks if the value in question is already present in the 
     * square containing (x, y).
     * 
     * @param x the row to place the value.
     * @param y the column to place the value.
     * @param val the value to be placed.
     * 
     * @return whether or not the value can be validly placed at the 
     * given x and y.
     */
    int start_x = 0, start_y = 0;
    if(x > 5)
    {
        start_x = 6;
    }
    else if(x > 2)
    {
        start_x = 3;
    }

    if(y > 5)
    {
        start_y = 6;
    }
    else if(y > 2)
    {
        start_y = 3;
    }
    
    for(int i = start_x; i < start_x + 3; i++)
    {
        for(int j = start_y; j < start_y + 3; j++)
        {
            if(grid[i][j] == val)
                return false;
        }
    }
    return true;
}
        

string Grid::checkValid(int x, int y, char val)
{
    /**
     * @brief Checks whether or not a given move is a valid one.
     * 
     * @param x the row to insert val.
     * @param y the column to insert val.
     * @param val the value to be inserted during the move in question.
     * 
     * @return Empty string if move is valid, an appropriate error 
     * message if the move is not.
     */
    
    if(!(x < 9 && x >= 0 && y < 9 && y >= 0))
    {
        return "ERROR: Invalid coordinates! ";
    }
    if(!(val <= '9' || val > '0'))
    {
        return "ERROR: Invalid value! ";
    }
    if(moves[x][y] == '-')
    {
        return "ERROR: This space cannot be altered! ";
    }
    for(int i = 0; i < 9; i++)
    {
        if(grid[x][i] == val || grid[i][y] == val)
        {
            return "ERROR: This number is present in this row and/or \
column! ";
        }
    }
    if(!checkSquare(x, y, val))
    {
        return "ERROR: This number is present in this box! ";
    }
    return "";
}


string Grid::writeNum(int x, int y, char val)
{
    /**
     * @brief Attempt to make a move in sudoku, first checking if said 
     * move is valid.
     * 
     * @param x the row to insert val.
     * @param y the column to insert val.
     * 
     * @return Empty string if the move has been completed, an 
     * appropriate error message if the move has not.
     */
    string message = checkValid(x, y, val);
    if(message == "")
    {
        grid[x][y] = val;
        moves[x][y] = val;
    }
    
    return message;
}

string Grid::checkUndo(int x, int y)
{
    /**
     * @brief Check if the move at the given coordinates can be validly
     * undone.
     * 
     * @param x the row to check.
     * @param y the column to check.
     * 
     * @return Empty string if the undo is valid, appropriate error 
     * message if not.
     */
    if(!(x < 9 && x >= 0 && y < 9 && y >= 0))
    {
        return "ERROR: Invalid coordinates! ";
    }
    if(moves[x][y] == '-')
    {
        return "ERROR: This space cannot be altered! ";
    }
    return "";
}

string Grid::undoNum(int x, int y)
{
    /**
     * @brief Attempt to undo a move in sudoku, first checking if it is 
     * valid to do so.
     * 
     * @param x the x value to check.
     * @param y the y value to check.
     * 
     * @return Empty string if the undo is completed, appropriate error
     * message if not.
     */
    string message = checkUndo(x, y);
    if(message == "")
    {
        moves[x][y] = 0;
        grid[x][y] = ' ';
    }
    
    return message;
}

void Grid::display()
{
    /**
     * @brief Prints the board of a Sudoku game to the terminal.
     */
    string line = "-------------------------";
    for (int i = 0; i < 9; i++)
    {
        if(i % 3 == 0)
        {
            cout << line << endl;
        }
        
        for (int j = 0; j < 3; j++) // each block of 3 numbers
        {
            cout << "|";
            for (int k = 0; k < 3; k++) // each number in each block of 3
            {
                cout << " " << grid[i][j * 3 + k];
            }
            cout << " ";
        }
        cout << "|" << endl;
    }
    cout << line << endl;
}
        





    
    
    
            
            
    
    
