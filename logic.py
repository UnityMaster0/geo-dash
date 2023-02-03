import os, sys
from random import randint

import pygame as pg
from worlddata import *

class Player(pg.sprite.Sprite):

    def __init__(self, pos, spikes, blocks, fake_blocks, bouncers, fly_portals, finish, invert_portals, gravity, *groups):
        super().__init__(*groups)
        self.image = pg.image.load('.//Resources/image.png')
        self.image = pg.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(topleft=pos)

        self.direction = pg.math.Vector2()
        self.gravity_force = gravity
        self.jump_force = 0
        self.mode = 'normal'
        self.mode_pause = False
        self.dead = False

        self.blocks = blocks
        self.fake_blocks = fake_blocks
        self.spikes = spikes
        self.bouncers = bouncers
        self.fly_portals = fly_portals
        self.finish = finish
        self.invert_portals = invert_portals

    def change_mode(self):
        
        if pg.sprite.spritecollideany(self, self.invert_portals) and self.mode == 'normal' and not self.mode_flag:
            
            self.mode = 'normal-invert'
            self.mode_flag = True
            self.mode_pause = True

        if pg.sprite.spritecollideany(self, self.invert_portals) and self.mode == 'normal-invert' and not self.mode_flag:
            
            self.mode = 'normal'
            self.mode_flag = True
            self.mode_pause = True

        if pg.sprite.spritecollideany(self, self.invert_portals) and self.mode == 'fly' and not self.mode_flag:
            self.mode = 'fly-invert'
            self.mode_flag = True

        if pg.sprite.spritecollideany(self, self.invert_portals) and self.mode == 'fly-invert' and not self.mode_flag:
            self.mode = 'fly'
            self.mode_flag = True


        if pg.sprite.spritecollideany(self, self.fly_portals) and self.mode == 'normal' and not self.mode_flag:
            self.mode = 'fly'
            self.image = pg.image.load('.//Resources/fly.png').convert_alpha()
            self.mode_flag = True

        if pg.sprite.spritecollideany(self, self.fly_portals) and self.mode == 'normal-invert' and not self.mode_flag:
            self.mode = 'fly-invert'
            self.image = pg.image.load('.//Resources/fly_invert.png').convert_alpha()
            self.mode_flag = True

        if pg.sprite.spritecollideany(self, self.fly_portals) and self.mode == 'fly' and not self.mode_flag:
            self.mode = 'normal'
            self.image = pg.image.load('.//Resources/image.png').convert_alpha()
            self.image = pg.transform.scale(self.image, (64, 64))
            self.mode_flag = True

        if pg.sprite.spritecollideany(self, self.fly_portals) and self.mode == 'fly-invert' and not self.mode_flag:
            self.mode = 'normal-invert'
            self.image = pg.image.load('.//Resources/image.png').convert_alpha()
            self.image = pg.transform.scale(self.image, (64, 64))
            self.mode_flag = True

        if not pg.sprite.spritecollideany(self, self.fly_portals) and not pg.sprite.spritecollideany(self, self.invert_portals):
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

        if pg.sprite.spritecollideany(self, self.fake_blocks):
            self.kill()
            self.dead = True
                    
    def floor_set_invert(self):
        self.pass_check = -1000
        for block in self.fake_blocks:
            if block.rect.x >= 0 and block.rect.x <= 114:
                if block.rect.y <= self.pass_check:
                    pass
                else:
                    self.floor = block.rect.y + 78
                    self.pass_check = block.rect.y
                    
        if pg.sprite.spritecollideany(self, self.blocks):
            self.kill()
            self.dead = True

    def bounce(self):
        if pg.sprite.spritecollideany(self, self.bouncers) and pg.key.get_pressed()[pg.K_SPACE]:
            self.jump_force = -30
            
    def bounce_invert(self):
        if pg.sprite.spritecollideany(self, self.bouncers) and pg.key.get_pressed()[pg.K_SPACE]:
            self.jump_force = 30

    def gravity(self):

        if self.rect.y <= self.floor:
            self.direction.y = self.gravity_force

        if self.rect.y > self.floor + 30 and self.mode_pause == False:
            self.kill()
            self.dead = True

        if self.rect.y > self.floor:
            self.rect.y = self.floor 

        self.mode_pause = False  

    def gravity_invert(self):

        if self.rect.y >= self.floor:
            self.direction.y = -self.gravity_force

        if self.rect.y < self.floor - 30 and self.mode_pause == False:
            self.kill()
            self.dead = True

        if self.rect.y < self.floor:
            self.rect.y = self.floor

        self.mode_pause = False

    def jump(self):

        if pg.key.get_pressed()[pg.K_SPACE] and self.rect.y == self.floor:
            self.jump_force = -30
        elif self.rect.y < self.floor:
            self.jump_force += 0.5

    def jump_invert(self):

        if pg.key.get_pressed()[pg.K_SPACE] and self.rect.y == self.floor:
            self.jump_force = 30
        elif self.rect.y > self.floor:
            self.jump_force -= 0.5

    def flying(self):

        self.direction.y = self.gravity_force

        if pg.key.get_pressed()[pg.K_SPACE]:
            self.jump_force = -20
        
        self.jump_force += 0.3
        
        if pg.sprite.spritecollideany(self, self.blocks):
            self.kill()
            self.dead = True

    def flying_invert(self):

        self.direction.y = -self.gravity_force

        if pg.key.get_pressed()[pg.K_SPACE]:
            self.jump_force = 20
       
        self.jump_force -= 0.3
        
        if pg.sprite.spritecollideany(self, self.blocks):
            self.kill()
            self.dead = True

    def move(self):
        self.rect.y += self.direction.y + self.jump_force

    def death(self):      
        if pg.sprite.spritecollideany(self, self.spikes):
            self.kill()
            self.dead = True
            
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
        if self.mode == 'normal-invert':
            self.floor_set_invert()
            self.bounce_invert()
            self.gravity_invert()
            self.jump_invert()
        if self.mode == 'fly-invert':
            self.flying_invert()
        self.move()
        self.death()
        self.end()

