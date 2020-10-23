from update import VisualizationState
from update import RGB
import math

def setRGB(colors, pos, color):
    if (pos > 0 and pos < len(colors)):
        colors[pos] = color

colA = RGB(255, 0, 0)
colB = RGB(0, 255, 0)
total = 0
factor = 0.5
grow = 1
brightness = 1

def sectionCallback(state, section):
    state = state
    print("new section")

def barCallback(state, bar):
    global brightness
    brightness = 1

def beatCallback(state, beat):
    global total
    total += math.pi / 2

def tatumCallback(state, tatum):
    state = state

def segmentCallback(state, segment):
    #print("new segment")
    state = state

def genericCallback(state, delta):
    global total
    global brightness
    total += delta * factor
    brightness *= 0.98
    for i in range(0, state.num_leds):
        ii = i / state.num_leds * math.pi
        state.colors[i] = (colA * abs(math.sin(ii + total)) + colB * abs(math.cos(ii + total))) * brightness
    for i in range(0, state.num_leds):
        state.colors[i] = RGB(int(state.colors[i].r), int(state.colors[i].g), int(state.colors[i].b))