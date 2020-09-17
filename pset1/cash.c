#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    //get user input for positive value for dollars
    float dollars;
    do
    {
        dollars = get_float("Change owed: ");
    }
    while (dollars < 0);
    //convert dollars to cents and round
    int cents = round(dollars * 100);
    //declare values for coins and coin counter
    int quarter = 25;
    int dime = 10;
    int nickel = 5;
    int penny = 1;
    int counter = 0;
    //continue whilst there is still cash left
    while (cents > 0)
    {
        //subtract quarter if possible
        if ((cents - quarter) >= 0)
        {
            cents -= quarter;
            counter += 1;
        }
        //otherwise subtract dime if possible
        else if ((cents - dime) >= 0)
        {
            cents -= dime;
            counter += 1;
        }
        //otherwise subtract nickel if possible
        else if ((cents - nickel) >= 0)
        {
            cents -= nickel;
            counter += 1;
        }
        //otherwise subtract a penny
        else
        {
            cents -= penny;
            counter += 1;
        }
    }
    printf("%i\n", counter);

}
