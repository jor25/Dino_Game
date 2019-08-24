# Use this site for online editing
# https://repl.it/languages/pygame

# 8/23/19 Wanted to make a game - used the google dinosaur

import pygame

pygame.init()

screen_width = 800
screen_height = 500
win = pygame.display.set_mode((screen_width, screen_height))

walk_right = [pygame.image.load('R_base.png'), pygame.image.load('R2_base.png')]
walk_left = [pygame.image.load('L_base.png'), pygame.image.load('L2_base.png')]
bg = pygame.image.load('bg1.png')
dino = pygame.image.load('base.png')
dinoL = pygame.image.load('baseL.png')
clock = pygame.time.Clock()


class player(object):
    def __init__(self, x, y, w, h):
        self.x = x  # Location
        self.y = y  # Location
        self.w = w  # character width
        self.h = h  # Character height
        self.vel = 10

        self.jumping = False
        self.jump_height = 10
        self.left = False
        self.right = False
        self.face_LR = True  # True = Right, False = Left
        self.walk_count = 0

    def draw_char(self, win):
        if self.walk_count + 1 >= 30:
            self.walk_count = 0

        if self.left:
            win.blit(walk_left[self.walk_count % 2], (self.x, self.y))
            self.walk_count += 1
        elif self.right:
            win.blit(walk_right[self.walk_count % 2], (self.x, self.y))
            self.walk_count += 1
        else:
            if self.face_LR:
                win.blit(dino, (self.x, self.y))
            else:
                win.blit(dinoL, (self.x, self.y))


def draw_window(Dino):
    win.blit(bg, (0, 0))
    Dino.draw_char(win)
    pygame.display.update()


if __name__ == "__main__":
    DINO = player(50, 425, 40, 60)

    run = True
    while run:
        clock.tick(30)  # Fps

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and DINO.x > DINO.vel:
            DINO.x -= DINO.vel
            DINO.left = True
            DINO.right = False
            DINO.face_LR = False
        elif keys[pygame.K_RIGHT] and DINO.x < screen_width - (DINO.w + DINO.vel):
            DINO.x += DINO.vel
            DINO.right = True
            DINO.left = False
            DINO.face_LR = True
        else:
            DINO.right = False
            DINO.left = False
            DINO.walk_count = 0

        if not (DINO.jumping):
            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                DINO.jumping = True
                DINO.right = False
                DINO.left = False
                DINO.walk_count = 0
        else:
            if DINO.jump_height >= -10:
                gravity = 1
                if DINO.jump_height < 0:
                    gravity = -1
                DINO.y -= (DINO.jump_height ** 2) / 2 * gravity
                DINO.jump_height -= 1
            else:
                DINO.jumping = False
                DINO.jump_height = 10

        draw_window(DINO)

pygame.quit()
