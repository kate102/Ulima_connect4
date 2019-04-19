import numpy as np  # For 2D array
import random # import random class
import copy
import gym
import math
import gym_connect4

env = gym.make('Connect4-v0')
env.reset()
for step_index in range(21):
    env.render()
    action = env.action_space.sample()
    observation, reward, done, info = env.step(action)
    print("Step {}:".format(step_index))
    print("action: {}".format(action))
    print("observation: {}".format(observation))
    print("reward: {}".format(reward))
    print("done: {}".format(done))
    print("info: {}".format(info))
    if done:
        break
