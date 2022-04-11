"""
Das Hauptmodul initialisiert Pygame,
erzeugt das Spiel und startet es.
"""

# import pygame as pg
from game import *
from defenders import Defenders

pg.init()
Defenders(width=800, height=600, caption="Space Defenders", background_color=BLACK).run()
pg.quit()
exit()




