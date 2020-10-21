#define _GNU_SOURCE
#include <stdint.h>
#include <stdlib.h>
#include <math.h>
#include <stdbool.h>
#include "patterns.h"
#include <stdio.h>
#include "../../common.h"

#define LERP(from, to, perc) ((from) + ((to) - (from)) * (perc))
#define PERIODIC(period) ((int)(total_t / (period)) != (int)((total_t + delta_t) / (period)))
#define SAWTOOTH(period) LERP(0, 1, (total_t - (int)(total_t / (period)) / (period))

#define BRIGHTNESS 255

Color colors[NUM_LEDS];

Color from_rgb(uint8_t r, uint8_t g, uint8_t b)
{
    return (Color){ .r = r, .g = g, .b = b };
}

void init_LEDs()
{
    for (int i = 0; i < NUM_LEDS; i++)
    {
        colors[i] = from_rgb(0, 0, 0);
    }
    srand(0);
}

double triangle(double total_t, double period)
{
    double elapsed_perc = total_t / period - (int)(total_t / period);
    if (elapsed_perc < 0.5)
    {
        return LERP(-1, 1, 2 * elapsed_perc);
    }
    else
    {
        return LERP(1, -1, 2 * (elapsed_perc - 0.5));
    }
}

void update_LEDs(double delta_t)
{
    static uint64_t ticks = 0;
    static double total_t = 0;

    double offset = triangle(total_t, 20);

    //printf("%d\n", abs((int)(offset * BRIGHTNESS)));

    for (size_t i = 0; i < NUM_LEDS; i++)
    {
        colors[i] = from_rgb(0,0,
            //abs((int)(pow(sin(((float)3 * i / NUM_LEDS + offset) * M_PI * 2), 2) * BRIGHTNESS)),
            //abs((int)(pow(cos(((float)3 * i / NUM_LEDS + offset) * M_PI * 2), 2) * BRIGHTNESS)),
            abs((int)(offset * BRIGHTNESS))
        );
        //colors[NUM_LEDS - i] = colors[i];
    }

    ticks = (ticks + 1) % NUM_LEDS;
    total_t += delta_t;
}
