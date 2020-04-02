import collect_states as CS
import random
import pygame
import numpy as np

# *************************************************************************************
# MODIFIABLE GLOBAL CONFIGS
# *************************************************************************************
# Global Configuration Variables
VIEW_TRAINING = not True                # Viewing variable: True if I want to see the game in action
VIEW_GRAPHING = True                    # True if I want to see dynamic graphing
HUMAN = False                           # Activate Human Player - ie if I want to play the game myself
SHOW_BOXES = False                      # Show boxes around dinos and enemies

# Genetic algorithm specific
GA_POP = 20                             # Population for genetic algorithm if in use
MAX_GAMES = 20                          # Number of games/generations to play
USE_PREV_GEN = not True                 # Use a previous generation's dino
REC_CUT_OFF = 1000                      # Recommended Cutoff Point

# *************************************************************************************
# DON'T TOUCH THESE GLOBALS
# *************************************************************************************
# Game Set up
NEURAL_PLAYER = not HUMAN               # Activate the Genetic Algorithm - AI will play
G_SCREEN_WIDTH = 800                    # Game screen width
G_SCREEN_HEIGHT = 500                   # Game screen height
MAX_ENEMIES = 2                         # Number of enemies, this is actually a lot. You'll see.
BEST_BRAIN = None                       # Save the best of the population and make a copy
SAVE_WEIGHTS = False                    # Variable to save weights - Auto activate at specific cutoff points

if HUMAN:
    FPS = 80                            # This will hurt your eyes less
    POP_SIZE = 1                        # Population size for human player
    VIEW_TRAINING = True                # Always let human see what dino is doing
else:
    FPS = 100                           # Game fps - for AI, go fast!
    POP_SIZE = GA_POP                   # Population size for AI, note: Performance slowdowns

if VIEW_TRAINING:
    clock = pygame.time.Clock()         # Initialize clock variable

# Global Weight configurations - ie MODEL ARCHITECTURE! (Don't touch or previous weights won't work)
NUM_INPUTS = 10                         # Number of inputs
NUM_HID_1 = 10                          # Number of nodes in hidden layer 1
NUM_HID_2 = 10                          # Number of nodes in hidden layer 2
NUM_OUT = 4                             # Number of outputs
W1_SHAPE = (NUM_HID_1, NUM_INPUTS)      # Weight Matrix 1 = (20,10)
W2_SHAPE = (NUM_HID_2, NUM_HID_1)       # Weight Matrix 2 = (20,20)
W3_SHAPE = (NUM_OUT, NUM_HID_2)         # Weight Matrix 3 = (4,20)

NUM_WEIGHTS = NUM_INPUTS*NUM_HID_1 + NUM_HID_1*NUM_HID_2 + NUM_HID_2*NUM_OUT    # Total number of weights

# Dino Configurations
HISTORIES = [CS.Collection(i) for i in range(POP_SIZE)]                         # Info on each dino for all generations

# Setting initial colors of dinosaurs
COLOR = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(POP_SIZE)]

# Dimensions of the population, pop size and number of weights in each
POP_DIMS = (POP_SIZE, NUM_WEIGHTS)

# Initialize all the weight values randomly between -1 and 1
DINO_BRAINS = np.random.choice(np.arange(-1, 1, step=0.01), size=POP_DIMS, replace=True)

if USE_PREV_GEN:
    CUT_OFF_POINTS = REC_CUT_OFF + 500      # Cutoff Points if using previous generations
else:
    CUT_OFF_POINTS = REC_CUT_OFF            # Standard cutoff point
