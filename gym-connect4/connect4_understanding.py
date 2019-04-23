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
INITIAL_GAMES = 4
rand = random.Random()

class TrainUlima():

    def model_data_preparation(self):
        # for each play we want to store the state of the board and the move
        self.training_data = []
        self.accepted_scores = []
        self.scores = []

        for _ in range(INITIAL_GAMES): # start by playing 10,000 games
            # score = 0
            self.previous_observation = []
            self.current_game = []

            for _ in range(MAX_STEPS):
                # action = env.action_space.sample() # can we change this to .get_avail_moves
                action = rand.choice(env.get_avail_moves())
                observation, reward, done, _ = env.step(action)

                # hot_action is the current Ulima move
                hot_action = [0, 0, 0, 0, 0, 0]
                hot_action.insert(action, 1)

                copy_observation = copy.deepcopy(observation)
                game_snapshot = []
                game_snapshot.append([copy_observation, hot_action])
                self.current_game  += game_snapshot
                if reward == 1:
                    self.training_data += self.current_game

                # score += reward
                # self.accepted_scores.append(score) # maybe can get rid of score and just add reward.
                if done:
                    break

            env.reset()

        # for _ in range(len(self.accepted_scores)):
        #     self.scores.append(reward)
        # self.accepted_scores = self.scores
        # print(self.accepted_scores)
        return self.training_data


    def train_model(self, training_data):
        for i in training_data:
            # print("This is training data ...")
            # print(i)
            X = i[0].reshape(-1, 42)[0]
            y = i[1]
        model = self.build_model(input_size=len(X), output_size=len(y))

        model.fit(X, y, epochs=10)
        return model

    def build_model(self, input_size, output_size):
        model = Sequential()
        model.add(Dense(128, input_dim=input_size, activation='relu'))
        model.add(Dense(52, activation='relu'))
        model.add(Dense(output_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam())
        return model

u = TrainUlima()
trained_model = u.train_model(u.model_data_preparation())
