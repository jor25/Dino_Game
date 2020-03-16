# 3/15/20 Making new changes to the generic dino game.

# 8/29/19 Making the generic google dinosaur game
# Then going to use Machine learning to train a model to play the game
# Planning to use Deep Q Learning

# Resources:
# Image Color Manipulation: https://stackoverflow.com/questions/12251896/colorize-image-while-preserving-transparency-with-pil
# Pil to Pygame images: https://stackoverflow.com/questions/25202092/pil-and-pygame-image
import pygame
import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import user_active as UA
import collect_states as CS

from PIL import Image
from PIL.ImageColor import getcolor, getrgb
from PIL.ImageOps import grayscale

# Initialize the game variable
pygame.init()

G_screen_width = 800
G_screen_height = 500

# Global Config Variables - load into different file later
# Viewing variable: True if I want to see the game in action
VIEW_TRAINING = True

# Activate Human Player:
HUMAN = True

# Test Neural Net:
NEURAL_PLAYER = not HUMAN

# Game fps
FPS = 100

nn = CS.Collection()


# Borrowed from stack
def image_tint(src, tint='#ffffff'):
    src = Image.open(src)

    tr, tg, tb = getrgb(tint)
    tl = getcolor(tint, "L")  # tint color's overall luminosity
    if not tl: tl = 1  # avoid division by zero
    tl = float(tl)  # compute luminosity preserving tint factors
    sr, sg, sb = map(lambda tv: tv/tl, (tr, tg, tb))  # per component adjustments

    # create look-up tables to map luminosity to adjusted tint
    # (using floating-point math only to compute table)
    luts = (list(map(lambda lr: int(lr*sr + 0.5), range(256))) +
            list(map(lambda lg: int(lg*sg + 0.5), range(256))) +
            list(map(lambda lb: int(lb*sb + 0.5), range(256))))
    l = grayscale(src)  # 8-bit luminosity version of whole image
    if Image.getmodebands(src.mode) < 4:
        merge_args = (src.mode, (l, l, l))  # for RGB verion of grayscale
    else:  # include copy of src image's alpha layer
        a = Image.new("L", src.size)
        a.putdata(src.getdata(3))
        merge_args = (src.mode, (l, l, l, a))  # for RGBA verion of grayscale
        luts += range(256)  # for 1:1 mapping of copied alpha values

    return Image.merge(*merge_args).point(luts)


dino1_png = image_tint('images/R_base.png', '#33b5e5')      # Lets me tint my dinosaur
d1_mode = dino1_png.mode
d1_size = dino1_png.size
d1_data = dino1_png.tobytes()

dino2_png = image_tint('images/R2_base.png', '#33b5e5')
d2_mode = dino2_png.mode
d2_size = dino2_png.size
d2_data = dino2_png.tobytes()
walk_right = [pygame.image.fromstring(d1_data, d1_size, d1_mode), pygame.image.fromstring(d2_data, d1_size, d1_mode)]

#walk_right = [pygame.image.load('images/R_base.png'), pygame.image.load('images/R2_base.png')]
bird_sprite = [pygame.image.load('images/bird_L1.png'), pygame.image.load('images/bird_L2.png')]
cactus_sprite = [pygame.image.load('images/cactus_1.png')]

clock = pygame.time.Clock()




