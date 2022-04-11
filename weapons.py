"""
Die Waffen des Spiels.
**Rocket**: Eine Rakete, die von unten abgeschossen wird.
**Bomb**: Eine Bombe, die vom Gener abgeworfen wird.
"""

from gameobjects import *


class Rocket(GameObject):
    def __init__(self, x, y, dx=None, dy=-1, height=20, speed=10, img_name=None):
        super().__init__(x, y, height, height, RED, img_name)
        self.speed = speed
        self.direction = (dx, dy)

    def update(self):
        super().update()
        if self.rect.bottom < 0 or self.rect.top > Game.game.bottom:
            self.destroy()  # Enfernen, wenn das Element das Spielfeld verlässt


class Bomb(GameObject):
    def __init__(self, x, y, dx=None, dy=1, height=10, speed=10, img_name=None):
        super().__init__(x, y, height, height, RED, img_name)
        self.speed = speed
        self.direction = (dx, dy)

    def update(self):
        super().update()
        if self.rect.bottom < 0 or self.rect.top > Game.game.bottom:
            self.destroy()  # Enfernen, wenn das Element das Spielfeld verlässt
