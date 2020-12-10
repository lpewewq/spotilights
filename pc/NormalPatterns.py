from Lightstrip import RGB
import math

colA = RGB(255, 0, 0)
colB = RGB(0, 0, 255)
brightness = 1
total = 0

def callback(led_state, delta):
    global total
    total += delta / 2

    for i in range(0, led_state.num_leds):
        ii = i / led_state.num_leds * math.pi
        led_state.colors[i] = (colA * abs(math.sin(ii + total)) + colB * abs(math.cos(ii + total))) * brightness
