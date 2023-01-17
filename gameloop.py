import sys
import time

import pygame as pg

from logic import Logic

class gameContoller:

    def __init__(self):
        
        pg.init()
        self.screen = pg.display.set_mode((1680, 1080))
        pg.display.set_caption('ShootnRun')
        self.clock = pg.time.Clock()
        pg.mouse.set_cursor(*pg.cursors.diamond)
        self.logic = Logic()

        self.fps = 60

    # Runs the game
    def run(self):
        global end_time
        while True:
            self.clock.tick(self.fps)
            for event in pg.event.get():
                if event.type == pg.QUIT or pg.key.get_pressed()[pg.K_ESCAPE]:
                    pg.quit()
                    sys.exit()
                     
            self.screen.fill('blue')
            self.logic.run()
            end_time = time.time()
            pg.display.update()

#Starts game loop
if __name__ == '__main__':
    game = gameContoller()
    game.run()
