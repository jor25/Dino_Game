# 3/15/20 Making new changes to the generic dino game.

# 8/29/19 Making the generic google dinosaur game
# Then going to use Machine learning to train a model to play the game
# Planning to use Deep Q Learning

# Resources:
# Random Color generation: https://stackoverflow.com/questions/28999287/generate-random-colors-rgb

import matplotlib.pyplot as plt
import seaborn as sb
import user_active as UA
import time
import player_class as plc
import enemy_class as enc
import gen_alg as ga
from manual_nn import *
from configs import *


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
        self.population = num_players       # Number of players
        self.score = 0                      # Game score
        self.speed = 10                     # Game speed that will increment
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
        self.cact_h = [50, 70, 80]      # Cactus heights
        self.cact_y = [420, 400, 390]   # Cactus initial y coordinates

        self.Enemies = [self.init_enemies(i) for i in range(max_enemies)]       # Summon list of enemies
        self.max_enemies = max_enemies                                          # Max Enemies

    def init_enemies(self, id):
        '''
        Game function that randomly initializes a new enemy. Cactus or Bird. Birds have a 1/3 chance of being made.
        :param id: takes in the enemy id so it knows which one to replace
        :return: New enemy class object initialized as a bird or cactus
        '''

        en_index = random.randint(0, 3) % 3         # Enemy type - bird or cactus
        rand_lmh = random.randint(0, 2)             # Randomly select low, middle, or high (category of enemy)
        offset = id * random.randrange(int(self.screen_width*.5), int(self.screen_width*.7), 100)

        if en_index == 0:       # About 1/3 times we get a bird
            # Initalize and return a bird for the given id
            return enc.enemy(self.screen_width + offset, self.bird_y[rand_lmh],
                             self.bird_w[rand_lmh], self.bird_h[rand_lmh],
                             -42, self.bird_sprite, rand_lmh, "bird", id)
        else:
            # Initialize and return a cactus for the given id
            return enc.enemy(self.screen_width + offset, self.cact_y[rand_lmh],
                             self.cact_w[rand_lmh], self.cact_h[rand_lmh],
                             -42, self.cactus_sprite, rand_lmh, "cact", id)


    def main_game(self, enemy_cd, dist_low, living_dinos, walk_points, record, moving_bg):
        '''
        Function that loops through and plays the game. Found in main. Runs 1 game at a time.
        :param enemy_cd: enemy cooldown integer
        :param dist_low: min distance between enemies integer
        :param living_dinos: number of remaining dinosaurs still alive integer
        :param walk_points: points collected by distance walking integer
        :param record: maximum visible points collected through games
        :param moving_bg: moving background integer offset
        :return: record integer, walk_points integer
        '''

        global CUT_OFF_POINTS                   # Update and call up the global cut off points
        global SAVE_WEIGHTS

        while not self.crash:                   # While the game has not crashed
            if VIEW_TRAINING:
                clock.tick(FPS)                 # Set clock FPS if training viewable

            enemy_cd += 1                       # Increment cooldown for enemies
            walk_points += 1                    # Increment walking points
            moving_bg += self.speed             # Increment background image

            for event in pygame.event.get():    # Get game close event - if user closes game window
                if event.type == pygame.QUIT:
                    self.crash = True           # Crash will get us out of the game loop

            if walk_points % 50 == 0:           # Get walkpoints every mod 50 steps
                self.got_walk_points = True     # Set flag for walk points

            for Enemy in self.Enemies:          # For each enemy
                Enemy.move()                    # Do the move then let the dinos react to it
                Enemy.vel = self.speed          # Update the speed of each enemy
                if not Enemy.alive and enemy_cd > dist_low:  # Enemy not alive and cooldown available
                    self.Enemies[Enemy.id] = self.init_enemies(Enemy.id)  # Modify that specific enemy with new init

            if enemy_cd > dist_low:             # Check to reset the enemy cooldown variable
                enemy_cd = 0

            if moving_bg > self.screen_width:   # Reset background image
                moving_bg = 0

            for index, DINO in enumerate(Dinos):                            # Go through all dinos
                if DINO.alive:                                              # Only do this if the current dino is alive
                    for Enemy in self.Enemies:                              # Go through all enemies
                        if Enemy.alive:                                     # Only check if enemy is alive

                            if DINO.y < Enemy.y + Enemy.h:                  # Check dino y coords with enemy y coords
                                if DINO.y + DINO.h > Enemy.y:               # Are we on a collision path?
                                    # Within hitbox x coords
                                    if DINO.x + DINO.w > Enemy.x:           # Check dino x coords with enemy
                                        if DINO.x < Enemy.x + Enemy.w:      # Is the enemy above or below me?
                                            DINO.take_dmg()                 # When dino collides with enemy - die

                                            if not DINO.alive:              # When dino out of lives
                                                living_dinos -= 1           # Deduct from number of living dinos
                                                if living_dinos <= 0:       # All dinos dead - reset game
                                                    self.crash = True       # All died - game over - shut down

                            if Enemy.x + Enemy.w < DINO.x and not Enemy.got_jumped:     # Successfully dodged enemy
                                # Set off the flags to avoid double counting points
                                Enemy.got_jumped = True
                                self.got_dodge_points = True
                                self.got_points = True
                                self.score += 10                                # Score increment by 10
                                self.dodge_points += 1                          # Dodge Points increment 1

                                if self.score % 100 == 0:                       # If score mod 100 is 0
                                    self.speed += 1                             # Increment speed
                                    if self.speed % 5 == 0 and dist_low >= 10:  # If mod of 5 and dist low not 10
                                        dist_low -= 10                          # Decriment distance low

                    if HUMAN:
                        final_move = UA.active_player(DINO)     # Get keyboard press
                        DINO.do_move(final_move, self)          # Perform new move and get new state

                        if not np.array_equal(final_move, [1, 0, 0, 0]) or walk_points % 100 == 0:
                            state = CS.get_state2(DINO, self.Enemies)               # Making some states
                            label_list.append(np.asarray(final_move, dtype=int))    # Append those labels
                            states_list.append(state)                               # Append those states

                    elif NEURAL_PLAYER:                             # Use the neural networks to make a prediction
                        state = CS.get_state2(DINO, self.Enemies)   # Making some states
                        restate = np.reshape(state, (-1, 10))       # Reshape to fit the model input
                        prediction = forward_propagation(restate, DINO_BRAINS[index])   # Make predictions
                        final_move = [0, 0, 0, 0]                   # Initialize empty move
                        final_move[np.argmax(prediction[0])] = 1    # Set model's top prediction = 1
                        DINO.do_move(final_move, self)              # Do the move

                        #if walk_points % 5 == 0:    # Collect states every 5 walkpoints
                        if not np.array_equal(state, np.zeros(10, dtype=int)):              # Collect if content in state
                            HISTORIES[DINO.id].labels.append(np.asarray(final_move, dtype=int))    # Collect labels while alive
                            HISTORIES[DINO.id].states.append(state)                                # Collect states while alive

                    record = get_record(self.score, record)     # Get the game record
                    self.got_points = False                     # Reset point indicator flags
                    self.got_dodge_points = False
                    self.got_walk_points = False

                    if self.score == CUT_OFF_POINTS and NEURAL_PLAYER:    # Arbitrary number to save the model at 1000
                        CUT_OFF_POINTS += 500
                        SAVE_WEIGHTS = True
                        self.crash = True               # Crash it if we reach here - Save the weights too...
                        print("Game Crashed Limit reached - new limit: {} - Allow Weight Save: {}".format(CUT_OFF_POINTS, SAVE_WEIGHTS))

            if VIEW_TRAINING:       # Show Dinos in action when View_training flag activated
                draw_window(font, self, Dinos, self.Enemies, moving_bg, record, final_move, living_dinos, counter_games)

        # Outside all the looping, give back the record and the walk points
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


