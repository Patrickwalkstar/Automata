# Name: pa2.py
# Author(s): Andres Rivera and Patrick Lee Walker
# Date: 9/18/2020
# Last updated: 9/27/2020
# Description: A python program that converts an input NFA
# to and equivalent DFA. Reads in a definition of NFA 'N', 
# converts 'N' to a DFA 'M', and writes the definition of 
# 'M' to a text file.
# Note: a majority of syncs were done by Andres, individual 
# and group contributions are listed under each function/section.

class NFA:
	""" Simulates an NFA """

	def __init__(self, nfa_filename):
		"""
		Contributor(s): Patrick, Andres
		Initializes NFA from the file whose name is
		nfa_filename.  (So you should create an internal representation
		of the nfa.)
		"""
		
		with open(nfa_filename, 'r') as nfa_file:

			self.num_states = int(nfa_file.readline())
			self.alphabet = nfa_file.readline().rstrip('\n')
			self.transitions = {}
			self.start_state = ''
			self.accept_states = []

			# Defines transition for NFA: (state, symbol in alphabet or 'e') --> {destination states}
			for line in nfa_file: 
				token_list = line.rstrip('\n').split(" ")

				# Read lines as transitions until the read-in line is the start state
				if len(token_list) > 1:
					current_state  = int(token_list[0])
					transition = token_list[1].strip("\'")
					destination_state = int(token_list[2])
					
					if (current_state, transition) not in self.transitions.keys():
						self.transitions[(current_state, transition)] = {destination_state}
					else: 
						self.transitions[(current_state, transition)].add(destination_state)
				else: 
					break
			
			self.start_state = int(nfa_file.readline().rstrip('\n')[0])
			self.accept_states = nfa_file.readline().rstrip('\n').split(" ")

		# Converts accept states from strings to ints (proper state format)
		for index in range(0, len(self.accept_states)):
				self.accept_states[index] = int(self.accept_states[index])
				
		nfa_file.close()

	def toDFA(self, dfa_filename):
		"""
		Contributor(s): Andres, Patrick
		Converts the "self" NFA into an equivalent DFA
		and writes it to the file whose name is dfa_filename.
		The format of the DFA file must have the same format
		as described in the first programming assignment (pa1).
		This file must be able to be opened and simulated by your
		pa1 program.

		This function should not read in the NFA file again.  It should
		create the DFA from the internal representation of the NFA that you 
		created in __init__.
		"""

		# Converts the "self" NFA into an equivalent DFA 
		dfa_construction = self.constructDFA()
		
		# Writes the constructed DFA to an external file based on the input filename
		self.writeDFA(dfa_filename, dfa_construction)
		

	def constructDFA(self):
		"""
		Contributor(s): Patrick, Andres
		Convert the internal representation of the NFA to an equivalent DFA. 
		Returns a tuple construction of the DFA - the states, transitions, 
		start state and accept states. Also, converts sets of states into 
		single number states to be consistent with PA1 DFA definitions.
		"""
		
		# DFA internal representation
		dfa_start_state = self.epsilon({self.start_state})
		dfa_accept_states = []
		dfa_transitions = {}
		dfa_states = [dfa_start_state]
		new_state_queue = [dfa_start_state]
		
		# While there are newly found states in new_state_queue, 
		# continue to find transitions
		while new_state_queue:
			for symbol in self.alphabet:
				current_state = frozenset(new_state_queue[0])
				new_dfa_state = self.getDFADestination(current_state, symbol)
				dfa_transitions[(current_state, symbol)] = new_dfa_state
				if new_dfa_state not in dfa_states:
					dfa_states.append(new_dfa_state)
					new_state_queue.append(new_dfa_state)

			new_state_queue.pop(0)

		# All DFA accept states are states that contain an NFA accept state
		dfa_accept_states = [state for state in dfa_states for accept_state in self.accept_states if accept_state in state]					
		
		# Changes DFA definition components to have unique single numbers instead of sets of states
		setStatesToNumber = self.getSetStatesToNumber(dfa_states)
		dfa_states = self.toListOfNumbers(dfa_states, setStatesToNumber)
		dfa_accept_states = self.toListOfNumbers(dfa_accept_states, setStatesToNumber)
		dfa_transitions = self.toTransitionsOfNumbers(dfa_transitions, setStatesToNumber)
		
		return (dfa_states, dfa_transitions, setStatesToNumber[dfa_start_state], dfa_accept_states)
		
	def epsilon(self, states=set()):
		"""
		Contributor(s): Andres, Patrick 
		Defines the epsilon function - takes in a set of states and 
		returns the set of states that contains the "from" and "to" 
		state in an epsilon transition. It also continuously checks 
		for further epsilon transitions.
		"""

		new_state = states
		state_sets_list = [states]

		# While there are epsilon transitions in at least 1 state in the set of states, 
		# apply the epsilon function to that state in the set of states
		while state_sets_list:
			for state in state_sets_list[0]:
				if(state, 'e') in self.transitions.keys():
					new_state = new_state.union(self.transitions[state, 'e'])
					# Stores the new set of states from the epsilon transition to apply the epsilon function on this new set
					state_sets_list.append(self.transitions[(state, 'e')])
			state_sets_list.pop(0)

		return frozenset(new_state)

	def getDFADestination(self, current_state, symbol):
		"""
		Contributor(s): Patrick, Andres
		Based on the input set of states "current_state", returns an output state that
		is the union of destination states states that come from the transitions from 
		each state in current_state via the input symbol.
		"""

		new_state = set()
		for element in current_state:
			if (element,symbol) in self.transitions.keys():
				new_state = new_state.union(self.epsilon(self.transitions[(element, symbol)]))
		return frozenset(new_state)
	
	def toTransitionsOfNumbers(self, dict_of_transitions = dict(), setStatesToNumber = dict()):
		"""
		Contributor(s): Andres
		Given a dictionary of sets of states that map to single numbered states,
		convert the current state and next state in a dictionary of "(current state, symbol) --> next state"
		transitions from sets of states to single numbered states.

		Returns a dictionary of (current state, symbol) --> next state transitions with all the states
		as numbers.
		"""
		
		dfa_transition_numbers = {}
		for (state_symbol_tuple, next_state) in dict_of_transitions.items():
			current_state = state_symbol_tuple[0]
			symbol = state_symbol_tuple[1]
			# Populate new dictionary of transitions with current_state and next_state as single numbered states
			dfa_transition_numbers[(setStatesToNumber[current_state], symbol)] = setStatesToNumber[next_state]
		return dfa_transition_numbers

	def toListOfNumbers(self, list_of_states = list(), setStatesToNumber = dict()):
		"""
		Contributor(s): Andres
		Given a dictionary of sets of states that map to singled numbered states, 
		convert a list of sets of states into a list of single numbered states.

		Returns a list of single numbered states.
		"""
		
		for index in range(len(list_of_states)):
			list_of_states[index] = setStatesToNumber[list_of_states[index]]
		
		return list_of_states
		
	def getSetStatesToNumber(self, dfa_states=frozenset()):
		"""
		Contributor(s): Andres
		Creates a mapping of set of states to single numbered states.

		Returns a dictionary of these mappings.
		"""

		return {state: count for count, state in enumerate(dfa_states, start=1)}

	def writeDFA(self, dfa_filename, dfa_construction=tuple()):
		"""
		Contributor(s): Patrick 
		Using a DFA construction input, this function writes to a text file 
		(input filename) the PA1 definition of a DFA.  
		Expects singled numbered DFA definition components.

		DFA construction referenced at: 0, DFA states; 
										1, DFA transitions; 
										2, DFA start state; 
										3, DFA accept states.
		"""
		
		dfa_file = open(dfa_filename, 'w')

		with open(dfa_filename, 'w') as dfa_file:
			dfa_file.write(str(len(dfa_construction[0])) + "\n")
			dfa_file.write(self.alphabet + "\n")

			for (sc, s) in dfa_construction[1].items():
				dfa_file.write("%d \'%s\' %d\n" % (sc[0],sc[1],s))

			dfa_file.write(str(dfa_construction[2]) + "\n")

			dfa_accept_states = dfa_construction[3]
			for index in range(len(dfa_accept_states)):
				dfa_accept_states[index] = str(dfa_accept_states[index])
			
			dfa_file.write(" ".join(dfa_construction[3]))

		dfa_file.close()