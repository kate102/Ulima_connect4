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
max_steps = 21 # half of 7 x 6 board
score_requirement = 1 # This is the score that means Ulima has done well
intial_games = 10000

def model_data_preparation():
    training_data = []
    accepted_scores = []
    for game_index in range(intial_games): # start by playing 10,000 games
        score = 0
        game_memory = []
        previous_observation = []
        for step_index in range(max_steps):
            action = env.action_space.sample() # can we change this to .get_avail_moves
            observation, reward, done, info = env.step(action)

            if len(previous_observation) > 0: # store the prev observation if there is one
                game_memory.append([previous_observation, action])

            previous_observation = observation
            score += reward
            if done:
                break

        if score >= score_requirement:
            accepted_scores.append(score) # if Ulima won the game then one hot encode the last action
            for data in game_memory:
                action = data[1]
                output = [0, 0, 0, 0, 0, 0]
                output.insert(action, 1)
                training_data.append([data[0], output])

        env.reset()

    print(accepted_scores)

    return training_data


# def build_model(input_size, output_size):
#     model = Sequential()
#     model.add(Dense(128, input_dim=input_size, activation='relu'))
#     model.add(Dense(52, activation='relu'))
#     model.add(Dense(output_size, activation='linear'))
#     model.compile(loss='mse', optimizer=Adam())
#     return model
#
#
# def train_model(training_data):
#     X = np.array([i[0] for i in training_data]).reshape(-1, len(training_data[0][0]))
#     y = np.array([i[1] for i in training_data]).reshape(-1, len(training_data[0][1]))
#     model = build_model(input_size=len(X[0]), output_size=len(y[0]))
#
#     model.fit(X, y, epochs=10)
#     return model
#
# trained_model = train_model(training_data)
