//I was just toying with this. I realize that it does not work at all.

#include <iostream>
#include <unordered_map>
#include <string.h>

using namespace std;

string find_pal(string input)
{
    char const* input_c = input.c_str();
    int size = (int) strlen(input_c), odd;
    char odd_c, output[size];
    unordered_map<char, int> chars;
    for(char c : input_c)
    {
        if(chars.count(c) == 0)
        {
            chars[c] = 1;
        }
        else
        {
            chars[c]++;
        }
    }
    for(char c : input_c)
    {
        if(chars[c] % 2 == 1)
        {
            odd_c = c;
            odd++;
        }
        if(odd > 1)
        {
            return "";
        }
    }
    int index = 0;
    for(auto i = chars.begin(); i != chars.end(); i++)
    {
        if(i != odd_c && *i > 0)
        {
            int j = *i, temp = index;
            for(index; index < temp + j / 2; index++)
            {
                output[index] = *(i + index - temp);
                *i -= 1;
            }
            i += index - temp;
        }
        if(i == chars.end() && chars[odd_c] > 0)
        {
            int temp = index;
            for(index; index < chars[odd_c] + temp; index++)
            {
                output[index] = *(i + index - temp);
            }
            i += index - temp;
        }
    }
}



}
