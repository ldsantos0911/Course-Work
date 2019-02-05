/*
 * Louis Santos
 * CS 11: C Track
 *
 * This program fields user input in the way of command line arguments,
 * creating a linked list of user-generated integers. Then, it sorts the
 * integers with the quicksort algorithm, finally printing the sorted list
 * if the user has not specified that nothing is to be printed.
 */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "linked_list.h"
#include "memcheck.h"

void print_error(char * argv[]);
int main(int argc, char * argv[]);
node *quicksort(node * list);
node *do_quicksort(node * list);

/*
 * @brief Prints a usage message to the terminal.
 *
 * @param argv: The command line arguments
 */
void print_error(char * argv[])
{
    fprintf(stderr, "usage: %s [-q] integers\n", \
    argv[0]);
}

int main(int argc, char * argv[])
{
    int arg = 1, index = 0, quiet = 0;
    node *current = NULL, *sorted = NULL;

    if(argc == 1)
    {
        print_error(argv);
        return 0;
    }
    for(arg = 1; arg < argc; arg++)
    {
        if(strcmp(argv[arg], "-q") == 0)
        {
            quiet = 1;
            continue;
        }

        current = create_node(atoi(argv[arg]), current);

        if (current == NULL)
        {
            fprintf(stderr, "Fatal error: out of memory. "
                    "Terminating program.\n");
            exit(1);
        }
        index++;
    }
    if(!index)
    {
        print_error(argv);
        exit(1);
    }
    printf("\n");

    sorted = quicksort(current);
    if(!quiet)
    {
        print_list(sorted);
    }
    free_list(sorted);
    print_memory_leaks();
    return 0;
}

/*
 * @brief: Uses the quicksort algorithm to sort a singly-linked list of
 * integers.
 *
 * @param list: A pointer to the first node of a singly linked list.
 *
 * @return A pointer to the first node of the sorted linked list.
 */
node *quicksort(node * list)
{
    node *list_front = NULL, *low_list = NULL, *high_list = NULL,
    *sorted = NULL, *low = NULL, *high = NULL;

    if(list == NULL || list->next == NULL)
    {
        return list;
    }
    list_front = create_node(list->data, NULL);
    for(sorted = list->next; sorted != NULL; sorted = sorted->next)
    {
        if(sorted->data < list_front->data)
        {
            low_list = create_node(sorted->data, low_list);
        }
        else if(sorted->data >= list_front->data)
        {
            high_list = create_node(sorted->data, high_list);
        }
    }
    high = quicksort(high_list);
    low = quicksort(low_list);
    list_front->next = high;
    high = list_front;
    sorted = append_lists(low, high);
    free_list(low);
    free_list(high);
    free_list(list);
    assert(is_sorted(sorted));
    return sorted;
}
