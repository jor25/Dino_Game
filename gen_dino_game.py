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
import time

import player_class as plc
import enemy_class as enc
import gen_alg as ga

from manual_nn import *
# *************************************************************************************
# GLOBAL CONFIGS
# *************************************************************************************
G_SCREEN_WIDTH = 800
G_SCREEN_HEIGHT = 500

# Global Config Variables - load into different file later
# Viewing variable: True if I want to see the game in action
VIEW_TRAINING = True

# True if I want to see dynamic graphing
VIEW_GRAPHING = True

# Activate Human Player:
HUMAN = False

# Test Neural Net:
NEURAL_PLAYER = not HUMAN

if HUMAN:
    FPS = 70       # This will hurt your eyes less
    POP_SIZE = 1   # Population size for human player
else:
    FPS = 100      # Game fps - for AI, go fast!
    POP_SIZE = 10  # Population size for AI, note: Performance slowdowns

MAX_GAMES = 15
MAX_ENEMIES = 1

# Setting up the networks as globals to keep them from getting wiped out with the main loop
population = [CS.Dna(i, 5) for i in range(POP_SIZE)]            # All the different network architectures
nn = [CS.Collection(population[i]) for i in range(POP_SIZE)]    # The actual networks (Dino Brains)
personal_scores = [[] for i in range(POP_SIZE)]

# Setting initial colors of dinosaurs
COLOR = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(POP_SIZE)]

if VIEW_TRAINING:
    clock = pygame.time.Clock()


# The population will have sol_per_pop chromosome where each chromosome has num_weights genes.
sol_per_pop = POP_SIZE
num_weights = n_x*n_h + n_h*n_h2 + n_h2*n_y

# Defining the population size.
pop_size = (sol_per_pop, num_weights)        # 50, 321

#Creating the initial population. of however many weights - they will be between -1 and 1
new_population = np.random.choice(np.arange(-1,1,step=0.01),size=pop_size,replace=True)