class Block(pg.sprite.Sprite):

    def __init__(self, pos, speed, *groups):
        super().__init__(*groups)
        self.image = pg.image.load('.//Resources/block.svg').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

        self.speed = -speed

    def scroll(self):
        self.rect.x += self.speed
        if self.rect.x <= -64:
            self.kill()

    def update(self):
        self.scroll()


class Spike(pg.sprite.Sprite):

    def __init__(self, pos, type, speed, *groups):
        super().__init__(*groups)
        self.image = pg.image.load('.//Resources/spike.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.image = pg.transform.scale(self.image, (64,42))
        
        if type == 'normal':
            pass
        if type == 'invert':
            self.image = pg.transform.rotate(self.image, 180)

        self.speed = -speed

    def scroll(self):
        self.rect.x += self.speed
        if self.rect.x <= -64:
            self.kill()

    def update(self):
        self.scroll()
        
class Orb(pg.sprite.Sprite):

    def __init__(self, pos, type, speed, *groups):
        super().__init__(*groups)
        if type == 'portal':
            self.image = pg.image.load('.//Resources/portal.png').convert_alpha()
        elif type == 'bouncer':
            self.image = pg.image.load('.//Resources/bouncer.png').convert_alpha()
        elif type == 'finish':
            self.image = pg.image.load('.//Resources/finish.png').convert_alpha()
        elif type == 'invert':
            self.image = pg.image.load('.//Resources/invert.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

        self.speed = -speed

    def scroll(self):
        self.rect.x += self.speed
        if self.rect.x <= -64:
            self.kill() 

    def update(self):
        self.scroll()

class Button(pg.sprite.Sprite):

    def __init__(self, pos, type, *groups):
        super().__init__(*groups)
        if type == 'portal':
            self.image = pg.image.load('.//Resources/portal.png').convert_alpha()
        elif type == 'bouncer':
            self.image = pg.image.load('.//Resources/bouncer.png').convert_alpha()
        elif type == 'finish':
            self.image = pg.image.load('.//Resources/finish.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

class Start:

    def __init__(self):

        self.buttons = pg.sprite.Group()

        self.choice_made = False

        Button((50,50), 'portal', self.buttons)
        Button((200,50), 'bouncer', self.buttons)
        Button((350,50), 'finish', self.buttons)

    def select(self):

        pos = pg.mouse.get_pos()
        pressed = pg.mouse.get_pressed()

        if pos >= (50, 114) and pos <= (114, 50) and pressed == (True, False, False):
            self.level = LEVELONE
            self.size = SIZEONE
            self.speed = SPEEDONE
            self.music = MUSICONE
            self.gravity = GRAVITYONE
            self.choice_made = True

        if pos >= (200, 114) and pos <= (264, 50) and pressed == (True, False, False):
            self.level = LEVELTWO
            self.size = SIZETWO
            self.speed = SPEEDTWO
            self.music = MUSICTWO
            self.gravity = GRAVITYTWO
            self.choice_made = True

        if pos >= (350, 114) and pos <= (414, 50) and pressed == (True, False, False):
            self.level = LEVELTHREE
            self.size = SIZETHREE
            self.speed = SPEEDTHREE
            self.music = MUSICTHREE
            self.gravity = GRAVITYTHREE
            self.choice_made = True

class Logic:

    def __init__(self):

        self.display_surface = pg.display.get_surface()
        # Creates sprite groups
        self.players = pg.sprite.Group()
        self.blocks = pg.sprite.Group()
        self.fake_blocks = pg.sprite.Group()
        self.spikes = pg.sprite.Group()
        self.bouncers = pg.sprite.Group()
        self.fly_portals = pg.sprite.Group()
        self.finish_portals = pg.sprite.Group()
        self.invert_portals = pg.sprite.Group()

        self.started = False
        self.start = Start()

    def makeSprites(self):
        self.player = Player((50, 576), self.spikes, self.blocks, self.fake_blocks, self.bouncers, self.fly_portals, self.finish_portals, self.invert_portals, self.start.gravity, self.players) 
        for self.row_index, row in enumerate(self.start.level):
            for self.col_index, col in enumerate(row):
                x = self.col_index * self.start.size
                y = self.row_index * self.start.size
                if col == 'x':
                    Block((x, y), self.start.speed, [self.blocks])
                if col == 'c':
                    Block((x, y), self.start.speed, [self.fake_blocks])
                if col == 's':
                    Spike((x, (y + 24)), 'normal', self.start.speed, [self.spikes])
                if col == 'z':
                    Spike((x, y), 'invert', self.start.speed, [self.spikes])
                if col == 'b':
                    Orb((x, y), 'bouncer', self.start.speed, [self.bouncers])
                if col == 'p':
                    Orb((x, y), 'portal', self.start.speed, [self.fly_portals])
                if col == 'f':
                    Orb((x, y), 'finish', self.start.speed, [self.finish_portals])
                if col == 'i':
                    Orb((x, y), 'invert', self.start.speed, [self.invert_portals])

    def restart(self):
        if self.player.dead == True:
            
            self.players.empty()
            self.blocks.empty()
            self.fake_blocks.empty()
            self.spikes.empty()
            self.bouncers.empty()
            self.fly_portals.empty()
            self.finish_portals.empty()
            self.invert_portals.empty()
            self.finish_portals.empty()
            self.invert_portals.empty()

            self.makeSprites()

            pg.mixer.init()
            pg.mixer.music.load(self.start.music)
            pg.mixer.music.set_volume(0.5)
            pg.mixer.music.play()

            self.player.dead = False

    def change_level(self):

        if pg.key.get_pressed()[pg.K_r]:
            self.start.choice_made = False
            self.started = False

            self.players.empty()
            self.blocks.empty()
            self.fake_blocks.empty()
            self.spikes.empty()
            self.bouncers.empty()
            self.fly_portals.empty()
            self.finish_portals.empty()
            self.invert_portals.empty()
            self.finish_portals.empty()
            self.invert_portals.empty()

            pg.mixer.music.stop()

    # Runs all game functions
    def run(self):
        if self.start.choice_made == False:
            self.start.select()
            self.start.buttons.draw(self.display_surface)

        if self.start.choice_made == True:
            
            if self.started == False:
                self.makeSprites()
                pg.mixer.init()
                pg.mixer.music.load(self.start.music)
                pg.mixer.music.set_volume(0.5)
                pg.mixer.music.play()
                self.started = True

            self.players.update()
            self.blocks.update()
            self.fake_blocks.update()
            self.spikes.update()
            self.bouncers.update()
            self.fly_portals.update()
            self.finish_portals.update()
            self.invert_portals.update()
            self.restart()
            self.change_level()
            self.players.draw(self.display_surface)
            self.blocks.draw(self.display_surface)
            self.fake_blocks.draw(self.display_surface)
            self.spikes.draw(self.display_surface)
            self.bouncers.draw(self.display_surface)
            self.fly_portals.draw(self.display_surface)
            self.finish_portals.draw(self.display_surface)
            self.invert_portals.draw(self.display_surface)