class game(object):
    def __init__(self, screen_width, screen_height, enemies):
        pygame.display.set_caption('Gen Dino Game')                                 # Game caption
        self.screen_width = screen_width                                            # Screen width
        self.screen_height = screen_height                                          # Screen height
        self.window = pygame.display.set_mode((screen_width, screen_height))        # Game window
        self.bg = pygame.image.load('images/bg3.png').convert_alpha()               # Background image
        self.crash = False                                                          # Collision
        self.player = player(200, 425, 45, 52)                                      # Summon player class
        self.enemies = enemies                                                      # Summon list of enemies
        self.max_enemies = 3
        self.score = 0                                                              # Game score
        self.speed = 10                                                             # Game speed that will increment
        self.got_points = False
        self.dodge_points = 0
        self.got_dodge_points = False
        self.got_walk_points = False


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

    # Display everything to the pygame window
    def draw(self, win, move):
        if self.walk_count + 1 >= 30:
            self.walk_count = 0

        txt_surf, txt_rect = self.display_msg(str(move))
        #if self.walk_count < 20:  # Wait 20 frames before turning off flag
        win.blit(txt_surf, txt_rect)

        if self.left:
            win.blit(pygame.transform.flip(
                (pygame.transform.scale(walk_right[self.walk_count % len(walk_right)], (self.w, self.h))),
                True, False), (self.x, self.y))

        elif self.right:
            win.blit(pygame.transform.scale(walk_right[self.walk_count % len(walk_right)], (self.w, self.h)), (self.x, self.y))

        else:
            if self.face_LR:
                win.blit(pygame.transform.scale(walk_right[self.walk_count % len(walk_right)], (self.w, self.h)), (self.x, self.y))

            else:
                win.blit(pygame.transform.flip(
                    (pygame.transform.scale(walk_right[self.walk_count % len(walk_right)], (self.w, self.h))),
                    True, False), (self.x, self.y))
        self.walk_count += 1

        self.hitbox = (self.x+2, self.y+2, self.w-3, self.h-3)      # This may be a bit redundant
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)  # Draw hit box
        pygame.draw.rect(win, (255, 165, 0), (self.hitbox[0] - 100, self.hitbox[1] - 100,
                                              self.hitbox[2] + 200, self.hitbox[3] + 200), 2)  # Draw yellow sensory box
        pygame.draw.rect(win, (255, 255, 0), (self.hitbox[0] - 200, self.hitbox[1] - 200,
                                              self.hitbox[2] + 400, self.hitbox[3] + 400), 2)  # Draw orange sensory box
        pygame.draw.rect(win, (0, 255, 0), (self.hitbox[0] - 300, self.hitbox[1] - 300,
                                            self.hitbox[2] + 600, self.hitbox[3] + 600), 2)  # Draw green sensory box

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
    def do_move(self, move, game, walk_points):

        if np.array_equal(move, [1,0,0,0]) and not self.jumping:    # Dino will just stay where it is if not jumping
            self.x = self.x
            self.y = self.y
            #print("just walking here")
        elif np.array_equal(move, [1,0,0,0]) and self.jumping:      # Dino will follow jump physics
            self.do_jump()


        #'''
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

        #'''
        # It does this for EVERY frame in the loop, need to complete the jump before can move...
        if np.array_equal(move, [0,0,0,1]):
            if not self.jumping:
                self.jumping = True
                #self.do_jump()      # Jumping
            else:
                self.do_jump()      # Jumping

    # Displays the recent move
    def display_msg(self, text):
        output_txt = pygame.font.SysFont('freesansbold.ttf', 20, True)
        txt_surf = output_txt.render(text, False, (0,0,0))
        txt_rect = txt_surf.get_rect()
        txt_rect.center = (self.x + 10, self.y - 30)

        return txt_surf, txt_rect


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

    def __init__(self, x, y, w, h, end, enemy_sprite, lmh, species):
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
        self.got_jumped = False
        self.low_mid_high = lmh
        self.species = species

    def draw(self, win):
        #self.move()
        if self.alive:                              # Draw enemy if alive
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

            # This may be a bit redundant
            pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)  # Draw hit box

    def move(self):                                     # Auto path for enemy to go on
        if self.vel > 0: # Go left
            if self.x - self.vel > self.path[1]:    # If enemy hasn't reached path end yet
                self.x -= self.vel                  # Continue left
                #print("bird moving: ", self.x, ' ', self.y)
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


