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
        
        level_select = input('What level do you want? (Answer 1-5): ')
        pg.display.set_caption('Geo-Dash')
        self.clock = pg.time.Clock()
        pg.mouse.set_cursor(*pg.cursors.diamond)

        if level_select == '1':
            self.logic = Logic(LEVELONE, SPEEDONE, SIZEONE, MUSICONE)
            pg.display.set_caption('Geo-Dash - Level 1')
            
        if level_select == '2':
            self.logic = Logic(LEVELTWO, SPEEDTWO, SIZETWO, MUSICTWO)
            pg.display.set_caption('Geo-Dash - Level 2')

        if level_select == '3':
            self.logic = Logic(LEVELTHREE, SPEEDTHREE, SIZETHREE, MUSICTHREE)
            pg.display.set_caption('Geo-Dash - Level 3')

        if level_select == '4':
            self.logic = Logic(LEVELFOUR, SPEEDFOUR, SIZEFOUR, MUSICFOUR)
            pg.display.set_caption('Geo-Dash - Level 4')

        if level_select == '5':
            self.logic = Logic(LEVELFIVE, SPEEDFIVE, SIZEFIVE, MUSICFIVE)
            pg.display.set_caption('Geo-Dash - Level 5')
    
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
