#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
        self.result = 'Win'
        
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
        self.bid += self.mybid
        
    def raisebet(self, myraise):
        self.myraise = myraise
        self.bid = self.rbid + self.myraise
        
    def fold(self):
        if self.card == 10:
            self.bid += 10
        self.result = 'Lose'
        
    def __str__(self):
        return self.name

    
