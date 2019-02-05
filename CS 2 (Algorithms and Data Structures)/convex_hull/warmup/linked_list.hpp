#ifndef __LINKEDLIST_H__
#define __LINKEDLIST_H__

struct Node
{
    int data;
    Node *next;

    /**
     * Constructor for a node structure.
     */
    Node(int data, Node *next)
    {
        this->data = data;
        this->next = next;
    }
};

/**
 * A class defining the shell of a linked list data structure.
 */
class List
{

/**
 * Public methods accessible by external code.
 */
public:
    List();
    ~List();
    void insert(int item);
    void printList();
    int getSize()
    {
      return num_elements;
    }

    Node *head;
    int num_elements;
};

#endif
