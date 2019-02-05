#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(void);

int main(void)
{
    char name[100];
    int n, i = 0;
    srand(time(0));


    printf("Enter your name: ");
    scanf("%99s", name);
    n = (int)(rand() / (RAND_MAX / 10)) + 1;

    while(i < n)
    {
        if(n % 2 == 0)
        {
            printf("%d: hello, %s!\n", n, name);
        }
        else
        {
            printf("%d: hi there, %s!\n", n, name);
        }
	i++;
    }
    return 0;
}
