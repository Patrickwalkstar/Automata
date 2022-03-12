# Name: pa3.py
# Author(s): Andres Rivera & Patrick Lee Walker
# Date: 10/09/2020
# Recently Updated: 10/21/2020
# Description: A Python program that creates a RegEx object by: 
# 	taking in a regular expression (regex) and its alphabet from a file, 
# 	validating and parsing the regex string into an abstract syntax tree (AST),
# 	converting the AST to an equivalent NFA, 
# 	and finally converting the NFA to an equivalent DFA via our code from PA2.
# 
# 	The resulting DFA determines whether an input string is in the language of 
# 	the regex or not.

class InvalidExpression(Exception):
	pass
	
class RegEx:
	""" Simulates a regular expression """
	def __init__(self, filename):
		""" 
		Contributor(s): Andres Rivera, Patrick Walker
		
		Initializes a RegEx object from the specifications
		in the file whose name is filename.

		Also initializes the equivalent Abstract Syntax Tree (AST), as well as
		the equivalent NFA and DFA. 
		"""
		
		with open(filename) as regex_file:
			self.alphabet = regex_file.readline().rstrip()
			self.operators = ('|', '*', 'concat')
			self.tokenized_regex = self.preprocess(regex_file.readline().rstrip())
			self.equivalent_ast = self.regexToAST()
			self.equivalent_nfa = self.constructNFA()
			self.equivalent_dfa = DFA(self.equivalent_nfa, self.alphabet)
		
	def simulate(self, str):
		"""
		Contributor(s): Andres Rivera, Patrick Walker

		Returns True if the string str is in the language of
		the "self" regular expression.
		"""

		return self.equivalent_dfa.simulate(str)

	def preprocess(self, regex):
		"""
		Contributor(s): Andres Rivera, Patrick Walker

		Returns the tokenized version of the regex string, or raises
		an InvalidExpression exception if the regex string is not valid.

		The algorithm for building the tokenized regex skips spaces; makes implicit concatenation explicit ('concat');
		and adds operators, parentheses, and symbols as separate tokens into a list.  If parentheses
		are not balanced; if operators are missing operands; if there is a pair of parentheses with no regex inside it;
		or if one of the characters in the regex string is unrecognizable, then the regex is invalid. 
		"""

		token_list = [] #list of alphabet symbols, parens, and/or operators (including 'concat')
		prev_char = ''
		unmatched_parens = 0
		
		for char in regex:
			if char == ' ':
				continue
			elif char in self.alphabet or char in ['e', 'N']: # 'e' for epsilon; 'N' for empty set
				if prev_char not in ['(', '|', '', 'concat']: # Then, there is an implied concatenation
					token_list.append('concat')
				token_list.append(char)
			elif char in self.operators:
				if prev_char in ['|', '', '(']: # Then, at least 1 operator is missing an operand
					raise InvalidExpression("Invalid Expression")
				elif prev_char == '*' and char == '*': #Then, reduces double-star subregexes to single star, though it may not for the entire regex
					token_list.pop()
				token_list.append(char)
			elif char == '(':
				if prev_char not in ['(', '|', '', 'concat']: # Then, there is an implied concatenation
					token_list.append('concat')
				token_list.append(char)
				unmatched_parens += 1
			elif char == ')':
				if prev_char == '(': # Then, there is no regex inside parentheses
					raise InvalidExpression("Invalid Expression")
				token_list.append(char)
				unmatched_parens -= 1
			else: # char is none of the above (i.e. it's unrecognizable)
				raise InvalidExpression("Invalid Expression")
			
			prev_char = char
		
		if unmatched_parens != 0: # Then, too many ')' (it's < 0) or too many '(' (it's > 0)
			raise InvalidExpression("Invalid Expression")

		return token_list 
		
	def regexToAST(self):
		"""
		Contributor(s): Andres Rivera, Patrick Walker

		Returns the AST that is equivalent to the tokenized regex string.

		The algorithm to build the AST is similar to the algorithm
		in the program specifications document.  The algorithm reads through each token
		in the tokenized regex string and handles operators (i.e. '|', '*', and the implied 'concat'),
		operands, left parentheses, and right parentheses in their own cases. The specific details
		for each case follows the algorithm described in the program specifications document.
		"""
		operands = [] # Stack of ASTs
		operators = [] # Stack of strings  

		for token in self.tokenized_regex: # read every token in our tokenized regex string
			if token in self.operators: 
				self.evaluateStacks(operators, operands, token)
			elif token == '(':
				operators.append(token)
			elif token == ')':
				while operators and (operators[-1] != '('):
					self.makeAndSaveASTs(operators, operands)
				operators.pop() # Removes '('
			else: # token is in the regex's alphabet, is epsilon ('e'), or is the empty set ('N')
				operands.append(AST([token]))

		while operators:
			self.makeAndSaveASTs(operators, operands) 
		
		return operands.pop()
	
	def evaluateStacks(self, operators, operands, scanned_operator):
		"""
		Contributor(s): Andres Rivera, Patrick Walker 

		This function implements part of the algorithm descirbed in the program specification document. (b_iii)
		The algorithm for updating the stacks is to make new ASTs from these stacks and save them
		until the operators stack is empty, has a left parenthesis as its topmost operator, or does 
		not have its topmost operator precede the same precedence as the scanned operator.  Then, save 
		the scanned operator to the top of the operators stack.
		"""

		while operators and operators[-1] != '(' \
			and (self.precedence(operators[-1]) >= self.precedence(scanned_operator)): 
			self.makeAndSaveASTs(operators, operands)
		operators.append(scanned_operator)

	
	def precedence(self, operator):
		"""
		Contributor(s): Andres Rivera, Patrick Walker

		Returns the numerical precedence of each operator
		"""
		
		if operator == '*': # Greatest precedence
		 	return 2
		elif operator == 'concat':
			return 1
		else: # operator == '|', least precedence 
			return 0
	
	def makeAndSaveASTs(self, operators, operands):
		"""
		Contributor(s): Andres Rivera, Patrick Walker

		Makes a new AST out of the topmost operator of the operators stack and the topmost operand 
		(or 2 topmost operands) of the operands stack, and saves this new AST back to the operands stack.
		"""
		operator = operators.pop()
		if operator == '*': # Unary operator, so 1 operand needed
			operand = operands.pop()
			operands.append(AST.merge(operand, AST(), operator))
		else: # Binary operator, so 2 operands needed
			operand2 = operands.pop()
			operand1 = operands.pop()
			operands.append(AST.merge(operand1, operand2, operator))

	
	def constructNFA(self):
		"""
		Contributor(s): Andres Rivera, Patrick Walker

		Returns the NFA that is equivalent to the regex's equivalent AST.

		The algorithm to build the equivalent NFA is to read through each node in the AST,
		and depending on which node is read, the appropriate number of ASTs are used to construct that NFA.
		Each NFA is constructed according to the proof of equivalence between NFAs and regexes (given in 
		the book).
		"""
		nfa_stack = []
		for node in self.equivalent_ast:
			if node == '|':
				nfa2 = nfa_stack.pop()
				nfa1 = nfa_stack.pop()
				nfa_stack.append(self.unionNFA(nfa1, nfa2))
			elif node == '*':
				nfa_stack.append(self.starNFA(nfa_stack.pop()))
			elif node == 'concat':
				nfa2 = nfa_stack.pop()
				nfa1 = nfa_stack.pop()
				nfa_stack.append(self.concatNFA(nfa1, nfa2))
			elif node == 'N':
				nfa_stack.append(self.emptySetNFA())
			elif node == 'e': 
				nfa_stack.append(self.epsilonNFA())
			else:
				nfa_stack.append(self.oneSymbolNFA(node))
			
		return nfa_stack.pop()

	def oneSymbolNFA(self, char: str):
		"""
		Contributor(s): Andres Rivera

		Returns the equivalent NFA for the case that
		the (sub)regex is only one symbol in the alphabet.

		The NFA only has two states, 1 and 2, where there is only one transition: (1,char) --> {2}.
		State 2 is the only accept state while state 1 is the start state, and the NFA uses the (sub)regex's alphabet
		"""
		return NFA(2, self.alphabet, {(1,char):{2}}, 1, [2])


	def epsilonNFA(self):
		"""
		Contributor(s): Andres Rivera

		Returns the equivalent NFA for the case that the (sub)regex is epsilon ('e')

		The NFA only has one state, 1. There are no transitions, but state 1 is both 
		the start state and the only accept state. The NFA inherits the (sub)regex's alphabet.
		"""
		return NFA(1, self.alphabet, {}, 1, [1])

	def emptySetNFA(self):
		"""
		Contributor(s): Andres Rivera

		Returns the equivalent NFA for the case that the (sub)regex is the empty set ('N').

		The NFA has only one state (state 1), no transitions, no accept states, and the (sub)regex's 
		alphabet. State 1 is also the start state.
		"""
		return NFA(1, self.alphabet, {}, 1, [])

	def unionNFA(self, nfa1, nfa2):
		"""
		Contributor(s): Andres Rivera, Patrick Walker
		
		Constructs an NFA, via the "|" operator, the union of two input NFAs.
		The resulting NFA, with the appropriate components is returned to the constructNFA function.

		The algorithm for constructing an NFA from the union of two other NFA's is to add a new state, 
		define it as the start state, and renumber nfa1's and nfa2's states accordingly, so all states 
		are unique. All states in nfa1 are renumbered as (1 + state in nfa1) - incrementing all nfa1's 
		states by 1. Then, the algorithm renumbers nfa2's states by continuing where nfa1 left off, so 
		nfa2's states are now (1 + state in nfa2 + number of states in nfa1 ).  
		
		Finally, the algorithm defines the new NFA according to the construction in the proof that union 
		is closed under regular languages.
		"""
		num_states = 1 + nfa1.num_states + nfa2.num_states

		# Renumber nfa1's and nfa2's accept states and combine them 
		accept_states = [1+state for state in nfa1.accept_states] + [1+state+nfa1.num_states for state in nfa2.accept_states]

		transitions = {(1,'e'):{2,2+nfa1.num_states}} # new start state to nfa1's and nfa2's renumbered start states

		# Renumbering and saving nfa1's transitions
		for (curr_state, symbol),set_states in nfa1.transitions.items():
			renumbered_set = {state+1 for state in set_states}
			transitions[(curr_state+1,symbol)] = renumbered_set

		# Renumbering and saving nfa2's transitions
		for (curr_state, symbol),set_states in nfa2.transitions.items():
			renumbered_set = {1+state+nfa1.num_states for state in set_states}
			transitions[(1+curr_state+nfa1.num_states, symbol)] = renumbered_set

		return NFA(num_states, self.alphabet, transitions, 1, accept_states)

	def concatNFA(self,nfa1,nfa2):  # sourcery skip: set-comprehension
		"""
		Contributor(s): Andres Rivera, Patrick Walker
		
		Constructs an NFA, via the "concat" operator, the concatenation of two input NFAs.
		The resulting NFA, with the appropriate components is returned to the constructNFA function.

		The algorithm for constructing an NFA from the concatenation of two other NFAs is an implementation
		of the proof that concatenation is closed under regular languages. In renumbering our states, we 
		incremented the states of nfa2 by the number of states in nfa1.
		"""
		
		num_states = nfa1.num_states + nfa2.num_states 
		transitions = {}

		# For each accept state in NFA1, remove it from the accept states and 
		# create an epsilon transition from that accept state to the start state of NFA2. 
		while nfa1.accept_states: 
			current_accept_state = nfa1.accept_states.pop() 
			if (current_accept_state, 'e') in nfa1.transitions.keys():
				nfa1.transitions[(current_accept_state, 'e')] = nfa1.transitions[(current_accept_state, 'e')].union({nfa1.num_states + 1})
			else: 
				transitions[(current_accept_state, 'e')] = {nfa2.start_state+nfa1.num_states}
		
		# Re-number the states in the transitions of NFA2.
		for (curr_state, symbol), destinations in nfa2.transitions.items(): 
			curr_state += nfa1.num_states
			renumbered_set = set()
			for state in destinations:
				renumbered_set.add(state+nfa1.num_states)
			transitions[(curr_state,symbol)] = renumbered_set
		
		# Add to the transitions, all of the transitions from NFA1
		transitions.update(nfa1.transitions) 

		# Re-number the accept states of NFA2
		nfa2.accept_states = [accept_state + nfa1.num_states for accept_state in nfa2.accept_states]

		return NFA(num_states, self.alphabet, transitions, nfa1.start_state, nfa2.accept_states)

	def starNFA(self, nfa):
		"""
		Contributor(s): Andres Rivera, Patrick Walker
		
		Constructs an NFA, via the "*" operator, the star operation on a single NFA.
		The resulting NFA, with the appropriate components is returned to the constructNFA function.

		The algorithm for constructing an NFA from applying the Kleene star on an NFA is an implementation of the proof that
		this star operator is closed under regular languages. The algorithm renumbers the states of the original nfa by incrementing them by 1. 
		"""

		# The resulting NFA has one additional state
		nfa.num_states += 1

		new_transitions = {}

		# Add an epsilon transition from each of the NFAs accept states, to the NFAs start state, as long as an
		# epsilon transition does not yet exist. If it does, add the NFA's start state to the set of destinations
		for accept_state in nfa.accept_states: 
			if (accept_state, 'e') not in nfa.transitions.keys():
				nfa.transitions[(accept_state, 'e')] = {nfa.start_state}
			else:
				nfa.transitions[(accept_state, 'e')] = nfa.transitions[(accept_state, 'e')].union({nfa.start_state})

		# The new start state is 1
		nfa.start_state = 1

		new_transitions[(nfa.start_state, 'e')] = {2} # the old start state was 1, thus it is now 2

		# Re-number the accept states of the NFA
		nfa.accept_states = [accept_state + 1 for accept_state in nfa.accept_states] + [nfa.start_state]

		# Re-number the states in the transitions of the NFA
		for (curr_state, symbol), destinations in nfa.transitions.items(): 
			curr_state += 1
			renumbered_set = {state+1 for state in destinations}
			new_transitions[(curr_state,symbol)] = renumbered_set

		# Assign the newly-numbered transitions to be the NFAs transitions
		nfa.transitions = new_transitions

		return nfa

