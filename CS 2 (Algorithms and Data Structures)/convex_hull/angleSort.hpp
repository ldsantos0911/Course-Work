#ifndef __ANGLESORT_H__
#define __ANGLESORT_H__

#include "structs.hpp"
#include <vector>

inline int inplace_partition(std::vector<Tuple*> &points, std::vector<double> &angles, \
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

// TODO Modify one of your sorting functions (bubble sort not permitted) and
// implement it here. Add extra arguments as needed.
inline void angle_sort(vector<Tuple*> &points, vector<double> &angles, int left, int right)
{
  if(right - left > 0)
  {
    int pivot = inplace_partition(points, angles, left, right);
    angle_sort(points, angles, left, pivot - 1);
    angle_sort(points, angles, pivot + 1, right);
  }
}

#endif
