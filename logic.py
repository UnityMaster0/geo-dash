import os, sys
from random import randint

import pygame as pg

from worlddata import *


class Player(pg.sprite.Sprite):

    def __init__(self, pos, spikes, blocks, bouncers, portals, finish, *groups):
        super().__init__(*groups)
        self.image = pg.image.load('.//Resources/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

        self.direction = pg.math.Vector2()
        self.gravity_force = 15
        self.jump_force = 0
        self.mode = 'normal'

        self.blocks = blocks
        self.spikes = spikes
        self.bouncers = bouncers
        self.portals = portals
        self.finish = finish

    def change_mode(self):
        if pg.sprite.spritecollideany(self, self.portals) and self.mode == 'normal' and not self.mode_flag:
            self.mode = 'fly'
            self.image = pg.image.load('.//Resources/fly.png').convert_alpha()
            self.mode_flag = True

        if pg.sprite.spritecollideany(self, self.portals) and self.mode == 'fly' and not self.mode_flag:
            self.mode = 'normal'
            self.image = pg.image.load('.//Resources/player.png').convert_alpha()
            self.mode_flag = True

        if not pg.sprite.spritecollideany(self, self.portals):
            self.mode_flag = False
    
    def floor_set(self):
        self.pass_check = 1000
        for block in self.blocks:
            if block.rect.x >= 0 and block.rect.x <= 114:
                if block.rect.y >= self.pass_check:
                    pass
                else:
                    self.floor = block.rect.y - 78
                    self.pass_check = block.rect.y

    def bounce(self):
        if pg.sprite.spritecollideany(self, self.bouncers) and pg.key.get_pressed()[pg.K_SPACE]:
            self.jump_force = -30

    def gravity(self):

        if self.rect.y <= self.floor:
            self.direction.y = self.gravity_force

        if self.rect.y > self.floor:
            self.rect.y = self.floor

    def jump(self):

        if pg.key.get_pressed()[pg.K_SPACE] and self.rect.y == self.floor:
            self.jump_force = -30
        elif self.rect.y < self.floor:
            self.jump_force += 0.5

    def flying(self):

        self.direction.y = self.gravity_force

        if pg.key.get_pressed()[pg.K_SPACE]:
            self.jump_force = -20
        elif self.rect.y < self.floor:
            self.jump_force += 0.3
        
        if pg.sprite.spritecollideany(self, self.blocks):
            pg.quit()
            sys.exit()

    def move(self):
        self.rect.y += self.direction.y + self.jump_force

    def death(self):
        if pg.sprite.spritecollideany(self, self.spikes):
            pg.quit()
            sys.exit()
    
    def end(self):
        if pg.sprite.spritecollideany(self, self.finish):
            print('Level Completed!')
            pg.quit()
            sys.exit()

    # Updates the player sprite
    def update(self):
        self.change_mode()
        if self.mode == 'normal':
            self.floor_set()
            self.bounce()
            self.gravity()
            self.jump()
        if self.mode == 'fly':
            self.flying()
        self.move()
        self.death()
        self.end()

class Block(pg.sprite.Sprite):

    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pg.image.load('.//Resources/block.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

        self.speed = -5

    def scroll(self):
        self.rect.x += self.speed
        if self.rect.x <= -64:
            self.kill()

    def update(self):
        self.scroll()


class Spike(pg.sprite.Sprite):

    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pg.image.load('.//Resources/spike.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.image = pg.transform.scale(self.image, (64,42))

        self.speed = -5

    def scroll(self):
        self.rect.x += self.speed
        if self.rect.x <= -64:
            self.kill()

    def update(self):
        self.scroll()
        
class Bouncer(pg.sprite.Sprite):

    def __init__(self, pos, type, *groups):
        super().__init__(*groups)
        if type == 'portal':
            self.image = pg.image.load('.//Resources/portal.png').convert_alpha()
        elif type == 'bouncer':
            self.image = pg.image.load('.//Resources/bouncer.png').convert_alpha()
        elif type == 'finish':
            self.image = pg.image.load('.//Resources/finish.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

        self.speed = -5

    def scroll(self):
        self.rect.x += self.speed
        if self.rect.x <= -64:
            self.kill() 

    def update(self):
        self.scroll()

class Logic:

    def __init__(self):

        self.display_surface = pg.display.get_surface()
        # Creates sprite groups
        self.players = pg.sprite.Group()
        self.blocks = pg.sprite.Group()
        self.spikes = pg.sprite.Group()
        self.bouncers = pg.sprite.Group()
        self.portals = pg.sprite.Group()
        self.finish = pg.sprite.Group()

        self.makeSprites()

    def makeSprites(self):
        self.player = Player((50, 576), self.spikes, self.blocks, self.bouncers, self.portals, self.finish, self.players) 
        for self.row_index, row in enumerate(LEVELTWO):
            for self.col_index, col in enumerate(row):
                x = self.col_index * TILE
                y = self.row_index * TILE
                if col == 'x':
                    Block((x, y), [self.blocks])
                if col == 's':
                    Spike((x, (y + 24)), [self.spikes])
                if col == 'b':
                    Bouncer((x, y), 'bouncer', [self.bouncers])
                if col == 'p':
                    Bouncer((x, y), 'portal', [self.portals])
                if col == 'f':
                    Bouncer((x, y), 'finish', [self.finish])

    # Runs all game functions
    def run(self):
        self.players.update()
        self.blocks.update()
        self.spikes.update()
        self.bouncers.update()
        self.portals.update()
        self.finish.update()
        self.players.draw(self.display_surface)
        self.blocks.draw(self.display_surface)
        self.spikes.draw(self.display_surface)
        self.bouncers.draw(self.display_surface)
        self.portals.draw(self.display_surface)
        self.finish.draw(self.display_surface)