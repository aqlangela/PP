# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 00:00:32 2015

@author: zhengzhang
"""
from chat_utils import *

class ClientSM:
    def __init__(self, s):
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.out_msg = ''
        self.s = s
        self.lastrecv = ''
        self.speak = True

    def set_state(self, state):
        self.state = state
        
    def get_state(self):
        return self.state
    
    def set_myname(self, name):
        self.me = name

    def get_myname(self):
        return self.me
        
    def connect_to(self, peer):
        msg = M_CONNECT + peer
        mysend(self.s, msg)
        response = myrecv(self.s)
        if response == (M_CONNECT+'ok'):
            self.peer = peer
            self.out_msg += 'You are connected with '+ self.peer + '\n'
            return (True)
        elif response == (M_CONNECT + 'busy'):
            self.out_msg += 'User is busy. Please try again later\n'
        elif response == (M_CONNECT + 'hey you'):
            self.out_msg += 'Cannot talk to yourself (sick)\n'
        elif response == (M_CONNECT + 'gaming'):
            self.out_msg += 'User is playing. Please try again later\n'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return(False)
        
    def game_with(self, peer):
        msg = M_GCONNECT + peer
        mysend(self.s, msg)
        response = myrecv(self.s)
        if response == (M_GCONNECT +'ok'):
            self.peer = peer
            self.out_msg += 'You are connected with '+ self.peer + '\n'
            return (True)
        elif response == (M_GCONNECT + 'busy'):
            self.out_msg += 'User is busy. Please try again later\n'
        elif response == (M_GCONNECT + 'hey you'):
            self.out_msg += 'Cannot play with yourself (moron)\n'
        elif response == (M_GCONNECT + 'chatting'):
            self.out_msg += 'User is chatting. Please try again later\n'
        elif response == (M_GCONNECT + 'gaming'):
            self.out_msg += 'User is gaming. Please try again later\n'        
        else:
            self.out_msg += 'User is not online, try again later\n'
        return(False)
    
    #???
    def quitgame(self):
        msg = M_QUITGAME
        mysend(self.s, msg)
        self.out_msg += 'You and ' + self.peer + 'quit the game\n'
        self.peer = ''
        
    def disconnect(self):
        msg = M_DISCONNECT
        mysend(self.s, msg)
        self.out_msg += 'You are disconnected from ' + self.peer + '\n'
        self.peer = ''

    def proc(self, my_msg, peer_code, peer_msg):
        self.out_msg = ''
#==============================================================================
# Once logged in, do a few things: get peer listing, connect, search
# And, of course, if you are so bored, just go
# This is event handling instate "S_LOGGEDIN"
#==============================================================================
        if self.state == S_LOGGEDIN:
            # todo: can't deal with multiple lines yet
            if len(my_msg) > 0:
                
                if my_msg == 'q':
                    self.out_msg += 'See you next time!\n'
                    self.state = S_OFFLINE
                    
                elif my_msg == 'time':
                    mysend(self.s, M_TIME)
                    time_in = myrecv(self.s)
                    self.out_msg += "Time is: " + time_in
                            
                elif my_msg == 'who':
                    mysend(self.s, M_LIST)
                    logged_in = myrecv(self.s)
                    self.out_msg += 'Here are all the users in the system:\n'
                    self.out_msg += logged_in
                            
                elif my_msg[0] == 'c':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.connect_to(peer) == True:
                        self.state = S_CHATTING
                        self.out_msg += 'Connect to ' + peer + '. Chat away!\n\n'
                        self.out_msg += '-----------------------------------\n'
                    else:
                        self.out_msg += 'Connection unsuccessful\n'
                        
                elif my_msg[0] == 'g':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.game_with(peer) == True:
                        self.state = S_GAMING
                        self.out_msg += 'Ger ready to play with ' + peer + '!\n\n'
                        self.out_msg += '-----------------------------------\n'
                        self.out_msg += 'Are you ready?(y/n/rec/...)\n'
                        self.out_msg += 'y: Simply start without equipment\n'
                        self.out_msg += 'n: I do not wanna play any more\n'
                        self.out_msg += 'rec: Start with card record machine'
                        self.lastrecv = 'Are you ready?'
                    else:
                        self.out_msg += 'Connection unsuccessful\n'
                        
                elif my_msg[0] == '?':
                    term = my_msg[1:].strip()
                    mysend(self.s, M_SEARCH + term)
                    search_rslt = myrecv(self.s)[1:].strip()
                    if (len(search_rslt)) > 0:
                        self.out_msg += search_rslt + '\n\n'
                    else:
                        self.out_msg += '\'' + term + '\'' + ' not found\n\n'
                        
                elif my_msg[0] == 'p':
                    poem_idx = my_msg[1:].strip()
                    mysend(self.s, M_POEM + poem_idx)
                    poem = myrecv(self.s)[1:].strip()
                    if (len(poem) > 0):
                        self.out_msg += poem + '\n\n'
                    else:
                        self.out_msg += 'Sonnet ' + poem_idx + ' not found\n\n'

                else:
                    self.out_msg += menu
                    
            if len(peer_msg) > 0:
                if peer_code == M_CONNECT:
                    self.peer = peer_msg
                    self.out_msg += 'Request from ' + self.peer + '\n'
                    self.out_msg += 'You are connected with ' + self.peer 
                    self.out_msg += '. Chat away!\n\n'
                    self.out_msg += '------------------------------------\n'
                    self.state = S_CHATTING
                    
                elif peer_code == M_GCONNECT:
                    self.peer = peer_msg
                    self.out_msg += '[Game System]' + 'Request from ' + self.peer + '\n'
                    self.out_msg += 'You are connected with ' + self.peer 
                    self.out_msg += 'Are you ready?(y/n/rec/...)\n'
                    self.out_msg += 'y: Simply start without equipment\n'
                    self.out_msg += 'n: I do not wanna play any more\n'
                    self.out_msg += 'rec: Start with card record machine'
                    self.lastrecv = 'Are you ready?'
                    self.state = S_GAMING

#==============================================================================
# Start chatting, 'bye' for quit
# This is event handling instate "S_CHATTING"
#==============================================================================
        elif self.state == S_CHATTING:
            if len(my_msg) > 0:     # my stuff going out
                mysend(self.s, M_EXCHANGE + "[" + self.me + "] " + my_msg)
                if my_msg == 'bye':
                    self.disconnect()
                    self.state = S_LOGGEDIN
                    self.peer = ''
            if len(peer_msg) > 0:    # peer's stuff, coming in
                if peer_code == M_CONNECT:
                    self.out_msg += "(" + peer_msg + " joined)\n"
                else:
                    self.out_msg += peer_msg

            # I got bumped out
            if peer_code == M_DISCONNECT:
                self.state = S_LOGGEDIN

            # Display the menu again
            if self.state == S_LOGGEDIN:
                self.out_msg += menu
#==============================================================================
# S_GAMING
#==============================================================================
        elif self.state == S_GAMING:
            if len(my_msg) > 0 and self.speak == True:
                if self.lastrecv == 'Are you ready?' or ('Play again?(y/n/rec/...)' in self.lastrecv):
                    if my_msg == 'n':
                        self.quitgame()
                        self.state = S_LOGGEDIN
                        self.peer = ''
                    elif my_msg == 'y' or my_msg == 'rec' or my_msg == 'cheat':
                        mysend(self.s, M_GAME + my_msg)
                        self.speak = False
                        self.out_msg += 'You are ready.'
                    else:
                        self.out_msg += 'Invalid reply. Try again.'
                elif self.lastrecv == 'Bid or Fold?':
                    if my_msg[0:4] == 'bid ':
                        if my_msg[4:].isdigit:
                            mysend(self.s, M_GAME + my_msg)
                            self.speak = False
                        else:
                            self.out_msg += 'Invalid bid, plesase input "bid number"'
                    elif my_msg == 'fold':
                        mysend(self.s, M_GAME + my_msg)
                        self.speak = False
                    else:
                        self.out_msg += 'Invalid reply. Try again.'
                    if self.speak == False:
                        self.out_msg = 'Operate successfully. Waiting for your rival'
                
                elif 'Call? Raise? Fold?' in self.lastrecv:
                    if my_msg == 'call':
                        mysend(self.s, M_GAME + my_msg)
                        self.speak = False
                    elif my_msg[0:6] == 'raise ':
                        if my_msg[6:].isdigit:
                            mysend(self.s, M_GAME + my_msg)
                            self.speak = False
                        else:
                            self.out_msg += 'Invalid raise, plesase input "raise number"'
                    elif my_msg == 'fold':
                        mysend(self.s, M_GAME + my_msg)
                        self.speak = False
                    else:
                        self.out_msg += 'Invalid reply. Try again.'
                    if self.speak == False:
                        self.out_msg = 'Operate successfully. Waiting for your rival'
                elif self.lastrecv == 'Press any key to continue':
                    mysend(self.s, M_GAME + my_msg)
                    self.speak = False
                    self.out_msg = 'Operate successfully.'
                
                
            if len(peer_msg) > 0:
                if peer_msg[-1] != '#':
                    self.speak = False
                    self.out_msg += ('[Game System]' + peer_msg)
                else:
                    self.speak = True
                    peer_msg = peer_msg[: -1]
                    if peer_msg == 'Your rival is ready!':
                        pass
                    else:
                        self.lastrecv = peer_msg
                    self.out_msg += ('[Game System]' + peer_msg)
            
            if peer_code == M_QUITGAME:
                self.out_msg += 'You quitted from game.'
                self.state = S_LOGGEDIN

            # Display the menu again
            if self.state == S_LOGGEDIN:
                self.out_msg += menu
#==============================================================================
# invalid state                       
#==============================================================================
        else:
            self.out_msg += 'How did you wind up here??\n'
            print_state(self.state)
            
        return self.out_msg
