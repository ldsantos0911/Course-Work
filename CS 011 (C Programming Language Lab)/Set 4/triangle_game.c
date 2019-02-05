/*
 * Louis Santos
 * CS 011: C
 *
 * The following code uses the helper functions defined in triangle_routines
 * to get a board for the Triangle Game from the user and attempt to solve
 * said board. Then, it prints the solution (if any) to the terminal in
 * reverse order.
 */

#include "triangle_routines.h"
#include <stdio.h>

#define NMOVES (36)
#define BSIZE (15)

/* The array containing all possible moves in the triangle game */
int moves[NMOVES][3] =
{
  {0, 1, 3}, {3, 1, 0}, {0, 2, 5}, {5, 2, 0}, {1, 3, 6}, {6, 3, 1},
  {2, 5, 9}, {9, 5, 2}, {3, 6, 10}, {10, 6, 3}, {5, 9, 14}, {14, 9, 5},
  {3, 4, 5}, {5, 4, 3}, {6, 7, 8}, {8, 7, 6}, {7, 8, 9}, {9, 8, 7},
  {10, 11, 12}, {12, 11, 10}, {11, 12, 13}, {13, 12, 11}, {12, 13, 14},
  {14, 13, 12}, {1, 4, 8}, {8, 4, 1}, {4, 8, 13}, {13, 8, 4}, {2, 4, 7},
  {7, 4, 2}, {4, 7, 11}, {11, 7, 4}, {3, 7, 12}, {12, 7, 3}, {5, 8, 12},
  {12, 8, 5}
};

int main(void);

/* Return the number of pegs on the board. */
int npegs(int board[]);

/* Return 1 if the move is valid on this board, otherwise return 0. */
int valid_move(int board[], int move[]);

/* Make this move on this board. */
void make_move(int board[], int move[]);

/* Unmake this move on this board. */
void unmake_move(int board[], int move[]);

/*
 * Solve the game starting from this board.  Return 1 if the game can
 * be solved; otherwise return 0.  Do not permanently alter the board passed
 * in. Once a solution is found, print the boards making up the solution in
 * reverse order.
 */
int solve(int board[]);

/**
 * @brief Accepts a triangle game board, then returns the number of pegs still
 * remaining on the board.
 *
 * @param board: The triangle game board.
 *
 * @return An int representing the number of pegs.
 */
int npegs(int board[])
{
    int space = 0, count = 0;
    for(; space < BSIZE; space++)
    {
        if(board[space] == 1)
        {
            count++;
        }
    }
    return count;
}

/*
 * @brief Accepts a triangle game board and a move on that board to test for
 * validity.
 *
 * @param board: The triangle game board.
 * @param move: The triangle game move.
 *
 * @return An int representing whether or not this move is valid.
 */
int valid_move(int board[], int move[])
{
    /* Evaluate whether or not the first peg can be validly jumped over a
     * middle peg to the last space, and return the result. */
    return (board[move[0]] == 1) && (board[move[1]] == 1) &&
    (board[move[2]] == 0);
}

/*
 * @brief Makes a move on a triangle game board.
 *
 * @param board: The triangle game board.
 * @param move: The triangle game move to be made.
 */
void make_move(int board[], int move[])
{
    board[move[0]] = board[move[1]] = 0;
    board[move[2]] = 1;
}

/*
 * @brief Undoes a specific move on a triangle game board, assuming the move
 * has already been made.
 *
 * @param board: The triangle game board.
 * @param move: The move to be unmade.
 */
void unmake_move(int board[], int move[])
{
    /* Effectively undo one peg jumping over another. */
    board[move[0]] = board[move[1]] = 1;
    board[move[2]] = 0;
}

/*
 * @brief Recursively solves a given triangle game board, printing each move
 * in reverse order if the board is solvable.
 *
 * @param board: The triangle game board.
 *
 * @return An int representing whether or not the board is solvable.
 */
int solve(int board[])
{
    int i = 0, solvable = 0;
    if(npegs(board) == 1)
    {
        /* If the board is solved, return 1 and print the final state. */
        triangle_print(board);
        return 1;
    }
    for(; i < NMOVES; i++)
    {
        if(valid_move(board, moves[i]))
        {
            /* If the current move is valid, make it, recursively check board
             * solvability, unmake the move, then print the board and return 1
             * if the board is solvable by the recursive check. */
            make_move(board, moves[i]);
            solvable = solve(board);
            unmake_move(board, moves[i]);
            if(solvable)
            {
                triangle_print(board);
                return 1;
            }
        }
    }
    /* If the board is not solvable, return 0 */
    return 0;
}

/*
 * @brief Get input from the user to construct the game board, then attempt to
 * solve the board and print an appropriate error message if the board is
 * unsolvable.
 */
int main(void)
{
    int solvable = 0;
    int board[BSIZE];
    triangle_input(board);
    solvable = solve(board);
    if(!solvable)
    {
        printf("This board is not solvable!\n");
    }
    return 0;
}
