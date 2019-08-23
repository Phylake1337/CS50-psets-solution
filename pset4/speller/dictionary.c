// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <strings.h>
#include <stdlib.h>

#include "dictionary.h"

// Represents number of buckets in a hash table
#define N 26
//int wordCount = 0;

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Represents a hash table
node *hashtable[N];

// Hashes word to a number between 0 and 25, inclusive, based on its first letter
unsigned int hash(const char *word)
{
    return tolower(word[0]) - 'a';
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize hash table
    for (int i = 0; i < N; i++)
    {
        hashtable[i] = NULL;
    }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into hash table

    while (fscanf(file, "%s", word) != EOF)
    {
        node *newNode = malloc(sizeof(node));
        unsigned int bucket = hash(word);
        strcpy((newNode -> word) , word);
        (newNode -> next) = hashtable[bucket];
        hashtable[bucket] = newNode;
    }

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    int wordCount = 0;
    for (int i = 0; i < N; i++)
    {
    node *nodePointer =  hashtable[i];
    while (nodePointer != NULL)
        {
            char *Word = (nodePointer -> word);
            nodePointer = (nodePointer -> next);
            wordCount++;
        }
    }
    return wordCount;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    unsigned int bucket = hash(word);
    node *curser =  hashtable[bucket];
    while (curser != NULL)
        {
            char *Word = (curser -> word);
            curser = (curser -> next);
            int flag = strcasecmp(Word , word);
            if (flag == 0)
            {
                return true;
            }
        }
    return false;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    node *temp ;
    for (int i = 0; i < N; i++)
    {
    node *curser =  hashtable[i];
    while (curser != NULL)
        {
            temp = curser;
            curser = (curser -> next);
            free(temp);
        }
    }
    return true;
}