"""
Die Klasse **Enemy** implementiert einen normalen Gegner.
Für stärkere Gegner kann **Boss** verwendet werden
"""

from gameobjects import *
from weapons import Bomb
import random

class Enemy(GameObject):
    def __init__(self, x, y, width=30, height=30, speed=10, power=3, color=RED, img_name=None):
        super().__init__(x, y, width, height, color, img_name)
        self.speed = speed
        self.power = power
        self.fade = 200 // power
        self.start_y = y
        self.direction = (1, 0)
        self.is_boss = False

    def update(self):
        super().update()
        if self.rect.left < 0 or self.rect.right > Game.game.width:
            self.rect.top += self.rect.height
            self.direction.x = -self.direction.x
        if self.rect.bottom >= Game.game.bottom:
            self.rect.top = self.start_y
            self.speed.x *= 1.1

    @classmethod
    def weak_enemy(cls, x, y):
        return cls(x, y, width=30, height=30, speed=10, power=3, color=RED, img_name="enemyred3.png")

    @classmethod
    def medium_enemy(cls, x, y):
        return cls(x, y, width=30, height=30, speed=10, power=5, color=RED, img_name="enemyred3.png")

    @classmethod
    def strong_enemy(cls, x, y):
        return cls(x, y, width=30, height=30, speed=10, power=10, color=RED, img_name="enemyred3.png")

    @classmethod
    def as_boss(cls, x, y, width=30, height=30, speed=10, power=10, color=RED, img_name="shipBlue_manned.png"):
        boss = cls(x, y+height//2, width, height, speed, power, color, img_name)
        boss.is_boss = True
        return boss

    def new_bombs(self):
        b1 = None
        b2 = None
        b3 = None
        if not self.destroying and self.running:
            if random.randint(0, 100) == 0:
                b1 = Bomb(x=self.rect.centerx, y=self.rect.bottom, dy=1)
            if self.is_boss:
                if random.randint(0, 100) == 0:
                    b2 = Bomb(x=self.rect.centerx -20, y=self.rect.bottom, dy=1)
                if random.randint(0, 100) == 0:
                    b3 = Bomb(x=self.rect.centerx + 20, y=self.rect.bottom, dy=1)
        return [b1, b2, b3]

    def hit(self):
        super().hit()
        self.change_alpha(-self.fade)


