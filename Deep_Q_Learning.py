# Deep Q Learning
# Attempting to make a network learn to play the jumping dinosaur game
# 9/11/19

import random
import numpy as np
import pandas as pd
from operator import add
from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers.core import Dense, Dropout


class DQL_AI(object):

    def __init__(self):
        self.reward = 0
        self.total_reward = 0
        self.gamma = 0.9
        self.dataframe = pd.DataFrame()
        self.short_memory = np.array([])
        self.agent_target = 1
        self.agent_predict = 0
        self.learning_rate = 0.0005 #0.0005
        self.model = self.network()                # Switch comments to train from scratch
        #self.model = self.network("test_weights1.hdf5")
        self.epsilon = 0
        self.actual = []
        self.memory = []

    def get_state(self, game, player, enemies):

        state = [
            player.jumping,
            player.y == 425, #jump_height == 10,
            # Collided with y box
            # Danger in front
            # Danger behind
            # Danger above
            len(enemies) == 0,  # no enemies on screen
            len(enemies) == 1,  # 1 enemy on screen
            #len(enemies) == 2,  # 2 enemies
            #len(enemies) >= 3,  # 3 or more enemies
            player.x < game.screen_width / 4,   # in the first quarter of screen
            player.x >= game.screen_width / 4 and player.x < game.screen_width / 2,   # in the 2nd quarter
            player.x >= game.screen_width / 2 and player.x < game.screen_width * (3/4),   # in the 3rd quarter
            player.x >= game.screen_width * (3/4),   # in the 4th quarter
            player.x > player.vel,  # Within left wall
            player.x < game.screen_width - (player.w + player.vel),   # Within right wall

            game.crash
            
            
            ]

        species = False         # False is cactus
        low = False
        mid = False
        high = False
        dir_ahead_behind = False
        dir_above_below = False
        prox_ahead = False  # enemy 100 pixels away in front
        prox_behind = False
        prox_above = False
        prox_below = False

        prox2_ahead = False  # enemy 200 pixels away in front
        prox2_behind = False
        prox2_above = False
        prox2_below = False

        prox3_ahead = False  # enemy 300 pixels away in front
        prox3_behind = False
        prox3_above = False
        prox3_below = False


        for enemy in enemies:

            if enemy.species == "bird":
                species = True  # True is bird
            if enemy.low_mid_high == 0:
                low = True
            elif enemy.low_mid_high == 1:
                mid = True
            else:
                high = True

            if player.y < enemy.hitbox[1] + enemy.hitbox[3] and player.y + player.h > enemy.hitbox[1]:   # danger on my current y cords
                dir_ahead_behind = True          # Directly ahead/behind

            if player.x + player.w > enemy.hitbox[0] and player.x < enemy.hitbox[0] + enemy.hitbox[2]:   # Danger on x cords
                dir_above_below = True              # Directly above/below

            # a combination of these should identify if enemy is within any direction of dino
            if player.x + player.w < enemy.x and player.x + player.w + 100 > enemy.x:    # an enemy is within the 100 pixels ahead of me
                prox_ahead = True

            if player.x > enemy.x + enemy.w and player.x - 100 < enemy.x + enemy.w:     # an enemy is within 100 pixels behind me
                prox_behind = True

            if player.y > enemy.y + enemy.h and player.y - 100 < enemy.x + enemy.h:     # enemy is within 100 pixels above
                prox_above = True

            if player.y + player.h < enemy.y and player.y + player.h + 100 > enemy.y:   # enemy is within 100 pixels below dino
                prox_below = True

            # a combination of these should identify if enemy is within any direction of dino
            if player.x + player.w < enemy.x and player.x + player.w + 200 > enemy.x:    # an enemy is within the 100 pixels ahead of me
                prox2_ahead = True

            if player.x > enemy.x + enemy.w and player.x - 200 < enemy.x + enemy.w:     # an enemy is within 100 pixels behind me
                prox2_behind = True

            if player.y > enemy.y + enemy.h and player.y - 200 < enemy.x + enemy.h:     # enemy is within 100 pixels above
                prox2_above = True

            if player.y + player.h < enemy.y and player.y + player.h + 200 > enemy.y:   # enemy is within 100 pixels below dino
                prox2_below = True

            # a combination of these should identify if enemy is within any direction of dino
            if player.x + player.w < enemy.x and player.x + player.w + 300 > enemy.x:    # an enemy is within the 100 pixels ahead of me
                prox3_ahead = True

            if player.x > enemy.x + enemy.w and player.x - 300 < enemy.x + enemy.w:     # an enemy is within 100 pixels behind me
                prox3_behind = True

            if player.y > enemy.y + enemy.h and player.y - 300 < enemy.x + enemy.h:     # enemy is within 100 pixels above
                prox3_above = True

            if player.y + player.h < enemy.y and player.y + player.h + 300 > enemy.y:   # enemy is within 100 pixels below dino
                prox3_below = True



        state.append(species)
        state.append(low)
        state.append(mid)
        state.append(high)
        state.append(dir_ahead_behind)
        state.append(dir_above_below)

        state.append(prox_ahead)
        state.append(prox_behind)
        state.append(prox_above)
        state.append(prox_below)

        state.append(prox2_ahead)
        state.append(prox2_behind)
        state.append(prox2_above)
        state.append(prox2_below)

        state.append(prox3_ahead)
        state.append(prox3_behind)
        state.append(prox3_above)
        state.append(prox3_below)

        for i in range(len(state)):
            if state[i]:
                state[i]=1
            else:
                state[i]=0





        #print(np.asarray(state))
        return np.asarray(state)

    def set_reward(self, player, game, crash, record):
        self.reward = 0

        if game.got_dodge_points:
            self.reward = 5  # * game.dodge_points
            game.got_dodge_points = False
            #print(self.reward)         # good for debug

        if game.got_walk_points:
            self.reward = 1  # * game.dodge_points
            game.got_walk_points = False
            #print(self.reward)         # good for debug


        if crash:
            self.reward = -10
            return self.reward

        return self.reward


    def network(self, weights=None):
        model = Sequential()
        model.add(Dense(output_dim=20, activation='relu', input_dim=29))        # max 144
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=20, activation='relu'))
        model.add(Dropout(0.15))

        model.add(Dense(output_dim=4, activation='softmax'))
        opt = Adam(self.learning_rate)
        model.compile(loss='mse', optimizer=opt)

        if weights:
            model.load_weights(weights)
            print("model loaded")
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay_new(self, memory):
        if len(memory) > 1000:
            minibatch = random.sample(memory, 1000)
        else:
            minibatch = memory
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(np.array([next_state]))[0])
            target_f = self.model.predict(np.array([state]))
            target_f[0][np.argmax(action)] = target
            #print(target_f)
            self.model.fit(np.array([state]), target_f, epochs=1, verbose=0)

    def train_short_memory(self, state, action, reward, next_state, done):
        target = reward
        if not done:
            target = reward + self.gamma * np.amax(self.model.predict(next_state.reshape((1, 29)))[0])
        target_f = self.model.predict(state.reshape((1, 29)))
        target_f[0][np.argmax(action)] = target
        self.model.fit(state.reshape((1, 29)), target_f, epochs=1, verbose=0)
