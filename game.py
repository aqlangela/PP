#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import playerinfo as info

class Game:
    
    def __init__(self, player1, player2):
        self.player1 = info.Info(player1)
        self.player2 = info.Info(player2)
        self.stack = [1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10]
        '''self.record = {self.player1:[(0, 0, 0) for i in range(10)], \
                                     self.player2:[(0, 0, 0) for i in range(10)]}'''
    
    def stackupdate(self):
        self.stack = [1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10]

    def initbid(self):
        return 'Your initial bid is 1 chip'
    
    def deal(self):
        if self.stack == []:
            self.stackupdate()
        self.player1.card = random.choice(self.stack)
        self.stack.remove(self.player1.card)
        self.player2.card = random.choice(self.stack)
        self.stack.remove(self.player2.card)
        
    def showcard(self, i):
        if i == 1:
            s = "Your rival's card is " + str(self.player1.card)
        else:
            s = "Your rival's card is " + str(self.player2.card)
        return s
    
    def reveal(self, i):
        if i == 1:
            s = "Your own card is " + str(self.player1.card)
        else:
            s = "Your own card is " + str(self.player2.card)
        return s
    
    def call(self, i):
        if i == 1:
            self.player1.bid = self.player2.bid
        else:
            self.player2.bid = self.player1.bid
        return 
    
    def record(self):
        return 'Card in the stack:' + str(self.stack)
        
    def compare(self):
        if self.player1.card > self.player2.card:
            self.player2.result = 'Lose'
        elif self.player1.card < self.player2.card:
            self.player1.result = 'Lose'
        else:
            self.player1.result = 'Draw'
            self.player2.result = 'Draw'
    #是直接在server还是在这里？
    def calculate(self):
        if self.player1.result == 'Lose':
            self.player1.chip -= self.player1.bid
            self.player2.chip += self.player1.bid
            self.player1.bid = 0
            self.player2.bid = 0
        elif self.player2.result == 'Lose':
            self.player2.chip -= self.player2.bid
            self.player1.chip += self.player2.bid
            self.player1.bid = 0
            self.player2.bid = 0
        self.player1.card = 0
        self.player2.card = 0
        
    def show(self):
        msg = ''
        msg += 'Player 1: Chip Owned: ' + str(self.player1.get_chip())
        msg += ' Chip on the table: ' + str(self.player1.get_bid() + '\n')
        msg += 'Player 2: Chip Owned: ' + str(self.player2.get_chip())
        msg += ' Chip on the table: ' + str(self.player2.get_bid() + '\n')
        return msg
        
'''if __name__ == "__main__":
    game = Game("a", "b")
    game.deal()
    print(game.showcard(2))
    print(game.record())
    print(game.player1.card)
    print(game.player2.card)
    game.player1.biding(1)
    game.call(1)
    game.compare()
    game.calculate()
    print(game.player1.get_chip())
    print(game.player2.chip)'''