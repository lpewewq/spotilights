#include <unistd.h>  /* UNIX standard function definitions */
#include <fcntl.h>   /* File control definitions */
#include <errno.h>   /* Error number definitions */
#include <termios.h> /* POSIX terminal control definitions */
#include <string.h>
#include <stdio.h>

#define BAUD B500000

int open_serial(char *device)
{
    int fd;

    fd = open(device, O_RDWR | O_NOCTTY | O_NDELAY);
    if (fd == -1)
    {
        perror("Unable to open device");
        return -1;
    }
    else
    {
        fcntl(fd, F_SETFL, 0);
    }

    if (fd < 0)
    {
        return fd;
    }

    struct termios tty;
    if (tcgetattr(fd, &tty) != 0)
    {
        printf("Error %i from tcgetattr: %s\n", errno, strerror(errno));
        close(fd);
        return -1;
    }

    tty.c_cflag &= ~PARENB;        // Clear parity bit, disabling parity (most common)
    tty.c_cflag |= CSTOPB;         // Set stop field, two stop bits used in communication
    tty.c_cflag |= CS8;            // 8 bits per byte (most common)
    tty.c_cflag |= CREAD | CLOCAL; // Turn on READ & ignore ctrl lines (CLOCAL = 1)
    tty.c_lflag &= ~ICANON;        // Disable canonical mode
    tty.c_lflag &= ~ECHO;          // Disable echo
    tty.c_lflag &= ~ECHOE;         // Disable erasure
    tty.c_lflag &= ~ECHONL;        // Disable new-line echo
    tty.c_lflag &= ~ISIG;          // Disable interpretation of INTR, QUIT and SUSP
    tty.c_iflag &= ~(IXON | IXOFF | IXANY); // Turn off s/w flow ctrl
    tty.c_iflag &= ~(IGNBRK|BRKINT|PARMRK|ISTRIP|INLCR|IGNCR|ICRNL); // Disable any special handling of received bytes
    tty.c_oflag &= ~OPOST; // Prevent special interpretation of output bytes (e.g. newline chars)
    tty.c_oflag &= ~ONLCR; // Prevent conversion of newline to carriage return/line feed
    cfsetispeed(&tty, BAUD);

    // Save tty settings, also checking for error
    if (tcsetattr(fd, TCSANOW, &tty) != 0)
    {
        printf("Error %i from tcsetattr: %s\n", errno, strerror(errno));
        close(fd);
        return -1;
    }

    return fd;
}
