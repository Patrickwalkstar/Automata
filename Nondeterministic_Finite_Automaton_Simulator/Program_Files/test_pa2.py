# Name: test_pa1.py
# Author: Dr. Glick
# Date: July 1, 2020
# Description: Tests pa2 for comp 370, fall 2020

import pa1
import pa2

def read_results_file(filename):
    file = open(filename)
    return [True if result == "Accept" else False for result in file.read().split()]

if __name__ == "__main__":
    num_test_files = 14
    for i in range(1, num_test_files + 1):
        nfa_filename = f"nfa{i}.txt"
        dfa_filename = f"dfa{i}.txt"
        input_filename = f"str{i}.txt"
        correct_results_filename = f"correct{i}.txt"

        print(f"Testing NFA {nfa_filename} on strings from {input_filename}")
        try:
            # Create NFA
            nfa = pa2.NFA(nfa_filename)

            # Convert to DFA
            nfa.toDFA(dfa_filename)

            # Create the DFA
            dfa = pa1.DFA(dfa_filename)

            # Open string file.
            string_file = open(input_filename)

            # Simulate DFA on test strings
            results = []
            for str in string_file:
                results.append(dfa.simulate(str.strip()))

            # Get correct results
            correct_results = read_results_file(correct_results_filename)

            # Check if correct
            if results == correct_results:
                print("  Correct results")
            else:
                print("  Incorrect results")
                print(f"  Your results = {results}")
                print(f"  Correct results = {correct_results}")
            print()
        except OSError as err:
            print(f"Could not open file: {err}")
        except Exception as err:
            print(f"Error simulating dfa: {err}")