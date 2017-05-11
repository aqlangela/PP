#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import playerinfo as info

class Game:
    
    def __init__(self, player1, player2):
        self.player1 = info.Info(player1)
        self.player2 = info.Info(player2)
        self.stack = [1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10]
        self.record = {self.player1:[(0, 0, 0) for i in range(10)], \
                                     self.player2:[(0, 0, 0) for i in range(10)]}

    
    def deal(self):
        self.player1.card = random.choice(self.stack)
        self.stack.remove(self.player1.card)
        self.player2.card = random.choice(self.stack)
        self.stack.remove(self.player2.card)
        
    def show(self, to_name, from_name):
        pass
        
    def reveal(self):
        return 
        
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
        elif self.player2.result == 'Lose':
            self.player2.chip -= self.player2.bid
            self.player1.chip += self.player2.bid
        self.player1.initbid()
        self.player2.initbid()
        
    def show(self):
        print(self.player1.get_chip(), self.player2.get_chip())
    
if __name__ == "__main__":
    game = Game("a", "b")
    game.deal()
    print(game.player1.card)
    print(game.player2.card)
    game.player1.biding("1")
    game.player2.call("1")
    game.calculate()
    print(game.player1.get_chip())
    print(game.player2.chip)