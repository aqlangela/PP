#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#start
#stack
#draw
#chip
#call
#raise
#fold
#calculate

class Info:
    
    def __init__(self, player):
        self.name = player
        self.card = 0
        self.chip = 30
        self.bid = 0
        self.rbid = 0
        #for every one bet
        self.mybid = 0
        self.myraise = 0
        self.result = ''
        
    def initbid(self):
        self.bid += 1  
        
    def get_chip(self):
        return self.chip
    
    def get_bid(self):
        return self.bid
        
    def get_result(self):
        return self.result
    
    def biding(self, mybid):
        self.mybid = mybid
        if self.bid_valid():
            self.bid += self.mybid
        else: 
            return "Invalid biding. Please bid again."
        
    def bid_valid(self):
        if self.mybid < 1 or (self.bid + self.mybid) > self.chip:
            return False
        return True
        
    def raisebet(self, myraise):
        self.myraise = myraise
        if self.raisebet_valid():
            self.bid = self.myraise + 1
        
    def raisebet_valid(self):
        if (self.myraise + 1 > self.rbid) and (self.myraise + 1 <= self.get_chip()):
            return True
        return False
        
    def fold(self):
        if self.card == 10:
            self.bid += 10
        self.result = 'Lose'
        
    def __str__(self):
        return self.name

'''if __name__ == "__main__":
    player1 = Info("A")
    player2 = Info("B")
    player1.biding(2)
    print(player1)'''
    