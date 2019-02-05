/**
 * @file
 * @author The CS2 TA Team
 * @version 1.0
 * @date 2013-2014
 * @copyright This code is in the public domain.
 *
 * @brief The gift wrapping and Graham scan convex hull algorithms
 * (implementation).
 *
 */
#include "HullAlgorithms.hpp"


using namespace std;

/**
 * TO STUDENTS: In all of the following functions, feel free to change the
 * function arguments and/or write helper functions as you see fit. Remember to
 * add the function header to HullAlgorithms.hpp if you write a helper function!
 *
 * Our reference implementation has four helper functions and the function(s)
 * copied over from angleSort.cpp.
 */

/**
 * @brief Determines the sign of a given int.
 *
 * @param num: the number to determine sign of.
 *
 * @return: -1 for negative, 0 for 0, 1 for positive.
 */
int sign(int num)
{
  if(num == 0)
    return 0;
  if(num < 0)
    return -1;
  return 1;
}

/**
 * @brief Finds the leftmost point of a given vector of points
 *
 * @param points: a vector of Tuples representing points.
 *
 * @return The leftmost point in points.
 */

Tuple* leftMost(vector<Tuple*> points)
{
  Tuple* point = points[0];
  for(unsigned int i = 0; i < points.size(); i++)
  {
    if(points[i]->x < point->x)
    {
      point = points[i];
      points[i] = nullptr;
    }
  }
  return point;
}

/**
 * @brief Calculates a quantity used to detemine on which side of a line between
 * two points a third point is.
 *
 * @param a: the first point of the line
 * @param b: the second point of the line
 * @param c: the other point
 *
 * @return A quantity whose sign determines the side of line ab, point c falls on.
 */

int find_d(Tuple * a, Tuple * b, Tuple * c)
{

  return (c->x - a->x)*(b->y - a->y) - (c->y - a->y)*(b->x - a->x);
}

/**
 * @brief Returns whether or not three points form a right turn.
 *
 * @param a: a pointer to a Tuple representing a point on a line.
 * @param b: a pointer to a Tuple representing a second point on a line.
 * @param c: a pointer to a Tuple representing the third point to compare.
 *
 * @return Whether or not point c is to the left of line ab.
 */
bool rightTurn(Tuple* a, Tuple* b, Tuple* c)
{
  int d = find_d(a, b, c);
  Tuple* test;
  if(a->y > b->y)
    test = new Tuple(a->x + 1, a->y);
  else
    test = new Tuple(a->x - 1, a->y);
  int sgn = sign(find_d(a, b, test));
  delete test;
  if(sign(d) == sgn)
    return true;
  else
    return false;
}
/**
 * This forms a convex hull by starting from the leftmost point and adding points
 * for which there are no points to the left of the line formed between the point
 * being checked and the previous point added. Concludes when the next point is
 * the original starting point.
 *
 * Tuple *point_o = LEFTMOST points, *point
 * ADD point_o TO HULL
 * point = point_o
 * vector<Tuple*>::iterator point_i = points.begin()
 * add = true
 * WHILE true
 *    add = true
 *    IF point == *point_i
 *        ++point_i
 *    IF point_i == points.end()
 *        point_i = points.begin()
 *    FOR EVERY POINT IN points
 *        IF point, *point_i, and points[i] MAKE A RIGHT TURN
 *            add = false
 *            break
 *    IF add
 *        PUT *point_i ON HULL
 *        IF point EQUALS ORIGINAL POINT
 *            break;
 *    point_i++;
 */
void DoGiftWrap(vector<Tuple*> points, ConvexHullApp *app)
{
    Tuple* point_o = leftMost(points), *point;
    app->add_to_hull(point_o);
    point = point_o;
    vector<Tuple*>::iterator point_i = points.begin();
    bool add = true;
    while(true)
    {
      add = true;
      if(point == *point_i)
        ++point_i;
      if(point_i == points.end())
        point_i = points.begin();
      for(unsigned int i = 0; i < points.size(); ++i)
      {
        if(rightTurn(point, *point_i, points[i]))
        {
          add = false;
          break;
        }
      }
      if(add)
      {
        point = *point_i;
        app->add_to_hull(point);
        if(point == point_o)
        {
          break;
        }
      }
      point_i++;
    }
}

/**
 * @brief Finds the lowest of a list of points
 *
 * @param points: A list of points.
 *
 * @return A pointer to a Tuple representing the geometrically lowest point of
 * a list of points.
 */
Tuple* findLowest(vector<Tuple*> points)
{
  Tuple * lowest = points[0];
  for(Tuple* point:points)
  {
    if(point->y > lowest->y)
    {
      lowest = point;
    }
  }
  return lowest;
}

 /**
 * Constructs a convex hull by considering three consecutive points in a list of
 * points sorted by the angle they form with the x-axis as defined by the lowest
 * point on the graph. Removes the second point being considered as long as a
 * right turn is being formed. Moves the first point to the previous middle point
 * when it is confirmed to be on the hull.
 *
 * CONSTRUCT ANGLES LIST AND SORT ANGLES AND POINTS
 * WHILE point_2 < points.size()
 *    WHILE POINTS BEING CONSIDERED FORM RIGHT turn
 *        ERASE MIDDLE
 *        MOVE THREE POINTS BACK BY ONE
 *    MOVE POINTS FORWARD BY ONE
 * ADD POINTS TO HULL
 */
void DoGrahamScan(vector<Tuple*> points, ConvexHullApp *app)
{
    vector<double> angles;
    Tuple* lowest = findLowest(points);

    for(unsigned int i = 0; i < points.size(); i++)
    {
      angles.push_back(-1 * points[i]->angle_wrt_pt(lowest));
    }
    angle_sort(points, angles, 0, angles.size() - 1);
    unsigned int point_0 = 0, point_1 = 1, point_2 = 2;

    while(point_2 < points.size())
    {
      while(rightTurn(points[point_0], points[point_1], points[point_2]))
      {
        points.erase(points.begin() + point_1);
        point_2--;
        point_1--;
        point_0--;
      }
      point_0 = point_1;
      point_1 = point_2;
      point_2++;
    }
    for(unsigned int i = 0; i < points.size(); i++)
    {
        app->add_to_hull(points[i]);
    }
    app->add_to_hull(points[0]);
}
