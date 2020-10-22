#define _GNU_SOURCE
#include <stdint.h>
#include <stdlib.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>

#include "patterns.h"
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

Color f_mul_rgb(double factor, Color clr)
{
    return (Color){ .r = factor * clr.r, .g = factor * clr.g, .b = factor * clr.b };
}

Color rgb_mul_rgb(Color clrA, Color clrB)
{
    return (Color){ .r = clrA.r * clrB.r, .g = clrA.g * clrB.g, .b = clrA.b * clrB.b };
}

void init_LEDs()
{
    for (int i = 0; i < NUM_LEDS; i++)
    {
        colors[i] = from_rgb(0, 0, 0);
    }
    srand(0);
}

double triangle(double x, double period)
{
    double elapsed_perc = x / period - (int)(x / period);
    if (elapsed_perc < 0.5)
    {
        return LERP(-1, 1, 2 * elapsed_perc);
    }
    else
    {
        return LERP(1, -1, 2 * (elapsed_perc - 0.5));
    }
}

struct Trail
{
    bool active;
    float pos;
    Color clr;
    double velocity;
    uint8_t trail_length;
};

void set_clr(int pos, Color clr)
{
    if (pos >= 0 && pos < NUM_LEDS) colors[pos] = clr;
}

#define MAX_TRAILS 20
void update_LEDs(double delta_t)
{
    static uint64_t ticks = 0;
    static double total_t = 0;
    static struct Trail trails[MAX_TRAILS];

    printf("\rFPS: %d                    ", (int)(1.0 / delta_t));

    if (PERIODIC(1))
    {
        for (size_t i = 0; i < MAX_TRAILS; i++)
        {
            if (!trails[i].active)
            {
                trails[i].active = true;
                trails[i].pos = 0;
                trails[i].velocity = 350;
                trails[i].trail_length = trails[i].velocity;
                break;
            }
        }
    }

    for (size_t i = 0; i < NUM_LEDS; i++)
    {
        colors[i] = from_rgb(0, 0, 0);
    }

    for (size_t i = 0; i < MAX_TRAILS; i++)
    {
        if (trails[i].active)
        {
            for (size_t j = 0; j < trails[i].trail_length; j++)
            {
                set_clr(trails[i].pos - j, f_mul_rgb(pow(1 - (float)j / trails[i].trail_length, 8),
                    from_rgb(0, (float)(trails[i].pos - j) / NUM_LEDS * 255, 255 - (float)(trails[i].pos - j) / NUM_LEDS * 255)));
            }
            trails[i].pos += trails[i].velocity * delta_t;
            if (trails[i].pos > NUM_LEDS + trails[i].trail_length) trails[i].active = false;
        }
    }

    ticks = (ticks + 1) % NUM_LEDS;
    total_t += delta_t;
}
