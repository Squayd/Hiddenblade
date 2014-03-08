#!/usr/bin/env python3
#Hiddenblade
#SMS based moderator program for Assassins
#http://en.wikipedia.org/wiki/Assassin_(game)

#William Carroll
#carroll.william.c@gmail.com

#Jay Stockbauer
#stockbauer@gmail.com

import random
import sys

ALIVE = True
DEAD = False
NEW_GAME = False
SAVED_GAME = True

class Hiddenblade(object):
	# The main game itself.
	# TODO Add functionality to pass a filename. If a filename is passed, 
	# check it for a valid game session and load it.
	def __init__(self,players):
		#run the actual game here
		self.players = players
		
		#Thinking about the sequence
		#Program gets run on my server box
		#If it is given a file (either from an in-progress game or one we
		#	create to start a game) it will load that game session and begin
		#If it's not given a file, it will prompt for a player name and each
		#	piece of information. It will display it to confirm before finally
		#	adding the player, then ask if there is another player.
		#When there are no more players to add, it will randomize the player
		#	roster and create a list in the order of assigned targets.
		#	Note - two lists.
		#It will then wait until the system clock reaches midnight and send
		#	an SMS to each player giving them the identity and information for
		#	their target.
		#It will then wait until it receives an SMS.
		#	Any SMS will use the sending phone number to identify the player
		#		sending it.
		#	If SMS begins with 'target' reply with the player's target
		#		information again.
		#	if SMS begins with 'players' reply with the alphabetized names of 
		#		the full player roster
		#	if SMS begins with 'survivors' reply with an alphabetized list of
		#		players still alive
		#	if SMS begins with 'kill' remove the player's target from the list
		#		and provide them information for their new target. Then
		#		send SMS to all players saying who was elimnated
		#			OR make it like hunger games - just say a player has been
		#			eliminated and have a nightly recap SMS or something
		#		If the player's new target is him/herself, announce them as the
		#			victor, announce the player who had the most kills, exit.
		#While waiting, possibly listen for console commands?
		
	def add_player(self,player):
		self.players.append(player)
		self.roster.append(player) #keep a separate list of all players
	def kill_player(self,player):
		self.players.remove(player)
		
	def get_target(self,player_phone)
		#Takes a phone number as an int to identify a player and returns that  player's target as a Player() object. If the
		#player is not found, returns None
                target = None
		for i in range(len(self.players))
			if self.players[i].phone == player_phone
                            if i == (len(players) - 1) #wrap around to start if selected player is last in the list
				target =  self.players[0]
			    else target = self.players[i+1]
                return target
	#Do we need an analog to this function that returns the previous player?
			
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
		## yeah, or maybe when a player is eliminated, the assassin gets assigned a new target.
		## end the game when the target becomes themself? I don't now, there are a billion ways.
		pass
		
		
class Player(object):
	#the player class, holds name, status, target, and hunter.
	#target and hunter act as next and previous list items.
	### python doesnt really have linked lists, but they have regular list support built in
	### I think it would be best to just keep a list, and use existing list.remove function
	### to delete players... player's target is next in list (first if they are last)
	### player's hunter is previous in list (last if they are first)
	###### Yeah, I got kinda stuck on linked list because it fits the idea of the way players relate to
	###### each other, but it's not necessary when we'd have to implement it ourselves and if we're saving
	###### to a flat file it's going to be a pain to rebuild that.
	def __init__(self, name, status=True):
		self.name = name
		self.status = status
		#maybe add address information? I think this info would be good to read from a file as well
		#so that it's not dependent on making code changes every time the player list changes
		### I think address, workplace, possibly make and color of vehicle. For certain we'll need a 
		### phone number. And any game tracking stats, like it could store a list of the names
		### this player eliminated.

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
	
	
