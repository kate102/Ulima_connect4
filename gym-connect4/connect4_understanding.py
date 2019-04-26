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
from keras.layers import Dropout

env = gym.make('Connect4-v0')
env.reset()
MAX_STEPS = 21 # half of 7 x 6 board
SCORE_REQUIREMENT = 1 # This is the score that means Ulima has done well. Could do it as a proportion of wins..?
INITIAL_GAMES = 4
rand = random.Random()

class TrainUlima():

    def model_data_preparation(self):
        # for each play we want to store the state of the board and the move
        self.board_data = []
        self.action_data =[]
        self.accepted_scores = []
        self.scores = []

        for _ in range(INITIAL_GAMES): # start by playing 10,000 games
            # score = 0
            self.previous_observation = []
            self.current_game_boards = []
            self.current_game_actions = []

            for _ in range(MAX_STEPS):
                # action = env.action_space.sample() # can we change this to .get_avail_moves
                action = rand.choice(env.get_avail_moves())
                observation, reward, done, _ = env.step(action)

                # hot_action is the current Ulima move
                hot_action = [0, 0, 0, 0, 0, 0]
                hot_action.insert(action, 1)

                copy_observation = copy.deepcopy(observation)

                self.current_game_boards.append(copy_observation)
                self.current_game_actions.append(hot_action)
                if reward == 1:
                    self.board_data += self.current_game_boards
                    self.action_data += self.current_game_actions

                if done:
                    break

            env.reset()

        return self.board_data, self.action_data


    def train_model(self):
        X_data, y = self.model_data_preparation()
        X = []
        for i in X_data:
            X.append(i.reshape(1, 42)[0]) # Check this works    
        X=np.array(X)
        y=np.array(y)
        first_board = X[0]
        first_board[first_board == -1] = 0
        first_board[first_board == 1] = 0
        y[y == -1] = 2
        print(first_board)
        model = self.build_model(input_size=first_board, output_size=first_board)
        model.fit([X], y, epochs=10)

        return model

    def build_model(self, input_size, output_size):
        model = Sequential()
        model.add(Dense(10, input_shape=(7,6,), activation='relu'))
        model.add(Dropout(0.6))
        model.add(Dense(10, activation='relu'))
        model.add(Dropout(0.6))
        # model.add(Dense(10, activation='relu'))
        # model.add(Dropout(0.6))
        # model.add(Dense(256, activation='relu'))
        # model.add(Dropout(0.6))
        # model.add(Dense(128, activation='relu'))
        # model.add(Dropout(0.6))
        model.add(Dense(2, activation='softmax'))
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        return model

u = TrainUlima()
trained_model = u.train_model()
