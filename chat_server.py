import time
import socket
import select
import sys
import string
import indexer
import pickle as pkl
from chat_utils import *
import chat_group as grp
import game as gm

class Server:
    def __init__(self):
        self.new_clients = [] #list of new sockets of which the user id is not known
        self.logged_name2sock = {} #dictionary mapping username to socket
        self.logged_sock2name = {} # dict mapping socket to user name
        self.all_sockets = []
        self.group = grp.Group()
        #start server
        self.server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(SERVER)
        self.server.listen(5)
        self.all_sockets.append(self.server)
        #initialize past chat indices
        self.indices={}
        # sonnet
        self.sonnet_f = open('AllSonnets.txt.idx', 'rb')
        self.sonnet = pkl.load(self.sonnet_f)
        self.sonnet_f.close()
        # game
        self.player1 = ""
        self.player2 = ""
        self.game = None
        self.lastsend1 = ''
        self.lastsend2 = ''
        self.ready = {}
        self.record = {1:0, 2:0}
        self.cheat = {1:0, 2:0}
        self.banker = None
        self.round = 1
        
    def get_round(self):
        return str(self.round)
        
    def new_client(self, sock):
        #add to all sockets and to new clients
        print('new client...')
        sock.setblocking(0)
        self.new_clients.append(sock)
        self.all_sockets.append(sock)

    def login(self, sock):
        #read the msg that should have login code plus username
        msg = myrecv(sock)
        if len(msg) > 0:
            code = msg[0]

            if code == M_LOGIN:
                name = msg[1:]
                if self.group.is_member(name) != True:
                    #move socket from new clients list to logged clients
                    self.new_clients.remove(sock)
                    #add into the name to sock mapping
                    self.logged_name2sock[name] = sock
                    self.logged_sock2name[sock] = name
                    #load chat history of that user
                    if name not in self.indices.keys():
                        try:
                            self.indices[name]=pkl.load(open(name+'.idx','rb'))
                        except IOError: #chat index does not exist, then create one
                            self.indices[name] = indexer.Index(name)
                    print(name + ' logged in')
                    self.group.join(name)
                    mysend(sock, M_LOGIN + 'ok')
                else: #a client under this name has already logged in
                    mysend(sock, M_LOGIN + 'duplicate')
                    print(name + ' duplicate login attempt')
            else:
                print ('wrong code received')
        else: #client died unexpectedly
            self.logout(sock)

    def logout(self, sock):
        #remove sock from all lists
        name = self.logged_sock2name[sock]
        pkl.dump(self.indices[name], open(name + '.idx','wb'))
        del self.indices[name]
        del self.logged_name2sock[name]
        del self.logged_sock2name[sock]
        self.all_sockets.remove(sock)
        self.group.leave(name)
        sock.close()

#==============================================================================
# main command switchboard
#==============================================================================
    def handle_msg(self, from_sock):
        #read msg code 
        msg = myrecv(from_sock)
        if len(msg) > 0:
            code = msg[0]           
#==============================================================================
# handle connect request
#==============================================================================
            if code == M_CONNECT:
                to_name = msg[1:]
                from_name = self.logged_sock2name[from_sock]
                if to_name == from_name:
                    msg = M_CONNECT + 'hey you'
                # connect to the peer
                elif self.group.is_member(to_name):
                    to_sock = self.logged_name2sock[to_name]
                    self.group.connect(from_name, to_name)
                    the_guys = self.group.list_me(from_name)
                    msg = M_CONNECT + 'ok'
                    for g in the_guys[1:]:
                        to_sock = self.logged_name2sock[g]
                        mysend(to_sock, M_CONNECT + from_name)
                elif self.group.is_gaming(to_name):
                    msg = M_CONNECT + 'gaming'
                else:
                    msg = M_CONNECT + 'no_user'
                mysend(from_sock, msg)
                
            if code == M_GCONNECT:
                to_name = msg[1:]
                from_name = self.logged_sock2name[from_sock]
                if to_name == from_name:
                    msg = M_GCONNECT + 'hey you'
                elif self.group.is_alone(to_name):
                    to_sock = self.logged_name2sock[to_name]
                    self.group.game_connect(from_name, to_name)
                    msg = M_GCONNECT + 'ok'
                    self.player1 = from_name
                    self.player2 = to_name
                    self.game = gm.Game(self.player1, self.player2)
                    to_sock = self.logged_name2sock[to_name]
                    self.lastsend1 = 'ok'
                    self.lastsend2 = 'ok'
                    mysend(to_sock, M_GCONNECT + from_name)
                elif self.group.is_chatting(to_name):
                    msg = M_GCONNECT + 'chatting'
                elif self.group.is_gaming(to_name):
                    msg = M_GCONNECT + 'gaming'
                else:
                    msg = M_GCONNECT + 'no_user'
                mysend(from_sock, msg)   
