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
import itertools
import time
import pickle

ALIVE = True
DEAD = False
NEW_GAME = False
SAVED_GAME = True

class Hiddenblade(object):
	# The main game itself.
	# TODO Add functionality to pass a filename. If a filename is passed, 
	# check it for a valid game session and load it.
	def __init__(self,player_list,filename=""):
		#run the actual game here
		self.roster = player_list
		self.dead_players = []  # maybe we don't need this if we just have roster
		
		#we should probably come up with some rules about file formatting...
		# like a file of names for a new game could have name_list as the first line
		# file for saved game could have saved_game as the first line
		# OR there could be a default save file that we could check no matter what
		# when a game is started, and if it doesn't exist or is empty, then we can 
		# prompt for the list of names, whether by manual input or file input
		##
		## i recommend looking into "pickle" as a way to save game state
		##
		if filename != "": self.read_names(filename)
		
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
		### it happened? I liked reading your texts about kevin's drink and your venom attack.
		### Another thought is that in the event of poison, maybe the person who died has to be the one
		### to report it, since the killer might not know exactly when it happened in that case.
		### I think I like immediate notification versus nightly recap, since a player can text 
		### 'survivors' to find out who is left anyway. and stuff doesn't necessarily happen every day
		#While waiting, possibly listen for console commands?
		### could have one game thread running in background, and the mainline can 
		### list a console menu with options or something (add player, pause game, stop game, etc)
		### that way if you had to restart the server, you could bring down the game in a safe way that would
		### write everything out in such a way that it could just be started up again later


######################## OPERATIONS TO THE ROSTER ########################
	def add_player(self,player):
	#keep a list of all players
		self.roster.append(player) 
	def remove_player(self,player):
	# in case someone wants to quit
		self.roster.remove(player)
	def get_roster(self): 
	# not sure this is necessary since we already have a direct reference to it
		for player in self.roster:
			yield player
	def get_living(self):
	#returns a generator of all living members in self.roster
		for player in self.roster:
			if player.status == ALIVE:
				yield player
	def get_dead(self):
	#returns a generator of all dead members in self.roster
		for player in self.roster:
			if player.status == DEAD:
				yield player
	def kill_player(self,killed_player):
	# changes killed_player's status from ALIVE to DEAD
	# record info in their player object on who killed them,
	# when they were killed, and the description of the death
		#get date/time somehow
		self.dead_players.append(killed_player)
		killer_player = self.get_hunter(killed_player)
		killer_player.killed_phone.append(killed_player.phone)
		killed_player.status = DEAD
		killed_player.killer_phone = killer_player.phone
		killed_player.date_killed = time.strftime("%H:%M:%S, %Y/%m/%d")
		
	def get_target(self,hunter_player):
	#returns the target of the player who is passed in		
		theLiving = list(self.get_living())
		theIndex = theLiving.index(hunter_player)
		if  theIndex == len(theLiving)-1:
			return theLiving[0] #if last player, his/her target is first player
		else: return theLiving[theIndex+1]
	def get_hunter(self,target_player):
	#returns the hunter of the player who was passed in
		theLiving = list(self.get_living())
		theIndex = theLiving.index(target_player)
		if  theIndex == 0:
			return theLiving[len(theLiving)-1] #if first player, his/her hunter is last player
		else: return theLiving[theIndex-1]

######################## CORE GAME FUNCTIONS ########################
	def start_game(self):
		#this will have to do more than just shuffle...
		random.shuffle(self.roster)
	def end_game(self):
		#write final stats to a file and exit?
		#maybe this can be called automatically from the main loop when the list reaches size 1
		## yeah, or maybe when a player is eliminated, the assassin gets assigned a new target.
		## end the game when the target becomes themself? I don't now, there are a billion ways.
		pass			
	def save(self):
	#save the game session to a file.
	#use pickle for saving game state, but when game ends, write a more universal CSV style
	#file for stat analysis
	#
	#do we use the same savefile name every time and only allow 1 saved game? (would we really need
	# to have more than 1 game saved at a time?). This implementation uses date/time to make a filename
	# so if you call the save function multiple times, you'll get multiple files.. this can build up fast
		savefile = "save_game_"+time.strftime("%Y%m%d_%H%M%S")
		pickle.dump(self.roster, open(savefile, "wb"))
		return savefile
	def load(self,filename):
	#load the game objects from a saved file
		self.roster = pickle.load(open(filename, "rb"))
		
	def read_names(self,filename): #TODO
	#read a file to get names for the roster.
		theFile = open(filename,'r')

######################## PRINT FUNCTIONS ########################
	def print_roster(self):
		for c in self.get_roster():
			self.print_player(c)
		print ("count: ",len(self.roster))
	def print_player(self,player):
		print (player.name,player.phone, sep="\t",end="\t")
		if player.status == ALIVE: print ("Alive")
		else: print ("Dead")
		if len(player.killed_phone) != 0 :
			print ("  killed:\t",player.killed_phone)
		if (player.status == DEAD):
			print ("  killed by:\t", player.killer_phone)
			print ("  died on:\t",player.date_killed)

	def print_living(self):
		count = 0
		for c in self.get_living():
			self.print_player(c)
			count = count + 1
		print ("living count: ",count)
	def print_dead(self):
		count = 0
		for c in self.get_dead():
			self.print_player(c)
			count = count + 1
		print ("death count: ",count)
			
		

		
		
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
	def __init__(self, name, phone, status=ALIVE):
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
	
	#theGame.start_game()	
	
	theGame.add_player(p4)
	theGame.add_player(p5)
	theGame.kill_player(p4)
	
	print("trying the experiment with generators")
	theGame.print_living()
	theGame.print_dead()
	print("player 3's target is:",end=" ")
	theGame.print_player(theGame.get_target(p1))
	print("player 3's hunter is:",end=" ")
	theGame.print_player(theGame.get_hunter(p1))
	#print(list(theGame.get_living()))
	
	thefile = theGame.save() # save the game
	theGame.kill_player(p3) # kill someone
	theGame.print_living() # p3 is dead
	theGame.load(thefile) # load saved game
	theGame.print_living() # p3 is back among the living!
	
