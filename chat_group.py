S_ALONE = 0
S_TALKING = 1
S_GAMING = 2

#==============================================================================
# Group class:
# member fields: 
#   - An array of items, each a Member class
#   - A dictionary that keeps who is a chat group
# member functions:
#    - join: first time in
#    - leave: leave the system, and the group
#    - list_my_peers: who is in chatting with me?
#    - list_all: who is in the system, and the chat groups
#    - connect: connect to a peer in a chat group, and become part of the group
#    - disconnect: leave the chat group but stay in the system
#==============================================================================

class Group:
    
    def __init__(self):
        self.members = {}
        self.chat_grps = {}
        self.game_grps = {}
        self.grp_ever = 0
        self.game_grp_ever = 0
        
    def join(self, name):
        self.members[name] = S_ALONE
        return
        
    def is_member(self, name):
        if name in self.members.keys():
            if self.members[name] == 0 or self.members[name] == 1:
                return True
        return False
    
    def is_alone(self, name):
        if name in self.members.keys():
            if self.members[name] == 0:
                return True
        return False

    def is_chatting(self, name):
        if name in self.members.keys():
            if self.members[name] == 1:
                return True
        return False
    
    def is_gaming(self, name):
        if name in self.members.keys():
            if self.members[name] == 2:
                return True
        return False
    
    def leave(self, name):
        self.disconnect(name)
        del self.members[name]
        return
        
    def find_group(self, name):
        found = False
        group_key = 0
        for k in self.chat_grps.keys():
            if name in self.chat_grps[k]:
                found = True
                group_key = k
                break
        return found, group_key
        
    def find_game_group(self, name):
        found = False
        group_key = 0
        for k in self.game_grps.keys():
            if name in self.game_grps[k]:
                found = True
                group_key = k
                break
        return found, group_key
        
    def connect(self, me, peer):
        peer_in_group = False
        #if peer is in a group, join it
        peer_in_group, group_key = self.find_group(peer)
        if peer_in_group == True:
            print(peer, "is talking already, connect!")
            self.chat_grps[group_key].append(me)
            self.members[me] = S_TALKING
        else:
            # otherwise, create a new group
            print(peer, "is idle as well")
            self.grp_ever += 1
            group_key = self.grp_ever
            self.chat_grps[group_key] = []
            self.chat_grps[group_key].append(me)
            self.chat_grps[group_key].append(peer)
            self.members[me] = S_TALKING
            self.members[peer] = S_TALKING
        print(self.list_me(me))
        return
        
    def disconnect(self, me):
        # find myself in the group, quit
        in_group, group_key = self.find_group(me)
        if in_group == True:
            self.chat_grps[group_key].remove(me)
            self.members[me] = S_ALONE
            # peer may be the only one left as well...
            if len(self.chat_grps[group_key]) == 1:
                peer = self.chat_grps[group_key].pop()
                self.members[peer] = S_ALONE
                del self.chat_grps[group_key]
        return
        
    def game_connect(self, me, peer):
        #if peer is in a group, join it
        print(peer, "is ready to connect!")
        self.game_grp_ever += 1
        group_key = self.game_grp_ever
        self.game_grps[group_key] = []
        self.game_grps[group_key].append(me)
        self.game_grps[group_key].append(peer)
        self.members[me] = S_GAMING
        self.members[peer] = S_GAMING     
        print(self.list_me(me))
    
    def game_disconnect(self, me):
        in_group, group_key = self.find_game_group(me)
        if in_group == True:
            self.game_grps[group_key].remove(me)
            self.members[me] = S_ALONE
            # peer may be the only one left as well...
            if len(self.game_grps[group_key]) == 1:
                peer = self.game_grps[group_key].pop()
                self.members[peer] = S_ALONE
                del self.game_grps[group_key]

    def list_all(self):
        # a simple minded implementation
        full_list = "Users: ------------" + "\n"
        full_list += str(self.members) + "\n"
        full_list += "Chat Groups: -----------" + "\n"
        full_list += str(self.chat_grps) + "\n"
        full_list += "Game Groups: -----------" + "\n"
        full_list += str(self.game_grps) + "\n"
        return full_list
        
    def list_me(self, me):
        # return a list, "me" followed by other peers in my group
        if me in self.members.keys():
            my_list = []
            my_list.append(me)
            in_group, group_key = self.find_group(me)
            in_game_group, game_group_key = self.find_game_group(me)
            if in_group == True:
                for member in self.chat_grps[group_key]:
                    if member != me:
                        my_list.append(member)
            elif in_game_group == True:
                for member in self.game_grps[game_group_key]:
                    if member != me:
                        my_list.append(member)
        return my_list

