from abc import ABC, abstractmethod

from app.visualizer import Lightstrip


class BaseVisualizer(ABC):
    def __init__(self, app):
        self.leds = Lightstrip(app)

    @abstractmethod
    def update(self, delta):
        return self.leds

    def cleanup(self):
        pass  # cleanup ressources
