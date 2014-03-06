#!/usr/bin/env python
#Hiddenblade
#SMS based moderator program for Assassins
#http://en.wikipedia.org/wiki/Assassin_(game)

#William Carroll
#carroll.william.c@gmail.com

#Jay Stockbauer
#stockbauer@gmail.com

import random

class Hiddenblade(object):
	# The main game itself. Probably unnecessary, but I'm used to java so :p
	## i think main game class makes sense, but probably dont need playerlist class
	# TODO Add functionality to pass a filename. If a filename is passed, 
	# check it for a valid game session and load it.
	def __init__(self,players):
		#run the actual game here
		self.players = players
	def add_player(self,player):
		self.players.append(player)
	def kill_player(self,player):
		self.players.remove(player)
	def save(self):
		#save the game session to a file.
		pass
	def print_players(self):
		for c in self.players:
			print c.name, c.status
		print "count: ",len(self.players) 
		print		
	def start_game(self):
		#this will have to do more than just shuffle...
		random.shuffle(self.players)
	def end_game(self):
		#write final stats to a stats file and exit?
		#maybe this can be called automatically from the main loop when the list reaches size 1
		pass
		
		
class Player(object):
	#the player class, holds name, status, target, and hunter.
	#target and hunter act as next and previous list items.
	### python doesnt really have linked lists, but they have regular list support built in
	### I think it would be best to just keep a list, and use existing list.remove function
	### to delete players... player's target is next in list (first if they are last)
	### player's hunter is previous in list (last if they are first)
	def __init__(self, name, status=True):
		self.name = name
		self.status = status
		#maybe add address information? I think this info would be good to read from a file as well
		#so that it's not dependent on making code changes every time the player list changes
	

if __name__ == '__main__':
	
	#playin' wit da objects
	p1 = Player("jay")
	p2 = Player("will")
	p3 = Player("kevin")
	p4 = Player("RB")
	p5 = Player("Ben")
	
	theGame = Hiddenblade([p1,p2,p3])
	theGame.print_players()
	theGame.start_game()	
	theGame.print_players()
	
	theGame.add_player(p4)
	theGame.print_players()
	theGame.kill_player(p2)
	theGame.print_players()
	theGame.add_player(p5)
	theGame.print_players()
	
	