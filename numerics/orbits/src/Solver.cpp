/**
 * @file Solver.cpp
 * @author Ellen Price <<eprice@caltech.edu>>
 * @version 1.0
 * @date 2013-2014
 * @copyright see License section
 *
 * @brief Functions that carry out numerical root-finding.
 *
 * @section License
 * Copyright (c) 2013-2014 California Institute of Technology.
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

#include "Solver.hpp"

#define PRECISION       (1.e-10)
#define TOLERANCE       (1.e-10)

using namespace std;

int sign(double num)
{
    if(num == 0)
    {
        return 0;
    }
    if(num > 0)
    {
        return 1;
    }
    return -1;
}

/**
 * @brief Solves f(x) = 0 in the interval [x1, x2] with the bisection
 * method
 *
 * @param[in] f The function to solve
 *
 * @param[in] x1 One side of the interval to search
 *
 * @param[in] x2 The other side of the interval to search
 *
 * @return The x-coordinate of the root
 */
double Solver::bisection(double (*f)(double), double x1, double x2)
{
    double m = (x1 + x2) / 2;
    while(abs(x2 - x1) > PRECISION && f(x1) != 0.0)
    {
        m = (x1 + x2) / 2;
        if(sign(f(x1)) == sign(f(m)))
        {
            x1 = m;
        }
        else
        {
            x2 = m;
        }
    }
    return x1;
}


/**
 * @brief Solves f(x) = 0 near x1 with the Newton-Raphson method
 *
 * @param[in] f The function to solve
 *
 * @param[in] fp The first derivative of f
 *
 * @param[in] x1 A starting point for the solver
 *
 * @return The x-coordinate of the root
 */
double Solver::newton_raphson(double (*f)(double), double (*fp)(double),
    double x1)
{
    double x0 = x1;
    while(abs(f(x1) / fp(x1)) > TOLERANCE && f(x1) != 0.0)
    {
        x1 = x0 - f(x0) / fp(x0);
        x0 = x1;
    }
    return x1;
}
