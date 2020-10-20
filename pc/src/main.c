#define _GNU_SOURCE
#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <stdint.h>
#include <unistd.h>
#include <math.h>

#include "serial.h"

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

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        fprintf(stderr, "Usage: lightstrip <usb device>\n");
        return EXIT_FAILURE;
    }

    int fd = open_serial(argv[1]);

    printf("Sleeping for 1 seconds...\n");
    sleep(1);

    for (int i = 0; i < NUM_LEDS; i++)
    {
        colors[i] = from_rgb(0, 0, 0);
    }

    uint8_t header[5] = { 42, 42, 42, 42, 42 };

    int ticks = 0;
    while (true)
    {
        for (size_t i = 0; i < NUM_LEDS; i++)
        {
            colors[i] = from_rgb(
                abs((int)(sin((float)(i * 3 + ticks) / NUM_LEDS * M_PI) * 255)),
                abs((int)(sin((float)(i * 2 + ticks) / NUM_LEDS * M_PI) * 255)),
                abs((int)(cos((float)(i + ticks) / NUM_LEDS * M_PI) * 255))
            );
        }
        ticks = (ticks + 2) % NUM_LEDS;

        write(fd, header, 5);
        for (size_t i = 0; i < NUM_LEDS; i++)
        {
            write(fd, colors + i, 3);
        }
    }

    close(fd);
    return EXIT_SUCCESS;
}
