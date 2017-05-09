#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  9 09:58:47 2017

@author: GBP
"""

#start
#stack
#draw
#chip
#call
#raise
#fold
#calculate


class Info():
    
    def __init__(self, player):
        self.name = player
        self.card = 0
        self.chip = 30
        self.bid = 1
        self.mybid = 0
        self.rivalbid = 0
        self.raisebet = 0
        self.result = 'Win'
        
    def initbid(self):
        self.bid = 1  
        
    def get_chip(self):
        return self.chip
    
    def biding(self, mybid):
        self.mybid = int(mybid)
        self.bid += self.mybid
        
    def bid_valid(self):
        if self.bid < 1 or self.bid > self.chip:
            return False
        return True
        
    def call(self, rivalbid):
        self.rivalbid = int(rivalbid)
        self.bid += self.rivalbid
    
    def raisebet(self, myraise):
        self.myraise = int(myraise)
        self.bid += self.myraise
        
    def raisebet_valid(self):
        if self.myraise > self.rivalbid:
            return True
        return False
        
    def fold(self):
        if self.card == 10:
            self.bid += 10
        self.result = 'Lose'
        
    def menu(self):
        #
        pass
    
    def __str__(self):
        if self.result == 'Win':
            return "%s: chip-%s, +%s" % (self.name, self.chip, self.rivalbid)
        else:
            return "%s: chip-%s, -%s" % (self.name, self.chip, self.rivalbid)
        pass

if __name__ == "__main__":
    player1 = Info("A")
    player2 = Info("B")
    player1.biding("2")
    player1.call("2")
    player2.call("2")