/**
 * @file
 * @author The CS2 TA Team
 * @version 1.0
 * @date 2013-2014
 * @copyright This code is in the public domain.
 *
 * @brief The bubble sort, quick sort, merge sort, and in-place quicksort
 * algorithms (implementation).
 *
 */
#include "sorter.hpp"

int main(int argc, char* argv[])
{
    // Set up buffers and data input

    std::vector<int> nums;
    std::string line;
    char *filename;
    int sort_type;

    // Ensure that at most one type of sort and at least a filename are specified.
    if (argc > 3 || argc < 2)
    {
        usage();
    }

    // default sort is bubble sort
    sort_type = BUBBLE_SORT;

    // Figure out which sort to use
    for (int i = 1; i < argc; ++i)
    {
        char *arg = argv[i];
        if (strcmp(arg, "-b") == 0) { sort_type = BUBBLE_SORT; }
        else if (strcmp(arg, "-q") == 0) { sort_type = QUICK_SORT; }
        else if (strcmp(arg, "-m") == 0) { sort_type = MERGE_SORT; }
        else if (strcmp(arg, "-qi") == 0) { sort_type = QUICK_SORT_INPLACE; }
        else { filename = argv[i]; }
    }

    // Read the file and fill our vector of integers
    // THIS FUNCTION IS STUDENT IMPLEMENTED
    readFile(filename, nums);

    switch (sort_type)
    {
        case BUBBLE_SORT:
        print_vector(bubbleSort(nums));
        break;

        case QUICK_SORT:
        print_vector(quickSort(nums));
        break;

        case MERGE_SORT:
        print_vector(mergeSort(nums));
        break;

        case QUICK_SORT_INPLACE:
        quicksort_inplace(nums, 0, nums.size() - 1);
        print_vector(nums);
        break;

        default:
        usage();
        break;
    }
    return 0;
}

/**
 * Usage    Prints out a usage statement and exits.
 */
void usage()
{
    std::cerr << usage_string << std::endl;
    exit(1);
}

/**
 * TO STUDENTS: In all of the following functions, feel free to change the
 * function arguments and/or write helper functions as you see fit. Remember to
 * add the function header to sorter.hpp if you write a helper function!
 */

/**
 * @brief swaps the two given elements in the given list.
 *
 * @param list the list containing the elements to be swapped.
 * @param i the index of the first element to be swapped.
 * @param j the index of the second element to be swapped.
 *
 * @return the modified list.
 */
std::vector<int> swap_elements(std::vector<int> &list, int i, int j)
{
  int temp = list[i];
  list[i] = list[j];
  list[j] = temp;
  return list;
}
/**
 * Moves through the elements of list, swapping any improperly ordered elements
 * and repeating while the elements of the list are unsorted.
 *
 * bool again = false;
 * IF list.size() < 2
 *    RETURN list
 * FOR int i = 0; i < list.size() - 1; i++
 *    IF list[i] < list[i + 1]
 *        swap_elements(list, i, i + 1)
 *        again = true
 * IF again == true
 *    bubbleSort(list)
 */
std::vector<int> bubbleSort(std::vector<int> &list)
{
    if(list.size() < 2)
    {
      return list;
    }
    bool again = false;
    for(unsigned int i = 0; i < list.size() - 1; i++)
    {
      if(list[i] > list[i + 1])
      {
        swap_elements(list, i, i + 1);
        again = true;
      }
    }
    if(again)
      bubbleSort(list);
    return list;
}


/**
 * @brief Append one vector to the end of another.
 *
 * @param a the vector to which to append the other vector.
 * @param b the vector to append to a.
 *
 * @return The combined vector.
 */
std::vector<int> combineList(std::vector<int> a, std::vector<int> &pivot, \
  std::vector<int> b)
{
  a.insert(a.begin(), pivot.begin(), pivot.end());
  a.insert(a.begin(), b.begin(), b.end());
  return a;
}

/**
 * Sorts a list of numbers by choosing a pivot point and placing
 * all values less than that pivot to the left of it and all values greater
 * than it to the right. Once that is done for a pivot, the sublists are sorted
 * and combined recursively. Once the list has been partitioned to either 1 or 0
 * elements, the sorted list is returned.
 *
 * IF list.size() < 2
 *    RETURN list
 * pivot = middle index of list
 * vector<int> a, b, pivot_l
 * pivot_l.push_back(list[pivot])
 * FOR int i = 0; i < list.size(); i++
 *    IF i != pivot
 *        IF list[i] < list[pivot]
 *            a.push_back(list[i])
 *        ELSE
 *            b.push_back(list[i])
 * RETURN combineList(quickSort(a), pivot_l, quickSort(b))
 */
std::vector<int> quickSort(std::vector<int> &list)
{
    if(list.size() < 2)
      return list;
    int pivot = (int) (list.size() / 2);
    std::vector<int> a, b, pivot_l;
    pivot_l.push_back(list[pivot]);
    for(int i = 0; i < (int)list.size(); i++)
    {
      if(i != pivot)
      {
        if(list[i] < list[pivot])
          a.push_back(list[i]);
        else
          b.push_back(list[i]);
      }
    }

    return combineList(quickSort(b), pivot_l, quickSort(a));
}

