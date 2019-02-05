/*
 * Louis Santos
 * CS 11: C track
 *
 * This program simulates a simple one-dimensional cellular automaton, running
 * on a given number of cells for a given number of generations, as specified
 * by command line arguments. This version treats the array of cells as an
 * array, using the appropriate indexing scheme.
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
        if(!cell_array[i])
        {
            printf(".");
        }
        else
        {
            printf("*");
        }
    }
    printf("\n");
}

/*
 * @brief Runs a one-dimensional version of the game of life.
 */
int main(int argc, char *argv[])
{
    int cells = 0, generations = 0, *cell_array, *cell_modified, i = 1;
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
    for(; i < cells - 1; i++)
    {
        if(rand() > RAND_MAX / 2)
        {
            cell_array[i] = 1;
        }
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
    int i = 0;
    i = 1;
    for(; i < cells - 1; i++)
    {

        if(!cell_array[i] && cell_array[i - 1] != cell_array[i + 1])
        {
            cell_modified[i] = 1;
        }
        else
        {
            cell_modified[i] = 0;
        }
    }
    for(i = 0; i < cells; i++)
    {
        cell_array[i] = cell_modified[i];
    }
}
