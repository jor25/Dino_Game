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


class Collection():
    def __init__(self):
        self.learning_rate = 0.001
        self.model = self.network()
        #self.model = self.network("model_files/nn_01.hdf5")


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


def get_state(game, player, enemy, move):
    state = [
        # Am I on the ground or in the air
        player.jumping,

        # Did dino crash?
        game.crash,

        # Directly ahead/behind - danger on my current y cords
        player.y < enemy.hitbox[1] + enemy.hitbox[3]
        and player.y + player.h > enemy.hitbox[1],

        # Directly above/below - danger on my x cords
        player.x + player.w > enemy.hitbox[0]
        and player.x < enemy.hitbox[0] + enemy.hitbox[2],

        # The 100 pixel box range
        # Enemy within 100 pixels ahead of dino
        player.x + player.w < enemy.x < player.x + player.w + 100,

        # Enemy within 100 pixels behind dino
        player.x > enemy.x + enemy.w > player.x - 100,
        
        # Enemy within 100 pixels above dino
        player.y > enemy.y + enemy.h
        and player.y - 100 < enemy.x + enemy.h,

        # Enemy within 100 pixels below dino
        player.y + player.h < enemy.y < player.y + player.h + 100,

        # The 200 pixel box range
        # Enemy within 200 pixels behind dino
        player.x + player.w < enemy.x < player.x + player.w + 200,

        # Enemy within 200 pixels behind dino
        player.x > enemy.x + enemy.w > player.x - 200,

        # Enemy within 200 pixels above dino
        player.y > enemy.y + enemy.h
        and player.y - 200 < enemy.x + enemy.h,

        # Enemy within 200 pixels below dino
        player.y + player.h < enemy.y < player.y + player.h + 200,

        # The 300 pixel box range
        # Enemy within 300 pixels behind dino
        player.x + player.w < enemy.x < player.x + player.w + 300,

        # Enemy within 300 pixels behind dino
        player.x > enemy.x + enemy.w > player.x - 300,

        # Enemy within 300 pixels above dino
        player.y > enemy.y + enemy.h
        and player.y - 300 < enemy.x + enemy.h,

        # Enemy within 300 pixels below dino
        player.y + player.h < enemy.y < player.y + player.h + 300

    ]

    label = move
    #print(state)
    print("Player ID: {} label: {} State: {}".format(player.id, np.asarray(label, dtype=int), np.asarray(state, dtype=int)))
    return np.asarray(label, dtype=int), np.asarray(state, dtype=int)


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
    state = np.zeros(16, dtype=int)     # state of 16

    # Am I on the ground or in the air
    if player.jumping:
        state[0] = 1

    # Did dino crash?
    if game.crash:
        state[1] = 1

    # Check all the enemies if any of these are true
    for enemy in enemies:
        # Enemy Anywhere within 300 pixels of dino - Won't check if they aren't in range - slight speed up
        if player.x + player.w < enemy.x < player.x + player.w + 300 \
            or player.x > enemy.x + enemy.w > player.x - 300 \
            or player.y > enemy.y + enemy.h and player.y - 300 < enemy.x + enemy.h \
            or player.y + player.h < enemy.y < player.y + player.h + 300:

            # Directly ahead/behind - danger on my current y cords
            if player.y < enemy.hitbox[1] + enemy.hitbox[3] and player.y + player.h > enemy.hitbox[1] and state[2] == 0:
                state[2] = 1

            # Directly above/below - danger on my x cords
            if player.x + player.w > enemy.hitbox[0] and player.x < enemy.hitbox[0] + enemy.hitbox[2] and state[3] == 0:
                state[3] = 1

            # The 100 pixel box range
            # Enemy within 100 pixels ahead of dino
            if player.x + player.w < enemy.x < player.x + player.w + 100 and state[4] == 0:
                state[4] = 1

            # Enemy within 100 pixels behind dino
            if player.x > enemy.x + enemy.w > player.x - 100 and state[5] == 0:
                state[5] = 1

            # Enemy within 100 pixels above dino
            if player.y > enemy.y + enemy.h and player.y - 100 < enemy.x + enemy.h and state[6] == 0:
                state[6] = 1

            # Enemy within 100 pixels below dino
            if player.y + player.h < enemy.y < player.y + player.h + 100 and state[7] == 0:
                state[7] = 1

            # The 200 pixel box range
            # Enemy within 200 pixels behind dino
            if player.x + player.w < enemy.x < player.x + player.w + 200 and state[8] == 0:
                state[8] = 1

            # Enemy within 200 pixels behind dino
            if player.x > enemy.x + enemy.w > player.x - 200 and state[9] == 0:
                state[9] = 1

            # Enemy within 200 pixels above dino
            if player.y > enemy.y + enemy.h and player.y - 200 < enemy.x + enemy.h and state[10] == 0:
                state[10] = 1

            # Enemy within 200 pixels below dino
            if player.y + player.h < enemy.y < player.y + player.h + 200 and state[11] == 0:
                state[11] = 1

            # The 300 pixel box range
            # Enemy within 300 pixels behind dino
            if player.x + player.w < enemy.x < player.x + player.w + 300 and state[12] == 0:
                state[12] = 1

            # Enemy within 300 pixels behind dino
            if player.x > enemy.x + enemy.w > player.x - 300 and state[13] == 0:
                state[13] = 1

            # Enemy within 300 pixels above dino
            if player.y > enemy.y + enemy.h and player.y - 300 < enemy.x + enemy.h and state[14] == 0:
                state[14] = 1

            # Enemy within 300 pixels below dino
            if player.y + player.h < enemy.y < player.y + player.h + 300 and state[15] == 0:
                state[15] = 1

    return state