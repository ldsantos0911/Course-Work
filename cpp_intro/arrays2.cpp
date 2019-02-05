/**
 * @file arrays1.cpp
 * @author The CS2 TA Team <cs2tas@caltech.edu>
 * @date 2014-2015
 * @copyright This code is in the public domain.
 *
 * @brief An array example.
 */

#include <iostream>
#include <cstdlib>
#include <ctime>

#define TEST_SIZE 10000000

using namespace std;

int max(int * arr, int size)
{
	/**
	 * @brief Finds the maximum value of an array.
     * 
     * @param arr pointer to the array to be used.
     * @param size the size of arr.
     * 
     * @return The element of arr with the highest numerical value.
     * 
	 */
	 
	int max = 0;
	for (int i = 0; i < size; i++)
	{
		if (*(arr + i) > max)
		{
			max = *(arr + i);
		}
	}
	return max;
}

double mean(int * arr, int size)
{
	/**
	 * @brief Calculates the arithmetic mean of the elements of an array.
     * 
     * @param arr pointer to the array to be used.
     * @param size the size of arr.
     * 
     * @return The arithmetic mean of the elements of arr.
     * 
	 */
	 
	double sum = 0.0;
	for (int i = 0; i < size; i++)
	{
		sum += *(arr + i);
	}
	return sum / size;
}

void replace_ascending(int * arr, int size)
{
	/**
	 * @brief Overwrites a given array with an ascending sequence.
     * 
     * @param arr pointer to the array to be overwritten.
     * @param size the size of arr.
     * 
	 */
	 
	for (int i = 0; i < size; i++)
	{
		*(arr + i) = i;
	}
}

void print_array(int * arr, int size)
{
    /**
     * @brief Prints an array to the terminal.
     * 
     * @param arr the pointer associated with the array to be printed.
     * @param size the size of arr.
     * 
     */
	for (int i = 0; i < size - 1; i++)
	{
		cout << *(arr + i) << ", ";
	}
	cout << *(arr + (size - 1));
}

/**
 * @brief Sets up and runs an array example.
 */
int main(int argc, char ** argv)
{

    /*-------- CHANGE NOTHING BELOW THIS LINE FOR PART 1 --------*/
    int * test_values = new int[TEST_SIZE];
    int real_size;

    // seed the PRNG
    srand(time(nullptr));

    // initialize the test array to garbage
    for (int i = 0; i < TEST_SIZE; i++)
    {
        test_values[i] = rand();
    }

    // determine a real size
    real_size = TEST_SIZE - (rand() % 20);

    // initialize the meaningful part of the test array to random numbers
    // all of which are less than one million
    for (int i = 0; i < real_size; i++)
    {
        test_values[i] = rand() % 1000000;
    }
    /*-------- CHANGE NOTHING ABOVE THIS LINE FOR PART 1 --------*/

    //
    // TODO: do your stuff here with the array `test_values`
    // of dynamic size `real_size`
    //
    
    cout << "Size: " << real_size << endl;
	cout << "Max: " << max(test_values, real_size) << endl;
	replace_ascending(test_values, real_size);
    cout << "Last element: " << test_values[real_size - 1] << endl;
	cout << "Mean of sequence: " << mean(test_values, real_size) << endl;
	/* Using the sequence to test the mean function allows cross-checking
	 * with the formula n/2.
	 */
    delete[] test_values;
}

