#include <cmath>
#include <iostream>
using namespace std;

double qfsolve(double a, double b, double c)
{
	/**
	 * @brief Solves the given quadratic equation.
	 *
	 * This function, given real coefficients A, B, C to the equation
	 * A*x*x + B*x + C = 0, returns the real part of a solution to the
	 * equation thus defined. Where two real solutions exist, the one
	 * closer to positive infinity is chosen.
	 *
	 * @param a the quadratic coefficient.
	 * @param b the linear coefficient.
	 * @param c the constant coefficient.
	 *
	 * @return the real part of a solution to the defined quadratic equation,
	 *         as described.
	 */
	
	if(4 * a * c > b * b)
	{
		return (-1.0 * b) / (2 * a);
	}
	else
	{
		double value = ((-1.0 * b) + sqrt(b * b - 4 * a * c)) / (2 * a);
		if(((-1.0 * b) + sqrt(b * b - 4 * a * c)) / (2 * a) < \
		((-1.0 * b) - sqrt(b * b - 4 * a * c)) / (2 * a))
		{
			value = ((-1.0 * b) - sqrt(b * b - 4 * a * c)) / (2 * a);
		}
		return value;
	}
}

int main(int argc, char ** argv)
{
	//Print qfsolve test-cases.
	cout << "a: -5, b: 7, c: 9 x: " << qfsolve(-5, 7, 9) << endl;
	cout << "a: -10, b: -7, c: 1, x: " << qfsolve(-10, -7, 1) << endl;
	cout << "a: -3, b: 4, c: 10, x: " << qfsolve(-3, 4, 10) << endl;
	cout << "a: -6, b: -3, c: 6, x: " << qfsolve(-6, -3, 6) << endl;
	cout << "a: -9, b: 3, c: 10, x: " << qfsolve(-9, 3, 10) << endl;
	cout << "a: 2, b: 3, c: 4, x: " << qfsolve(2, 3, 4) << endl;
	return 0;
}
		