#==============================================================================
# handle message exchange   
#==============================================================================
            elif code == M_EXCHANGE:
                from_name = self.logged_sock2name[from_sock]
                the_guys = self.group.list_me(from_name)
                said = msg[1:]
                said2 = text_proc(said, from_name)
                self.indices[from_name].add_msg_and_index(said2)
                for g in the_guys[1:]:
                    to_sock = self.logged_name2sock[g]
                    self.indices[g].add_msg_and_index(said2)                
                    mysend(to_sock, msg)
#==============================================================================
#listing available peers
#==============================================================================
            elif code == M_LIST:
                from_name = self.logged_sock2name[from_sock]
                msg = self.group.list_all()
                mysend(from_sock, msg)
#==============================================================================
#retrieve a sonnet
#==============================================================================
            elif code == M_POEM:
                poem_indx = int(msg[1:])
                from_name = self.logged_sock2name[from_sock]
                print(from_name + ' asks for ', poem_indx)
                poem = self.sonnet.get_sect(poem_indx)
                print('here:\n', poem)
                mysend(from_sock, M_POEM + poem)
#==============================================================================
#time
#==============================================================================
            elif code == M_TIME:
                ctime = time.strftime('%d.%m.%y,%H:%M', time.localtime())
                mysend(from_sock, ctime)
#==============================================================================
#search
#==============================================================================
            elif code == M_SEARCH:
                term = msg[1:]
                from_name = self.logged_sock2name[from_sock]
                print('search for ' + from_name + ' for ' + term)
                search_rslt = (self.indices[from_name].search(term)).strip()
                print('server side search: ' + search_rslt)
                mysend(from_sock, M_SEARCH + search_rslt)
#==============================================================================
# the "from" guy has had enough (talking to "to")!
#==============================================================================
            elif code == M_DISCONNECT:
                from_name = self.logged_sock2name[from_sock]
                the_guys = self.group.list_me(from_name)
                self.group.disconnect(from_name)
                the_guys.remove(from_name)
                if len(the_guys) == 1:  # only one left
                    g = the_guys.pop()
                    to_sock = self.logged_name2sock[g]
                    mysend(to_sock, M_DISCONNECT)