class game(object):
    def __init__(self, screen_width, screen_height, max_enemies, num_players=1):
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
        self.bg_len = self.bg.get_size()[0]                                         # Background image width
        self.crash = False                                                          # Collision
        self.players = [plc.player(200, 425, 45, 52, i, COLOR[i]) for i in range(num_players)]    # Summon player class
        self.population = num_players                                               # Number of players
        self.score = 0                                                              # Game score
        self.speed = 10                                                             # Game speed that will increment
        self.got_points = False             # Flag for points
        self.dodge_points = 0               # Actual dodge_points
        self.got_dodge_points = False       # Flag for dodge_points
        self.got_walk_points = False        # Flag for walk points

        # Make the bird sprites game objects and specifications
        self.bird_sprite = [pygame.image.load('images/bird_L1.png').convert_alpha(),
                            pygame.image.load('images/bird_L2.png').convert_alpha()]
        self.bird_w = [46, 46, 46]      # Bird widths
        self.bird_h = [42, 42, 42]      # Bird heights
        self.bird_y = [440, 370, 300]   # Bird initial y coordinate

        # Set cactus sprite object specifications
        self.cactus_sprite = [pygame.image.load('images/cactus_1.png').convert_alpha()]
        self.cact_w = [25, 35, 40]      # Cactus widths
        self.cact_h = [50, 70, 80]     # Cactus heights
        self.cact_y = [420, 400, 390]   # Cactus initial y coordinates

        self.Enemies = [self.init_enemies(i) for i in range(max_enemies)]       # Summon list of enemies
        self.max_enemies = max_enemies                                          # Max Enemies
        #self.temp_enemies = np.asarray(self.Enemies)    # testing this out for potential performance speed up


    def init_enemies(self, id):
        '''
        Game function that randomly initializes a new enemy. Cactus or Bird.
        :param id: takes in the enemy id so it knows which one to replace
        :return: New enemy class object initialized as a bird or cactus
        '''

        en_index = random.randint(0, 3) % 3         # Enemy type - bird or cactus
        rand_lmh = random.randint(0, 2)             # Randomly select low, middle, or high (category of enemy)
        offset = id * random.randrange(self.screen_width-200, self.screen_width+200, 100)

        #print("MAKE ENEMY ID: {}".format(id))
        if en_index == 0:       # About 1/3 times we get a bird
            return enc.enemy(self.screen_width + offset, self.bird_y[rand_lmh], self.bird_w[rand_lmh], self.bird_h[rand_lmh],
                             -42, self.bird_sprite, rand_lmh, "bird", id)
        else:
            return enc.enemy(self.screen_width + offset, self.cact_y[rand_lmh], self.cact_w[rand_lmh], self.cact_h[rand_lmh],
                             -42, self.cactus_sprite, rand_lmh, "cact", id)


    def main_game(self, enemy_cd, dist_low, dist_high, living_dinos, walk_points, record, moving_bg):
        '''
        Function that loops through and plays the game. Found in main. Runs 1 game at a time.
        :param enemy_cd: enemy cooldown integer
        :param dist_low: min distance between enemies integer
        :param dist_high: max distance between enemies integer
        :param living_dinos: number of remaining dinosaurs still alive integer
        :param walk_points: points collected by distance walking integer
        :param record: maximum visible points collected through games
        :param moving_bg: moving background integer offset
        :return: record integer, walk_points integer
        '''
        while not self.crash:
            if VIEW_TRAINING:
                clock.tick(FPS)         # Clock FPS if training viewable

            enemy_cd += 1                       # Cooldown for enemies
            walk_points += 1                    # Walking points

            for event in pygame.event.get():        # Get game close event
                if event.type == pygame.QUIT:
                    self.crash = True

            if walk_points % 50 == 0:               # Get walkpoints every 50 steps
                self.got_walk_points = True

            for index, DINO in enumerate(Dinos):    # Go through all dinos
                if DINO.alive:                      # Only do this if the current dino is alive
                    for Enemy in self.Enemies:      # Go through all enemies
                        if Enemy.alive:             # Only check if enemy is alive
                            Enemy.vel = self.speed
                            Enemy.move()
                            #if DINO.alive and Enemy.alive:
                            if DINO.y < Enemy.y + Enemy.h:
                                if DINO.y + DINO.h > Enemy.y:
                                    # Within hitbox x coords
                                    if DINO.x + DINO.w > Enemy.x:
                                        if DINO.x < Enemy.x + Enemy.w:
                                            DINO.take_dmg()                 # When dino collides with bird

                                            if not DINO.alive:              # When dino out of lives
                                                living_dinos -= 1
                                                # print("DINO {} - DEAD".format(DINO.id))
                                                if living_dinos <= 0:       # All dinos dead - reset game
                                                    self.crash = True       # Died - game over - shut down
                                                    # print("Game CRASHED!!")

                            if Enemy.x + Enemy.w < DINO.x and not Enemy.got_jumped:     # Successfully dodged enemy
                                # Set off the flags
                                Enemy.got_jumped = True
                                self.got_dodge_points = True
                                self.got_points = True
                                self.score += 10                                        # Score increment by 10
                                self.dodge_points += 1                                  # Dodge Points increment 1

                                if self.score % 100 == 0:                       # If score mod 100 is 0, increment speed
                                    self.speed += 1
                                    if self.speed % 5 == 0 and dist_low != 10:  # if it reaches a mod of 10 then drop spacing between enemies
                                        dist_low -= 10

                        elif not Enemy.alive and enemy_cd > dist_low: # Enemy not alive - remake the enemy and go to next enemy
                            #print("Making New Enemy for id: {}\tCD: {}".format(Enemy.id, enemy_cd))
                            self.Enemies[Enemy.id] = self.init_enemies(Enemy.id)    # Modify that specific enemy with new init

                    if enemy_cd > dist_low:     # Check to reset the enemy cooldown variable
                        enemy_cd = 0

                    if HUMAN:       # Global human flag is activated
                        final_move = UA.active_player(DINO)
                        DINO.do_move(final_move, self)  # Perform new move and get new state

                        if not np.array_equal(final_move, [1, 0, 0, 0]) or walk_points % 100 == 0:
                            state = CS.get_state2(self, DINO, self.Enemies)  # Making some states
                            label_list.append(np.asarray(final_move, dtype=int))
                            states_list.append(state)

                    elif NEURAL_PLAYER:         # Use the neural network to make a prediction
                        state = CS.get_state2(self, DINO, self.Enemies)     # Making some states
                        restate = np.reshape(state, (-1, 10))               # Reshape to fit the model input
                        '''
                        prediction = nn[index].model.predict(restate)       # Predict with specific model
                        '''
                        prediction = forward_propagation(restate, new_population[index])

                        # print(prediction)
                        final_move = [0, 0, 0, 0]                   # Initialize empty move
                        final_move[np.argmax(prediction[0])] = 1    # Set model's top prediction = 1
                        # Use the below for Debugging
                        ##print("Dino: {}\t\tFinal_move: {}\t\tState: {}".format(DINO.id, final_move, state))
                        DINO.do_move(final_move, self)  # Do new move and get new state

                        #if walk_points % 5 == 0:    # Collect states every 5 walkpoints
                        if not np.array_equal(state, np.zeros(10, dtype=int)):              # Collect if content in state
                            nn[DINO.id].labels.append(np.asarray(final_move, dtype=int))    # Collect labels while alive
                            nn[DINO.id].states.append(state)                                # Collect states while alive

                    record = get_record(self.score, record)
                    self.got_points = False             # Reset point indicator flags
                    self.got_dodge_points = False
                    self.got_walk_points = False

                    moving_bg += self.speed             # Increment background image
                    if moving_bg > self.screen_width:   # Reset background image
                        moving_bg = 0

                    if self.score == 1000:              # Arbitrary number to save the model at
                        #nn[index].model.save_weights('weight_files/Dino[{}]got_1000_points.hdf5'.format(index))
                        self.crash = True       # Crash it
                        print("Weights Saved!")
                    # print("dino.x = {}, dino.y ={}".format(DINO.x, DINO.y))

            if VIEW_TRAINING:       # Show Dinos in action when View_training flag activated
                draw_window(font, self, Dinos, self.Enemies, moving_bg, record, final_move, living_dinos, counter_games)

        # After game crash show me how each dino scored on fitness and show stats
        for dino in Dinos:
            print("---------------------------------------------------\n"
                  "Dino ID: {}\t\tFitness: {}\n\tInput: {}\t\tHidden: {}\t\tOut: {}"
                  "".format(dino.id, dino.fitness, nn[dino.id].input_layer,
                            nn[dino.id].hidden_layers, nn[dino.id].output_layer))

        # Outside all the looping, give back these variables
        return record, walk_points


