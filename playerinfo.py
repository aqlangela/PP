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
        self.bid = 1
        self.rbid = 0
        #for every one bet
        self.mybid = 0
        self.myraise = 0
        self.result = 'Win'
        
    def initbid(self):
        self.bid = 1  
        
    def get_chip(self):
        return self.chip
        
    def get_result(self):
        return self.result
    
    def biding(self, mybid):
        self.mybid = int(mybid)
        if self.bid_valid():
            self.bid += self.mybid
        else: 
            return "Invalid biding. Please bid again."
        
    def bid_valid(self):
        if self.mybid < 1 or (self.bid + self.mybid) > self.chip:
            return False
        return True
        
    def call(self, rbid):
        self.rbid = int(rbid)
        self.bid += self.rbid

    def raisebet(self, myraise):
        self.myraise = int(myraise)
        if self.raisebet_valid():
            self.bid += self.myraise
        
    def raisebet_valid(self):
        if (self.myraise + self.bid) > self.rbid:
            return True
        return False
        
    def fold(self):
        if self.card == 10:
            self.bid += 10
        self.result = 'Fold Lose'
        
    def __str__(self):
        return self.name

if __name__ == "__main__":
    player1 = Info("A")
    player2 = Info("B")
    player1.biding("2")
    player1.call("2")
    player2.call("2")
    print(player1)
    