#==============================================================================
# Gaming: Indian Cards; implement
#==============================================================================
            elif code == M_GAME:
                reply = msg[1:]
                from_name = self.logged_sock2name[from_sock]
                sock = {1:self.logged_name2sock[self.player1], 
                        2:self.logged_name2sock[self.player2]}
                if (self.lastsend1, self.lastsend2) == ('ok', 'ok'):
                    if from_name == self.player1:
                        if reply == 'rec':
                            self.record[1] = 1
                        elif reply == 'cheat':
                            self.cheat[1] = 1
                        elif reply == 'y':
                            pass
                        self.ready[1] = 1
                        mysend(sock[2], M_GAME + 'Your rival is ready!#')
                    else:
                        if reply == 'rec':
                            self.record[2] = 1
                        elif reply == 'cheat':
                            self.cheat[2] = 1
                        elif reply == 'y':
                            pass
                        self.ready[2] = 1
                        mysend(sock[1], M_GAME + 'Your rival is ready!#')
                    if self.ready == {1:1, 2:1}:
                        #start game
                        mysend(sock[1], M_GAME + 'Game Started!')
                        mysend(sock[2], M_GAME + 'Game Started!')
                        self.lastsend1, self.lastsend2 = 'start', 'start'
                        self.banker = self.player1
                        
                if (self.lastsend1, self.lastsend2) == ('start', 'start'):
                    for i in [1,2]:
                        mysend(sock[i], M_GAME + '\n\nRound ' +self.get_round())
                        if self.record[i]:
                            mysend(sock[i], M_GAME + self.game.record())
                    self.game.deal()
                    mysend(sock[1], M_GAME + self.game.showcard(2))
                    mysend(sock[2], M_GAME + self.game.showcard(1))
                    for i in [1,2]:
                        if self.cheat[i]:
                            mysend(sock[i], M_GAME + self.game.reveal(i))
                    mysend(sock[1], M_GAME + 'Chips you have: ' + str(self.game.player1.get_chip()))
                    mysend(sock[2], M_GAME + 'Chips you have: ' + str(self.game.player2.get_chip()))
                    self.game.player1.initbid()
                    self.game.player2.initbid()
                    for i in [1,2]:
                        mysend(sock[i], M_GAME + self.game.initbid())
                    if self.banker == self.player1:
                        mysend(sock[1], M_GAME + 'Bid or Fold?#')
                        mysend(sock[2], M_GAME + 'Waiting for banker...')
                        (self.lastsend1, self.lastsend2) = ('ask', 'wait')
                    else:
                        mysend(sock[2], M_GAME + 'Bid or Fold?#')
                        mysend(sock[1], M_GAME + 'Waiting for banker...')
                        (self.lastsend1, self.lastsend2) = ('wait', 'ask')
                        
                elif (self.lastsend1, self.lastsend2) == ('ask', 'wait'):
                    if reply == 'fold':
                        self.game.player1.fold()
                        mysend(sock[2], M_GAME + 'Your rival folded.')
                        (self.lastsend1, self.lastsend2) = ('result', 'result')
                    elif reply[0:4] == 'bid ':
                        reply = int(reply.strip().split()[1])
                        self.game.player1.biding(reply)
                        self.game.player2.rbid = self.game.player1.get_bid()
                        msg = 'Your rival bided ' + str(reply) + ' chips. Call? Raise? Fold?#'
                        mysend(sock[2], M_GAME + msg)
                        (self.lastsend1, self.lastsend2) = ('wait', 'ask')
                    elif reply == 'call':
                        self.game.call(1)
                        self.game.compare()
                        mysend(sock[2], M_GAME + 'Your rival called.')
                        (self.lastsend1, self.lastsend2) = ('result', 'result')
                    elif reply[0:6] == 'raise ':
                        reply = int(reply.strip().split()[1])
                        self.game.player1.raisebet(reply)
                        self.game.player2.rbid = self.game.player1.get_bid()
                        msg = 'Your rival raised ' + str(reply) + ' chips. Call? Raise? Fold?#'
                        mysend(sock[2], M_GAME + msg)
                        (self.lastsend1, self.lastsend2) = ('wait', 'ask')
                        
                elif (self.lastsend1, self.lastsend2) == ('wait', 'ask'):
                    if reply == 'fold':
                        self.game.player2.fold()
                        mysend(sock[1], M_GAME + 'Your rival folded.')
                        (self.lastsend1, self.lastsend2) = ('result', 'result')
                    elif reply[0:4] == 'bid ':
                        reply = int(reply.strip().split()[1])
                        self.game.player2.biding(reply)
                        self.game.player1.rbid = self.game.player2.get_bid()
                        msg = 'Your rival bided ' + str(reply) + ' chips. Call? Raise? Fold?#'
                        mysend(sock[1], M_GAME + msg)
                        (self.lastsend1, self.lastsend2) = ('ask', 'wait')
                    elif reply == 'call':
                        self.game.call(2)
                        self.game.compare()
                        mysend(sock[1], M_GAME + 'Your rival called.')
                        (self.lastsend1, self.lastsend2) = ('result', 'result')
                    elif reply[0:6] == 'raise ':
                        reply = int(reply.strip().split()[1])
                        self.game.player2.raisebet(reply)
                        self.game.player1.rbid = self.game.player2.get_bid()
                        msg = 'Your rival raised ' + str(reply) + ' chips. Call? Raise? Fold?#'
                        mysend(sock[1], M_GAME + msg)
                        (self.lastsend1, self.lastsend2) = ('ask', 'wait')
                        
                if (self.lastsend1, self.lastsend2) == ('result', 'result'):
                    for i in [1,2]:
                        mysend(sock[i], M_GAME + 'Result:')
                        mysend(sock[i], M_GAME + self.game.reveal(i))
                    if self.game.player1.get_result() == 'Lose':
                        self.banker = self.player2
                    elif self.game.player2.get_result() == 'Lose':
                        self.banker = self.player1
                    else:
                        pass                        
                    mysend(sock[1], M_GAME + 'You(Player1) ' + self.game.player1.get_result() + ' this turn.')
                    mysend(sock[2], M_GAME + 'You(Player2) ' + self.game.player2.get_result() + ' this turn.')
                    self.game.calculate()
                    self.round += 1
                    
                    for i in [1,2]:
                        mysend(sock[i], M_GAME + self.game.show())
                    if self.game.player1.get_chip() <= 0:
                        mysend(sock[1], M_GAME + 'You(Player1) lose the game! Play again?(y/n/rec/...)#')
                        mysend(sock[2], M_GAME + 'You(Player2) win the game! Play again?(y/n/rec/...)#')
                        self.game = gm.Game(self.player1, self.player2)
                        self.ready = {}
                        self.record = {1:0, 2:0}
                        self.cheat = {1:0, 2:0}
                        (self.lastsend1, self.lastsend2) = ('ok', 'ok')
                    elif self.game.player2.get_chip() <= 0:
                        mysend(sock[1], M_GAME + 'You(Player1) win the game! Play again?(y/n/rec/...)#')
                        mysend(sock[2], M_GAME + 'You(Player2) lose the game! Play again?(y/n/rec/...)#')
                        self.game = gm.Game(self.player1, self.player2)
                        self.ready = {}
                        self.record = {1:0, 2:0}
                        self.cheat = {1:0, 2:0}
                        (self.lastsend1, self.lastsend2) = ('ok', 'ok')
                    else:
                        bankersock = self.logged_name2sock[self.banker]
                        mysend(bankersock, M_GAME + 'Press any key to continue#')
                        (self.lastsend1, self.lastsend2) = ('start', 'start')
