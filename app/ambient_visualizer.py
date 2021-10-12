import colorsys

from app.lightstrip_state import RGB


class AmbientVisualizer:
    col_a = RGB(1, 0, 0)
    col_b = RGB(1, 1, 0)
    brightness = 1
    wave_pos = 0

    def update(self, delta, leds):
        self.wave_pos += delta / 5
        for i in range(0, leds.n_leds):
            ii = i / leds.n_leds  # * math.pi
            # self.leds.set_color(i,
            # pow(math.sin(ii * math.pi), 3) * (self.col_a * abs(math.sin(ii + self.wave_pos)) + self.col_b * abs(math.cos(ii + self.wave_pos))) * self.brightness)
            (r, g, b) = colorsys.hsv_to_rgb(ii * 2 + self.wave_pos, 1, 1)
            # self.leds.set_color(i, RGB(r, g, b))

            if i < 90:
                leds.set_color(i, RGB(1, 0, 0))
            else:
                leds.set_color(i, RGB(0, 0, 1))
        return leds
