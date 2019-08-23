#include <cs50.h>
#include <stdio.h>
#include <string.h>

int main(int argc, string argv[])
{
    if (argc == 2)
    {
        string key = argv[1];
        for (int i = 0; i < strlen(key); i++)
        {
            int k=key[i]-48;
            if (k > 9)
            {
                printf("Usage: ./caesar key\n");  
                return 1; 
            }

        }
        printf("Key int: %i \n", atoi(key));
        string plaintxt = get_string("Write plaintxt: ");
        for (int i = 0; i < strlen(plaintxt); i++)
        {
            if (('A' <= plaintxt[i] && plaintxt[i] <= 'Z'))
            {
                plaintxt[i] -= 65;
                plaintxt[i] = (plaintxt[i] + atoi(key)) % 26 + 65;
            }

            if (('a' <= plaintxt[i] && plaintxt[i] <= 'z'))
            {
                plaintxt[i] -= 97;
                plaintxt[i] = (plaintxt[i] + atoi(key)) % 26 + 97;
            }     
        }
        printf("ciphertext: %s\n", plaintxt);
    }
    
    else
    {
        printf("Usage: ./caesar key\n");  
    }
         
}
