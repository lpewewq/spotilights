#define _DEFAULT_SOURCE
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <stdint.h>
#include <unistd.h>  /* UNIX standard function definitions */
#include <fcntl.h>   /* File control definitions */
#include <errno.h>   /* Error number definitions */
#include <termios.h> /* POSIX terminal control definitions */

#define NUM_LEDS 180

typedef struct
{
    uint8_t g; // Must be in this order
    uint8_t r;
    uint8_t b;
} __attribute__((packed)) Color;

Color colors[NUM_LEDS];

Color from_rgb(uint8_t r, uint8_t g, uint8_t b)
{
    return (Color){ .r = r, .g = g, .b = b };
}

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

void send_buffer(int fd)
{
    for (size_t i = 0; i < NUM_LEDS; i++)
    {
        uint8_t d[1] = { 50 };
        write(fd, d, 1);
        write(fd, d, 1);
        write(fd, d, 1);
        usleep(500000);
    }
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

    //for (size_t i = 0; i < NUM_LEDS; i++)
    //{
    //    colors[i] = (Color){ .r = 255, .g = 0, .b = 0 };
    //}

    //int dot_index = 0;
    //int direction = 1;

    while (true)
    {
        send_buffer(fd);

        /*colors[dot_index] = from_rgb(0, 0, 0);
        dot_index += direction;
        colors[dot_index] = from_rgb(dot_index + 50, 255 - dot_index, 0);
        if (dot_index == NUM_LEDS - 1) direction = -1;
        if (dot_index == 0) direction = 1;*/
    }

    return EXIT_SUCCESS;
}
