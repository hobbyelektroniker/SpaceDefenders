"""
Der Spieler wird durch die Klasse **Player** erstellt.
"""

from gameobjects import *
from weapons import Rocket, Bomb


class Player(GameObject):
    """
    Diese Klasse erzeugt einen Spieler. Obligatorisch ist die Angabe der Startposition *x* und *y*.
    Mit *power* wird festgelegt, wieviele Male der Spieler getroffen werden muss, damit er zerstört wird.
    Der Gesundheitszustand in Prozent kann mit *get_health()* abgefragt werden.
    *img_name* ist der Name einer Datei, die ein Bild für die Darstellung zur Verfügung stellt.
    Zum Laden wird die Klasse **AssetFactory** verwendet.
    Das Bild wird automatisch für das angegebene Rechteck skaliert.
    """
    def __init__(self, x, y, width=100, height=50, speed=10, power=5, color=BLUE, img_name=None):
        super().__init__(x, y, width, height, color, img_name)
        self.speed = speed
        self.power = power
        self.full_power = power
        self.delta_alpha = 0
        self.base_width = width
        self.base_height = height
        self.__zoom = 1.0
        self.hit_sound = Game.game.sounds.get_sound("rumble1.ogg")

    def update(self):
        super().update()
        if self.rect.top < 50:
            self.rect.top = 50
        if self.rect.bottom > Game.game.bottom:
            self.rect.bottom = Game.game.bottom
        if self.rect.right < 0:
            self.rect.left = Game.game.width
        if self.rect.left > Game.game.width:
            self.rect.right = 0

    def new_rocket(self):
        return Rocket(x=self.rect.centerx, y=self.rect.top, dy=-1, img_name="laserBlue01.png")

    def collision_check(self, sprites):
        for sprite in sprites:
            if type(sprite) is Bomb:
                if self.rect.colliderect(sprite.rect):
                    self.hit()
                    sprite.hit()

    def hit(self):
        super().hit()
        self.hit_sound.play()

    def get_health(self):
        return 100 * self.power / self.full_power

    def zoom_in(self):
        self.set_zoom(self.__zoom + 0.25)

    def zoom_out(self):
        self.set_zoom(self.__zoom - 0.25)

    def set_zoom(self, value):
        self.__zoom = max(min(value, 2.0), 0.25)
        w = int(self.base_width * self.__zoom)
        h = int(self.base_height * self.__zoom)
        self.create_image(width=w, height=h)

    def on_event(self, event):
        super().on_event(event)
        if event.type == pg.KEYDOWN:
            if event.key == K_KP_PLUS:
                self.zoom_in()
            elif event.key == K_KP_MINUS:
                self.zoom_out()
            elif event.key == K_KP_ENTER:
                self.set_zoom(1)
