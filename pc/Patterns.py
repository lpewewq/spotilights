from Lightstrip import RGB
import math

def setRGB(colors, pos, color):
    if (pos > 0 and pos < len(colors)):
        colors[pos] = color

colA = RGB(255, 0, 0)
colB = RGB(0, 255, 0)
total = 0
factor = 1
evenFactor = 0.5
oddFactor = 1.5
grow = 1
brightness = 1
beat_num = 0

def sectionCallback(led_state, section):
    print(section)

def barCallback(led_state, bar):
    global factor
    factor /= abs(factor)
    factor *= -1

def beatCallback(led_state, beat):
    global total
    global beat_num
    global factor
    global brightness
    if (beat["confidence"] > 0):
        total += math.pi / 2
        if beat_num % 2 == 0:
            brightness += 0.5
        beat_num += 1
    print(beat)

def tatumCallback(led_state, tatum):
    tatum = tatum

def segmentCallback(led_state, segment):
    led_state = led_state

def genericCallback(led_state, delta):
    global total
    global brightness
    totalFactor = 0
    if beat_num % 2 == 0:
        totalFactor += evenFactor
    else:
        totalFactor += oddFactor
    totalFactor *= factor
    total += delta * totalFactor
    brightness = min(brightness, 1)
    brightness *= 0.98
    for i in range(0, led_state.num_leds):
        ii = i / led_state.num_leds * math.pi
        led_state.colors[i] = (colA * abs(math.sin(ii + total)) + colB * abs(math.cos(ii + total))) * brightness

    for i in range(0, led_state.num_leds):
        led_state.colors[i] = RGB(
            min(255, abs(int(led_state.colors[i].r))),
            min(255, abs(int(led_state.colors[i].g))),
            min(255, abs(int(led_state.colors[i].b))))
