import collect_states as CS
import random
import pygame
import numpy as np

# *************************************************************************************
# ALL GLOBAL CONFIGS
# *************************************************************************************

# Global Weight configurations - ie MODEL ARCHITECTURE!
NUM_INPUTS = 10                         # Number of inputs
NUM_HID_1 = 20                          # Number of nodes in hidden layer 1
NUM_HID_2 = 20                          # Number of nodes in hidden layer 2
NUM_OUT = 4                             # Number of outputs
W1_SHAPE = (NUM_HID_1, NUM_INPUTS)      # Weight Matrix 1 = (20,10)
W2_SHAPE = (NUM_HID_2, NUM_HID_1)       # Weight Matrix 2 = (20,20)
W3_SHAPE = (NUM_OUT, NUM_HID_2)         # Weight Matrix 3 = (4,20)

# The total number of weights from each layer
NUM_WEIGHTS = NUM_INPUTS*NUM_HID_1 + NUM_HID_1*NUM_HID_2 + NUM_HID_2*NUM_OUT

# Game Screen Dimensions
G_SCREEN_WIDTH = 800                    # Game screen width
G_SCREEN_HEIGHT = 500                   # Game screen height

# Global Configuration Variables
VIEW_TRAINING = not True                # Viewing variable: True if I want to see the game in action
VIEW_GRAPHING = True                    # True if I want to see dynamic graphing
HUMAN = False                           # Activate Human Player - ie if I want to play the game myself
NEURAL_PLAYER = not HUMAN               # Activate the Genetic Algorithm - AI will play

# Game settings for specific set up
MAX_GAMES = 20                          # Number of games to play
MAX_ENEMIES = 2                         # Number of enemies, this is actually a lot. You'll see.

if HUMAN:
    FPS = 70                            # This will hurt your eyes less
    POP_SIZE = 1                        # Population size for human player
else:
    FPS = 100                           # Game fps - for AI, go fast!
    POP_SIZE = 20                       # Population size for AI, note: Performance slowdowns

# Setting up the network history as globals to keep them from getting wiped out with the main loop
HISTORIES = [CS.Collection(i) for i in range(POP_SIZE)]    # Information about each dino after every generation

# Setting initial colors of dinosaurs
COLOR = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(POP_SIZE)]

if VIEW_TRAINING:
    clock = pygame.time.Clock()

# Dimensions of the population, pop size and number of weights in each
POP_DIMS = (POP_SIZE, NUM_WEIGHTS)

# Initialize all the weight values randomly. They will be between -1 and 1
DINO_BRAINS = np.random.choice(np.arange(-1, 1, step=0.01), size=POP_DIMS, replace=True)
