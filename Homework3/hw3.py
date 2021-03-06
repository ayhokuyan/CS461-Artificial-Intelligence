# -*- coding: utf-8 -*-
"""Untitled4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aisRsdbKIrj3rbtZLYjcbou3Y7vN8G-X
"""

'''
In this code we take alpha-beta pruning code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python/
for getting child nodes we add an counter with a name isThisEndOfRecursion also for getting initial board situation we use maxValue and
minValue parameters.
1. Ayhan Okuyan
2. Barış Akçin
3. Berkan Özdamar
4. Deniz Doğanay
5. Mustafa Bay
'''
class Game:
    def __init__(self):
        self.initialize_game()
        self.depth = 0

        #list that holds all child states according to depth
        self.childState = list()

        #check for end of recursion
        self.isThisEndOfRecursion = 0

    #Set the current state of the game and make player X the first player
    def initialize_game(self):
        self.current_state = [['_','_','_'],
                              ['_','_','_'],
                              ['_','_','_']]

        # Player X is the first player
        self.player_turn = 'X'

    #Update the board with current state
    def draw_board(self):
        for i in range(0, 3):
            for j in range(0, 3):
                print('{}|'.format(self.current_state[i][j]), end=" ")
            print()
        print()



    # Checks if the game has ended and returns the winner or draw in each case
    def is_end(self):
        # Vertical win
        for i in range(0, 3):
            if (self.current_state[0][i] != '_' and
                self.current_state[0][i] == self.current_state[1][i] and
                self.current_state[1][i] == self.current_state[2][i] and
                self.current_state[0][i] == self.current_state[2][i]):
                return self.current_state[0][i]

        # Horizontal win
        for i in range(0, 3):
            if (self.current_state[i][0] != '_' and
                self.current_state[i][0] == self.current_state[i][1] and
                self.current_state[i][1] == self.current_state[i][2] and
                self.current_state[i][0] == self.current_state[i][2]):
                return self.current_state[i][0]

        # Main diagonal win
        if (self.current_state[0][0] != '_' and
            self.current_state[0][0] == self.current_state[1][1] and
            self.current_state[0][0] == self.current_state[2][2] and
            self.current_state[1][1] == self.current_state[2][2]):
            return self.current_state[0][0]

        # Second diagonal win
        if (self.current_state[0][2] != '_' and
            self.current_state[0][2] == self.current_state[1][1] and
            self.current_state[0][2] == self.current_state[2][0] and
            self.current_state[1][1] == self.current_state[2][0]):
            return self.current_state[0][2]

        # Check whether the board is full or not
        for i in range(0, 3):
            for j in range(0, 3):
                # if there's an empty field, we continue the game
                if (self.current_state[i][j] == '_'):
                    return None

        # If none of these above, then the game is tie. so return;
        return '_'

    # alpha beta pruning for the max player. Returns maxValue and position of that maxValue with posX and posY.
    # when the boolean variable active is True, it turns on alpha-beta pruning. it it is false, code only uses minimax.
    def max_alpha_beta(self, alpha, beta, active):

        # Since the minimum value can be -1 which is lose, we initially set our maxValue to -2 instead of -inf.
        maxValue = -2
        # position of maxValue with respect to posX and posY are initially set to None.
        posX = None
        posY = None

        result = self.is_end()

        if result == 'X':
            self.isThisEndOfRecursion = self.isThisEndOfRecursion - 1
            return (-1, 0, 0)
        elif result == 'O':
            self.isThisEndOfRecursion = self.isThisEndOfRecursion - 1
            return (1, 0, 0)
        elif result == '_':
            self.isThisEndOfRecursion = self.isThisEndOfRecursion - 1
            return (0, 0, 0)

        # For every possible valid space, play O and check values until it reaches endgame. Then evaluate each state value.
        for i in range(0, 3):
            for j in range(0, 3):
                if self.current_state[i][j] == '_':
                    self.current_state[i][j] = 'O'
                    self.isThisEndOfRecursion = self.isThisEndOfRecursion + 1
                    (minValue, alphaMin, betaMin) = self.min_alpha_beta(alpha, beta, True)
                    if self.isThisEndOfRecursion == 1:
                      print(-minValue)

                    # Check child nodes to update maxValue and position of it.
                    if minValue > maxValue:
                        maxValue = minValue
                        posX = i
                        posY = j
                    self.current_state[i][j] = '_'

                    # Evalueate the state values using alpha-beta pruning.
                    if ( active == True ):
                        if maxValue >= beta:
                            self.isThisEndOfRecursion = self.isThisEndOfRecursion - 1
                            return (maxValue, posX, posY)

                        if maxValue > alpha:
                            alpha = maxValue
        self.isThisEndOfRecursion = self.isThisEndOfRecursion - 1
        return (maxValue, posX, posY)


    # alpha beta pruning for the min player. Returns maxValue and position of that minValue with pos_X and pos_Y.
    # when the boolean variable active is True, it turns on alpha-beta pruning. it it is false, code only uses minimax.
    def min_alpha_beta(self, alpha, beta, active):

        # Since the maximum value can be 1 which is win, we initially set our maxValue to 2 instead of inf.
        minValue = 2
        # position of minValue with respect to posX and posY are initially set to None.
        pos_X = None
        pos_Y = None

        result = self.is_end()

        if result == 'X':
            self.isThisEndOfRecursion = self.isThisEndOfRecursion - 1
            return (-1, 0, 0)
        elif result == 'O':
            self.isThisEndOfRecursion = self.isThisEndOfRecursion - 1
            return (1, 0, 0)
        elif result == '_':
            self.isThisEndOfRecursion = self.isThisEndOfRecursion - 1
            return (0, 0, 0)

        # For every possible valid space, play X and check values until it reaches endgame. Then evaluate each state value.
        for i in range(0, 3):
            for j in range(0, 3):
                if self.current_state[i][j] == '_':
                    self.current_state[i][j] = 'X'
                    self.isThisEndOfRecursion = self.isThisEndOfRecursion + 1
                    (maxValue, alphaMax, betaMax) = self.max_alpha_beta(alpha, beta, True)
                    if self.isThisEndOfRecursion == 1:
                      print(-maxValue)

                    # Check child nodes to update minValue and position of it.
                    if maxValue < minValue:

                        minValue = maxValue
                        pos_X = i
                        pos_Y = j

                    self.current_state[i][j] = '_'

                    # Evalueate the state values using alpha-beta pruning.
                    if ( active == True ):
                        if minValue <= alpha:
                            self.isThisEndOfRecursion = self.isThisEndOfRecursion - 1
                            return (minValue, pos_X, pos_Y)

                        if minValue < beta:
                            beta = minValue
        self.isThisEndOfRecursion = self.isThisEndOfRecursion - 1
        return (minValue, pos_X, pos_Y)

    # This fucntion makes AI play both O and X checking the maxValue and minValues and make best decision for both players.
    def play_alpha_beta(self):

        while True:
            self.draw_board()
            print("Child states are")
            self.result = self.is_end()

            # Player X wins
            if self.result != None and self.result == 'X':
                print("Current state is 1")
                print('The winner is X!')

            # Player O wins.
            if self.result != None and self.result == 'O':
                print("Current state is -1")
                print('The winner is O!')

            # The game is a tie.
            if self.result != None and self.result == '_':
                print("Current state is 0")
                print("It's a tie!")


            if self.result != None:
                self.initialize_game()
                return

            # Player X's turn.
            if self.player_turn == 'X':
                self.isThisEndOfRecursion = self.isThisEndOfRecursion + 1
                (minValue, pos_X, pos_Y) = self.min_alpha_beta(-2, 2, True)
                self.current_state[pos_X][pos_Y] = 'X'
                print()
                print('Current State is {}'.format(minValue), end=" ")
                print()
                self.player_turn = 'O'

            # player O's turn.
            else:
                self.isThisEndOfRecursion = self.isThisEndOfRecursion + 1
                (maxValue, posX, posY) = self.max_alpha_beta(-2, 2, True)
                self.current_state[posX][posY] = 'O'
                print()
                print('Current State is {}'.format(maxValue), end=" ")
                print()
                self.player_turn = 'X'

            # Makes the game wait for your command.
            temp = input('Press Enter to Continue: ')

def main():
    g = Game()
    g.play_alpha_beta()

if __name__ == "__main__":
    main()