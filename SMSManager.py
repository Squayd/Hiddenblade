#!/usr/bin/env python3
#Hiddenblade - SMS manager
#SMS based moderator program for Assassins
#http://en.wikipedia.org/wiki/Assassin_(game)

#William Carroll
#carroll.william.c@gmail.com

#Jay Stockbauer
#stockbauer@gmail.com

#the interface between the SMS library and the Hiddenblade library
#this module needs access to a queue of incoming SMS, but also
#needs to be able to access the Hiddenblade object that represents the game
#so that it can take action based on the incoming messages.

#This module will be run in it's own thread.  The general set of actions will be as follows:
# declare instance of Hiddenblade game
# add players (read from file or taken from console input)
# run the "start game" method to shuffle players and get things in motion
# spawn necessary threads 
## 1. SMS thread that wakesup up every 10 minutes or so to check for new texts
## 2. console input thread that waits for a user to take an action based on a menu of selections
###  a. pause game (ignore/delete all incoming texts until game resumes)
###  b. stop game (save, then terminate threads, exit loops, and close program)
###  c. save game (save the current state of the game (the roster) as a pickle object
## 3. last thread will simple wait for SMS to be added to the queue, and take action when SMS is received

# For thread #3: 
# while (True)
#	sleep 10 minutes
#	check queue for sms
#	perform function based on SMS action
#	issue appropriate message if previous call was successful
#	
#
from Hiddenblade import Player
import Hiddenblade
import queue





#valid actions that can be taken via SMS
ACTIONS = [	'list_players',		#0
			'list_living',		#1
			'give_target',		#2
			'kill_target',		#3
			'kill_self',		#4
			'send_broadcast',	#5
			'get_options'		#6
		  ]
ACTION_WORDS = {'players': ACTIONS[0],
		        'survivors': ACTIONS[1],
				'target': ACTIONS[2],
				'kill': ACTIONS[3],
				'dead': ACTIONS[4],
				'broadcast':ACTIONS[5],
				'options':ACTIONS[6]
			   }
theSMSQueue = queue.Queue()
theGame = Hiddenblade.Hiddenblade()

def message_parser(message):
#message is taken directly from SMS, parsed, and an action is taken based on what was received
#going to assume for now that message is an array of strings, where first item is
#the sender's phone number, and the second item is the text message
	
	#parse the message
	number = message[0]
	parsed_message = message[1].split(":") #action followed by message
	action = parsed_message[0].lower()
	if len(parsed_message) > 1:	
		description = parsed_message[1]
	
	#get the player object associated with the number
	theSender = theGame.get_player_by_number(number)
	living = theSender.status
	if theSender is not None:
		print(theSender.name,' sent a text')
	#send back an error message since the text must contain a valid action
		if action not in ACTION_WORDS:
			print('action not found')
		elif ACTION_WORDS[action] == ACTIONS[0]:
			print('requested a list of players')
			theGame.print_roster()
		elif ACTION_WORDS[action] == ACTIONS[1]:
			print('requested a list of LIVING players')
			theGame.print_living()
		elif ACTION_WORDS[action] == ACTIONS[2] and living:
			print('requested personal target')
			print('your target is: ',(theGame.get_target(theSender)).name)
		elif ACTION_WORDS[action] == ACTIONS[3] and living:
			target = theGame.get_target(theSender)
			theGame.kill_player(target)
			print(target.name,' has been removed from the living')
			print(target.name," ",description)
		elif ACTION_WORDS[action] == ACTIONS[4] and living:
			print('requested self death')
			theGame.kill_player(theSender)
			print('broadcast: ',theSender.name," ",description)
		elif ACTION_WORDS[action] == ACTIONS[5]:
			print('broadcast message:',description)
		elif ACTION_WORDS[action] == ACTIONS[6]:
			for x in ACTION_WORDS:
				print(x)
		
	
	
def check_sms_stuff():
#spawn thread to check text and/or email, and add unread stuff to the global queue
	pass

def send_broadcast(roster,message):
#a general message sent to all players
	for i in roster:
		print(message)
	
def receive_kill_message(self,message):
	pass



if __name__ == '__main__':

	

	p1 = Player("jay","5202046430")
	p2 = Player("will","5204196428")
	p3 = Player("kevin","5205768292")
	p4 = Player("RB","5204193553")
	p5 = Player("Ben","5209816884")

	#theGame.start_game()	
	theGame.add_player(p1)
	theGame.add_player(p2)
	theGame.add_player(p3)
	theGame.add_player(p4)
	theGame.add_player(p5)
	game_over = False
	
	#spawn threads before going into infinite loop
	
	##thread for check_sms_stuff that puts things on "theSMSQueue"
	
	##thread for menu TBD
	
	
	#while(!game_over):   #actually, this loop might be a spawned thread, and the console menu might be mainline
		

		#grab item from queue
		#current_msg = theSMSQueue.get() 
		#call message_parser to take action based on received message
	current_msg = ['5202046430','options']
	message_parser(current_msg)		#parse the SMS
	current_msg = ['5202046430','target']
	message_parser(current_msg)		#parse the SMS
	current_msg = ['5202046430','broadcast: this is a test of the emergency broadcast system']
	message_parser(current_msg)		#parse the SMS
	current_msg = ['5202046430','survivors']
	message_parser(current_msg)		#parse the SMS
	current_msg = ['5202046430','dead: couldn\'t get his heart to pump the coagulated blood...']
	message_parser(current_msg)		#parse the SMS
	current_msg = ['5202046430','players']
	message_parser(current_msg)		#parse the SMS
	#theSMSQueue.task_done() 		#notify the SMS function that we're done with the queue item
		
	
		
		# here is where we'd possibly a second queue that communicates with the console menu
		# function, and we can take action on our Hiddenblade object based on the console
	

		#check for game-ending condition, the last thing we do in the loop
	#	if len(list(theGame.get_living())) == 1: 
	#		game_over = True
	
	#terminate threads, write stats to file
	