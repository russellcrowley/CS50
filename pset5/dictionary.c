// Speller
// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 10000;

// Hash table
node *table[N];
//word count for size function
int wordcount = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    int h = hash(word);
    //point cursor at word to be checked's value:
    node *cursor = table[h];
    //check through list in node
    while (cursor != NULL)
    {
        //check if word matches
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }
        //move to next node
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *hash_word)
{
    //http://www.cse.yorku.ca/~oz/hash.html
    unsigned long hash = 5381;
    int c;
    while ((c = toupper(*hash_word++)))
    {
        hash = ((hash << 5) + hash) + c; /* hash * 33 + c */
    }
    //Fit hash number into number of blocks set aside for hashtable
    return hash % N;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    //Open dictionary file
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }
    char word[LENGTH + 1];
    //Read strings from file one at a time
    while (fscanf(file, "%s", word) != EOF)
    {
        //fscanf(file, %s, word), fscanf will return EOF at end of file
        //Create a new node for each word
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            printf("Nothing in node");
            return false;
        }
        //pointer to next node and word
        strcpy(n->word, word);
        //Hash word to obtain a hash value
        int h = hash(word);
        //new pointer to hash value
        n->next = table[h];
        //head set to new pointer
        table[h] = n;
        wordcount += 1;
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    //Return number of words in dictionary. Count nodes, or keep track when loading hash table
    return wordcount;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    //Go through buckets
    for (int i = 0; i < N; i += 1)
    {
        //set cursor to bucket
        node *cursor = table[i];
        while (cursor)
        {
            //create temp cursor
            node *temp = cursor;
            //move cursor to next node
            cursor = cursor->next;
            //free temp
            free(temp);
        }
    }
    return true;
}
