"""
Diese Klassen erstellen Bestandteile der Benutzeroberfläche.
Es handel sich dabei um Ausgabeelemente für Text und Grafik.
**TextObject**: Ein Element zur Textausgabe.
**Symbols**: Eine Zahl wird duch eine bestimmte Anzahl Bilder ausgedrückt.
**Power**: Leistung oder verbleibende Energie wird duch einen Balken in % ausgedrückt.
"""

import pygame as pg
from pygame.math import Vector2
from game import *


class TextObject:
    def __init__(self, font, position, alignement, color):
        self.font = font
        self.visible = True
        self.position = Vector2(position)
        self.alignement = alignement
        self.color = color
        self.__surface = None
        self.__rect = None
        self.text = ""

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        self.__text = value
        self.__surface = self.font.render(value, False, self.color)
        self.__rect = self.__surface.get_rect()

    def draw(self, screen):
        if self.visible:
            self.__rect.y = self.position.y
            if self.alignement == 'l':
                self.__rect.x = self.position.x
            elif self.alignement == 'm':
                self.__rect.centerx = self.position.x
            else:
                self.__rect.x = self.position.x - self.__rect.width
            screen.blit(self.__surface, self.__rect)


class Symbols:
    def __init__(self, position, alignement, height, img_name):
        self.visible = True
        self.position = Vector2(position)
        self.alignement = alignement
        self.height = height
        self.load_img(img_name)
        self.__rect = self.__surface.get_rect()
        self.value = 1

    def load_img(self, name):
        self.__surface = Game.game.images.get(name, height=self.height)

    def draw_symbol(self, pos, screen):
        w = int(self.__surface.get_width() * 1.2)
        self.__rect.y = self.position.y
        if self.alignement == 'l':
            self.__rect.x = self.position.x + pos * w
        elif self.alignement == 'm':
            self.__rect.centerx = self.position.x + pos * w // 2
        else:
            self.__rect.x = self.position.x - self.__rect.width - pos * w
        screen.blit(self.__surface, self.__rect)

    def draw(self, screen):
        if self.visible:
            for pos in range(self.value):
                self.draw_symbol(pos, screen)


class Power:
    def __init__(self, position, alignement, width, height, color, bg_color=BLACK):
        self.visible = True
        self.position = Vector2(position)
        self.alignement = alignement
        self.height = height
        self.width = width
        self.color = color
        self.bg_color = bg_color
        self.__surface = pg.Surface((width, height))
        self.__rect = self.__surface.get_rect()
        self.__rect.topright = self.position
        self.value = 100
        self.__num = 0

    def draw(self, screen):
        if self.visible:
            x = 100 - ((self.width * self.value) // 100)
            self.__surface.fill(self.bg_color)
            self.__surface.fill(self.color, (x, 0, self.width - x, self.height))
            screen.blit(self.__surface, self.__rect)
