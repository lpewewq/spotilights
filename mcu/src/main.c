#define F_CPU 16000000L

#include <stdbool.h>
#include <stdint.h>
#include <avr/io.h>
#include <util/delay.h>

void led_init()
{
    DDRB |= (1 << 5);
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
    return UDR0;
}

int main()
{
    uart_init();

    while (true)
    {
        unsigned char c = (unsigned char)uart_recv();
        while (c-- != 0)
        {
            PORTB |= (1 << 5);
            _delay_ms(500);
            PORTB &= (0 << 5);
            _delay_ms(500);
        }
    }

    return 0;
}