def draw_window(font, Game, Dino, pellets, Birds, mv_bg, record, final_move):
    Game.window.blit(Game.bg, (-mv_bg, 0))                       # Looping background
    Game.window.blit(Game.bg, (-mv_bg + Game.screen_width, 0))
    text_score = font.render("SCORE: {}".format(Game.score), True, (255, 0, 0))          # Display score on screen
    Game.window.blit(text_score, (Game.screen_width/20, Game.screen_height * .02))                    # Place the score
    text_lives = font.render("RECORD: {}".format(record), True, (255, 0, 0))          # Display score on screen
    Game.window.blit(text_lives, (Game.screen_width/20, Game.screen_height * .10))                    # Place the score
    Dino.draw(Game.window, final_move)          # Draws dino


    for bird in Birds:
        bird.draw(Game.window)          # Draws bird


    for pellet in pellets:  # Draws fireballs
        pellet.draw(Game.window)
    pygame.display.update()


def init_ai_game(player, game, enemy, test_ai, record):
    state_init1 = test_ai.get_state(game, player, enemy)
    action = [1,0,0,0]
    player.do_move(action, game, 0)
    state_init2 = test_ai.get_state(game, player, enemy)
    reward1 = test_ai.set_reward(player, game, game.crash, record)
    test_ai.remember(state_init1, action, reward1, state_init2, game.crash)
    test_ai.replay_new(test_ai.memory)


def get_record(score, record):
    if score >= record:
        return score
    else:
        return record


def plot_ai_results(array_counter, array_score):
    sb.set(color_codes=True)
    ax = sb.regplot(np.array([array_counter])[0], np.array([array_score])[0], color="b", x_jitter=.1, line_kws={'color':'green'})
    ax.set(xlabel='games', ylabel='score')
    plt.show()



