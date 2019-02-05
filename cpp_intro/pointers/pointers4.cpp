/**
 * @file pointers4.cpp
 * @author The CS2 TA Team <cs2tas@caltech.edu>
 * @date 2015
 * @copyright This code is in the public domain.
 *
 * @brief Pointer-fu Exercise 4: Typecasting vs. address-of
 */

#include <cstdlib>
#include <iostream>

using namespace std;

/**
 * @brief performs type castings
 */
int main(int argc, char *argv[])
{
    int a = 5, *b;
    void *c;

    // Now make `b` point to `a`.
    b = &a;
    /* Casting a to a pointer does not create a pointer to a. I fixed 
     * this by instead setting b to a's memory address.
     */
    

    /***** CHANGE NOTHING BELOW THIS LINE *****/
    cout << "The value pointed by `b` is " << *b;
    /***** CHANGE NOTHING ABOVE THIS LINE *****/

    // Allocate an array of 10 ints.
    c = malloc(10 * sizeof(int));

    // Get the address of the array.
    b = (int *) c;
    /* c is already a pointer, but it was a pointer of the wrong type.
     * Casting the address of c sets b to c's memory address. Casting c
     * yields the memory address of the array. All I did was removed &.
     */

    /***** CHANGE NOTHING BELOW THIS LINE *****/
    b[2] = 5;
    /***** CHANGE NOTHING ABOVE THIS LINE *****/

    return 0;
}
