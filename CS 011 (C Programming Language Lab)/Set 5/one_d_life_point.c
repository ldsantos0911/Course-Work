/*
 * Louis Santos
 * CS 11: C track
 *
 * This program simulates a simple one-dimensional cellular automaton, running
 * on a given number of cells for a given number of generations, as specified
 * by command line arguments. This version uses pointers to locations in the
 * cell array to access and modify values.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "memcheck.h"

int main(int argc, char *argv[]);
void print_usage(char *argv[]);
void one_d_life(int *cell_array, int cells, int *cell_modified);
void print_cells(int *cell_array, int cells);

/*
 * @brief Print the usage message for this program to the terminal.
 */
void print_usage(char *argv[])
{
    fprintf(stderr, "usage: %s cells generations\n", argv[0]);
}

/*
 * @brief Prints an array to the terminal.
 *
 * @param cell_array pointer to the start of the array to print.
 * @param cells length of cell_array
 */
void print_cells(int *cell_array, int cells)
{
    int i = 0;
    for(; i < cells; i++)
    {
        if(!(*cell_array))
        {
            printf(".");
        }
        else
        {
            printf("*");
        }
        cell_array++;
    }
    printf("\n");
}

/*
 * @brief Runs a one-dimensional version of the game of life.
 */
int main(int argc, char *argv[])
{
    int cells = 0, generations = 0, *cell_array, *cell_modified, \
    *iterate, i = 1;
    srand(time(0));
    if(argc < 3)
    {
          print_usage(argv);
          exit(1);
    }
    cells = atoi(argv[1]);
    generations = atoi(argv[2]);
    cell_array = (int*)calloc(cells, sizeof(int));
    if(cell_array == NULL)
    {
        fprintf(stderr, "Error! Memory allocation failed!\n");
        exit(1);
    }
    iterate = cell_array + 1;
    for(; i < cells - 1; i++)
    {
        if(rand() > RAND_MAX / 2)
        {
            *iterate = 1;
        }
        iterate++;
    }
    for(; generations > 0; generations--)
    {
        print_cells(cell_array, cells);
        cell_modified = (int*)calloc(cells, sizeof(int));
        if(cell_modified == NULL)
        {
            fprintf(stderr, "Error! Memory allocation failed!\n");
            exit(1);
        }
        one_d_life(cell_array, cells, cell_modified);
        free(cell_modified);
    }
    free(cell_array);
    print_memory_leaks();
    return 0;
}

/*
 * @brief Updates the passed according to the formula given in the assignment.
 *
 * @param cell_array Pointer to the start of the array to update.
 * @param cells Length of cell_array.
 */
void one_d_life(int *cell_array, int cells, int *cell_modified)
{
    int *prev, *current, *next, *current_mod, i = 0;
    current = cell_array;
    current_mod = cell_modified;
    for(; i < cells; i++)
    {
        *current_mod = *current;
        current++;
        current_mod++;
    }
    current = cell_array + 1;
    current_mod = cell_modified + 1;
    prev = current_mod - 1;
    next = current_mod + 1;
    i = 1;
    for(; i < cells - 1; i++)
    {
        if(*current_mod == 0 && *prev != *next)
        {
            *current = 1;
        }
        else
        {
            *current = 0;
        }
        current_mod++;
        current++;
        prev++;
        next++;
    }
}
