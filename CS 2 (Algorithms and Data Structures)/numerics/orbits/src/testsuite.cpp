/**
 * @file test_solver.cpp
 * @author Ellen Price <<eprice@caltech.edu>>
 * @version 1.0
 * @date 2013-2014
 * @copyright see License section
 *
 * @brief Simple test suite for Solver.
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
#include <cstdio>

using namespace Solver;

double f1(double x)
{
    return x;
}

double f1p(double x)
{
    return 1;
}

double f2(double x)
{
    return x*x + 4*x + 4;
}

double f2p(double x)
{
    return 2*x + 4;
}

double f3(double x)
{
    return x + cos(x);
}

double f3p(double x)
{
    return 1 - sin(x);
}

double f4(double x)
{
    return x + sin(x);
}

double f4p(double x)
{
    return 1 + cos(x);
}

int main()
{
    printf("Correct Answer: %f\n", 0.0);
    printf("Bisection: %f\n", bisection(f1, -1, 1));
    printf("Newton-Raphson: %f\n", newton_raphson(f1, f1p, -1));
    printf("\n");

    printf("Correct Answer: %f\n", -2.0);
    printf("Bisection: %f\n", bisection(f2, -4, 0));
    printf("Newton-Raphson: %f\n", newton_raphson(f2, f2p, -1));
    printf("\n");

    printf("Correct Answer: %f\n", -0.739085);
    printf("Bisection: %f\n", bisection(f3, -2, 0));
    printf("Newton-Raphson: %f\n", newton_raphson(f3, f3p, -2));
    printf("\n");

    printf("Correct Answer: %f\n", 0.0);
    printf("Bisection: %f\n", bisection(f4, -1, 1));
    printf("Newton-Raphson: %f\n", newton_raphson(f4, f4p, -1));
    printf("\n");

    return 0;
}
