# 3/15/20 Making new changes to the generic dino game.

# 8/29/19 Making the generic google dinosaur game
# Then going to use Machine learning to train a model to play the game
# Planning to use Deep Q Learning

# Resources:
# Random Color generation: https://stackoverflow.com/questions/28999287/generate-random-colors-rgb

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

if HUMAN:
    FPS = 100       # This will hurt your eyes less
    POP_SIZE = 1    # Population size for human player
else:
    FPS = 1000      # Game fps - for AI, go fast!
    POP_SIZE = 10   # Population size for AI, note: Performance slowdowns

MAX_GAMES = 10

# Setting up the networks as globals to keep them from getting wiped out with the main loop
nn = [CS.Collection() for i in range(POP_SIZE)]
personal_scores = [[] for i in range(POP_SIZE)]
# Setting initial colors of dinosaurs
color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(POP_SIZE)]

clock = pygame.time.Clock()


class game(object):
    def __init__(self, screen_width, screen_height, enemies, num_players=1):
        '''
        Initialize the game object and all it's variables.
        :param screen_width: Given an integer screen width
        :param screen_height: Given an integer screen height
        :param enemies: Given a list of enemy objects
        :param num_players: Given an integer amount for number of players - more for ai training.
        '''
        pygame.display.set_caption('Gen Dino Game')                                 # Game caption
        self.screen_width = screen_width                                            # Screen width
        self.screen_height = screen_height                                          # Screen height
        self.window = pygame.display.set_mode((screen_width, screen_height))        # Game window
        self.bg = pygame.image.load('images/bg4.png').convert_alpha()               # Background image
        print(self.bg.get_size())
        self.bg_len = self.bg.get_size()[0]
        print(self.bg_len)
        self.crash = False                                                          # Collision
        self.players = [plc.player(200, 425, 45, 52, i, color[i]) for i in range(num_players)]    # Summon player class
        self.population = num_players
        self.enemies = enemies                                                          # Summon list of enemies
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


def draw_window(font, Game, Dinos, Birds, mv_bg, record, final_move, remaining_dinos, counter_games):
    '''
    The main drawing window, this is where everything is animated. Need all aspects that will be animated.
    :param font:
    :param Game: Game class object
    :param Dinos: Dino class objects
    :param Birds: Enemy class objects
    :param mv_bg: A moving background integer variable
    :param record: A integer record number
    :param final_move: A numpy one hot array of four elements
    :param remaining_dinos: An integer variable listing how many dinos are still in play
    :param counter_games: An integer variable showing what game number we're on
    :return: N/A
    '''
    Game.window.blit(Game.bg, (-mv_bg, 0))                       # Looping background
    Game.window.blit(Game.bg, (-mv_bg + Game.screen_width, 0))

    # Placing text on the screen
    all_text = "Gen #: {}   RECORD: {}\nPOP # {}/{}   SCORE: {}".format(
        counter_games, record, remaining_dinos, Game.population, Game.score)
    temp = all_text.split('\n')
    rendered_text_1 = font.render(temp[0], True, (255,0,0))
    rendered_text_2 = font.render(temp[1], True, (255, 0, 0))
    Game.window.blit(rendered_text_1, (Game.screen_width / 20, Game.screen_height * .02))
    Game.window.blit(rendered_text_2, (Game.screen_width / 20, Game.screen_height * .1))

    # Display all the dinosaurs that are still alive
    for dino in Dinos:
        if dino.alive:
            dino.draw(Game.window, final_move)      # Draws dino

    # Display all the birds
    for bird in Birds:
        bird.draw(Game.window)                      # Draws bird

    # Draw all the stuff
    pygame.display.update()