def plot_game_records(array_counter, array_score):
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


if __name__ == "__main__":
    # Initialize the genetic algorithm
    Gen_A = ga.Gen_alg(POP_SIZE, HISTORIES, NUM_WEIGHTS)

    # Loading a specific dino brain from previous runs
    if USE_PREV_GEN:
        load_all_networks()

    # Initialize a few game variables
    counter_games = 0       # Keep track of what game we're on
    game_scores = [0]       # Used for plotting later on
    record = 0              # Keep track of the high scores
    temp_states = None      # EXPERIMENTAL list of states
    temp_labels = None      # EXPERIMENTAL list of labels

    if HUMAN:
        states_list = []
        label_list = []

    if VIEW_GRAPHING:
        fig = plt.figure()      # Initialize Matplotlib figure
        images = []             # List of matplotlib elements

        # Initialize all the plots
        for i in range(len(Gen_A.population)):
            temp_img, = plt.plot(Gen_A.population[i].fit_vals, np.arange(len(Gen_A.population[i].fit_vals)), "{}".format(COLOR[i]))
            images.append(temp_img)

    if VIEW_TRAINING:
        pygame.init()                                           # Initialize pygame
        font = pygame.font.SysFont('comicsansms', 40, True)     # Font to display on screen

    # The multi-game loop, keeps playing the game until MAX_GAMES is reached
    while counter_games < MAX_GAMES:
        living_dinos = POP_SIZE         # Number of dinos on field - Also resets for each game
        Game = game(G_SCREEN_WIDTH, G_SCREEN_HEIGHT, MAX_ENEMIES, living_dinos)     # Initialize game object
        Dinos = Game.players

        moving_bg = 0       # Where to start the background image offset
        enemy_cd = 0        # Limit the amount of enemies at any given time
        dist_low = 80       # Min distance between enemy spawns #100
        walk_points = 0     # How far dino has walked - most likely will be used with GA

        # The main game loop
        record, walk_points = Game.main_game(enemy_cd, dist_low, living_dinos, walk_points, record, moving_bg)

        if HUMAN:  # Used to save run to file and quit before new run if human.
            # New data
            #CS.write_data(states_list)
            #CS.write_data(label_list, "state_data/label")

            # add to data
            #CS.append_data(states_list)
            #CS.append_data(label_list, "state_data/label")
            print("QUIT NOOOWWW!!")

        # Increment Game counter, add scores, and display information
        counter_games += 1
        game_scores.append(Game.score)
        print('Game', counter_games, '      Score:', Game.score, '      Record:', record,
              '      Dodge Points', Game.dodge_points, '    Walk Points', walk_points)

        # Activate GA! Get a list of indexes to update and the best dino
        next_gen_updates, top_dino_id = Gen_A.check_fitness(Dinos, DINO_BRAINS)

        if game_scores[np.argmax(game_scores)] == Game.score:           # Highest score?
            BEST_BRAIN = DINO_BRAINS[top_dino_id].copy()                # Get a copy of the best dino brain
            details = "Dino[{}]_Gen[{}]_record[{}]".format(top_dino_id, counter_games+1, Game.score)
            #print("The Best Brain: {}\nID: {}\nGame Num: {}".format(BEST_BRAIN, top_dino_id, counter_games+1))
            print("\t{}".format(details))

        if VIEW_GRAPHING:
            # Display the dynamically updating graph after each generation
            graph_display(images, HISTORIES, counter_games, Gen_A.mutation_rate)

    # Save the weights to file
    if SAVE_WEIGHTS and NEURAL_PLAYER:
        save_weights_as_csv(BEST_BRAIN, details)

    # Arrange a list of games for plotting - Display plot from records
    game_num = np.arange(counter_games+1)
    plot_game_records(game_num, game_scores)
