"""
Die Klasse **Game** ist die Basisklasse für alle Games.

Es stehen auch die statischen Methoden **create_font**,
**create_sys_font** und **render_text** zur Verfügung.
"""

import os, glob
import pygame as pg
from pygame.locals import *
import pickle

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GRAY = (100, 100, 100)
BROWN = (153, 76, 0)
ORANGE = (214, 122, 30, 127)


class Game:
    """
    **Basisklasse für beliebige Pygame-Spiele**

        Einzige Instanz der Klasse
            *Game.game*

        Assetverwaltung über Objekte
            *.images*, *.sounds* und *.music*

            Die Dateien für Bilder und Geräusche müssen sich im Unterverzeichnis "assets" befinden.

            Die Dateien für Musik müssen sich im Unterverzeichnis "assets/music" befinden.

        Erzeugung von Fonts
            *Game.create_font(size, name)*

            *Game.create_sys_font(size, name)*

        Textfeld
            *Game.render_text(text, font, color, bg_color=None)* -> Surface
    """
    game = None

    def __init__(self, width, height, caption, background_color=BLACK, fps=30):
        self.main_dir = os.path.split(os.path.abspath(__file__))[0]
        self.asset_dir = os.path.join(self.main_dir, "assets")
        self.music_dir = os.path.join(self.asset_dir, "music")
        self.speed_factor = 1
        self.width = width
        self.height = height
        self.caption = caption
        self.background_color = background_color
        self.background = None
        self.fps = fps
        self.screen = pg.display.set_mode((width, height))
        pg.display.set_caption(caption)
        self.clock = pg.time.Clock()
        self.running = False
        self.pause = False
        self.music = self.Music()
        self.sounds = self.Sounds()
        self.images = self.Images()
        self.next_event = USEREVENT # nächste Event-Id
        Game.game = self

    def set_timer_event(self, event, millis, loop=0):
        pg.time.set_timer(event, millis, loop)

    def new_timer_event(self, millis, loop=0):
        event = self.next_event
        self.next_event += 1
        self.set_timer_event(event, millis, loop)
        return event

    def delete_timer_event(self, event):
        self.set_timer_event(event, 0)

    def run(self):
        self.prepare()
        self.running = True
        self.pause = False
        while self.running:
            self.clock.tick(self.fps)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    break
                if event.type == pg.KEYDOWN and event.key == pg.K_1:
                    self.speed_factor = 0.5
                elif event.type == pg.KEYDOWN and event.key == pg.K_2:
                    self.speed_factor = 1.0
                elif event.type == pg.KEYDOWN and event.key == pg.K_3:
                    self.speed_factor = 1.5
                elif event.type == pg.KEYDOWN and event.key == pg.K_m:
                    self.music.pause = not self.music.pause
                elif event.type == pg.KEYDOWN and event.key == pg.K_p:
                    self.pause = not self.pause
                else:
                    self.handle_event(event)
            self.handle_keys(pg.key.get_pressed())
            self.update()
            self.draw()
            pg.display.update()  # pg.display.flip()

    def all_objects(self):
        return []

    def prepare(self):
        pass

    def handle_event(self, event):
        pass

    def handle_keys(self, keys):
        pass

    def update(self):
        pass

    def draw(self):
        if self.background:
            self.screen.blit(self.background, self.background.get_rect())
        else:
            self.screen.fill(self.background_color)

    class Sounds():
        def __init__(self):
            self.__list = dict()

        def clear(self):
            self.__list.clear()

        def add(self, name):
            names = glob.glob(os.path.join(Game.game.asset_dir, name))
            for name in names:
                try:
                    self.__list[os.path.basename(name).upper()] = pg.mixer.Sound(name)
                except:
                    print("Cannot load sound:", name)

        def get_list(self):
            return self.__list.copy()

        def get_sound(self, name):
            class NoneSound:
                def play(self):
                    pass

            name = name.upper()
            if name in self.__list:
                return self.__list[name]
            else:
                print(f"{name} not found")
                return NoneSound()

    class Images():
        def __init__(self):
            self.__list = dict()

        def clear(self):
            self.__list.clear()

        def add(self, name):
            names = glob.glob(os.path.join(Game.game.asset_dir, name))
            for name in names:
                try:
                    image = pg.image.load(name).convert()
                    colorkey = image.get_at((0, 0))
                    image.set_colorkey(colorkey, RLEACCEL)
                    self.__list[os.path.basename(name).upper()] = image
                except:
                    print("Cannot load image:", name)

        def get_list(self):
            return self.__list.copy()

        def get(self, name, width=None, height=None, alpha=255):
            name = name.upper()
            if name in self.__list:
                img = self.__list[name]
                img_width, img_height = img.get_size()  # Grösse
                img_ratio = img_width / img_height  # Seitenverhältnis

                if width and not height:
                    height = width // img_ratio
                elif height and not width:
                    width = int(height * img_ratio)
                elif not height and not width:
                    width, height = img_width, img_height

                # image erstellen und skaliertes Bild hineinkopieren
                sf = pg.Surface((width, height), SRCALPHA)
                img.set_alpha(alpha)
                sf.blit(pg.transform.smoothscale(img, (width, height)), (0, 0))
                return sf
            else:
                print(f"{name} not found")
                return None

    class Music():
        def __init__(self):
            self.__list = dict()
            self._ready = False
            self._play = False
            self._pause = False

        def clear(self):
            self.__list.clear()

        def add(self, name):
            names = glob.glob(os.path.join(Game.game.music_dir, name))
            for name in names:
                try:
                    self.__list[os.path.basename(name).upper()] = name
                except:
                    print("Cannot load music:", name)

        def get_list(self):
            return self.__list.copy()

        @property
        def player(self):
            return pg.mixer.music

        def choose(self, name):
            name = name.upper()
            if name in self.__list:
                self.player.load(self.__list[name])
                Game.music_ready = True
                if self.play:
                    self.player.play(-1)
                if self.pause:
                    self.player.pause()
            else:
                print(f"{name} not found")
                pg.mixer.music.stop()

        @property
        def pause(self):
            return self._pause

        @pause.setter
        def pause(self, value):
            self._pause = value
            if value:
                self.player.pause()
            else:
                self.player.unpause()

        @property
        def play(self):
            return self._play

        @play.setter
        def play(self, value):
            self._play = value
            if value:
                self.player.play(-1)
            else:
                self.player.stop()

    @staticmethod
    def create_font(size, name=None):
        if name:
            fullname = os.path.join(Game.game.asset_dir, "fonts")
            fullname = os.path.join(fullname, name)
            try:
                font = pg.font.Font(fullname, size)
            except pg.error as message:
                print("Cannot load font:", fullname)
                raise SystemExit(message)
        else:
            font = pg.font.Font(None, size)
        return font

    @staticmethod
    def create_sys_font(size, name=None):
        if name:
            try:
                font = pg.font.SysFont(name, 30)
            except pg.error as message:
                print("Cannot load sys_font:", name)
                raise SystemExit(message)
        else:
            font = pg.font.Font(None, size)
        return font

    @staticmethod
    def render_text(text, font, color, bg_color=None):
        return font.render(text, False, color, bg_color)


