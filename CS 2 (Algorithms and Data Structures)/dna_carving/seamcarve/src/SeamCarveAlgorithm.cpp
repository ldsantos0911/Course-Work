/*
 * SeamCarveAlgorithm.cpp
 * Defines the seam carving algorithm.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are
 * met:
 *
 * * Redistributions of source code must retain the above copyright
 *   notice, this list of conditions and the following disclaimer.
 * * Redistributions in binary form must reproduce the above
 *   copyright notice, this list of conditions and the following disclaimer
 *   in the documentation and/or other materials provided with the
 *   distribution.
 * * Neither the name of the  nor the names of its
 *   contributors may be used to endorse or promote products derived from
 *   this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 *
 */

#include "SeamCarveApp.hpp"
#include <iostream>
using namespace std;

#define min(x, y)           ((x) < (y) ? (x) : (y))

/*
 * @brief Locates the minimum adjacent value above a given position in a 2-d
 * matrix.
 *
 * @param grid: The matrix to be analyzed.
 * @param x: The horizontal position of the point being considered.
 * @param y: The vertical position of the point being considered.
 *
 * @return An array of length two, specifying the x value of the minimum value
 *         above and adjacent to the point being considered, and the minimum
 *         value, itself.
 */
unsigned int * min_above(unsigned int **grid, int x, int y, int w)
{
    unsigned int * min_ab = new unsigned int[2];
    if(x > 0 && x < w - 1)
    {

        min_ab[1] = min(min(grid[x - 1][y - 1], grid[x][y - 1]), grid[x + 1][y -1]);
        if(min_ab[1] == grid[x - 1][y - 1])
            min_ab[0] = x - 1;
        else if(min_ab[1] == grid[x][y - 1])
            min_ab[0] = x;
        else
            min_ab[0] = x + 1;
    }
    else if(x == w - 1)
    {
        min_ab[1] = min(grid[x - 1][y - 1], grid[x][y - 1]);
        if(min_ab[1] == grid[x - 1][y - 1])
            min_ab[0] = x - 1;
        else
            min_ab[0] = x;
    }
    else if(x == 0)
    {
        min_ab[1] = min(grid[x][y - 1], grid[x + 1][y - 1]);
        if(min_ab[1] == grid[x][y - 1])
            min_ab[0] = x;
        else
            min_ab[0] = x + 1;
    }
    else
    {
        cout << "Incorrect x in min_above!" << endl;
    }
    return min_ab;
}

/**
 * @brief Peforms the seam carving algorithm.
 *
 * @param smap 2-d saliency map with width `w` and height `h`; can be
 * indexed by `smap[i][j]`
 *
 * @param w Width of the saliency map
 *
 * @param h Height of the saliency map
 *
 * @return An array of the x-coordinates of the seam, starting from the top of
 * the image.
 */
unsigned int *DoSeamCarve(unsigned int **smap, int w, int h)
{

    unsigned int *seam = new unsigned int[h];
    unsigned int **cost = new unsigned int*[w];
    unsigned int min_x = 0, min_val;

    for(int i = 0; i < w; i++)
    {
        cost[i] = new unsigned int[h];
    }
    for(int i = 0; i < w; i++)
    {
        cost[i][0] = smap[i][0];
    }

    for(int row = 1; row < h; row++)
    {
        for(int col = 0; col < w; col++)
        {
            unsigned int * min_ab = min_above(cost, col, row, w);
            cost[col][row] = smap[col][row] + min_ab[1];
            delete[] min_ab;
        }
    }
    min_val = cost[0][h - 1];
    for(int j = 1; j < w; j++)
    {
        if(cost[j][h - 1] < min_val)
            min_x = j;
    }
    seam[h - 1] = min_x;
    for(int y_coord = h - 1; y_coord > 0; y_coord--)
    {
        unsigned int * min_ab = min_above(cost, min_x, y_coord, w);
        seam[y_coord - 1] = min_ab[0];
        min_x =  seam[y_coord - 1];
        delete[] min_ab;
    }
    for(int i = 0; i < w; i++)
        delete[] cost[i];
    delete[] cost;
    return seam;
}