if __name__ == "__main__":

    #test_ai = DQL_AI()  # The AI
    #test_ai = CS.Collection()

    font = pygame.font.SysFont('comicsansms', 40, True)     # Font to display on screen

    cact_w = [25, 35, 45]
    cact_h = [50, 70, 100]
    cact_y = [420, 400, 370]


    counter_games = 0
    game_scores = []        # for plotting later on
    game_num = []
    record = 0

    if HUMAN:
        states_list = []
        label_list = []

    while counter_games < 2000: #150
        #counter_games += 1
        BIRDS = []
        GAME = game(G_screen_width, G_screen_height, BIRDS)
        DINO = GAME.player #player(50, 425, 45, 52)



        pellets = []
        pellet_cooldown = 0
        moving_bg = 0


        enemy_cd = 0
        dist_high = 150
        dist_low = 100

        # Perform first move
        #init_ai_game(DINO, GAME, BIRDS, test_ai, record)

        walk_points = 0


        while not GAME.crash:

            if VIEW_TRAINING:
                clock.tick(FPS)  #30 # Fps # visible at fast on 100     # 500 good for training
            keys = pygame.key.get_pressed()


            #print("low: {}\nhigh: {}\nspeed: {}".format(dist_low, dist_high, GAME.speed))
            if len(BIRDS) < GAME.max_enemies and enemy_cd > random.randint(dist_low, dist_high):
                enemy_cd = 0
                index = random.randint(0, 3) % 3
                rand_lmh = random.randint(0, 2)
                #print("MAKE ENEMY")
                if index == 0:   # about 1/3 times we get a bird
                    BIRDS.append(enemy(G_screen_width, 440 - rand_lmh * 70, 46, 42, -42, bird_sprite, rand_lmh, "bird"))
                else:
                    BIRDS.append(enemy(G_screen_width, cact_y[index], cact_w[index], cact_h[index], -42, cactus_sprite, index, "cact"))

            enemy_cd += 1


            if pellet_cooldown > 0:
                pellet_cooldown += 1
            if pellet_cooldown > 3:
                pellet_cooldown = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    GAME.crash = True

            for BIRD in BIRDS:
                BIRD.vel = GAME.speed
                BIRD.move()
                if DINO.alive and BIRD.alive:
                    if DINO.y < BIRD.hitbox[1] + BIRD.hitbox[3]:
                        if DINO.y + DINO.h > BIRD.hitbox[1]:
                            # Within hitbox x coords
                            if DINO.x + DINO.w > BIRD.hitbox[0]:
                                if DINO.x < BIRD.hitbox[0] + BIRD.hitbox[2]:
                                    DINO.take_dmg()                             # When dino collides with bird

                elif BIRD.x + BIRD.w < DINO.x and not BIRD.got_jumped:  # Successfully dodged enemy
                    BIRD.got_jumped = True
                    GAME.score += 10

                    GAME.dodge_points += 1
                    GAME.got_dodge_points = True
                    #print("dodged")

                elif not BIRD.alive:                # When a bird dies, pop it from list and + score
                    #GAME.score += 10
                    GAME.got_points = True
                    if GAME.score % 100 == 0:
                        GAME.speed += 1
                        GAME.max_enemies += 1
                        if GAME.speed % 5 == 0 and dist_low != 10:      # if it reaches a mod of 10 then drop spacing between enemies
                            dist_low -= 10
                            dist_high -= 10

                    BIRDS.pop(BIRDS.index(BIRD))

                elif not DINO.alive:                # When dino out of lives
                    GAME.crash = True               # Died - game over - shut down



            walk_points += 1

            if walk_points % 50 == 0:
                #GAME.score += 1
                GAME.got_walk_points = True

            if HUMAN:
                final_move = UA.active_player(DINO)
                #print("{}\t{}".format(final_move, DINO.jumping))
                DINO.do_move(final_move, GAME, walk_points)                     # perform new move and get new state
                
                for BIRD in BIRDS:
                    if not np.array_equal(final_move, [1,0,0,0]) or walk_points % 100 == 0:
                        label, state = CS.get_state(GAME, DINO, BIRD, final_move)  # Making some states
                        label_list.append(label)
                        states_list.append(state)

            elif NEURAL_PLAYER:

                final_move = [1,0,0,0]
                try:
                    #for BIRD in BIRDS:
                    label, state = CS.get_state(GAME, DINO, BIRDS[0], final_move)  # Making some states
                    npstate = np.asarray(state)
                    restate = np.reshape(npstate, (-1,16))
                    prediction = nn.model.predict(restate) 
                    #print(prediction)
                    final_move = [0,0,0,0]
                    final_move[np.argmax(prediction[0])] = 1
                    print(final_move)
                    #final_move[random.randint(0,3)] = 1
                    DINO.do_move(final_move, GAME, walk_points)                     # perform new move and get new state
                except:
                    #print ("NO BIRDS")
                    DINO.do_move(final_move, GAME, walk_points)                     # perform new move and get new state

            else:
                print("NOPE - BAD AI")


            record = get_record(GAME.score, record)
            GAME.got_points = False         # Reset point indicator
            GAME.got_dodge_points = False
            GAME.got_walk_points = False

            moving_bg += GAME.speed                         # Increment background image
            if moving_bg > GAME.screen_width:               # Reset background image
                moving_bg = 0

            # Comment in when you want to see dino jumping
            if VIEW_TRAINING:
                draw_window(font, GAME, DINO, pellets, BIRDS, moving_bg, record, final_move)
            #print("dino.x = {}, dino.y ={}".format(DINO.x, DINO.y))
        if HUMAN:       # Save run to file and quit before new run if human.
            # New data
            #CS.write_data(states_list)
            #CS.write_data(label_list, "state_data/label")

            # add to data
            #CS.append_data(states_list)
            #CS.append_data(label_list, "state_data/label")
            print("QUIT NOOOWWW!!")

        counter_games += 1
        print('Game', counter_games, '      Score:', GAME.score, '      Record:', record,
              '      Dodge Points', GAME.dodge_points, '    Walk Points', walk_points)

        game_num.append(counter_games)
        game_scores.append(GAME.score)

    #test_ai.model.save_weights('test_weights1.hdf5')
    plot_ai_results(game_num, game_scores)

    # Quit when exiting loop
    #pygame.quit()
