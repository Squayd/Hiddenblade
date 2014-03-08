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
	def __init__(self,player_list):
		#run the actual game here
		self.roster = player_list
		self.dead_players = []  # maybe we dont need this if we just have roster
		
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
		###maybe we could consider an option to dynamically add an extra player 
		### to an in-progress game if it's before midnight, or if noone has 
		###been killed yet, without  stopping the program...
		### would be cool but maybe not very useful
		### also, there has to be a better way to add discussion-type comments...
		### maybe directly on github?
		
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
		#   if SMS beings with 'dead' remove the player who sent the text from the list
		#		and provide the killer with info on his/her next target
		### sounds good, maybe everything after the keyword 'Kill' or 'dead' can be a description of how
		### it happened? i liked reading your texts about kevin's drink and your venom attack
		### another thought is that in the event of poison, maybe the person who died has to be the one
		### to report it, since the killer might not know exactly when it happened in that case.
		### i think i like immediate notification versus nightly recap, since a player can text 
		### 'surviors' to find out who is left anyway. and stuff doesnt necessarily happen every day
		#While waiting, possibly listen for console commands?
		### could have one game thread running in background, and the mainline can 
		### list a console menu with options or something (add player, pause game, stop game, etc)
		### that way if you had to restart the server, you could bring down the game in a safe way that would
		### write everything out in such a way that it could just be started up again later
		
	def add_player(self,player):
		self.roster.append(player) #keep a separate list of all players
	def kill_player(self,killed_player,killer_player):
		#get date/time somehow
		self.dead_players.append(killed_player)
		killed_player.status = DEAD
		killed_player.killer_phone = killer_player.phone
		killed_player.date_killed = 0
		
	def get_target(self,player_phone):
		#Takes a phone number as an int to identify a player and returns that  player's target as a Player() object. If the
		#player is not found, returns None
		target = "None"
		for i in range(len(self.roster)):
			if (self.roster[i].phone == player_phone):
				if i == (len(self.roster) - 1): #wrap around to start if selected player is last in the list
					target =  self.roster[0]
				else:
					target = self.roster[i+1]
		return target
	#Do we need an analog to this function that returns the previous player?
	### sure, why not :D get_hunter or something
			
	def save(self):
		#save the game session to a file.
		pass
	def print_roster(self):
		for c in self.roster:
			print c.name,"\t",c.phone,"\t",
			if c.status == ALIVE: print "Alive"
			else: print "Dead"
			if (c.status == DEAD):
				print "  killed by:\t", c.killer_phone,
				print "  died on:\t",c.date_killed
				print "  killed:\t",c.killed_phone
		print "count: ",len(self.roster) 
		print		
		
	def start_game(self):
		#this will have to do more than just shuffle...
		random.shuffle(self.roster)
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
	### to delete roster... player's target is next in list (first if they are last)
	### player's hunter is previous in list (last if they are first)
	###### Yeah, I got kinda stuck on linked list because it fits the idea of the way players relate to
	###### each other, but it's not necessary when we'd have to implement it ourselves and if we're saving
	###### to a flat file it's going to be a pain to rebuild that.
	def __init__(self, name,phone, status=ALIVE):
		self.name = name
		self.status = status
		self.killer_phone = ""  # phone of this player's killer
		self.killed_phone = [] # list of people (phone) this player killed
		self.date_killed = 0 # date/time the player was killed
		self.phone = phone  #phone number of this player (this is probably the best unique ID to use)
		
		#maybe add address information? I think this info would be good to read from a file as well
		#so that it's not dependent on making code changes every time the player list changes
		### I think address, workplace, possibly make and color of vehicle. For certain we'll need a 
		### phone number. And any game tracking stats, like it could store a list of the names
		### this player eliminated.

if __name__ == '__main__':
	
	p1 = Player("jay",5203024499)
	p2 = Player("will",5204196428)
	p3 = Player("kevin",5205768292)
	p4 = Player("RB",5204193553)
	p5 = Player("Ben",5209816884)

	theGame = Hiddenblade([p1,p2,p3])
	theGame.print_roster()
	theGame.start_game()	
	theGame.print_roster()
	
	theGame.add_player(p4)
	theGame.print_roster()
	theGame.kill_player(p2,p3)
	theGame.print_roster()
	theGame.add_player(p5)
	theGame.print_roster()
	
	
