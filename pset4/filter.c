// Just the helpers file, not the accompanying ones
#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    //Iterate through columns and rows
    for (int i = 0 ; i < height; i += 1)
    {
        for (int j = 0; j < width; j += 1)
        {
            //Read values of pixels for each colour
            int blue = image [i][j].rgbtBlue;
            int green = image [i][j].rgbtGreen;
            int red = image [i][j].rgbtRed;
            //Take average of three pixels
            float greyvalue;
            greyvalue = round(((float)red + (float)blue + (float)green) / 3);

            //Apply this value to all 3 fields of pixel
            image [i][j].rgbtBlue = greyvalue;
            image [i][j].rgbtGreen = greyvalue;
            image [i][j].rgbtRed = greyvalue;
        }
    }

    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    //Iterate through columns and rows
    for (int i = 0 ; i < height; i += 1)
    {
        for (int j = 0; j < width; j += 1)
        {
            //Read values of pixels for each colour
            int blue = image [i][j].rgbtBlue;
            int green = image [i][j].rgbtGreen;
            int red = image [i][j].rgbtRed;
            //Apply depia filter to each colour of pixel
            int sepiaRed = round(0.393 * red + 0.769 * green + 0.189 * blue);
            int sepiaGreen = round(0.349 * red + 0.686 * green + 0.168 * blue);
            int sepiaBlue  = round(0.272 * red + 0.534 * green + 0.131 * blue);

            //Set red pixel to 255
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            //Set Green pixel to 255
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            //Set Blue pixel to 255
            if (sepiaBlue > 255)
            {
                sepiaRed = 255;
            }
            //otherwise set values
            image [i][j].rgbtRed = sepiaRed;
            image [i][j].rgbtGreen = sepiaGreen;
            image [i][j].rgbtBlue = sepiaBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    //Iterate through columns
    for (int i = 0 ; i < height; i += 1)
    {
        //Iterate through rows to halfway point
        for (int j = 0; j < width / 2; j += 1)
        {
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - (j + 1)];
            image[i][width - (j + 1)] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    //Set up iteration for each pixel and temp array
    int sumBlue;
    int sumGreen;
    int sumRed;
    float counter;
    RGBTRIPLE temp[height][width];
    for (int i = 0 ; i < height; i += 1)
    {
        for (int j = 0; j < width; j += 1)
        {
            sumBlue = 0;
            sumGreen = 0;
            sumRed = 0;
            counter = 0;
            //Adds up values of neighbouring 8 pixels, skipping if outside picture
            for (int k = -1; k < 2; k += 1)
            {
                if (((i + k) < 0) || ((i + k) > height - 1))
                {
                    continue;
                }
                for (int m = -1; m < 2; m += 1)
                {
                    if (((j + m) < 0) || ((j + m) > width - 1))
                    {
                        continue;
                    }
                    sumBlue += image[i + k][j + m].rgbtBlue;
                    sumGreen += image[i + k][j + m].rgbtGreen;
                    sumRed += image[i + k][j + m].rgbtRed;
                    counter += 1;
                }
                //Averages pixel values (with counter) and changes pixel
                temp[i][j].rgbtBlue = round(sumBlue / counter);
                temp[i][j].rgbtGreen = round(sumGreen / counter);
                temp[i][j].rgbtRed = round(sumRed / counter);
            }
        }
    }
    //Replace image with temp (blurred) values for each pixel
    for (int i = 0 ; i < height; i += 1)
    {
        for (int j = 0; j < width; j += 1)
        {
            image[i][j].rgbtBlue = temp[i][j].rgbtBlue;
            image[i][j].rgbtGreen = temp[i][j].rgbtGreen;
            image[i][j].rgbtRed = temp[i][j].rgbtRed;
        }

    }
    return;
}
