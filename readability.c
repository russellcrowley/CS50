#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

int main(void)
{
    //get a string of text from the user
    string text = get_string("Text: ");
    //declare variables
    int letters = 0;
    int words = 1;
    int sentences = 0;
    //the counting bit
    for (int i = 0; i < strlen(text); i += 1)
    {
        //counting letters
        if (isalpha(text[i]))
        {
            letters += 1;
        }
        //counting words
        else if (text[i] == ' ')
        {
            words += 1;
        }
        //counting sentences
        else if ((text[i] == '.') || (text[i] == '?') || (text[i] == '!'))
        {
            sentences += 1;
        }
    }
    //implementing COleman - Lau index to get grase
    float L = ((float) letters / (float) words) * 100;
    float S = ((float) sentences / (float) words) * 100;
    float index = 0.0588 * L - 0.296 * S - 15.8;
    //final statement
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", (int) round(index));
    }
}

