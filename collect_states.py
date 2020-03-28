# Creating file to collect data from players on how to dino run.
# Train NN after human plays.
# 11/21/19


import random
import numpy as np
import pandas as pd
from operator import add
from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers.core import Dense, Dropout
import keras.losses as kl

'''
Class for each individual in the population will be built off this information.
This information will later be scrambled with crossover to create new population.
'''
class Dna:
    def __init__(self, id, chrom_num):
        self.id = id                            # The populant's id number
        self.num_layers = chrom_num
        self.fit_vals = [0]                     # Accuracy scores to be added
        self.input_layer = 14                   # Same number for each input
        self.hidden_layers = [random.randint(1, 70) for i in range(self.num_layers)]       # Set hidden layers randomly
        self.output_layer = 4                   # Placeholder output layer
        self.history = [id]                     # List of all combinations


class Collection():
    def __init__(self, dna):
        self.learning_rate = 0.001
        #self.model = self.network()
        #self.model = self.network("model_files/nn_01.hdf5")

        self.mod_id = dna.id
        self.input_layer = dna.input_layer
        self.hidden_layers = dna.hidden_layers
        self.output_layer = dna.output_layer
        self.model = self.create_network()  # No initial weights
        self.fit_vals = dna.fit_vals    # [0]
        self.states = []    # 16 inputs
        self.labels = []    # 4 outputs
        #self.model = self.create_network("weight_files/nn_3.hdf5")  # Using my trained weights

    def create_network(self, weights=None):
        # Create my model
        model = Sequential()
        model.add(Dense(output_dim=self.hidden_layers[0], activation='relu', input_dim=self.input_layer))    # Input
        for i in range(1, len(self.hidden_layers)):
            model.add(Dense(output_dim=self.hidden_layers[i], activation='relu'))           # Add all hidden layers
            model.add(Dropout(0.15))
        model.add(Dense(output_dim=self.output_layer, activation='softmax'))                # Output layer
        opt = Adam(self.learning_rate)      # Set learning rate

        # Compile model
        model.compile(loss=kl.categorical_crossentropy, metrics=['accuracy'], optimizer=opt)
        #print("Model ID: {} compiled".format(self.mod_id))     # Verify updates

        # Load weights if they're available
        if weights:
            model.load_weights(weights)
            print("model loaded")
        return model

    def network(self, weights=None):
        model = Sequential()
        model.add(Dense(output_dim=40, activation='relu', input_dim=16))        # max 144
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=40, activation='relu'))
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=40, activation='relu'))
        model.add(Dropout(0.15))

        model.add(Dense(output_dim=4, activation='softmax'))
        opt = Adam(self.learning_rate)
        model.compile(loss='mse', metrics=['accuracy'], optimizer=opt)

        if weights:
            model.load_weights(weights)
            print("model loaded")
        return model


# https://stackoverflow.com/questions/6081008/dump-a-numpy-array-into-a-csv-file
def write_data(data, file_name="state_data/data"):
    np.savetxt("{}.csv".format(file_name), data, delimiter=",", fmt='%i')
    print("DATA SAVED.")
    pass

def append_data(data, file_name="state_data/data"):
    with open("{}.csv".format(file_name),'ab') as f:
        np.savetxt(f, data, delimiter=",", fmt='%i')
    print("DATA APPENDED.")


def read_data(data_file="state_data/data.csv"):
    ''' Read the csv file data into a 2d numpy array.
        Give back 2d array and the number of instances.
        ndarray data
        int num_p
    '''
    # Numpy read in my data - separate by comma, all ints.  
    data = np.loadtxt(data_file, delimiter=",", dtype=int)
    
    return data


def get_state2(game, player, enemies):
    '''
    Function that collects all the states of the game from the dinosaur's perspective.
    This one specifically looks at all enemies available within a certain distance.
    Fairly hardcoded encoding of data.
    :param game: Game object
    :param player: 1 Dino object
    :param enemies: All enemies list
    :return: Give back a numpy label and state
    '''
    state = np.zeros(14, dtype=int)     # state of 16
    '''
    # Am I on the ground or in the air
    if player.jumping:
        state[0] = 1

    # Did dino crash?
    if game.crash:
        state[1] = 1
    '''
    # Check all the enemies if any of these are true
    for enemy in enemies:
        # Enemy Anywhere within 150 pixels of dino - Won't check if they aren't in range - slight speed up
        if player.x + player.w < enemy.x < player.x + player.w + 150 \
            or player.x > enemy.x + enemy.w > player.x - 150 \
            or player.y > enemy.y + enemy.h and player.y - 150 < enemy.x + enemy.h \
            or player.y + player.h < enemy.y < player.y + player.h + 150:

            # Directly ahead/behind - danger on my current y cords
            if player.y < enemy.hitbox[1] + enemy.hitbox[3] and player.y + player.h > enemy.hitbox[1] and state[0] == 0:
                state[0] = 1

            # Directly above/below - danger on my x cords
            if player.x + player.w > enemy.hitbox[0] and player.x < enemy.hitbox[0] + enemy.hitbox[2] and state[1] == 0:
                state[1] = 1

            # The 50 pixel box range
            # Enemy within 50 pixels ahead of dino
            if player.x + player.w < enemy.x < player.x + player.w + 50 and state[2] == 0:
                state[2] = 1

            # Enemy within 50 pixels behind dino
            if player.x > enemy.x + enemy.w > player.x - 50 and state[3] == 0:
                state[3] = 1

            # Enemy within 50 pixels above dino
            if player.y > enemy.y + enemy.h and player.y - 50 < enemy.x + enemy.h and state[4] == 0:
                state[4] = 1

            # Enemy within 50 pixels below dino
            if player.y + player.h < enemy.y < player.y + player.h + 50 and state[5] == 0:
                state[5] = 1

            # The 100 pixel box range
            # Enemy within 100 pixels behind dino
            if player.x + player.w < enemy.x < player.x + player.w + 100 and state[6] == 0:
                state[6] = 1

            # Enemy within 100 pixels behind dino
            if player.x > enemy.x + enemy.w > player.x - 100 and state[7] == 0:
                state[7] = 1

            # Enemy within 100 pixels above dino
            if player.y > enemy.y + enemy.h and player.y - 100 < enemy.x + enemy.h and state[8] == 0:
                state[8] = 1

            # Enemy within 100 pixels below dino
            if player.y + player.h < enemy.y < player.y + player.h + 100 and state[9] == 0:
                state[9] = 1

            # The 150 pixel box range
            # Enemy within 150 pixels behind dino
            if player.x + player.w < enemy.x < player.x + player.w + 150 and state[10] == 0:
                state[10] = 1

            # Enemy within 150 pixels behind dino
            if player.x > enemy.x + enemy.w > player.x - 150 and state[11] == 0:
                state[11] = 1

            # Enemy within 150 pixels above dino
            if player.y > enemy.y + enemy.h and player.y - 150 < enemy.x + enemy.h and state[12] == 0:
                state[12] = 1

            # Enemy within 150 pixels below dino
            if player.y + player.h < enemy.y < player.y + player.h + 150 and state[13] == 0:
                state[13] = 1

    return state