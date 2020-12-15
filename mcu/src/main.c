#define F_CPU 16000000L
#include <stdbool.h>
#include <stdint.h>
#include <util/delay.h>
#include <avr/io.h>

#define NUM_LEDS    180
#define BUFFER_SIZE (NUM_LEDS * 3)
#define HEADER_SIZE  5
#define HEADER_START 42
#define LED_DDR      DDRD
#define LED_PORT     PORTD
#define LED_PIN      3

extern void output_grb(uint8_t *buffer, uint16_t bytes);

uint8_t colors[BUFFER_SIZE];

void LEDs_show()
{
    output_grb(colors, BUFFER_SIZE);
    LED_PORT &= ~(1 << LED_PIN);
    _delay_us(60);
}

void LEDs_init()
{
    LED_DDR  |= (1 << LED_PIN);
    LED_PORT &= ~(1 << LED_PIN);
}

void uart_init()
{
    // Baud rate: 500000 bps
    UBRR0H = (uint8_t)(3 >> 8);
    UBRR0L = (uint8_t)(3 & 0xFF);
    UCSR0A = (1 << U2X0);                  // Double speed
    UCSR0B = (1 << RXEN0) | (0 << TXEN0);  // Enable the receiver, disable transmitter
    UCSR0C = (1 << USBS0) | (3 << UCSZ00); // 2 stop bits, 8 bit data
}

uint8_t uart_recv()
{
    // Busy wait until data is present
    while (!(UCSR0A & (1 << RXC0)));
    return UDR0;
}

int main()
{
    LEDs_init();
    LEDs_show();
    uart_init();

    uint8_t header_count = 0;
    uint16_t curr_index   = 0;
    while (true)
    {
        uint8_t data = uart_recv();
        if (header_count < HEADER_SIZE)
        {
            if (data == HEADER_START + header_count)
            {
                header_count++;
            }
            else
            {
                header_count = 0;
            }
        }
        else
        {
            colors[curr_index] = data;
            curr_index++;
            if (curr_index == BUFFER_SIZE)
            {
                header_count = 0;
                curr_index = 0;
                LEDs_show();
            }
        }
    }

    return 0;
}