def draw_window(font, Game, Dinos, Birds, mv_bg, record, final_move, remaining_dinos, counter_games):
    '''
    The main drawing window, this is where everything is animated. Need all aspects that will be animated.
    :param font: pygame font object
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

    # Looping background image
    Game.window.blit(Game.bg, (-mv_bg, 0))
    Game.window.blit(Game.bg, (-mv_bg + Game.screen_width, 0))

    # Placing text on the screen
    all_text = "Gen #: {}   RECORD: {}\nPOP # {}/{}   SCORE: {}".format(
        counter_games + 1, record, remaining_dinos, Game.population, Game.score)
    temp = all_text.split('\n')
    rendered_text_1 = font.render(temp[0], True, (255, 0, 0))
    rendered_text_2 = font.render(temp[1], True, (255, 0, 0))
    Game.window.blit(rendered_text_1, (Game.screen_width / 20, Game.screen_height * .02))
    Game.window.blit(rendered_text_2, (Game.screen_width / 20, Game.screen_height * .1))

    # Display all the dinosaurs that are still alive
    for dino in Dinos:
        if dino.alive:
            dino.draw(Game.window, final_move)  # Draws dino

    # Display all the birds
    for bird in Birds:
        if bird.alive:
            bird.draw(Game.window)  # Draws bird

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
    '''
    Function that plots all the max scores of the game at the end.
    May make this into a subplot.
    :param array_counter: All the generation numbers
    :param array_score: All the max scores per generation
    :return: N/A
    '''
    sb.set(color_codes=True)
    ax = sb.regplot(np.array([array_counter])[0], np.array([array_score])[0],
                    color="b", x_jitter=.1, line_kws={'color': 'green'})
    ax.set(xlabel='games', ylabel='score')
    plt.show()


def graph_display(images, population, gen_num, mut_rate):
    '''
    Dynamically plot the fitness values of the population every generation.
    May also include a score subgraph and key for each of the dinosaurs.
    :param images: List of matplotlib objects
    :param population: The Neural Networks of each of the dinosaurs
    :param gen_num: Current Generation number
    :param mut_rate: The mutation rate of the genetic algorithm
    :return: N/A
    '''
    max_fitness = population[0].fit_vals[ np.argmax(population[0].fit_vals) ]
    pop_len = len(images) #int(len(images)*.05 + 1)   # for speed up - show only 5% of population
    for i in range(pop_len):    # population length
        images[i].set_ydata(population[i].fit_vals)
        images[i].set_xdata(np.arange(len(population[i].fit_vals)))

        ax = plt.gca()
        ax.relim()              # recompute the ax.dataLim
        ax.autoscale_view()     # update ax.viewLim using the new dataLim

        temp_max = population[i].fit_vals[ np.argmax(population[i].fit_vals) ]
        if max_fitness < temp_max:
            max_fitness = temp_max  # Update best score

    # Place the title of the plot with dynamic details
    fig.suptitle('Genetic Algorithm\n'
                 'Max Fitness: {}'
                 '      Generation: {}'
                 '      Pop Size: {}'
                 '      Mutation Rate: {}'.format(max_fitness, gen_num, len(population), mut_rate), fontsize=10)

    # Draw the plots and wait.
    plt.draw()
    plt.pause(1e-15)
    time.sleep(0.1)


def trainer(networks, next_gen, best_states, best_labels):
    '''
    EXPERIMENTAL function to train the models for x epochs based on best of the generation's collected and labeled data.
    Note that this function is still experimental and it causes significant performance issues at the moment.
    :param networks: the list of neural networks Collection class
    :param next_gen: List of indexes of those who underperformed in the generation
    :param best_states: States collected from the best dino - 2d array
    :param best_labels: Labels collected from the best dino - 2d array
    :return: N/A
    '''

    print("state shape: {}\t label shape: {}".format(best_states.shape, best_labels.shape))

    # Train Model - loop through each and train accordingly
    for network in networks:
        # Reset all their states and labels
        network.states = []     # Full reset
        network.labels = []     # Full reset

        # Added a section to only train the models that were just initialized, not the older ones.
        #if network.mod_id in next_gen:
        print("--------------------\nTraining DINO {}".format(network.mod_id))
        network.model.fit(best_states, best_labels, epochs=1, verbose=1, shuffle=True)


if __name__ == "__main__":
    Gen_A = ga.Gen_alg(POP_SIZE, nn)        # Initialize the genetic algorithm

    # Initialize a few game variables
    counter_games = 0       # Keep track of what game we're on
    game_scores = [0]        # Used for plotting later on
    record = 0              # Keep track of the high scores
    temp_states = None      # EXPERIMENTAL list of states
    temp_labels = None      # EXPERIMENTAL list of labels
    images = []             # List of matplotlib elements

    if HUMAN:
        states_list = []
        label_list = []

    if VIEW_GRAPHING:
        # Initialize Matplotlib figure, the game variable, and font
        fig = plt.figure()

    if VIEW_TRAINING:
        pygame.init()   # Initialize pygame
        font = pygame.font.SysFont('comicsansms', 40, True)     # Font to display on screen

    for i in range(len(Gen_A.population)):
        print("Pop_Id: {}\nLayers: {}\n".format(Gen_A.population[i].mod_id, Gen_A.population[i].hidden_layers))

        # Initialize all the plots
        temp_img, = plt.plot(Gen_A.population[i].fit_vals, np.arange(len(Gen_A.population[i].fit_vals)))
        images.append(temp_img)


    # The multi-game loop, keeps playing the game until MAX_GAMES is reached
    while counter_games < MAX_GAMES:
        living_dinos = POP_SIZE         # Number of dinos on field - Also resets for each game
        Game = game(G_SCREEN_WIDTH, G_SCREEN_HEIGHT, MAX_ENEMIES, living_dinos)
        Dinos = Game.players

        moving_bg = 0       # Where to start the background image offset
        enemy_cd = 0        # Limit the amount of enemies at any given time
        dist_high = 250     # Max distance between enemy spawns #150
        dist_low = 80       # Min distance between enemy spawns #100
        walk_points = 0     # How far dino has walked - most likely will be used with GA

        # The main game loop
        record, walk_points = Game.main_game(enemy_cd, dist_low, dist_high, living_dinos, walk_points, record, moving_bg)
        #print("After {}".format(new_population[0]))
        if HUMAN:  # Save run to file and quit before new run if human.
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
            score.append(Dinos[i].fitness)  # just in case I want to see how the dinos are doing individually

        game_scores.append(Game.score)

        # Activate GA! Get a list of indexes to update and the best dino
        next_gen_updates, top_dino_id = Gen_A.check_fitness(Dinos, new_population)
        print("UPDATE THESE ID's: {}".format(next_gen_updates))


        if VIEW_GRAPHING:
            # Display the dynamically updating graph after each generation
            graph_display(images, nn, counter_games, Gen_A.mutation_rate)

    game_num = np.arange(counter_games+1)
    plot_ai_results(game_num, game_scores)

