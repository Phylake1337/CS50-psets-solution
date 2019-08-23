#include <cs50.h>
#include <stdio.h>

void print_dashs (int length);
int take_input(void);
    
int main(void)
{
        int height = take_input();
        for(int i=1; i<=height ;i++)
        {
            //printf("Spaces: %i -- Dashs: %i",height-i,i);
            if (i < height)
            {
              printf("%*c", height-i,' ');  
            }
            print_dashs(i);
            printf("%*c", 2,' ');
            print_dashs(i);
            printf("\n");
        }
}
void print_dashs (int length)
{
   for(int j=0 ; j < length ; j++)
   {
        printf("%c",'#');
   }
}

int take_input(void)
{
    int n;
    do
    {
     n = get_int("Height: "); 
    }
    while(n<1 || n>8);
    return n;
}
