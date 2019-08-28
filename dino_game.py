# Use this site for online editing
# https://repl.it/languages/pygame

# 8/23/19 Wanted to make a game - used the google dinosaur

import pygame

pygame.init()

screen_width = 800
screen_height = 500
score = 0

win = pygame.display.set_mode((screen_width, screen_height))

walk_right = [pygame.image.load('R_base.png'), pygame.image.load('R2_base.png')]
walk_left = [pygame.image.load('L_base.png'), pygame.image.load('L2_base.png')]
bg = pygame.image.load('bg1.png')
dino = pygame.image.load('base.png')
dinoL = pygame.image.load('baseL.png')
clock = pygame.time.Clock()


class player(object):
    def __init__(self, x, y, w, h):
        self.init_coord = (x, y, w, h)  # Initial coordinates
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
        self.hitbox = (self.x, self.y, self.w, self.h)  # x, y, w, and h
        self.took_dmg = False
        self.health = 3
        self.alive = True

    def draw(self, win):
        if self.walk_count + 1 >= 30:
            self.walk_count = 0

        if self.left:
            # pygame.transform.scale(walk_left[self.walk_count % 2], (self.w + 20, self.h + 20)) # for scaling
            win.blit(pygame.transform.scale(walk_left[self.walk_count % 2], (self.w, self.h)), (self.x, self.y))
            #win.blit(walk_left[self.walk_count % 2], (self.x, self.y))
            self.walk_count += 1
        elif self.right:
            win.blit(pygame.transform.scale(walk_right[self.walk_count % 2], (self.w, self.h)), (self.x, self.y))
            #win.blit(walk_right[self.walk_count % 2], (self.x, self.y))
            self.walk_count += 1
        else:
            if self.face_LR:
                #win.blit(dino, (self.x, self.y))
                win.blit(pygame.transform.scale(dino, (self.w, self.h)), (self.x, self.y))

            else:
                #win.blit(dinoL, (self.x, self.y))
                win.blit(pygame.transform.scale(dinoL, (self.w, self.h)), (self.x, self.y))

        self.hitbox = (self.x, self.y, self.w, self.h)      # This may be a bit redundant
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)  # Draw hit box

    def take_dmg(self):
        self.took_dmg = True
        # Reset jump height if mid jump
        if self.jumping:
            self.jumping = False
            self.jump_height = 10
        # Reset spawn location
        self.x = 50
        self.y = self.init_coord[1] - (self.h - self.init_coord[3]) #425
        if self.health > 0:     # Not Dead
            self.health -= 1
        else:
            self.alive = False  # It Dead.

        pygame.display.update()
        pause = 0
        while pause < 100:
            pygame.time.delay(10)
            pause += 1
            for event in pygame.event.get():     # If i try to do something while frozen
                if event.type == pygame.QUIT:
                    pause = 250
                    pygame.quit()

class projectile(object):
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
        self.hitbox = (self.x, self.y, self.w, self.h)  # x, y, w, and h
        self.took_dmg = False
        self.health = 3
        self.alive = True

    def draw(self, win):
        self.move()
        if self.alive:                              # Draw enemy if alive
            if self.walk_count + 1 >= 30:
                self.walk_count = 0

            if self.vel > 0:    # moving right
                win.blit(self.go_right[self.walk_count % 2], (self.x, self.y))
                self.walk_count += 1
            else:
                win.blit(self.go_left[self.walk_count % 2], (self.x, self.y))
                self.walk_count += 1

            if self.took_dmg:   # If got hit
                txt_surf, txt_rect = self.display_msg("OUCH!")
                if self.walk_count > 20:        # Wait 20 frames before turning off flag
                    self.took_dmg = False       # Turn off the damage flag
                win.blit(txt_surf, txt_rect)

            self.hitbox = (self.x, self.y, self.w, self.h)  # This may be a bit redundant
            pygame.draw.rect(win, (255, 0, 0), (self.x, self.y - 20, 30, 10))
            pygame.draw.rect(win, (0, 255, 0), (self.x, self.y - 20, 10 * self.health, 10))

            pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)  # Draw hit box

    def move(self):                                     # Auto path for enemy to go on
        if self.vel > 0:                                # Going to the right
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1                # Switch directions
                self.walk_count = 0
        else:                                           # Going to the left
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1                # Switch directions
                self.walk_count = 0

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


