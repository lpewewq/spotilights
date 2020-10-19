#define F_CPU 16000000L

#include <stdbool.h>
#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>

#include <util/delay.h>
#include <avr/io.h>
#include <avr/interrupt.h>

#define NUM_LEDS  180

#define LED_DDR  DDRB
#define LED_PORT PORTB
#define LED_PIN  2

typedef struct
{
    uint8_t g; // Must be in this order
    uint8_t r;
    uint8_t b;
} __attribute__((packed)) Color;

extern void output_grb(Color *color, uint16_t n);

Color colors[NUM_LEDS];

void debug()
{
    colors[NUM_LEDS - 1] = (Color){ .g = 255, .r = 0, .b = 0 };
}

void uart_init()
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
    //debug();
    return UDR0;
}

ISR (TIMER0_OVF_vect)
{
    output_grb(colors, NUM_LEDS * 3);
    LED_PORT &= ~(1 << LED_PIN);
    _delay_us(100);
}

int main()
{
    LED_DDR  |= (1 << LED_PIN);
    LED_PORT &= ~(1 << LED_PIN);

    TCCR0B = (1 << CS02) | (0 << CS01) | (1 << CS00);
    TIMSK0 |= (1 << TOIE0);
    sei();

    uart_init();

    for (size_t i = 0; i < NUM_LEDS; i++)
    {
        colors[i] = (Color){ .r = 255, .g = 0, .b = 0 };
    }

    size_t curr_index = 0;
    while (true)
    {
        colors[curr_index] = (Color){ .g = 0, .r = uart_recv(), .b = uart_recv() };
        curr_index = (curr_index + 1) % NUM_LEDS;
    }

    return 0;
}
