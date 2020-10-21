#define _GNU_SOURCE
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <stdbool.h>
#include <stdint.h>
#include <unistd.h>
#include <sys/time.h>

#include "../../common.h"
#include "patterns.h"
#include "serial.h"

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        fprintf(stderr, "Usage: lightstrip <usb device>\n");
        return EXIT_FAILURE;
    }

    int fd = open_serial(argv[1]);
    if (fd == -1)
    {
        return EXIT_FAILURE;
    }

    printf("Successfully connected to LED Strip. Using %d LEDs.\n", NUM_LEDS);
    sleep(1);

    init_LEDs();

    uint8_t header[HEADER_SIZE];
    for (size_t i = 0; i < HEADER_SIZE; i++) header[i] = HEADER_START + i;

    struct timeval begin;
    struct timeval end;
    struct timeval diff;
    gettimeofday(&begin, NULL);
    while (true)
    {
        gettimeofday(&end, NULL);
        timersub(&end, &begin, &diff);
        begin = end;
        update_LEDs((double)diff.tv_usec / 1000000);

        write(fd, header, HEADER_SIZE);
        for (size_t i = 0; i < NUM_LEDS; i++)
        {
            write(fd, colors + i, 3);
        }
    }

    close(fd);
    return EXIT_SUCCESS;
}
