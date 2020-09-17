#include <stdio.h>
#include <cs50.h>

int main(void)
{
    //get user input 'n' between 1 and 8
    int height;
    do
    {
        height = get_int("Height 1-8: ");
    }
    while (height < 1 || height > 8);

    //running through the loop "height" times
    for (int i = 0; i < height; i += 1)
    {
        //print (height - hashes) spaces
        int spaces = (height - 1) - i;
        int hashes = i + 1;
        for (int j = 0; j < spaces; j += 1)
        {
            printf(" ");
        }
        //print hashes equal to loop number
        for (int k = 0 ; k < hashes; k += 1)
        {
            printf("#");
        }
        //print middle space between hashes
        printf("  ");
        //print hashes again
        for (int k = 0 ; k < hashes; k += 1)
        {
            printf("#");
        }
        //move to new line, then start loop again
        printf("\n");
    }

}
