#!/usr/bin/env python
#Hiddenblade
#SMS based moderator program for Assassins
#http://en.wikipedia.org/wiki/Assassin_(game)

#William Carroll
#carroll.william.c@gmail.com

#JAY ADD YOUR CREDENTIALS HERE OR SOMETHING

the_game = Hiddenblade()

class Hiddenblade(object):
	# The main game itself. Probably unnecessary, but I'm used to java so :p
	# TODO Add functionality to pass a filename. If a filename is passed, 
	# check it for a valid game session and load it.
	def __init__(self):
		#run the actual game here
	def save();
		#save the game session to a file.
	
class PlayerList(object):
	# The list of players. A doubly linked list.
	def __init__(self):
		player_count = 0
		first_player = Player()
		
	def add_player(Player() new_player)
		players.append(new_player)
		
class Player(object):
	#the player class, holds name, status, target, and hunter.
	#target and hunter act as next and previous list items.
	def __init__(self, name)