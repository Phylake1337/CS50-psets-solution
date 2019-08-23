#include <stdio.h>
#include <cs50.h>
#include <math.h>

void CheckType (int length,long credNum);
int getLength (long credNum);
bool checkSum (int credArray[],int length);

int main(void)
{
    long credit = get_long("Credit Number: ");
    int length = getLength (credit);
    //printf("Length: %i \n",length);
    //Long to array
    int credArray[length];
    int c = 0;
    long credNum = credit;
    
    while(credNum!= 0)
    {
        credArray[c] = credNum%10;
        credNum = credNum/10;
        c++;
    }

    bool checkResult= checkSum (credArray,length);
    if (checkResult)
        CheckType (length,credit);
    else
        printf("INVALID\n");  
}


int getLength (long credNum)
{
    int length=0 ;
    while (credNum != 0)
    {
        credNum = credNum/10;
        length++;
    }
    return length;
}

void CheckType (int length,long credNum)
{
    string credType;
    switch (length)
    {
        case (15):
            if ((credNum / 10000000000000) == 34 || (credNum / 10000000000000) == 37 )
                printf("AMEX\n");
            else
                printf("INVALID\n");        
            break;
            
        case (13):
            if ((credNum / 1000000000000) == 4)
                printf("VISA\n");
            else
                printf("INVALID\n");        
            break;
         
        case (16):
            {
                bool flag=false;
                if ((credNum / 1000000000000000) == 4)
                {
                    flag =true;
                    printf("VISA\n");
                }
                int ind = 51;
                for(int i=0 ;i<5 ;i++)
                {
                    if ((credNum / 100000000000000) == ind+i)
                        {   
                            flag = true;
                            printf("MASTERCARD\n");  
                        }
                }
                if (!flag)
                    printf("INVALID\n");
                break;             
            }
        default:
            printf("INVALID\n");        
    }
}

bool checkSum (int credArray[], int length)
{
    int Sum = 0;
    int temp= 0;
    for(int l=1; l<length; l=l+2)
    {
     //printf("credArray[%i] = %i \n",l,credArray[l]);
     temp = credArray[l]*2;
     int tempL = temp%10;
     temp = temp/10;
     int tempR = temp;
     int digitSum = tempL+tempR;
     credArray[l] = digitSum;
     //printf("tempR: %i -- tempL: %i \n",tempL,tempR);
    }
    for (int i=0; i<length; i++)
    {
        //printf("array[[%i]: %i \n" ,i ,credArray[i]);  
        Sum += credArray[i];  
    }
        //printf("Sum: %i \n",Sum);
        if (Sum%10 == 0)                
            return true;
        else 
            return false;
}
