#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])
{
    //check there's only one command line argument
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    //check the command line argument is all integers
    for (int i = 0; i < strlen(argv[1]); i += 1)
    {
        if (isdigit(argv[1][i]) == false)
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }
    int key;
    key = atoi(argv[1]);

    //get plaintext from user
    string plaintext = get_string("plaintext: ");

    //return ciphertext, rotate the characters by the command line input
    printf("ciphertext: ");
    for (int i = 0; i < strlen(plaintext); i += 1)
    {
        //if uppercase, rotate
        if (isupper(plaintext[i]))
        {
            printf("%c", ((plaintext[i] - 65 + key) % 26 + 65));
        }
        //if lowercase, rotate
        else if (islower(plaintext[i]))
        {
            printf("%c", ((plaintext[i] - 97 + key) % 26 + 97));
        }
        //if other, leave as is
        else
        {
            printf("%c", plaintext[i]);
        }
    }
    //new line and return 0
    printf("\n");
    return 0;
}
