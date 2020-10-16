#define F_CPU 16000000L

#include <stdbool.h>
#include <stdint.h>
#include <avr/io.h>
#include <util/delay.h>

#define T0H_US 0.40
#define T1H_US 0.80
#define T0L_US 0.85
#define T1L_US 0.45
#define RES_US 0.50

#define NUM_LEDS  (4 * 3)
#define COL_DEPTH 24

#define LED_DDR  DDRB
#define LED_PORT PORTB
#define LED_PIN  2

typedef union
{
    struct
    {
        uint8_t g; // Must be in this order
        uint8_t r;
        uint8_t b;
    } as_rgb;

    uint32_t as_int;
} Color;

extern void output_grb(Color *color, uint16_t n);

Color from_rgb(uint8_t r, uint8_t g, uint8_t b)
{
    return (Color){ .as_rgb = { .r = r, .g = g, .b = b }};
}

int main()
{
    LED_DDR  |= (1 << LED_PIN);
    LED_PORT &= ~(1 << LED_PIN);

    Color colors[NUM_LEDS] = {
        from_rgb(0, 255,   0),
        from_rgb(0,   0,   0),
        from_rgb(0,   0, 0),
        from_rgb(0, 0,   0)
    };

    while (true)
    {
        output_grb(colors, NUM_LEDS);
        LED_PORT &= ~(1 << LED_PIN);
        _delay_us(60);
    }

    return 0;
}

/*void uart_init()
{
    // Baud rate: 9600 bps
    UBRR0L = (uint8_t)(103 & 0xFF);
    UBRR0H = (uint8_t)(103 >> 8);
    // Enable the receiver, we will never send
    UCSR0B |= (1 << RXEN0) | (0 << TXEN0);
}

uint8_t uart_recv()
{
    // Busy wait until data is present
    while (!(UCSR0A & (1 << RXC0)));
    return UDR0;
}*/
