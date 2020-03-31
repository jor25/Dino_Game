# Creating file to collect data from players on how to dino run.
# Can train Neural Network on collected data
# 11/21/19
# Resources:
#   https://stackoverflow.com/questions/6081008/dump-a-numpy-array-into-a-csv-file

import numpy as np

class Collection():
    def __init__(self, id):
        self.learning_rate = 0.001
        self.mod_id = id        # Model Id
        self.fit_vals = [0]     # Fitness Values
        self.states = []        # 10 inputs per state
        self.labels = []        # 4 outputs per label


def write_data(data, file_name="state_data/data"):
    '''
    Function to write state or label data into a csv file
    :param data: 2d numpy array of states or labels
    :param file_name: Path and name of the file to save this data to
    :return: N/A
    '''
    np.savetxt("{}.csv".format(file_name), data, delimiter=",", fmt='%i')
    print("DATA SAVED.")


def append_data(data, file_name="state_data/data"):
    '''
    Function that appends state or label data into a previously existing csv file.
    :param data: 2d numpy array of states or labels
    :param file_name: Path and name of the file to save this data to
    :return: N/A
    '''
    with open("{}.csv".format(file_name),'ab') as f:
        np.savetxt(f, data, delimiter=",", fmt='%i')
    print("DATA APPENDED.")


def read_data(data_file="state_data/data.csv"):
    '''
    Read the csv file data into a 2d numpy array.
    Give back 2d array and the number of instances.
    :param data_file: Path to state data or label data csv's
    :return: ndarray data numpy array
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
    state = np.zeros(10, dtype=int)     # state of 10

    # Check all the enemies if any of these are true
    for enemy in enemies:
        # Enemy Anywhere within 100 pixels of dino - Won't check if they aren't in range - slight speed up
        if player.x + player.w < enemy.x < player.x + player.w + 100 \
            or player.x > enemy.x + enemy.w > player.x - 100 \
            or player.y > enemy.y + enemy.h and player.y - 100 < enemy.x + enemy.h \
            or player.y + player.h < enemy.y < player.y + player.h + 100:

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

    return state