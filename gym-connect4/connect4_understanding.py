import numpy as np  # For 2D array
import random # import random class
import copy
import gym
from gym import spaces, error, utils
from gym.utils import seeding
import math
import gym_connect4
from keras.models     import Sequential
from keras.layers     import Dense
from keras.optimizers import Adam

env = gym.make('Connect4-v0')
env.reset()
MAX_STEPS = 21 # half of 7 x 6 board
SCORE_REQUIREMENT = 1 # This is the score that means Ulima has done well. Could do it as a proportion of wins..?
INITIAL_GAMES = 5

class Ulima():

    def model_data_preparation(self):
        self.training_data = []
        self.accepted_scores = []
        for game_index in range(INITIAL_GAMES): # start by playing 10,000 games
            score = 0
            self.game_memory = []
            self.previous_observation = []

            for step_index in range(MAX_STEPS):
                action = env.action_space.sample() # can we change this to .get_avail_moves
                observation, reward, done, info = env.step(action)

                if len(self.previous_observation) > 0: # store the prev observation if there is one
                    self.game_memory.append([self.previous_observation, action])

                self.previous_observation = observation
                score += reward
                if done:
                    break

            # if score >= SCORE_REQUIREMENT: # only saves won games but should probs also save lost games
            self.accepted_scores.append(score) # if Ulima won the game then one hot encode the last action
            for data in self.game_memory:
                action = data[1]
                hot_move = [0, 0, 0, 0, 0, 0]
                hot_move.insert(action, 1)
                self.training_data.append([data[0], hot_move]) # should this be self.previous_observation in stead of data[0]

            env.reset()

        print(self.accepted_scores)

        return self.training_data


    # def build_model(input_size, output_size):
    #     model = Sequential()
    #     model.add(Dense(128, input_dim=input_size, activation='relu'))
    #     model.add(Dense(52, activation='relu'))
    #     model.add(Dense(output_size, activation='linear'))
    #     model.compile(loss='mse', optimizer=Adam())
    #     return model
    #
    #
    # def train_model(self.training_data):
    #     X = np.array([i[0] for i in self.training_data]).reshape(-1, len(self.training_data[0][0]))
    #     y = np.array([i[1] for i in self.training_data]).reshape(-1, len(self.training_data[0][1]))
    #     model = build_model(input_size=len(X[0]), output_size=len(y[0]))
    #
    #     model.fit(X, y, epochs=10)
    #     return model
    #
    # trained_model = train_model(self.training_data)