class AST: 
	""" Simulates an AST """

	def __init__(self, nodes=list()):
		"""
		Contributor(s): Andres Rivera, Patrick Walker

		Initializes AST from a list of nodes in postfix order
		"""
		self.nodes = nodes
	
	def __str__(self):
		"""
		Contributor(s): Andres Rivera
		
		Defines the string representation of an AST
		Returns the string representation of the list of nodes
		"""
		return str(self.nodes)

	def __iter__(self):
		"""
		Contributor(s): Andres Rivera

		Defines how to iterate over an AST
		Returns the iterator for the list of nodes
		"""
		return iter(self.nodes)

	@classmethod
	def merge(cls, leftSubtree, rightSubtree, root):
		"""
		Contributor(s): Andres Rivera, Patrick Walker

		Combines two ASTs into postfix order
		In our implementation, depth-first-traversal of 
		the AST is equivalent to the postfix ordering of
		the regex.
		"""
		return cls(leftSubtree.nodes + rightSubtree.nodes + [root])

class NFA:
	""" Simulates an NFA """

	def __init__(self, num_states, alphabet, transitions, start_state, accept_states):
		"""
		Contributor(s): Patrick, Andres
		Initializes NFA from memory by passing in all necessary pieces
		"""
		
		self.num_states = num_states # int()
		self.alphabet = alphabet # ''
		self.transitions = transitions # {} of (state, symbol):set(set of states) pairs
		self.start_state = start_state # int()
		self.accept_states = accept_states # [] of int()


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

class DFA:
	""" Simulates a DFA """

	def __init__(self, nfa, alphabet):
		"""
		Contributor(s): Andres Rivera, Patrick Walker
		Initializes a DFA from memory using the equivalent DFA of an NFA and the
		regex's alphabet.
		"""
		
		equivalent_dfa = nfa.constructDFA()
		self.num_states = len(equivalent_dfa[0])
		self.alphabet = alphabet
		self.transitions = equivalent_dfa[1]
		self.start_state = equivalent_dfa[2]
		self.accept_states = equivalent_dfa[3]
		
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

		return current_state in (self.accept_states)