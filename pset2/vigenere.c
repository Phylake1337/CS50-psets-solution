#include <cs50.h>
#include <stdio.h>
#include <string.h>

int shift(int key);
int main(int argc, string argv[])
{
    if (argc == 2)
    {
        string key = argv[1];
        //printf("Strlen for key: %lu", strlen(key));
        int Shift[strlen(key)];
        //check terminal-command argument
        for (int i = 0; i < strlen(key); i++)
        {
            if (key[i] < 65)
            {
                printf("Usage: ./caesar key\n");  
                return 1; 
            }
            
            else 
            {
                Shift[i] = shift(key[i]);                
            }
        }
        //Ciphering
        string plaintxt = get_string("Write plaintxt: ");
        int c = 0;
        for (int i = 0; i < strlen(plaintxt); i++)
        {
            if (('A' <= plaintxt[i] && plaintxt[i] <= 'Z'))
            {
                plaintxt[i] -= 65;
                plaintxt[i] = (plaintxt[i] + Shift[(i - c) % strlen(key)]) % 26 + 65;
            }

            else if (('a' <= plaintxt[i] && plaintxt[i] <= 'z'))
            {       
                plaintxt[i] -= 97;
                plaintxt[i] = (plaintxt[i] + Shift[(i - c) % strlen(key)]) % 26 + 97;
            }  
            
            else
            {
                c++;                
            }
            
        }
        printf("ciphertext: %s\n", plaintxt);
    }
    
    else
    {
        printf("Usage: ./caesar key\n");  
        return 1;
    }  
}

int shift(int key)
{
    if (key >= 'A' && key <= 'Z')
    {
        return key - 65;
    }
    else if (key >= 'a' && key <= 'z')
    {
        return key - 97;
    }
    else
    {
        printf("Can't calculate the shift for %c \n", key);
        return 1;
    }
}
