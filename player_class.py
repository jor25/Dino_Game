# Creating new file for the player class to clean up code
# 3-17-20

# Resources:
# Image Tinting: https://stackoverflow.com/questions/12251896/colorize-image-while-preserving-transparency-with-pil
# Pil to Pygame images: https://stackoverflow.com/questions/25202092/pil-and-pygame-image
import pygame
import numpy as np
from PIL import Image
from PIL.ImageColor import getcolor, getrgb
from PIL.ImageOps import grayscale

class player(object):
    def __init__(self, x, y, w, h, id, color_code):
        self.id = id                                        # Player's Id number
        self.color = color_code                             # String of hex color codes
        self.init_coord = (x, y, w, h)                      # Initial coordinates
        self.x = x                                          # Location x cord
        self.y = y                                          # Location y cord
        self.w = w                                          # Player width
        self.h = h                                          # Player height
        self.vel = 10                                       # Player speed
        self.jumping = False
        self.jump_height = 10
        self.left = False
        self.right = False
        self.face_LR = True                                 # True = Right, False = Left
        self.walk_count = 0
        self.hitbox = (self.x, self.y, self.w, self.h)      # x, y, w, and h
        self.took_dmg = False
        self.health = 0
        self.alive = True
        self.my_sprites = self.make_my_sprites(['images/R_base.png', 'images/R2_base.png'], self.color)#'#00FF31')
        self.fitness = 0
        self.dodge_points = 0

    def make_my_sprites(self, sprite_images, color_tint):
        """
        Create custom colored sprites for specific characters
        :param sprite_images: List of Strings - Paths to different sprites in list format ['images/R_base.png', 'images/R2_base.png']
        :param color_tint: String - The color to tint those sprites in this format '#00FF31'
        :return: list of pygame sprite objects
        """
        my_sprites = []
        for image in sprite_images:
            my_png = self.image_tint(image, color_tint)
            png_mode = my_png.mode
            png_size = my_png.size
            png_data = my_png.tobytes()
            my_sprites.append(pygame.image.fromstring(png_data, png_size, png_mode).convert_alpha())        # Convert alpha makes it run faster?
        return my_sprites

    # Borrowed from stack - may make this a more general function...
    def image_tint(self, src, tint='#ffffff'):
        src = Image.open(src)

        tr, tg, tb = getrgb(tint)
        tl = getcolor(tint, "L")  # tint color's overall luminosity
        if not tl: tl = 1  # avoid division by zero
        tl = float(tl)  # compute luminosity preserving tint factors
        sr, sg, sb = map(lambda tv: tv / tl, (tr, tg, tb))  # per component adjustments

        # create look-up tables to map luminosity to adjusted tint
        # (using floating-point math only to compute table)
        luts = (list(map(lambda lr: int(lr * sr + 0.5), range(256))) +
                list(map(lambda lg: int(lg * sg + 0.5), range(256))) +
                list(map(lambda lb: int(lb * sb + 0.5), range(256))))
        l = grayscale(src)  # 8-bit luminosity version of whole image
        if Image.getmodebands(src.mode) < 4:
            merge_args = (src.mode, (l, l, l))  # for RGB verion of grayscale
        else:  # include copy of src image's alpha layer
            a = Image.new("L", src.size)
            a.putdata(src.getdata(3))
            merge_args = (src.mode, (l, l, l, a))  # for RGBA verion of grayscale
            luts += range(256)  # for 1:1 mapping of copied alpha values

        return Image.merge(*merge_args).point(luts)

    # Display everything to the pygame window
    def draw(self, win, move):
        if self.walk_count + 1 >= 30:
            self.walk_count = 0

        txt_surf, txt_rect = self.display_msg("{} {} {}".format(self.id, move, self.fitness))
        #if self.walk_count < 20:  # Wait 20 frames before turning off flag
        win.blit(txt_surf, txt_rect)

        if self.left:
            win.blit(pygame.transform.flip(
                (pygame.transform.scale(self.my_sprites[self.walk_count % len(self.my_sprites)], (self.w, self.h))),
                True, False), (self.x, self.y))

        elif self.right:
            win.blit(pygame.transform.scale(self.my_sprites[self.walk_count % len(self.my_sprites)], (self.w, self.h)), (self.x, self.y))

        else:
            if self.face_LR:
                win.blit(pygame.transform.scale(self.my_sprites[self.walk_count % len(self.my_sprites)], (self.w, self.h)), (self.x, self.y))

            else:
                win.blit(pygame.transform.flip(
                    (pygame.transform.scale(self.my_sprites[self.walk_count % len(self.my_sprites)], (self.w, self.h))),
                    True, False), (self.x, self.y))
        self.walk_count += 1

        self.hitbox = (self.x+2, self.y+2, self.w-3, self.h-3)      # This may be a bit redundant
        #'''
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)  # Draw hit box
        pygame.draw.rect(win, (255, 165, 0), (self.hitbox[0] - 50, self.hitbox[1] - 50,
                                              self.hitbox[2] + 100, self.hitbox[3] + 100), 2)  # Draw yellow sensory box
        pygame.draw.rect(win, (255, 255, 0), (self.hitbox[0] - 100, self.hitbox[1] - 100,
                                              self.hitbox[2] + 200, self.hitbox[3] + 200), 2)  # Draw orange sensory box
        '''
        pygame.draw.rect(win, (0, 255, 0), (self.hitbox[0] - 150, self.hitbox[1] - 150,
                                            self.hitbox[2] + 300, self.hitbox[3] + 300), 2)  # Draw green sensory box
        #'''

    # Don't really need this function of generic game
    def take_dmg(self):
        self.alive = False

    # Do a jump
    def do_jump(self):
        if self.jump_height >= -10:
            gravity = 1  # Means Going UP!

            if self.jump_height < 0:  # Means Going Down
                gravity = -1

            self.y -= (self.jump_height ** 2) / 2 * gravity
            # print(self.y)
            self.jump_height -= 1

        else:  # On the ground
            self.jumping = False
            self.jump_height = 10

    # Putting player moves in generic function to allow model to select
    def do_move(self, move, game, walk_points, state):
        self.fitness = game.dodge_points * 10
        '''
        self.fitness = walk_points
        #if np.array_equal(move, [0,0,0,1]):
        #    self.fitness -= 10
        if game.got_dodge_points:
            self.fitness += 10
        '''
        '''
        if self.alive == False:
            self.fitness -= 10

        if game.got_walk_points:        # got walk points
            self.fitness += 1
            #if np.array_equal(move, [0,0,0,1]) and 0 not in state[[2,3,4,5,6,7]]:     # Jumping with nothing in range 100
            #   self.fitness -= 5
        '''

        if np.array_equal(move, [1,0,0,0]) and not self.jumping:    # Dino will just stay where it is if not jumping
            self.x = self.x
            self.y = self.y

        elif np.array_equal(move, [1,0,0,0]) and self.jumping:      # Dino will follow jump physics
            self.do_jump()

        if np.array_equal(move, [0,1,0,0]):         # Move left
            if self.x > self.vel:                   # Within the left wall
                self.x -= self.vel
            self.left = True
            self.right = False
            if self.jumping:
                self.do_jump()

        if np.array_equal(move, [0,0,1,0]):                             # Move right
            if self.x < game.screen_width - (self.w + self.vel):        # Within the right wall
                self.x += self.vel
            self.right = True
            self.left = False
            if self.jumping:
                self.do_jump()

        # It does this for EVERY frame in the loop, need to complete the jump before can move...
        if np.array_equal(move, [0,0,0,1]):
            if not self.jumping:
                self.jumping = True
            else:
                self.do_jump()      # Jumping

    # Displays the recent move
    def display_msg(self, text):
        output_txt = pygame.font.SysFont('freesansbold.ttf', 20, True)
        txt_surf = output_txt.render(text, False, (0,0,0))
        txt_rect = txt_surf.get_rect()
        txt_rect.center = (self.x + 10, self.y - 30)

        return txt_surf, txt_rect