def get_record(score, record):
    '''
    Function that gets the high score.
    :param score: integer, The current score
    :param record: integer, the highest score
    :return: highest of the two values
    '''
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

    while counter_games < MAX_GAMES:
        BIRDS = []
        living_dinos = POP_SIZE  # Number of dinos on field - Also resets for each game
        Game = game(G_screen_width, G_screen_height, BIRDS, living_dinos)
        DINos = Game.players

        moving_bg = 0       # Where to start the background image offset
        enemy_cd = 0        # Limit the amount of enemies at any given time
        dist_high = 100     # Max distance between enemy spawns #150
        dist_low = 50       # Min distance between enemy spawns #100
        walk_points = 0     # How far dino has walked - most likely will be used with GA

        # The main multi-game loop
        while not Game.crash:

            if VIEW_TRAINING:
                clock.tick(FPS)  #30 # Fps # visible at fast on 100     # 500 good for training

            keys = pygame.key.get_pressed()     # Get what the user selected

            # This is where I initialize random enemies onto the field
            # Check to see if less than max enemies and enemy cooldown is somewhere between low and high distance
            if len(BIRDS) < Game.max_enemies and enemy_cd > random.randint(dist_low, dist_high):
                enemy_cd = 0
                index = random.randint(0, 3) % 3
                rand_lmh = random.randint(0, 2)
                #print("MAKE ENEMY")
                if index == 0:   # about 1/3 times we get a bird
                    BIRDS.append(enc.enemy(G_screen_width, 440 - rand_lmh * 70, 46, 42, -42, Game.bird_sprite, rand_lmh, "bird"))
                else:
                    BIRDS.append(enc.enemy(G_screen_width, cact_y[index], cact_w[index], cact_h[index], -42, Game.cactus_sprite, index, "cact"))

            enemy_cd += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Game.crash = True

            for index, DINO in enumerate(DINos):
                if DINO.alive:      # only do this if the current dino is alive
                    for BIRD in BIRDS:
                        BIRD.vel = Game.speed
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
                            Game.score += 10

                            Game.dodge_points += 1
                            Game.got_dodge_points = True
                            #print("dodged")

                        elif not BIRD.alive:                # When a bird dies, pop it from list and + score
                            #Game.score += 10
                            Game.got_points = True
                            if Game.score % 100 == 0:
                                Game.speed += 1
                                Game.max_enemies += 1
                                if Game.speed % 5 == 0 and dist_low != 10:      # if it reaches a mod of 10 then drop spacing between enemies
                                    dist_low -= 10
                                    dist_high -= 10

                            BIRDS.pop(BIRDS.index(BIRD))

                        if not DINO.alive:                # When dino out of lives
                            living_dinos -= 1
                            print("DINO {} - DEAD".format(DINO.id))
                            if living_dinos <= 0:               # All dinos dead - reset game
                                Game.crash = True               # Died - game over - shut down
                                print("Game CRASHED!!")

                    walk_points += 1

                    if walk_points % 50 == 0:
                        Game.got_walk_points = True

                    if HUMAN:
                        final_move = UA.active_player(DINO)
                        DINO.do_move(final_move, Game, walk_points)     # Perform new move and get new state

                        if not np.array_equal(final_move, [1,0,0,0]) or walk_points % 100 == 0:
                            state = CS.get_state2(Game, DINO, BIRDS)  # Making some states
                            label_list.append(np.asarray(final_move, dtype=int))
                            states_list.append(state)

                    elif NEURAL_PLAYER:
                        # Use the neural network to make a prediction
                        final_move = [1,0,0,0]
                        state = CS.get_state2(Game, DINO, BIRDS)                 # Making some states
                        restate = np.reshape(state, (-1, 16))                           # Reshape to fit the model input
                        prediction = nn[index].model.predict(restate)                   # Predict with specific model
                        #print(prediction)
                        final_move = [0,0,0,0]                                          # Initialize empty move
                        final_move[np.argmax(prediction[0])] = 1                        # Set model's top prediction = 1
                        # Use the below for Debugging
                        ##print("Dino: {}\t\tFinal_move: {}\t\tState: {}".format(DINO.id, final_move, state))
                        DINO.do_move(final_move, Game, walk_points)                     # Do new move and get new state

                    record = get_record(Game.score, record)
                    Game.got_points = False         # Reset point indicator
                    Game.got_dodge_points = False
                    Game.got_walk_points = False

                    moving_bg += Game.speed                         # Increment background image
                    if moving_bg > Game.screen_width:               # Reset background image
                        moving_bg = 0

                    # Comment in when you want to see dino jumping
                    if VIEW_TRAINING:
                        draw_window(font, Game, DINos, BIRDS, moving_bg, record, final_move, living_dinos, counter_games)

                    if Game.score == 1000:   # Arbitrary number to save the model at
                        nn[index].model.save_weights('Dino[{}]got_1000_points.hdf5'.format(index))
                        print("Weights Saved!")
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
        print('Game', counter_games, '      Score:', Game.score, '      Record:', record,
              '      Dodge Points', Game.dodge_points, '    Walk Points', walk_points)

        for i, score in enumerate(personal_scores):
            score.append(DINos[i].fitness)             # just in case I want to see how the dinos are doing individually

        game_scores.append(Game.score)

    game_num = np.arange(counter_games)
    plot_ai_results(game_num, game_scores)

    # Quit when exiting loop
    #pygame.quit()
