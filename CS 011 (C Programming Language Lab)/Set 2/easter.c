/*
 * Louis Santos
 * CS 011: C
 * The following code reads years from a given text file, then determines the
 * month and day on which Easter falls during the given year.
 * It then prints the month, day, and year to another text file, with the
 * line of the original year in the input file corresponding to the line of
 * the outputted statement in the output file.
 */


#include <stdio.h>
#include <stdlib.h>

int main(void);
int calculate_Easter_date(int year);

/*
 * @brief: Read the lines from the given file, calling calculate_Easter_date()
 * on each of them. Print the appropriate message to the output file.
 */
int main(void)
{
    int line = 0, date = 0, scan = 0;
    while(1)
    {
        scan = scanf("%d", &line);
        if(scan == EOF) /* If we have reached the end of the file, break */
        {
            break;
        }
        date = calculate_Easter_date(line);
        if(date == 0) /* If the given year was invalid */
        {
            /* Print to error file */
            fprintf(stderr, "Invalid year (%d)!\n", line);
            continue;
        }
        else if(date < 0) /* If the month is March */
        {
            printf("%d - March %d\n", line, abs(date));
        }
        else /* If the month is April */
        {
            printf("%d - April %d\n", line, abs(date));
        }
    }
    return 0;
}

/*
 * @brief: Given a year in the range 1582-39999, calculate the date of Easter in
 * that year, using Donald Knuth's algorithm.
 *
 * @param year: The year for which the Easter date will be calculated
 *
 * @return: The date of Easter, with a negative int indicating March and a
 * positive one indicating April.
 */
int calculate_Easter_date(int year)
{
    int golden, century, skip_leap, correction, sunday, epact, calendar_full;

    if(year < 1582 || year > 39999) /* If the year is invalid, return 0 */
    {
        return 0;
    }
    /* Determine what year this is in the metonic cycle */
    golden = (year % 19) + 1;
    century = (year / 100) + 1;
    skip_leap = (3 * century / 4) - 12; /* Leap years skipped */
    correction = ((8 * century + 5) / 25) - 5;
    /* ^^Correction factor to account for the moon's irregular orbit */

    sunday = (5 * year / 4) - skip_leap - 10; /* Gives a Sunday */
    epact = (11 * golden + 20 + correction - skip_leap) % 30;
    /* ^^Specifies when a full moon occurs */

    if((epact == 25 && golden > 11) || epact == 24)
    {
        epact++;
    }
    calendar_full = 44 - epact; /* Specifies full moon date on calendar */
    /* Easter should be the first Sunday after the first full moon after
     * March 21st. Therefore, if the calendar_full is less than 21 (i.e before
     * March 21st), add 30 days.
     */
    if(calendar_full < 21)
    {
        calendar_full += 30;
    }

    /* Advance to the nearest Sunday */
    calendar_full = calendar_full + 7 - ((sunday + calendar_full) % 7);

    /* If the date is > 31, Easter is in April. Subtract 31 days and return. */
    if(calendar_full > 31)
    {
        return calendar_full - 31;
    }
    /* If the date is in March, return the negative of the date, to assist
     * interpretation in receiver function.
     */
    return -calendar_full;
}
