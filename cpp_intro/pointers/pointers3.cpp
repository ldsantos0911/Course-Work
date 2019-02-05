/**
 * @file pointers3.cpp
 * @author The CS2 TA Team <cs2tas@caltech.edu>
 * @date 2015
 * @copyright This code is in the public domain.
 *
 * @brief Pointer-fu Exercise 3: "Entangled" pointers
 */

#include <cstdlib>
#include <iostream>

using namespace std;

/**
 * @brief Set two pointers to the same memory and free them.
 */
int main(int argc, char *argv[])
{
    int *a, *b;

    // Allocate an array of 10 ints.
    a = (int *) malloc(10 * sizeof(int));

    // Now `b` points to the same array of ints.
    b = a;

    free(a);
    
    /*
     * Since a and b point to the same memory location, it is not 
     * necessary to free it twice. Freeing a and b frees an already 
     * freed memory location. I fixed the error by only freeing a.
     */

    return 0;
}
