/*
 * Louis Santos
 * CS 011: C
 *
 * The following code can be used to perform either a bubble sort or a
 * minimum element sort on an array of no more than 32 integers. Integers are
 * given as command line arguments, as is the option to use bubble sort and to
 * supress command line output.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#define NUMS_MAX 32

int main(int argc, char * argv[]);
void print_error(char * argv[]);
void bubble_sort(int nums[], int nums_len);
void min_sort(int nums[], int nums_len);

void print_error(char * argv[])
{
    fprintf(stderr, "usage: %s [-b] [-q] list of 32 or fewer integers\n", \
    argv[0]);
}

int main(int argc, char *argv[])
{
    int arg = 1, index = 0, nums[NUMS_MAX], bubble = 0, quiet = 0;
    if(argc == 1)
    {
        print_error(argv);
        return 0;
    }
    for(arg = 1; arg < argc; arg++)
    {
        if(strcmp(argv[arg], "-b") == 0)
        {
            bubble = 1;
        }
        else if(strcmp(argv[arg], "-q") == 0)
        {
            quiet = 1;
        }
        else
        {
            if(index == NUMS_MAX)
            {
                print_error(argv);
                return 0;
            }
            nums[index] = atoi(argv[arg]);
            index++;
        }
    }
    if(index == 0)
    {
        print_error(argv);
        return 0;
    }
    printf("\n");
    if(bubble)
    {
        bubble_sort(nums, index);
    }
    else
    {
        min_sort(nums, index);
    }
    if(!quiet)
    {
        for(bubble = 0; bubble < index; bubble++)
        {
            printf("%d\n", nums[bubble]);
        }
    }
    return 0;
}

/*
 * @brief: Uses a minimum sorting algorithm to sort an array of integers in
 * place.
 *
 * @param nums: The array of integers to be sorted.
 * @param nums_len: The length of the nums array.
 */
void min_sort(int nums[], int nums_len)
{
    int start = 0, smallest = 0, index = 0;
    while(1)
    {
        /* set the index of the min element to the start of this sub-array */
        smallest = start;
        /* determine the smallest element in the sub-array from start to the end
           of nums */
        for(index = start; index < nums_len; index++)
        {
            if(nums[index] < nums[smallest])
            {
                smallest = index;
            }
        }
        /* swap nums[start] with nums[smallest], putting nums[smallest] in its
           proper place */
        index = nums[start];
        nums[start] = nums[smallest];
        nums[smallest] = index;
        /* increment start to consider the next sub-array */
        start++;
        /* break once we have reached the end of nums */
        if(start >= nums_len)
        {
            break;
        }
    }
    /* verify that nums is sorted */
    for (index = 1; index < nums_len; index++)
    {
        assert(nums[index] >= nums[index - 1]);
    }
}

/*
 * @brief: Uses a bubble sorting algorithm to sort an array of integers in
 * place.
 *
 * @param nums: The array of integers to be sorted.
 * @param nums_len: The length of the nums array.
 */
void bubble_sort(int nums[], int nums_len)
{
    int again = 1, i, temp;
    /* loop while the array is not sorted */
    while(again)
    {
        again = 0;
        /* loop through nums and swap all adjacent elements that are out of
           order with respect to each other */
        for(i = 0; i < nums_len - 1; i++)
        {
            if(nums[i] > nums[i + 1])
            {
                temp = nums[i];
                nums[i] = nums[i + 1];
                nums[i + 1] = temp;
                /* if any swapping has been done, indicate that another pass is
                   required */
                again = 1;
            }
        }
    }
    /* verify that nums is sorted */
    for (i = 1; i < nums_len; i++)
    {
        assert(nums[i] >= nums[i - 1]);
    }
}
