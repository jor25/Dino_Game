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
      
        #"""
        # Where am I on the x coordinates
        # in the first quarter of screen
        #player.x < game.screen_width / 4,
        
        # in the 2nd quarter
        #player.x >= game.screen_width / 4
        #    and player.x < game.screen_width / 2,
        
        # in the 3rd quarter
        #player.x >= game.screen_width / 2 
        #    and player.x < game.screen_width * (3/4),
        
        # in the 4th quarter
        #player.x >= game.screen_width * (3/4),
        #"""
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
        player.x + player.w < enemy.x 
            and player.x + player.w + 100 > enemy.x,

        # Enemy within 100 pixels behind dino
        player.x > enemy.x + enemy.w 
            and player.x - 100 < enemy.x + enemy.w,
        
        # Enemy within 100 pixels above dino
        player.y > enemy.y + enemy.h 
            and player.y - 100 < enemy.x + enemy.h,

        # Enemy within 100 pixels below dino
        player.y + player.h < enemy.y 
            and player.y + player.h + 100 > enemy.y,

        # The 200 pixel box range
        # Enemy within 200 pixels behind dino
        player.x + player.w < enemy.x
            and player.x + player.w + 200 > enemy.x,

        # Enemy within 200 pixels behind dino
        player.x > enemy.x + enemy.w 
            and player.x - 200 < enemy.x + enemy.w,

        # Enemy within 200 pixels above dino
        player.y > enemy.y + enemy.h 
            and player.y - 200 < enemy.x + enemy.h,

        # Enemy within 200 pixels below dino
        player.y + player.h < enemy.y 
            and player.y + player.h + 200 > enemy.y,

        # The 300 pixel box range
        # Enemy within 300 pixels behind dino
        player.x + player.w < enemy.x 
            and player.x + player.w + 300 > enemy.x,

        # Enemy within 300 pixels behind dino
        player.x > enemy.x + enemy.w 
            and player.x - 300 < enemy.x + enemy.w,

        # Enemy within 300 pixels above dino
        player.y > enemy.y + enemy.h 
            and player.y - 300 < enemy.x + enemy.h,

        # Enemy within 300 pixels below dino
        player.y + player.h < enemy.y 
            and player.y + player.h + 300 > enemy.y
    
    ]

    label = move
    #print(state)
    print("label: {} State: {}".format(np.asarray(label, dtype=int), np.asarray(state, dtype=int)))
    return np.asarray(label, dtype=int), np.asarray(state, dtype=int)
