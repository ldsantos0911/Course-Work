#ifndef __LOOPEDLIST_H__
#define __LOOPEDLIST_H__

#include <vector>
#include "linked_list.hpp"
using namespace std;

inline bool is_looped(List* lst)
{
  int index = 0;
  Node * temp = lst->head;
  while(temp != nullptr)
  {
    if(index > lst->num_elements)
      return true;
    temp = temp->next;
    index++;
  }
  return false;
}

#endif
