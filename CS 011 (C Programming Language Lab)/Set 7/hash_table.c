/*
 * CS 11, C Track, lab 7
 *
 * FILE: hash_table.c
 *
 *       Implementation of the hash table functionality.
 *
 */

/*
 * Include the declaration of the hash table data structures
 * and the function prototypes.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "hash_table.h"
#include "memcheck.h"


/*** Hash function. ***/

int hash(char *s)
{
    int hash_key = 0, i = 0, size = strlen(s);
    for(; i < size; i++)
    {
        hash_key += (int) s[i];
    }
    return hash_key % NSLOTS;
}


/*** Linked list utilities. ***/

/* Create a single node. */
node *create_node(char *key, int value)
{
    node * new_node = (node*)malloc(sizeof(node));
    if(new_node == NULL)
    {
        fprintf(stderr, "Issue allocating memory. Exiting...");
        exit(1);
    }
    new_node->key = key;
    new_node->value = value;
    new_node->next = NULL;
    return new_node;
}


/* Free all the nodes of a linked list. */
void free_list(node *list)
{
    node *temp;
    while(list != NULL)
    {
        temp = list->next;
        free(list->key);
        free(list);
        list = temp;
    }
}


/*** Hash table utilities. ***/

/* Create a new hash table. */
hash_table *create_hash_table()
{
    hash_table *table = (hash_table*)malloc(sizeof(hash_table));
    if(table == NULL)
    {
        fprintf(stderr, "Issue allocating memory. Exiting...");
        exit(1);
    }
    table->slot = (node**)calloc(NSLOTS, sizeof(node*));
    if(table->slot == NULL)
    {
        fprintf(stderr, "Issue allocating memory. Exiting...");
        exit(1);
    }
    return table;
}


/* Free a hash table. */
void free_hash_table(hash_table *ht)
{
    int i = 0;
    for(; i < NSLOTS; i++)
    {
        free_list(ht->slot[i]);
    }
    free(ht->slot);
    free(ht);
}


/*
 * Look for a key in the hash table.  Return 0 if not found.
 * If it is found return the associated value.
 */
int get_value(hash_table *ht, char *key)
{
    int hash_key = hash(key);
    node * row = (ht->slot)[hash_key], *col;
    if(row == NULL)
    {
        return 0;
    }
    col = row;
    while(col != NULL)
    {
        if(strcmp(col->key, key) == 0)
        {
            return col->value;
        }
        col = col->next;
    }
    return 0;
}


/*
 * Set the value stored at a key.  If the key is not in the table,
 * create a new node and set the value to 'value'.  Note that this
 * function alters the hash table that was passed to it.
 */
void set_value(hash_table *ht, char *key, int value)
{
    int hash_key = hash(key), found = 0;
    node *row = (ht->slot)[hash_key], *col, *col_prev;
    if(row == NULL)
    {
        ht->slot[hash_key] = create_node(key, value);
    }
    else
    {
        col = row;
        while(col != NULL)
        {
            if(strcmp(col->key, key) == 0)
            {
                found = 1;
                col->value = value;
                free(key);
                break;
            }
            col_prev = col;
            col = col->next;
        }
        if(!found)
        {
            col_prev->next = create_node(key, value);
        }
    }
}


/* Print out the contents of the hash table as key/value pairs. */
void print_hash_table(hash_table *ht)
{
    int i = 0;
    node *col;
    for(; i < NSLOTS; i++)
    {
        col = ht->slot[i];
        while(col != NULL)
        {
            printf("%s %d\n", col->key, col->value);
            col = col->next;
        }
    }
}
