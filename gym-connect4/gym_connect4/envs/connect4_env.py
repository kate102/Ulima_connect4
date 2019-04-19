import numpy as np  # For 2D array
import random # import random class
import copy
import gym
import math
from gym import spaces, error

rand = random.Random()

class Connect4Env(gym.Env):
    NUM_ROWS = 6
    NUM_COLS = 7
    NUM2WIN = 4
    def __init__(self): # initialize
        self.board = np.zeros((self.NUM_ROWS, self.NUM_COLS)) # define board with number of rows and columns
        self.ulima_player = rand.choice([1, -1]) #randomise if the ulima player is O or X

    def step(self, move):
        if move not in self.get_avail_moves():
            raise Exception("Invalid move: {}".format(move))

        self.last_board = copy.deepcopy(self.board)

        self.player_make_move(1, move) # player 1 always goes first. Player 1 is randomised between ulima and computer.
        if self.done == False:
            self.player_make_move(-1, move)
        return self.state, self.reward, self.done, {}

    def reset(self):
        self.__init__()

    def render(self, arg):
        True

    def player_make_move(self, player, move):
        moves = self.get_avail_moves()
        if player == self.ulima_player:
            move_choice = move
        else:
            move_choice = rand.choice(moves)
        self.make_move(move_choice)
        winner = self.get_winner()
        self.reward = 0
        self.done = False
        self.state = self.board
        if winner:
            self.done = True
            print('GAME ENDS')
            if player == self.ulima_player:
                self.reward = 1
                print('ULIMA WON')

    def __str__(self): # dunder string method to display the board for use with ASCII. Called automatically.
        str_board = "\n\n" + str(self.board).replace("0.", "_").replace("-1.", " O").replace("1.", "X")
        str_board = str_board.replace("[", " ").replace("]", " ")
        return str_board

    def get_avail_moves(self): # returns columns that are available
        return [m for m in range(self.NUM_COLS) if self.board[0][m] == 0] # check top row for empty

    def make_move(self, move): # sum of the rows and columns
        if np.sum(self.board) == 0: #if the sum is 0 it's player1
            player = 1 # if sum is 1 it's player -1 turn
        else:
            player = -1

        j = 0
        while j+1 < self.NUM_ROWS and self.board[j+1][move] == 0: j+=1 # how far down it goes

        self.board[j][move] = player # puts -1 or 1 in the empty cell

    def get_winner(self): # check every 4x4 subboard
        for i in range(self.NUM_ROWS-self.NUM2WIN+1): #(6-4) + 1) suboard of 4 upto where start point is num2win away from end of board
            for j in range(self.NUM_COLS-self.NUM2WIN+1): #(7-4) + 1
                subboard = self.board[i:i+self.NUM2WIN, j:j+self.NUM2WIN]
                if np.max(np.abs(np.sum(subboard, 0))) == self.NUM2WIN: # check the vertical; if the sum of the values in column is abs(4) then win (the sum will never be more
                    return True                                            # than 4, and if it's less then 4 then it's obviously not a win)
                if np.max(np.abs(np.sum(subboard, 1))) == self.NUM2WIN: # check the horizontal (same for vertical)
                    return True
                elif np.abs(sum([subboard[k, k] for k in range(self.NUM2WIN)])) == self.NUM2WIN: # diaganol
                    return True
                elif np.abs(sum([subboard[k, self.NUM2WIN-1-k] for k in range(self.NUM2WIN)])) == self.NUM2WIN: # opp diaganol
                    return True
        return False
