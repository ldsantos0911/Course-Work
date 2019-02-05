/**
 * @file testsuite.cpp
 * @author Ellen Price <<eprice@caltech.edu>>
 * @version 1.0
 * @date 2014-2015
 * @copyright see License section
 *
 * @brief Performs tests of the CoordinateQueue and CoordinateStack classes.
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

#include <cstdio>
#include <iostream>
#include "CoordinateStack.hpp"
#include "CoordinateQueue.hpp"

using namespace std;

int main()
{
    Coordinate c;
    CoordinateQueue *queue = new CoordinateQueue();
    CoordinateStack *stack = new CoordinateStack();

    //Test the CoordinateStack


    cout << "Testing CoordinateStack..." << endl;
    cout << "Expected emptiness: 1" << endl;
    cout << "Actual emptiness: " << stack->is_empty() << endl;
    cout << "Expected top value: (-1, -1)" << endl;
    c = stack->pop();
    cout << "Actual top value: " << c.x << " " << c.y << endl;
    cout << "Expected peek: (-1, -1)" << endl;
    c = stack->peek();
    cout << "Actual peek: " << c.x << " " << c.y << endl;

    c = Coordinate(5, 10);
    stack->push(c);

    cout << "Expected emptiness: 0" << endl;
    cout << "Actual emptiness: " << stack->is_empty() << endl;
    cout << "Expected peek: (5, 10)" << endl;
    c = stack->peek();
    cout << "Actual peek: " << c.x << " " << c.y << endl;
    cout << "Expected pop: (5, 10)" << endl;
    c = stack->pop();
    cout << "Actual pop: " << c.x << " " << c.y << endl;
    cout << "Expected emptiness: 1" << endl;
    cout << "Actual emptiness: " << stack->is_empty() << endl;


    //Test the CoordinateQueue
    cout << endl << endl << "Testing CoordinateQueue..." << endl;
    cout << "Expected emptiness: 1" << endl;
    cout << "Actual emptiness: " << queue->is_empty() << endl;
    cout << "Expected top value: (-1, -1)" << endl;
    c = queue->dequeue();
    cout << "Actual top value: " << c.x << " " << c.y << endl;
    cout << "Expected peek: (-1, -1)" << endl;
    c = queue->peek();
    cout << "Actual peek: " << c.x << " " << c.y << endl;

    c = Coordinate(5, 10);
    Coordinate d = Coordinate(15, 20);
    queue->enqueue(c);
    queue->enqueue(d);


    cout << "Expected emptiness: 0" << endl;
    cout << "Actual emptiness: " << queue->is_empty() << endl;
    cout << "Expected peek: (5, 10)" << endl;
    c = queue->peek();
    cout << "Actual peek: " << c.x << " " << c.y << endl;
    cout << "Expected dequeue: (5, 10)" << endl;
    c = queue->dequeue();
    cout << "Actual dequeue: " << c.x << " " << c.y << endl;
    cout << "Expected emptiness: 0" << endl;
    cout << "Actual emptiness: " << queue->is_empty() << endl;

    cout << "Expected peek: (15, 20)" << endl;
    d = queue->peek();
    cout << "Actual peek: " << d.x << " " << d.y << endl;
    cout << "Expected dequeue: (15, 20)" << endl;
    d = queue->dequeue();
    cout << "Actual dequeue: " << d.x << " " << d.y << endl;
    cout << "Expected emptiness: 1" << endl;
    cout << "Actual emptiness: " << queue->is_empty() << endl;


    delete queue;
    delete stack;

    return 0;
}
