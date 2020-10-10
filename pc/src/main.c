#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>  /* UNIX standard function definitions */
#include <fcntl.h>   /* File control definitions */
#include <errno.h>   /* Error number definitions */
#include <termios.h> /* POSIX terminal control definitions */

int open_serial(char *device)
{
    int fd;
    fd = open(device, O_RDWR | O_NOCTTY | O_NDELAY);
    if (fd == -1)
    {
        perror("Unable to open device");
    }
    else
    {
        fcntl(fd, F_SETFL, 0);
    }
    return fd;
}

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        fprintf(stderr, "Usage: lightstrip <usb device>\n");
        return EXIT_FAILURE;
    }

    int fd = open_serial(argv[1]);
    if (fd < 0)
    {
        return EXIT_FAILURE;
    }

    printf("Successfully openend serial! Press some numbers.\n");

    int c;
    while ((c = getchar()) != EOF)
    {
        if (c != '\n')
        {
            c -= '0'; // Adjust: Number to send = Times LED blinks
            ssize_t n = write(fd, (void*)&c, 1);
            if (n < 0)
            {
                fprintf(stderr, "Write syscall failed\n");
            }
        }
    }

    return EXIT_SUCCESS;
}