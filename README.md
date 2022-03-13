# Automata, Computability and Formal Languages
Programs that explore the space of automata theory, the creaton and application of finite state machines and formal grammars. Though not present in these programs, studies included the topics of computability and Turing machines.

## TO RUN: 
1. Navigate to a directory containing a programs files and run the `test_*.py` file in the command line.
2. Use `run.sh` to test any of the programs. You will be prompted to provide the name of the program to run.


## Program Descriptions
---

### ***Deterministic Finite Automaton Simulator***

**DESCRIPTION**:

A Python program the simulates the computation of a DFA _M_ on an input string, and reports if the string is accepted by _M_. It reads in a text definition of a DFA _M_, reads in a string to computationally simulate, and evaluates to see if the string is in the language of the DFA. 

**TEST**

For each test DFA there is: 
* the DFA specification file (e.g. dfa1.txt),
* a file containing test strings (e.g. str1.txt),
* and a file containing the correct answers for each test string (e.g. correct1.txt), one answer (Accept or Reject) per line. 

The lines of correct1.txt correspond to the lines of str1.txt

To test, execute the following command:
    
    $ python3 test_py1.py

This tests the program's DFA class on all of the test DFAs in the files described above, and reports the results in the terminal.

### ***Nondeterministic Finite Automaton Simulator***

**DESCRIPTION**:

A Python program that converts an input NFA to an equivalent DFA. It reads in a text definition of NFA _N_, converts _N_ to a DFA _M_, and writes the text definition of _M_ to an external text file. By doing this, this program can then use the above program to read in a number of strings to computationally simulate, and evalutate to see if the strings are in the language of the DFA.

**TEST**:

Test Data Includes:

* the NFA specification file (e.g. nfa1.txt),
* a file containing test strings (e.g. str1.txt),
* and a file containing the correct answers for each test string (e.g. correct1.txt), one answer (_Accept_ or _Reject_) per line.

The lines of correct1.txt, for example, correspond to the lines of str1.txt

To test, execute the following command:
    
    $ python3 test_py2.py

This tests the accuracy of the program's conversion of the input NFA to the output DFA, and the subsequent computational simulations on the produced DFA. This testing function then applies the same tests as the first program by testing the DFA class on all of the test DFAs in the files produced by this program. It then reports the results in the terminal.

### ***Regular Expression Simulator and Lexical Analysis***

**DESCRIPTION**:

A Python program that creates a RegEx object by:
* taking in a text version of a regular expression (regex) and its alphabet from a file
* validating and parsing the regex string into an abstract syntax tree (AST)
* converting the AST to an equivalent NFA,
* and finally converting the NFA to an equivalent DFA (using the NFA simulator)

The resulting DFA, via the DFA Simulator (with a modified constructor for the DFA), can be used to determine whether an input string is in the language of the regex or not.

**TEST**:

For each test regular expression there is: 
* the regular expression specification file (e.g. regex1.txt),
* a file containing test strings (e.g. str1.txt),
* and a file containing the correct answers for each test string (e.g. correct1.txt)

The lines of correct1.txt, for example, correspond to the lines of str1.txt

To test, execute the following command:
    
    $ python3 test_py3.py

This tests the program's RegEx Class on all of the test regular expressions in the files described above, and it reports the results in the terminal. 


**NOTE:** _No modules/classes/libraries were used to complete the lexical analysis or parsing of the input strings, nor were they used for any of the other tasks that are part of the algorithms that were used in this programs implementation._

