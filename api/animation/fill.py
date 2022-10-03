import asyncio

from .base import BaseAnimation


class FillAnimation(BaseAnimation):
    def __init__(self, strip: "LEDStrip", color: int) -> None:
        super().__init__(strip)
        self.color = color

    async def loop(self) -> None:
        self.strip.fillColor(self.color)
        self.strip.show()
        await asyncio.sleep(1)


# from .spotify import SharedData, animation_loop, update_playback
# async def fill(strip, _red, _green, _blue):
#     beat = None
#     red = _red
#     green = _green
#     blue = _blue
#     shared_playback = SharedData()
#     shared_analysis = SharedData()

#     def on_playback_change(playback, analysis):
#         print("now playing:", playback.item.name, playback.is_playing)

#     def on_section(section):
#         global red, green, blue
#         red += 7
#         green += 17
#         blue += 13
#         red %= 256
#         green %= 256
#         blue %= 256

#     def on_beat(_beat):
#         global beat
#         beat = _beat

#     def on_loop(progress):
#         # global bpm
#         # if bpm:
#         #     beat = beatsin88(int(bpm * 256), 128, 255) / 255
#         # else:
#         #     beat = 1
#         # strip.fillColor(Color(int(red * beat), int(green * beat), int(blue * beat)))
#         global beat

#         _beat = 1 - (progress - beat.start) / beat.duration
#         strip.fillColor(Color(int(red * _beat), int(green * _beat), int(blue * _beat)))

#         strip.show()

#     try:
#         update_playback_task = asyncio.create_task(update_playback(shared_playback, shared_analysis))
#         await animation_loop(shared_playback, shared_analysis, on_loop=on_loop, on_section=on_section, on_beat=on_beat, on_playback_change=on_playback_change)
#     finally:
#         update_playback_task.cancel()

