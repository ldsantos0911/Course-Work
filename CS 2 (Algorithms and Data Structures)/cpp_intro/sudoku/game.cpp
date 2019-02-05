#include <iostream>
#include <string.h>
#include "game.hpp"
#include "grid.hpp"

using namespace std;

Game::Game()
{
    /**
     * @brief Constructs a Game object.
     */
}

Game::~Game()
{
    /**
     * @brief Called when a Game object is destroyed.
     */
}

void Game::getMove(char move[], string message)
{
    /**
     * @brief Get user input, preliminarily testing its validity. 
     * Interpret this input as a Sudoku move.
     * 
     * @param move[] a char array of length 4 to be modified in place 
     * with the different components of a move.
     * @param message a string containing either nothing or an error
     * message to be shown before prompting the user.
     */
    string move_proto = "";
    cout << message << "Enter a move: " << endl;
    getline(cin, move_proto);
    cout << endl;
    
    if(move_proto[0] == 'q')
    {
        move[0] = 'q';
        return;
    }
    
    while(move_proto[0] != 'u' && move_proto[0] != 'd')
    {
        cout << "ERROR: invalid move! Enter a move: " << endl;
        cin >> move_proto;
        cout << endl;
    }
    int i_real = 0;
    for(unsigned int i = 0; i < move_proto.size(); i++)
    {
        if(move_proto[i] != ' ') // If the current character is useful
        {
            if((move_proto[0] == 'u' && i_real > 2) || (move_proto[0] == \
            'd' && i_real > 3))
            {
                /*
                 * If the string entered is too long, for any number of 
                 * reasons, call getMove() again with an error message.
                 */
                return getMove(move, "ERROR: invalid move! ");
            }
            move[i_real] = move_proto[i];
            i_real++;
            
        }
    }
    
}

void Game::Run()
{
    /**
     * @brief Run and administer a game of Sudoku.
     */
    const char *filename;
    string tmp;
    cout << "Enter a board filepath: ";
    cin >> tmp;
    cin.ignore();
    cout << endl;
    filename = tmp.c_str();
    Grid board = Grid(filename);
    string message;
    char move[4];
    
    
    while(!board.isComplete())
    {
        board.display();
        cout << '\n';
        getMove(move, message);
        if(move[0] == 'u')
        {
            message = board.undoNum(move[1] - 49, move[2] - 49);
            // "- 49" gets the int from the chars in move[1] and move[2]
        }
        else if(move[0] == 'd')
        {
            message = board.writeNum(move[1] - 49, move[2] - 49, move[3]);
            // See above regarding "- 49"
        }
        else
        {
            // The only other permitted value of move[0] is 'q' for 'quit'.
            cout << "Goodbye!" << endl;
            return;
        }
    }
    cout << "Congatulations! The puzzle has been SOLVED!" << endl;
}
        
