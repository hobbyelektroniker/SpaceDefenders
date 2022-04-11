"""
Dieses Modul implementiert das aktuelle Spiel.
"""

from pygame import surface
from game import *
from player import Player
from guiobjects import TextObject, Symbols, Power
from enemy import Enemy


class Defenders(Game):

    def prepare(self):
        self.images.add("*.png")
        self.sounds.add("*.ogg")

        self.music.add("*.ogg")
        self.music.choose("SpaceCadet.ogg")
        self.music.play = True

        self.laser_sound = self.sounds.get_sound("laser2.ogg")

        # Fonts
        self.gui_font = pg.font.SysFont("comicsansms", 30)
        self.gameover_font = pg.font.SysFont("comicsansms", 60)

        # Variable
        self.bottom = self.height - 20
        self.level = 0
        self.score = 0
        self.players = 3
        self.wait_for_new_game = True
        self.pause = False
        self.gameover = False

        # Statischer Hintergrund
        self.background = surface.Surface(self.screen.get_size())
        pg.draw.rect(self.background, BROWN, (0, self.bottom, self.width, self.width - self.bottom))

        # GUI Elemente
        self.gui_level = TextObject(self.gui_font, (5, 5), 'l', RED)
        self.gui_points = TextObject(self.gui_font, (self.width // 2, 5), 'm', RED)
        self.gui_players = Symbols((self.width - 5, 5), 'r', 30, "playership1_blue.png")
        self.gui_player_health = Power((self.width - 5, 40), 'r', 100, 10, GREEN)

        self.gui_gameover = TextObject(self.gameover_font, (self.width // 2, self.height // 4), 'm', RED)
        self.gui_gameover.text = "Game Over"

        self.gui_new_game = TextObject(self.gui_font, (self.width // 2, self.height // 2), 'm', WHITE)
        self.gui_new_game.text = "N für neues Spiel"

        # Spielelemente
        self.player = None
        self.enemies = []
        self.rockets = []
        self.bombs = []

    def new_game(self):
        self.gameover = False
        self.wait_for_new_game = False
        self.level = 0
        self.score = 0
        self.players = 3
        self.new_player()
        self.new_level()

    def new_player(self):
        if self.players > 0:
            self.players -= 1
            self.player = Player(x=self.width // 2, y=self.height - 80, power=5, img_name="playership1_blue.png")

    def new_level(self):
        self.level += 1
        # Es wird ein bestehender Player verwendet
        # Alle Bomben und Raketen löschen
        self.bombs.clear()
        self.rockets.clear()
        # Neue Gegner
        self.enemies.clear()
        for i in range(3 + 2 * self.level):
            self.enemies.append(Enemy(x=50 + 50 * i, y=50, power=self.level, img_name="enemyred3.png"))
        if self.level % 2:
            self.music.choose("CheerfulAnnoyance.ogg")
        else:
            self.music.choose("WackyWaiting.ogg")

    def all_objects(self):
        if self.player:
            all = [self.player]
        else:
            all = []
        all += self.enemies + self.bombs + self.rockets
        return all

    def handle_event(self, event):
        if event.type == pg.KEYDOWN:
            if self.wait_for_new_game and event.key == pg.K_n:
                self.wait_for_new_game = False
                self.new_game()
            else:
                if event.key == K_SPACE and not self.gameover:
                    rocket = self.player.new_rocket()
                    if rocket:
                        self.laser_sound.play()
                        self.rockets.append(rocket)

        for game_object in self.all_objects():
            game_object.on_event(event)

    def handle_keys(self, keys):
        if self.wait_for_new_game:
            return
        self.player.direction = (0, 0)
        if keys[pg.K_RIGHT] and not keys[pg.K_LEFT]:
            self.player.direction.x = 1
        elif keys[pg.K_LEFT] and not keys[pg.K_RIGHT]:
            self.player.direction.x = -1
        if keys[pg.K_UP] and not keys[pg.K_DOWN]:
            self.player.direction.y = -1
        elif keys[pg.K_DOWN] and not keys[pg.K_UP]:
            self.player.direction.y = 1

    def update(self):
        self.gui_level.text = f"Level {self.level}"
        self.gui_players.value = self.players
        self.gui_points.text = f"{self.score}"

        self.gui_points.visible = (not self.wait_for_new_game) or self.gameover
        self.gui_player_health.visible = not self.wait_for_new_game
        self.gui_new_game.visible = self.wait_for_new_game
        self.gui_level.visible = self.level > 0
        self.gui_gameover.visible = self.gameover

        if self.wait_for_new_game:
            return

        for obj in self.all_objects():
            obj.update()

        for enemy in self.enemies:
            # Kollision Gegner und Spieler
            if enemy.collision_with(self.player):
                self.player.destroy()
                enemy.destroy()
            # Gegner können Bomben abwerfen
            bombs = enemy.new_bombs()
            for bomb in bombs:
                if bomb:
                    self.bombs.append(bomb)

        for rocket in self.rockets:
            # Kollision Rakete und Bombe
            for bomb in self.bombs:
                if rocket.collision_with(bomb):
                    rocket.destroy()
                    bomb.destroy()
                    break
            # Kollision Rakete und Gegner
            for enemy in self.enemies:
                if rocket.collision_with(enemy):
                    rocket.destroy()
                    enemy.hit()
                    if enemy.destroyed:
                        if enemy.is_boss:
                            self.score += 5
                            self.new_level()
                        else:
                            self.score += 1
                            if len(self.enemies) == 1:
                                # einen Boss erzeugen
                                boss = Enemy.as_boss(x=self.width // 2, y=50, width=self.level * 100,
                                                     height=self.level * 50,
                                                     speed=self.level * 2, power=10)
                                self.enemies.append(boss)

        for bomb in self.bombs:
            # Kollision Bombe mit Spieler
            if bomb.collision_with(self.player):
                bomb.destroy()
                self.player.hit()

        # Zerstörte Objekte entfernen
        self.enemies = [enemy for enemy in self.enemies if not enemy.destroyed]
        self.bombs = [bomb for bomb in self.bombs if not bomb.destroyed]
        self.rockets = [rocket for rocket in self.rockets if not rocket.destroyed]

        if len(self.enemies) == 0:
            self.new_level()

        # Anzeige des Player - Zustands
        self.gui_player_health.value = self.player.get_health()

        if self.player.destroyed:
            if self.players > 0:
                # Es sind noch Spieler in der Reserve
                self.new_player()
            else:
                # Das Spiel ist beendet
                print("Game Over")
                self.music.choose("GameOver.ogg")
                self.gameover = True
                self.wait_for_new_game = True

    def draw(self):
        super().draw()
        self.gui_level.draw(self.screen)
        self.gui_players.draw(self.screen)
        self.gui_points.draw(self.screen)
        self.gui_new_game.draw(self.screen)
        self.gui_gameover.draw(self.screen)
        self.gui_player_health.draw(self.screen)

        if self.wait_for_new_game:
            return

        pg.sprite.RenderPlain(self.all_objects()).draw(self.screen)
