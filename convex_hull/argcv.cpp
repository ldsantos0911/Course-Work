/**
 * @file
 * @author The CS2 TA Team
 * @version 1.0
 * @date 2013-2014
 * @copyright This code is in the public domain.
 *
 * @brief A command-line argument example.
 *
 */

#include <iostream>

using namespace std;


int main(int argc, char const *argv[])
{
    cout << "argc: " << argc << endl;
    cout << "argv: ";
    for (int i = 0; i < argc; ++i)
    {
        cout << argv[i] << " ";
    }
    cout << endl;
    return 0;
}