def draw_window(font, Dino, pellets, Bird, mv_bg):
    win.blit(bg, (-mv_bg, 0))                       # Looping background
    win.blit(bg, (-mv_bg + screen_width, 0))
    text_score = font.render("SCORE: {}".format(score), True, (255, 0, 0))          # Display score on screen
    win.blit(text_score, (screen_width/20, screen_height * .02))                    # Place the score
    text_lives = font.render("LIVES: {}".format(Dino.health), True, (255, 0, 0))          # Display score on screen
    win.blit(text_lives, (screen_width/20, screen_height * .10))                    # Place the score
    Dino.draw(win)          # Draws dino
    Bird.draw(win)          # Draws bird
    for pellet in pellets:  # Draws fireballs
        pellet.draw(win)
    pygame.display.update()


if __name__ == "__main__":
    font = pygame.font.SysFont('comicsansms', 40, True)     # Font to display on screen
    DINO = player(50, 425, 45, 52)
    BIRDS = []
    BIRD = enemy(150, 425, 46, 42, 500)
    pellets = []
    pellet_cooldown = 0
    moving_bg = 0

    for i in range(10):
        BIRDS.append(enemy(150 + i * 10, 425 - i * 10, 46, 42, 500 + i * 10))

    b_num = 0   # Bird number - goes up to 3?

    run = True
    while run:
        clock.tick(30)  # Fps

        if pellet_cooldown > 0:
            pellet_cooldown += 1
        if pellet_cooldown > 3:
            pellet_cooldown = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if DINO.alive and BIRDS[b_num].alive:
            if DINO.y < BIRDS[b_num].hitbox[1] + BIRDS[b_num].hitbox[3]:
                if DINO.y + DINO.h > BIRDS[b_num].hitbox[1]:
                    # Within hitbox x coords
                    if DINO.x + DINO.w > BIRDS[b_num].hitbox[0]:
                        if DINO.x < BIRDS[b_num].hitbox[0] + BIRDS[b_num].hitbox[2]:
                            # Bird takes damage
                            DINO.take_dmg()
                            score += 1
        elif not BIRDS[b_num].alive:
            if b_num < 9:
                DINO.y = int(DINO.y - (DINO.h * .1))
                DINO.w = int(DINO.w * 1.1)
                DINO.h = int(DINO.h * 1.1)
                b_num = (b_num + 1) % 10  # go to next bird?


        for pellet in pellets:
            if BIRDS[b_num].alive:
                # Within the hitbox y coords
                if pellet.y - pellet.radius < BIRDS[b_num].hitbox[1] + BIRDS[b_num].hitbox[3]:
                    if pellet.y + pellet.radius > BIRDS[b_num].hitbox[1]:
                        # Within hitbox x coords
                        if pellet.x + pellet.radius > BIRDS[b_num].hitbox[0]:
                            if pellet.x - pellet.radius < BIRDS[b_num].hitbox[0] + BIRDS[b_num].hitbox[2]:
                                # Bird takes damage
                                BIRDS[b_num].take_dmg()
                                score += 1
                                # Pellet removed from screen
                                pellets.pop(pellets.index(pellet))

            if pellet.x < screen_width and pellet.x > 0:
                pellet.x += pellet.vel
            else:
                pellets.pop(pellets.index(pellet))

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and pellet_cooldown == 0:
            if DINO.face_LR:  # Facing right
                facing = 1
            else:
                facing = -1
            if len(pellets) < 20:
                pellets.append(
                    projectile(round(DINO.x + DINO.w // 2), round(DINO.y + DINO.h // 2), 6, (255, 0, 0), facing))
            pellet_cooldown = 1

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

        if not DINO.jumping:
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

        moving_bg += 5                      # Increment background image
        if moving_bg > screen_width:        # Reset background image
            moving_bg = 0
        draw_window(font, DINO, pellets, BIRDS[b_num], moving_bg)

pygame.quit()
