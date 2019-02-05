#include <iostream>
using namespace std;

/**
 * @brief A class containing the state of a game of sudoku. 
 */
class Game
{
    public:
        void getMove(char move[], string message);
        void Run();
        Game();
        ~Game();
};
