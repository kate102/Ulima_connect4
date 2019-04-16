import numpy as np  # For 2D array
import random # import random class

rand = random.Random()

class Connect4():
    NUM_ROWS = 6
    NUM_COLS = 7
    NUM2WIN = 4
    def __init__(self): # initialize
        self.board = np.zeros((self.NUM_ROWS, self.NUM_COLS)) # define board with number of rows and columns

    def __str__(self): # dunder string method to display the board for use with ASCII. Called automatically.
        str_board = "\n\n" + str(self.board).replace("0.", "_").replace("-1.", " O").replace("1.", "X")
        str_board = str_board.replace("[", " ").replace("]", " ")
        return str_board

    def get_avail_moves(self): # returns columns that are available
        return [m for m in range(self.NUM_COLS) if self.board[0][m] == 0] # check top row for empty

    def make_move(self, move): # sum of the rows and columns
        if np.sum(self.board) == 0: #if the sum is 0 it's player1
            player = 1 # if sum is 1 it's player 2 turn
        else:
            player = -1

        j = 0
        while j+1 < self.NUM_ROWS and self.board[j+1][move] == 0: j+=1 # if it's available

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


def main():
    XO = {-1: "O", 0: "Nobody", 1: "X"}
    my_game = Connect4()
    moves = my_game.get_avail_moves()
    print(my_game)
    player = 1 # first player is alway 1, but 1 is randomly assign to human or computer
    human_player = rand.choice([1, -1]) #randomise if the human player is O or X
    while moves != []: #loop until the board is full (so as long as we can make a move)

        if player == human_player:
            print(f"Available moves are: {moves}")
            move = int(input("Enter move human: "))
        else:
            move = rand.choice(moves)
        my_game.make_move(move)
        print(my_game)
        winner =  my_game.get_winner()
        if winner:
            print(f"{XO[player]} Wins!")
            break
        moves = my_game.get_avail_moves()
        player = -player #switches between human and computer


if __name__ == "__main__":
    main()