/**
 * This sorts a given list of integers by first merging (into sorted sublists
 * of width 2*width) adjacent sublists of width 1, then width 2, and so on until
 * the width reaches the width of the overall list, at which point the loop stops.
 *
 * IF list.size() > 1
 *    width = 1
 *    vector<int> left, right, merged
 *    WHILE wisth <= list.size() / 2
 *        FOR i = 0; i < list.size() / width / 2; i++
 *            FOR  j = i * width * 2; j < i * width * 2 + width; j++
 *                left.push_back(list[j])
 *                right.push_back(list[j + width])
 *            merged = merge(left, right)
 *            FOR k = i * width * 2; k < i * width * 2 + merged.size(); k++
 *                list[k] = merged[k - i * width * 2]
 *            merged.clear()
 *            left.clear()
 *            right.clear()
 *        width *= 2
 *    IF list HAS ODD NUM ELEMENTS
 *        left.assign(ALL OF list BUT LAST ELEMENT)
 *        right.push_back(LAST ELEMENT of list)
 *        merged = merge(left, right)
 *        REPLACE list WITH merged
 * return list
 */
std::vector<int> mergeSort(std::vector<int> &list)
{

    if(list.size() > 1)
    {
      unsigned int width = 1;
      std::vector<int> left, right, merged;

      while(width <= list.size() / 2)
      {
        for(unsigned int i = 0; i < (unsigned int) (list.size() / width / 2); i++)
        {
          for(unsigned int j = i * width * 2; j < i * width * 2 + width; j++)
          {
            left.push_back(list[j]);
            right.push_back(list[j + width]);
          }
          merged = merge(left, right);

          for(unsigned int k = i * width * 2; k < i * width * 2 + merged.size(); k++)
          {
            list[k] = merged[k - i * width * 2];
          }
          merged.clear();
          left.clear();
          right.clear();
        }
        width *= 2;
      }
      if(list.size() % 2 == 1)
      {
        left.assign(list.begin(), list.end() - 1);
        right.push_back(list[list.size() - 1]);
        merged = merge(left, right);
        list.assign(merged.begin(), merged.end());
      }
    }
    return list;
}

/**
 * @brief Merge two vectors into one, simultaneously placing all of the merged
 * vector's elements in ascending order.
 *
 * @param left The first vector to be merged.
 * @param right The second vector to be merged.
 *
 * @return The merged vector.
 */
std::vector<int> merge(std::vector<int> &left, std::vector<int> &right)
{
    std::vector<int>::iterator left_i = left.begin(), right_i = right.begin();
    int n = 0;
    while(right_i != right.end())
    {
      if(left_i == left.end())
      {
        left.push_back(*right_i);
        std::advance(right_i, 1);
      }
      else if(*left_i >= *right_i)
      {
        left.insert(left_i, *right_i);
        std::advance(right_i, 1);
        n++;
        left_i = left.begin();
        std::advance(left_i, n);
      }
      else
      {
        std::advance(left_i, 1);
        n++;
      }
    }
    return left;
}


/*
 * @brief Places all elements of a sublist of a vector which are less than the
 * center element of the sublist to the left of the center and all which are
 * greater to the right.
 *
 * @param list: the vector to be rearranged.
 * @param left: the left most index of the sublist to consider
 * @param right: the right most index of the sublist to considered
 *
 * @return The new location of the pivot point.
 */
int inplace_partition(std::vector<int> &list, int left, int right)
{
  int pivot = (int)(right + left) / 2;
  int temp, low_index = left, high_index = pivot + 1;

  while(low_index < pivot || high_index <= right)
  {

    if(list[low_index] > list[pivot] && list[high_index] < list[pivot])
    {
      temp = list[low_index];
      list[low_index] = list[high_index];
      list[high_index] = temp;

    }
    else if(list[low_index] > list[pivot])
    {
      temp = list[low_index];
      for(int i = low_index; i < pivot; i++)
      {
        list[i] = list[i + 1];
      }
      list[pivot] = temp;
      pivot--;
      low_index--;
    }
    else if(list[high_index] < list[pivot])
    {
      temp = list[high_index];
      for(int i = high_index; i > pivot; i--)
      {
        list[i] = list[i - 1];
      }
      list[pivot] = temp;
      pivot++;
      high_index--;
    }
    if(low_index < pivot)
      low_index++;
    if(high_index <= right)
      high_index++;
  }
  return pivot;
}

/*
 * quicksort_inplace:  In-place version of the quicksort algorithm. Requires
 *              O(1) instead of O(N) space, same time complexity. Each call of
 *              the method partitions the list around the pivot (an item taken
 *              from the middle of the array) with items left of the pivot
 *              smaller than it and items to its right larger than it. Then the
 *              method recursively sorts the left and right portions of the list
 *              until it reaches its base case: a list of length 1 is already
 *              sorted.
 *
 * IF right - left > 0
 *    pivot = inplace_partition(list, left, right)
 *    quicksort_inplace(list, left, pivot - 1)
 *    quicksort_inplace(list, pivot + 1, right)
 *
 * @param list: pointer to integer array to be sorted
 * @param left: the lower index of the sublist being considered
 * @param right: the higher index of the sublist being considered
 *
 * @returns:    Nothing, the array is sorted IN-PLACE.
 *
 */
void quicksort_inplace(std::vector<int> &list, int left, int right)
{
    if(right - left > 0)
    {
      int pivot = inplace_partition(list, left, right);
      quicksort_inplace(list, left, pivot - 1);
      quicksort_inplace(list, pivot + 1, right);
    }
}
