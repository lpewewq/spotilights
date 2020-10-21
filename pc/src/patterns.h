#pragma once
#include <stdint.h>
#include "../../common.h"

typedef struct
{
    uint8_t g; // Must be in this order
    uint8_t r;
    uint8_t b;
} __attribute__((packed)) Color;

extern Color colors[NUM_LEDS];
void init_LEDs();
void update_LEDs(double delta_t);
