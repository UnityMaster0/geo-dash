import sys
import time

import pygame as pg

from worlddata import *
from logic import Logic

FPS = 60

class gameContoller:

    def __init__(self):

        pg.init()
        self.screen = pg.display.set_mode((1680, 1080))
        pg.display.set_caption('Geo-Dash')
        self.clock = pg.time.Clock()
        pg.mouse.set_cursor(*pg.cursors.diamond)
        self.logic = Logic()

    # Runs the game
    def run(self):
        while True:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT or pg.key.get_pressed()[pg.K_ESCAPE]:
                    pg.quit()
                    sys.exit()
                     
            self.screen.fill('blue')
            self.logic.run()
            pg.display.update()

#Starts game loop
if __name__ == '__main__':
    game = gameContoller()
    game.run()