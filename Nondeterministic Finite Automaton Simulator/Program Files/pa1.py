# Name: pa1.py
# Author(s): Andres Rivera and Patrick Lee Walker
# Origin Date: 8/30/2020
# Recent Update: 9/05/2020
# Description: A python program that simulates the 
# computation of a DFA 'M' on an input string, and 
# reports if the string is accepted by 'M'. Reads in a 
# definition of a DFA 'M', reads in a string, evaluates.

import sys

class DFA:
	""" Simulates a DFA """

	def __init__(self, filename):
		"""
		Initializes DFA from the file whose name is
		filename
		"""
		dfa_file = open(filename, 'r')
		self.num_states = int(dfa_file.readline())
		self.alphabet = dfa_file.readline().rstrip('\n')
		self.transitions = {}
		self.start_state = ''	
		self.accept_states = []
		
		# Reads in all transitions and stops once start_state has been read
		for line in dfa_file: 

			# List of line elements, either a transition mapping or a start state.
			token_list = line.rstrip('\n').split(" ")

			# Line contains more than one item, it's a transition mapping. Else, it's a start state.
			if len(token_list) > 1:
    				
    			# DFA transition function: (state, symbol) --> state
				self.transitions[(int(token_list[0]), token_list[1].strip("\'"))] = int(token_list[2])
			else: 
				self.start_state = int(token_list[0])
				break
		
		self.accept_states = dfa_file.readline().rstrip('\n').split(" ")
		
		# Converting each accept state from a string to an integer and storing it into a list
		for index in range(0, len(self.accept_states)):
			self.accept_states[index] = int(self.accept_states[index])
    		
		dfa_file.close()

	def simulate(self, str):
		""" 
		Simulates the DFA on input str.  Returns
		True if str is in the language of the DFA,
		and False if not.
		"""
		current_state = self.start_state
		
		# For each read in symbol, use the transitions dictionary to transition from current_state to the next state
		# Then, reassign current_state
		for symbol in str:
			current_state = self.transitions[(current_state, symbol)]

		if current_state in (self.accept_states):
    			return True
		else: 
				return False