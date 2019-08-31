# Used this site for online pygame editing
# https://repl.it/languages/pygame

# 8/29/19 Making the generic google dinosaur game
# Then going to use Machine learning to train a model to play the game
# Planning to use Deep Q Learning

import pygame
import random

pygame.init()

G_screen_width = 800
G_screen_height = 500


walk_right = [pygame.image.load('R_base.png'), pygame.image.load('R2_base.png')]
#walk_left = [pygame.image.load('L_base.png'), pygame.image.load('L2_base.png')]

bird_sprite = [pygame.image.load('bird_L1.png'), pygame.image.load('bird_L2.png')]

cactus_sprite = [pygame.image.load('cactus_1.png')]


dino = pygame.image.load('base.png')
dinoL = pygame.image.load('baseL.png')

clock = pygame.time.Clock()





class game(object):
    def __init__(self, screen_width, screen_height, enemies):
        pygame.display.set_caption('Gen Dino Game')                                 # Game caption
        self.screen_width = screen_width                                            # Screen width
        self.screen_height = screen_height                                          # Screen height
        self.window = pygame.display.set_mode((screen_width, screen_height))        # Game window
        self.bg = pygame.image.load('bg1.png')                                      # Background image
        self.crash = False                                                          # Collision
        self.player = player(50, 425, 45, 52)                                       # Summon player class
        self.enemies = enemies                                                      # Summon list of enemies
        self.max_enemies = 3
        self.score = 0                                                              # Game score
        self.speed = 5                                                              # Game speed that will increment


class player(object):
    def __init__(self, x, y, w, h):
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


    def draw(self, win):
        if self.walk_count + 1 >= 30:
            self.walk_count = 0

        if self.left:
            win.blit(pygame.transform.flip(
                (pygame.transform.scale(walk_right[self.walk_count % 2], (self.w, self.h))),
                True, False), (self.x, self.y))

        elif self.right:
            win.blit(pygame.transform.scale(walk_right[self.walk_count % 2], (self.w, self.h)), (self.x, self.y))

        else:
            if self.face_LR:
                win.blit(pygame.transform.scale(walk_right[self.walk_count % 2], (self.w, self.h)), (self.x, self.y))

            else:
                win.blit(pygame.transform.flip(
                    (pygame.transform.scale(walk_right[self.walk_count % 2], (self.w, self.h))),
                    True, False), (self.x, self.y))
        self.walk_count += 1

        self.hitbox = (self.x+2, self.y+2, self.w-3, self.h-3)      # This may be a bit redundant
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
    #go_right = [pygame.image.load('bird_R1.png'), pygame.image.load('bird_R2.png')]
    #go_left = [pygame.image.load('bird_L1.png'), pygame.image.load('bird_L2.png')]

    def __init__(self, x, y, w, h, end, enemy_sprite):
        self.init_coord = (x, y, w, h)  # Initial coordinates
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

    def draw(self, win):
        self.move()
        if self.alive:                              # Draw enemy if alive
            if self.walk_count + 1 >= 30:
                self.walk_count = 0

            if self.vel < 0:    # moving left
                win.blit(pygame.transform.flip(pygame.transform.scale(self.enemy_sprite[self.walk_count % len(self.enemy_sprite)], (self.w, self.h)), True, False), (self.x, self.y))
                self.walk_count += 1
            else:
                win.blit(pygame.transform.scale(self.enemy_sprite[self.walk_count % len(self.enemy_sprite)], (self.w, self.h)), (self.x, self.y))
                self.walk_count += 1

            if self.took_dmg:   # If got hit
                txt_surf, txt_rect = self.display_msg("OUCH!")
                if self.walk_count > 20:        # Wait 20 frames before turning off flag
                    self.took_dmg = False       # Turn off the damage flag
                win.blit(txt_surf, txt_rect)

            self.hitbox = (self.x, self.y, self.w, self.h)  # This may be a bit redundant
            pygame.draw.rect(win, (255, 0, 0), (self.x, self.y - 20, 40, 10))
            pygame.draw.rect(win, (0, 255, 0), (self.x, self.y - 20, 40 * self.health, 10))

            pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)  # Draw hit box

    def move(self):                                     # Auto path for enemy to go on
        if self.vel > 0: # Go left
            if self.x - self.vel > self.path[1]:    # If enemy hasn't reached path end yet
                self.x -= self.vel                  # Continue left
            else:
                #
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


