# Creating a new file for the enemy class for code clean up
# 3-17-20
from configs import *
import pygame

class enemy(object):

    def __init__(self, x, y, w, h, end, enemy_sprite, lmh, species, id):
        self.init_coord = (x, y, w, h)  # Initial coordinates
        self.id = id
        self.x = x  # x coordinate
        self.y = y  # y coordinate
        self.w = w  # Character width
        self.h = h  # Character height
        self.end = end  # Point to turn around
        self.path = [self.x, self.end]
        self.vel = 5
        self.direction = -1
        self.walk_count = 0
        self.hitbox = (self.x, self.y, self.w, self.h)  # x, y, w, and h
        self.took_dmg = False
        self.health = 1
        self.alive = True
        self.enemy_sprite = enemy_sprite
        self.got_jumped = False
        self.low_mid_high = lmh
        self.species = species

    def draw(self, win):
        #self.move()
        if self.alive:                              # Draw enemy if alive
            '''
            txt_surf, txt_rect = self.display_msg(str(self.id))
            win.blit(txt_surf, txt_rect)
            '''
            if self.walk_count + 1 >= 30:
                self.walk_count = 0

            if self.vel < 0:    # moving left
                win.blit(pygame.transform.flip(pygame.transform.scale(
                    self.enemy_sprite[self.walk_count % len(self.enemy_sprite)], (self.w, self.h)),
                    True, False), (self.x, self.y))
                self.walk_count += 1

            else:
                win.blit(pygame.transform.scale(
                    self.enemy_sprite[self.walk_count % len(self.enemy_sprite)], (self.w, self.h)),
                    (self.x, self.y))
                self.walk_count += 1

            if self.took_dmg:   # If got hit
                txt_surf, txt_rect = self.display_msg("OUCH!")
                if self.walk_count > 20:        # Wait 20 frames before turning off flag
                    self.took_dmg = False       # Turn off the damage flag
                win.blit(txt_surf, txt_rect)

            if SHOW_BOXES:
                pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)  # Draw hit box

    def move(self):                                     # Auto path for enemy to go on
        if self.vel > 0: # Go left
            if self.x - self.vel > self.path[1]:    # If enemy hasn't reached path end yet
                self.x -= self.vel                  # Continue left
                self.hitbox = (self.x, self.y, self.w, self.h)
            else:
                if self.alive:
                    self.alive = False                  # Make a bird disappear

    def take_dmg(self):
        self.took_dmg = True
        if self.health > 0:     # Not Dead
            self.health -= 1
        else:
            self.alive = False  # It Dead.

    def display_msg(self, text):
        output_txt = pygame.font.SysFont('freesansbold.ttf', 20, True)
        txt_surf = output_txt.render(text, False, (0,0,0))
        txt_rect = txt_surf.get_rect()
        txt_rect.center = (self.x + 10, self.y - 30)

        return txt_surf, txt_rect