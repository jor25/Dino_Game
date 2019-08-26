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


class fire_ball(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 20 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class enemy(object):
    go_right = [pygame.image.load('bird_R1.png'), pygame.image.load('bird_R2.png')]
    go_left = [pygame.image.load('bird_L1.png'), pygame.image.load('bird_L2.png')]

    def __init__(self, x, y, w, h, end):
        self.x = x  # x coordinate
        self.y = y  # y coordinate
        self.w = w  # Character width
        self.h = h  # Character height
        self.end = end  # Point to turn around
        self.path = [self.x, self.end]
        self.vel = 10

        self.walk_count = 0

    def draw(self, win):
        self.move()
        if self.walk_count + 1 >= 30:
            self.walk_count = 0

        if self.vel > 0:    # moving right
            win.blit(self.go_right[self.walk_count % 2], (self.x, self.y))
            self.walk_count += 1
        else:
            win.blit(self.go_left[self.walk_count % 2], (self.x, self.y))
            self.walk_count += 1


    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walk_count = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walk_count = 0


def draw_window(Dino, bullets, Bird):
    win.blit(bg, (0, 0))
    Dino.draw_char(win)  # Draws dino
    Bird.draw(win)
    for bullet in bullets:  # Draws fireballs
        bullet.draw(win)
    pygame.display.update()


if __name__ == "__main__":
    DINO = player(50, 425, 40, 60)
    BIRD = enemy(100, 425, 46, 42, 500)
    bullets = []

    run = True
    while run:
        clock.tick(30)  # Fps

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for bullet in bullets:
            if bullet.x < screen_width and bullet.x > 0:
                bullet.x += bullet.vel
            else:
                bullets.pop(bullets.index(bullet))

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            if DINO.face_LR:  # Facing right
                facing = 1
            else:
                facing = -1
            if len(bullets) < 20:
                bullets.append(
                    fire_ball(round(DINO.x + DINO.w // 2), round(DINO.y + DINO.h // 2), 6, (255, 0, 0), facing))

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
            if keys[pygame.K_UP]:
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

        draw_window(DINO, bullets, BIRD)

pygame.quit()