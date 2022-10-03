import asyncio
from abc import ABC, abstractmethod


class BaseAnimation(ABC):
    """Interface for animations."""

    def __repr__(self) -> str:
        return type(self).__name__ + "()"

    def __init__(self, strip: "LEDStrip") -> None:
        self.strip = strip

    async def start(self) -> None:
        try:
            while True:
                await self.loop()
                await asyncio.sleep(0)
        except Exception as e:
            print(f"{self} excepted:", e)

    @abstractmethod
    async def loop(self) -> None:
        """Animation loop"""
