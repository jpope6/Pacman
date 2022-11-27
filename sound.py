import pygame as pg
import time


class Sound:
    def __init__(self):
        pg.mixer.init()
        pg.mixer.music.set_volume(0.1)

    def play_startup(self):
        pg.mixer.music.load("./assets/sounds/startup.wav")
        pg.mixer.music.play(0, 0.0)

    def stop_sound(self):
        pg.mixer.music.stop()

    def play_dead(self):
        pg.mixer.music.load("./assets/sounds/pacman_dead.wav")
        pg.mixer.music.play(0, 0.0)

    def play_waka(self):
        pg.mixer.music.load("./assets/sounds/wakawaka.wav")
        pg.mixer.music.play(0, 0.0)

    def play_base(self):
        pg.mixer.music.load("./assets/sounds/back_to_base.wav")
        pg.mixer.music.play(0, 0.0)

    def play_faster(self):
        pg.mixer.music.load("./assets/sounds/faster_ghost_siren.wav")
        pg.mixer.music.play(0, 0.0)

    def play_fruit(self):
        pg.mixer.music.load("./assets/sounds/get_fruit.wav")
        pg.mixer.music.play(0, 0.0)

    def play_ghost_chase(self):
        pg.mixer.music.load("./assets/sounds/ghost_chase.wav")
        pg.mixer.music.play(1, 0.0)

    def play_ghost_eaten(self):
        pg.mixer.music.load("./assets/sounds/ghost_eaten.wav")
        pg.mixer.music.play(0, 0.0)

    def play_ghost_siren(self):
        pg.mixer.music.load("./assets/sounds/ghost_siren.wav")
        pg.mixer.music.play(0, 0.0)

    def play_highscore(self):
        pg.mixer.music.load("./assets/sounds/new_highscore.wav")
        pg.mixer.music.play(0, 0.0)

    def play_power_up(self):
        pg.mixer.music.load("./assets/sounds/power_up.wav")
        pg.mixer.music.play(2, 0.0)
