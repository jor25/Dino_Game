# 3/15/20 Making new changes to the generic dino game.

# 8/29/19 Making the generic google dinosaur game
# Then going to use Machine learning to train a model to play the game
# Planning to use Deep Q Learning


import pygame
import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import user_active as UA
import collect_states as CS

import player_class as plc
import enemy_class as enc

# Initialize the game variable
pygame.init()

G_screen_width = 800
G_screen_height = 500

# Global Config Variables - load into different file later
# Viewing variable: True if I want to see the game in action
VIEW_TRAINING = True

# Activate Human Player:
HUMAN = False

# Test Neural Net:
NEURAL_PLAYER = not HUMAN

# Game fps
FPS = 100

# Population size
POP_SIZE = 3    # Can't fully handle 10

nn = [CS.Collection() for i in range(POP_SIZE)]


clock = pygame.time.Clock()


class game(object):
    def __init__(self, screen_width, screen_height, enemies, num_players=1):
        pygame.display.set_caption('Gen Dino Game')                                 # Game caption
        self.screen_width = screen_width                                            # Screen width
        self.screen_height = screen_height                                          # Screen height
        self.window = pygame.display.set_mode((screen_width, screen_height))        # Game window
        self.bg = pygame.image.load('images/bg3.png').convert_alpha()               # Background image
        self.crash = False                                                          # Collision
        self.players = [plc.player(200, 425, 45, 52, i) for i in range(num_players)]                                      # Summon player class
        self.enemies = enemies                                                      # Summon list of enemies
        self.max_enemies = 3
        self.score = 0                                                              # Game score
        self.speed = 10                                                             # Game speed that will increment
        self.got_points = False
        self.dodge_points = 0
        self.got_dodge_points = False
        self.got_walk_points = False
        # Make the sprites game objects?
        self.bird_sprite = [pygame.image.load('images/bird_L1.png').convert_alpha(),
                            pygame.image.load('images/bird_L2.png').convert_alpha()]
        self.cactus_sprite = [pygame.image.load('images/cactus_1.png').convert_alpha()]

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


def draw_window(font, Game, Dinos, pellets, Birds, mv_bg, record, final_move):
    Game.window.blit(Game.bg, (-mv_bg, 0))                       # Looping background
    Game.window.blit(Game.bg, (-mv_bg + Game.screen_width, 0))
    text_score = font.render("SCORE: {}".format(Game.score), True, (255, 0, 0))          # Display score on screen
    Game.window.blit(text_score, (Game.screen_width/20, Game.screen_height * .02))                    # Place the score
    text_lives = font.render("RECORD: {}".format(record), True, (255, 0, 0))          # Display score on screen
    Game.window.blit(text_lives, (Game.screen_width/20, Game.screen_height * .10))                    # Place the score
    for dino in Dinos:
        if dino.alive:
            dino.draw(Game.window, final_move)          # Draws dino


    for bird in Birds:
        bird.draw(Game.window)          # Draws bird

    for pellet in pellets:  # Draws fireballs
        pellet.draw(Game.window)
    pygame.display.update()



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
        living_dinos = POP_SIZE  # Number of dinos on field - Also resets for each game
        GAME = game(G_screen_width, G_screen_height, BIRDS, living_dinos)
        #DINo = GAME.player #player(50, 425, 45, 52)
        #DINos = [DINo, GAME.player]
        DINos = GAME.players


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
                    BIRDS.append(enc.enemy(G_screen_width, 440 - rand_lmh * 70, 46, 42, -42, GAME.bird_sprite, rand_lmh, "bird"))
                else:
                    BIRDS.append(enc.enemy(G_screen_width, cact_y[index], cact_w[index], cact_h[index], -42, GAME.cactus_sprite, index, "cact"))

            enemy_cd += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    GAME.crash = True


            for index, DINO in enumerate(DINos):
                if DINO.alive:      # only do this if the current dino is alive
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

                        if not DINO.alive:                # When dino out of lives
                            living_dinos -= 1
                            print("ONE DEAD")
                            if living_dinos <= 0:               # All dinos dead - reset game
                                GAME.crash = True               # Died - game over - shut down
                                print("GAME CRASHED!!")



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
                            prediction = nn[index].model.predict(restate)
                            #print(prediction)
                            final_move = [0,0,0,0]                              # Initialize empty move
                            final_move[np.argmax(prediction[0])] = 1            # Set the model's prediction top to 1
                            print("Dino: {}\tFinal_move: {}".format(DINO.id, final_move))
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
                        draw_window(font, GAME, DINos, pellets, BIRDS, moving_bg, record, final_move)
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
