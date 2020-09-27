#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    //Declare variables
    unsigned char buffer[512];
    int file_counter = 0;
    char *input = argv[1];
    FILE *output = NULL;
    int jpeg_already = 0;
    //If command line != 1 then quit
    if (argc != 2)
    {
        printf("Provide one command line argument\n");
        return 1;
    }
    //Open memory card, throw error if this doesn't work
    FILE *input_point = fopen(input, "r");
    if (input == NULL)
    {
        printf("Error accessing file\n");
        return 1;
    }
    ////Read 512 bytes into a buffer, repeat until end of card:
    while (fread(buffer, 512, 1, input_point) == 1)
    {
        //If start of new JPEG
        if ((buffer[0] == 0xff) && (buffer[1] == 0xd8) && (buffer[2] == 0xff) && ((buffer[3] & 0xf0) == 0xe0))
        {
            //If not first JPEG
            if (jpeg_already == 1)
            {
                //Close current file
                fclose(output);
            }
            //Else it must be first JPEG
            else
            {
                jpeg_already = 1;
            }
            //Create and write to file
            char filename[8];
            sprintf(filename, "%03i.jpg", file_counter);
            output = fopen(filename, "a");
            fwrite(buffer, 512, 1, output);

            file_counter += 1;
        }
        else
        {
            //If already found JPEG, carry on writing
            if (jpeg_already == 1)
            {
                fwrite(buffer, 512, 1, output);
            }
        }
    }
    //Close any remaining file
    fclose(input_point);
    fclose(output);
    return 0;
}
