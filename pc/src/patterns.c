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

Color lerp_rgb(Color clrA, Color clrB, double perc)
{
    return (Color){ .r = LERP(clrA.r, clrB.r, perc), .g = LERP(clrA.g, clrB.g, perc), .b = LERP(clrA.b, clrB.b, perc) };
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
    static int trail_index = 0;

    if (PERIODIC(5))
    {
        trails[trail_index] = (struct Trail){
            .active = true,
            .pos = 0,
            .velocity = 20,
            .clr = trail_index % 2 == 0 ? from_rgb(200, 0, 0) : from_rgb(0, 0, 200),
            .trail_length = 30
        };
        trail_index = (trail_index + 1) % MAX_TRAILS;
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
                set_clr(trails[i].pos - j,
                    f_mul_rgb(
                        pow((1 - (float)j / trails[i].trail_length), 10),
                        trails[i].clr));
            }
            trails[i].pos += trails[i].velocity * delta_t;
            if (trails[i].pos > NUM_LEDS + trails[i].trail_length) trails[i].active = false;
        }
    }

    ticks = (ticks + 1) % NUM_LEDS;
    total_t += delta_t;
}
