/**
 * @file
 * @author The CS2 TA Team
 * @version 1.0
 * @date 2013-2014
 * @copyright This code is in the public domain.
 *
 * @brief An example of sorting (x, y) pairs by angle.
 *
 */
#include "structs.hpp"
#include <vector>

/*
 * @brief Places all elements of a sublist of a vector which are less than the
 * center element of the sublist to the left of the center and all which are
 * greater to the right.
 *
 * @param points: the points to be rearranged.
 * @param angles: the angles to be arranged
 * @param left: the left most index of the sublist to consider
 * @param right: the right most index of the sublist to considered
 *
 * @return The new location of the pivot point.
 */
int inplace_partition(std::vector<Tuple*> &points, std::vector<double> &angles, \
  int left, int right)
{
  int pivot = (int)(right + left) / 2;
  int low_index = left, high_index = pivot + 1;
  double temp_a;
  Tuple * temp_p;

  while(low_index < pivot || high_index <= right)
  {

    if(angles[low_index] > angles[pivot] && angles[high_index] < angles[pivot])
    {
      temp_a = angles[low_index];
      temp_p = points[low_index];
      angles[low_index] = angles[high_index];
      points[low_index] = points[high_index];
      angles[high_index] = temp_a;
      points[high_index] = temp_p;
    }
    else if(angles[low_index] > angles[pivot])
    {
      temp_a = angles[low_index];
      temp_p = points[low_index];
      for(int i = low_index; i < pivot; i++)
      {
        angles[i] = angles[i + 1];
        points[i] = points[i + 1];
      }
      angles[pivot] = temp_a;
      points[pivot] = temp_p;
      pivot--;
      low_index--;
    }
    else if(angles[high_index] < angles[pivot])
    {
      temp_a = angles[high_index];
      temp_p = points[high_index];
      for(int i = high_index; i > pivot; i--)
      {
        angles[i] = angles[i - 1];
        points[i] = points[i - 1];
      }
      angles[pivot] = temp_a;
      points[pivot] = temp_p;
      pivot++;
      high_index--;
    }
    if(low_index < pivot)
      low_index++;
    if(high_index <= right)
      high_index++;
  }
  return pivot;
}

/*
 * quicksort_inplace:  In-place version of the quicksort algorithm. Requires
 *              O(1) instead of O(N) space, same time complexity. Each call of
 *              the method partitions the list around the pivot (an item taken
 *              from the middle of the array) with items left of the pivot
 *              smaller than it and items to its right larger than it. Then the
 *              method recursively sorts the left and right portions of the list
 *              until it reaches its base case: a list of length 1 is already
 *              sorted. Sorts the list of angles, simultaneously sorting the
 *              corresponding points.
 *
 * IF right - left > 0
 *    pivot = inplace_partition(list, angles, left, right)
 *    sort(list, angles, left, pivot - 1)
 *    sort(list, angles, pivot + 1, right)
 *
 * @param points: pointer to the points array to be sorted
 * @param angles: pointer to angles array to be sorted
 * @param left: the lower index of the sublist being considered
 * @param right: the higher index of the sublist being considered
 *
 * @returns:    Nothing, the array is sorted IN-PLACE.
 *
 */
void sort(vector<Tuple*> &points, vector<double> &angles, int left, int right)
{
  if(right - left > 0)
  {
    int pivot = inplace_partition(points, angles, left, right);
    sort(points, angles, left, pivot - 1);
    sort(points, angles, pivot + 1, right);
  }
}

int main(int argc, char const *argv[])
{
    vector<double> angles {4.2, 2.8, 1.4, 5.0, 3.3};
    vector<Tuple*> points;
    // Print the initial points and angles
    for (unsigned int i = 0; i < angles.size(); ++i)
    {
        points.push_back(new Tuple(i, i));
    }
    for (vector<Tuple*>::iterator i = points.begin(); i != points.end(); ++i)
    {
        (*i)->printTuple();
    }
    for (vector<double>::iterator i = angles.begin(); i != angles.end(); ++i)
    {
        cout << *i << endl;
    }

    // Now sort them with respect to angle (points[i] corresponds to angle[i])

    /** THIS IS THE ONLY LINE OF THE MAIN LOOP YOU NEED TO MODIFY. */
    sort(points, angles, 0, angles.size() - 1);
    /** REPLACE THE LINE ABOVE WITH A CALL TO YOUR SORTING FUNCTION. */

    // and print out the new points and angles
    for (vector<Tuple*>::iterator i = points.begin(); i != points.end(); ++i)
    {
        (*i)->printTuple();
    }
    for (vector<double>::iterator i = angles.begin(); i != angles.end(); ++i)
    {
        cout << *i << endl;
    }

    // Don't want to leak memory...
    // Either of the below implementations works
    // for (std::vector<Tuple*>::iterator i = points.begin(); i != points.end(); ++i)
    // {
    //     delete (*i);
    // }
    for (unsigned int i = 0; i < points.size(); ++i)
    {
        delete points[i];
    }
    return 0;
}