def draw_window(font, Game, Dino, pellets, Birds, mv_bg):
    Game.window.blit(Game.bg, (-mv_bg, 0))                       # Looping background
    Game.window.blit(Game.bg, (-mv_bg + Game.screen_width, 0))
    text_score = font.render("SCORE: {}".format(Game.score), True, (255, 0, 0))          # Display score on screen
    Game.window.blit(text_score, (Game.screen_width/20, Game.screen_height * .02))                    # Place the score
    text_lives = font.render("LIVES: {}".format(Dino.health), True, (255, 0, 0))          # Display score on screen
    Game.window.blit(text_lives, (Game.screen_width/20, Game.screen_height * .10))                    # Place the score
    Dino.draw(Game.window)          # Draws dino


    for bird in Birds:
        bird.draw(Game.window)          # Draws bird


    for pellet in pellets:  # Draws fireballs
        pellet.draw(Game.window)
    pygame.display.update()



if __name__ == "__main__":
    font = pygame.font.SysFont('comicsansms', 40, True)     # Font to display on screen

    BIRDS = []


    GAME = game(G_screen_width, G_screen_height, BIRDS)
    DINO = GAME.player #player(50, 425, 45, 52)

    cact_w = [25, 35, 45]
    cact_h = [50, 70, 100]
    cact_y = [420, 400, 370]

    pellets = []
    pellet_cooldown = 0
    moving_bg = 0



    while not GAME.crash:
        clock.tick(30)  # Fps
        keys = pygame.key.get_pressed()

        if len(BIRDS) < GAME.max_enemies:
            index = random.randint(0, 3) % 3
            if index == 0:   # about 1/3 times we get a bird
                BIRDS.append(enemy(G_screen_width + random.randint(200, 800), 440 - (random.randint(0, 2)) * 70, 46, 42, -42, bird_sprite))
            else:
                BIRDS.append(enemy(G_screen_width + random.randint(200, 800), cact_y[index], cact_w[index], cact_h[index], -42, cactus_sprite))

        if pellet_cooldown > 0:
            pellet_cooldown += 1
        if pellet_cooldown > 3:
            pellet_cooldown = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GAME.crash = True

        for BIRD in BIRDS:
            if DINO.alive and BIRD.alive:
                if DINO.y < BIRD.hitbox[1] + BIRD.hitbox[3]:
                    if DINO.y + DINO.h > BIRD.hitbox[1]:
                        # Within hitbox x coords
                        if DINO.x + DINO.w > BIRD.hitbox[0]:
                            if DINO.x < BIRD.hitbox[0] + BIRD.hitbox[2]:
                                DINO.take_dmg()                             # When dino collides with bird

            elif not BIRD.alive:                # When a bird dies, pop it from list and + score
                GAME.score += 100
                BIRDS.pop(BIRDS.index(BIRD))

            elif not DINO.alive:                # When dino out of lives
                GAME.crash = True               # Died - game over - shut down




        # Dino making moves here
        if keys[pygame.K_LEFT] and DINO.x > DINO.vel:       # Hit the left wall
            DINO.x -= DINO.vel
            DINO.left = True
            DINO.right = False
            DINO.face_LR = False
        elif keys[pygame.K_RIGHT] and DINO.x < GAME.screen_width - (DINO.w + DINO.vel):     # Hit the right wall
            DINO.x += DINO.vel
            DINO.right = True
            DINO.left = False
            DINO.face_LR = True
        else:                                                   # Standing Still
            DINO.right = False
            DINO.left = False


        if not DINO.jumping:
            if keys[pygame.K_UP]:
                DINO.jumping = True
                DINO.right = False
                DINO.left = False
                DINO.walk_count = 0
        else:                                       # Jump function
            if DINO.jump_height >= -10:
                gravity = 1
                if DINO.jump_height < 0:
                    gravity = -1
                DINO.y -= (DINO.jump_height ** 2) / 2 * gravity
                DINO.jump_height -= 1
            else:
                DINO.jumping = False
                DINO.jump_height = 10

        moving_bg += GAME.speed                         # Increment background image
        if moving_bg > GAME.screen_width:               # Reset background image
            moving_bg = 0
        draw_window(font, GAME, DINO, pellets, BIRDS, moving_bg)


    # Quit when exiting loop
    pygame.quit()
