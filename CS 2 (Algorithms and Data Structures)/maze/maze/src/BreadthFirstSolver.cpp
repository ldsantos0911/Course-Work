/**
 * @file BreadthFirstSolver.cpp
 * @author Ellen Price <<eprice@caltech.edu>>
 * @version 2.0
 * @date 2014-2015
 * @copyright see License section
 *
 * @brief Functions for maze solver that implements breadth-first search.
 *
 * @section License
 * Copyright (c) 2014-2015 California Institute of Technology.
 * All rights reserved.
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
 * The views and conclusions contained in the software and documentation are those
 * of the authors and should not be interpreted as representing official policies,
 * either expressed or implied, of the California Institute of Technology.
 *
 */

#include "BreadthFirstSolver.hpp"

/**
 * @brief Initializes the solver.
 *
 * @param[in] app Pointer to the main MazeSolverApp class.
 */
BreadthFirstSolver::BreadthFirstSolver(class MazeSolverApp *app)
{
    queue = new CoordinateQueue(app);
    init();
}

/**
 * @brief Initializes the solver (student-implemented).
 */
void BreadthFirstSolver::init()
{
    for(int i = 0; i < WIDTH; i++)
    {
        for(int j = 0; j < HEIGHT; j++)
        {
            visited[i][j].visited = false;
        }
    }
}

/**
 * @brief Deinitializes the solver.
 */
BreadthFirstSolver::~BreadthFirstSolver()
{
    delete queue;
    deinit();
}

/**
 * @brief Deinitializes the solver (student-implemented).
 */
void BreadthFirstSolver::deinit()
{
}

/**
 * @brief Solve the maze given by `maze`.
 *
 * @param[in] maze MazeGrid object that stores the maze to be
 * solved.
 */
void BreadthFirstSolver::solve(MazeGrid *maze)
{
    Coordinate c;
    int res;
    queue->enqueue(Coordinate(MAZE_START_X, MAZE_START_Y));
    while(!queue->is_empty())
    {
        c = queue->peek();
        visited[c.x][c.y].visited = true;
        if(c.x == MAZE_END_X && c.y == MAZE_END_Y)
        {
            break;
        }
        res = maze->get_possible_moves(c.x, c.y);
        if(res & E && !visited[c.x + 1][c.y].visited)
        {
            visited[c.x + 1][c.y].from = c;
            queue->enqueue(Coordinate(c.x + 1, c.y));

        }
        if(res & W && !visited[c.x - 1][c.y].visited)
        {
            visited[c.x - 1][c.y].from = c;
            queue->enqueue(Coordinate(c.x - 1, c.y));

        }
        if(res & N && !visited[c.x][c.y - 1].visited)
        {
            visited[c.x][c.y - 1].from = c;
            queue->enqueue(Coordinate(c.x, c.y - 1));

        }
        if(res & S && !visited[c.x][c.y + 1].visited)
        {
            visited[c.x][c.y + 1].from = c;
            queue->enqueue(Coordinate(c.x, c.y + 1));
        }
        queue->dequeue();
    }
}

/**
 * @brief Retrieves the current path through the maze.
 *
 * @return Vector storing the current path through the maze.
 */
vector<Coordinate> BreadthFirstSolver::get_path()
{

    vector<Coordinate> list;
    Coordinate c = queue->peek();
    int x = c.x, y = c.y, x_temp, y_temp;
    while(true)
    {
        list.push_back(Coordinate(x, y));
        if(x == MAZE_START_X && y == MAZE_START_Y)
            break;
        x_temp = x;
        y_temp = y;
        x = visited[x_temp][y_temp].from.x;
        y = visited[x_temp][y_temp].from.y;
    }
    return list;
}