#==============================================================================
#QUITGAME
#==============================================================================
            elif code == M_QUITGAME:
                from_name = self.logged_sock2name[from_sock]
                self.group.game_disconnect(from_name)
                if from_name == self.player1:
                    to_sock = self.logged_name2sock[self.player2]
                    self.player1 = ''
                    self.player2 = ''
                    mysend(to_sock, M_QUITGAME)
                else:
                    to_sock = self.logged_name2sock[self.player1]
                    self.player1 = ''
                    self.player2 = ''
                    mysend(to_sock, M_QUITGAME)
#==============================================================================
#the "from" guy really, really has had enough
#==============================================================================
            elif code == M_LOGOUT:
                self.logout(from_sock)
        else:
            #client died unexpectedly
            self.logout(from_sock)   

#==============================================================================
# main loop, loops *forever*
#==============================================================================
    def run(self):
        print ('starting server...')
        while(1):
           read,write,error=select.select(self.all_sockets,[],[])
           print('checking logged clients..')
           for logc in list(self.logged_name2sock.values()):
               if logc in read:
                   self.handle_msg(logc)
           print('checking new clients..')
           for newc in self.new_clients[:]:
               if newc in read:
                   self.login(newc)
           print('checking for new connections..')
           if self.server in read :
               #new client request
               sock, address=self.server.accept()
               self.new_client(sock)
           
def main():
    server=Server()
    server.run()

main()
