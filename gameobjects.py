"""
**GameObject** ist eine Spriteklasse, von der sämtliche beweglichen
Spielobjekte abgeleitet werden.
"""

import pygame as pg
from pygame.sprite import Sprite
from pygame.math import Vector2
from game import *
import time


class GameObject(Sprite):
    def __init__(self, x, y, width=None, height=None, color=BLUE, img_name=None):
        super().__init__()
        self.__height = height
        self.__width = width
        self.__img_name = img_name
        self.__color = color
        self.__alpha = 255
        self.rect = Rect(x, y, 1, 1)
        self.create_image(img_name=img_name, width=width, height=height, color=color, alpha=self.alpha)
        self.rect.centerx = x
        self.rect.centery = y

        self.power = 1  # Anzahl Treffer bis tot
        self.__speed = Vector2(1, 1)
        self.__direction = Vector2(0, 0)
        self.visible = True
        self.running = True
        self.destroying = False
        self.destroyed = False
        self._drag_mode = False

    def create_image(self, img_name=None, alpha=None, width=None, height=None, color=None):
        if color:
            self.__color = color
        else:
            color = self.__color
        if width:
            self.__width = width
        else:
            width = self.__width
        if height:
            self.__height = height
        else:
            height = self.__height
        if img_name:
            self.__img_name = img_name
        else:
            img_name = self.__img_name
        if alpha:
            self.__alpha = alpha
        else:
            alpha = self.alpha
        x, y = self.rect.x, self.rect.y
        if img_name:
            self.image = Game.game.images.get(img_name, height=height, alpha=alpha)
        else:
            self.image = pg.Surface((width, height))
            self.image.set_alpha(alpha)
            pg.draw.rect(self.image, color, (0, 0, width, height))
        self.rect = self.image.get_rect()
        self.__height = self.rect.height
        self.__width = self.rect.width
        self.rect.x = x
        self.rect.y = y

    @property
    def alpha(self):
        return self.__alpha

    @alpha.setter
    def alpha(self, value):
        value = max(min(value, 255), 0)
        if self.alpha != value:
            self.create_image(alpha=value)

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, value):
        x, y = self.__direction.x, self.__direction.y
        if type(value) is Vector2:
            x1, y1 = value.x, value.y
        elif type(value) is tuple:
            x1, y1 = value
        elif type(value) in (int, float):
            x1 = value
            y1 = value
        else:
            x1 = None
            y1 = None
        if x1 in (-1, 0, 1):
            x = x1
        if y1 in (-1, 0, 1):
            y = y1
        self.__direction = Vector2(x, y)

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, value):
        x, y = self.__speed.x, self.__speed.y
        if type(value) is Vector2:
            self.__speed = value
            return
        elif type(value) is tuple:
            x, y = value
        elif type(value) in (int, float):
            x = value
            y = value
        self.__speed = Vector2(x, y)

    def set_position(self, pos):
        # pos ist Tupel (x, y)
        self.rect.center = pos

    def update(self):
        self.running = not Game.game.pause
        if self._drag_mode:
            # Der Maus folgen
            self.set_position(pg.mouse.get_pos())
        elif self.running:
            # Normale Bewegung
            mv = Vector2(int(self.direction.x * self.speed.x * Game.game.speed_factor),
                         int(self.direction.y * self.speed.y * Game.game.speed_factor))
            self.rect.move_ip(mv)

    def hit(self):
        self.power -= 1
        if self.power <= 0:
            self.destroy()

    def destroy(self):
        self.destroyed = True

    def collision_with(self, sprite):
        return self.rect.colliderect(sprite.rect)

    def change_alpha(self, value):
        self.alpha += value

    def on_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pg.mouse.get_pos()):
                self._drag_mode = True
        elif event.type == pg.MOUSEBUTTONUP:
            self._drag_mode = False
