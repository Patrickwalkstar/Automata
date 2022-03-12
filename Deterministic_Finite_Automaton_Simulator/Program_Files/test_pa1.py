# Name: test_pa1.py
# Author: Dr. Glick
# Date: July 1, 2020
# Description: Tests pa1 for comp 370, fall 2020

import pa1

def read_results_file(filename):
    file = open(filename)
    return [True if result == "Accept" else False for result in file.read().split()]

if __name__ == "__main__":
    test_dfa_files = ["dfa1.txt", "dfa2.txt", "dfa3.txt", "dfa4.txt", "dfa5.txt",
                        "dfa6.txt", "dfa7.txt", "dfa8.txt", "dfa9.txt", "dfa10.txt"]
    test_string_files = ["str1.txt", "str2.txt", "str3.txt", "str4.txt", "str5.txt",
                        "str6.txt", "str7.txt", "str8.txt", "str9.txt", "str10.txt"]
    correct_output_files = ["correct1.txt", "correct2.txt", "correct3.txt",
                            "correct4.txt", "correct5.txt", "correct6.txt",
                            "correct7.txt", "correct8.txt", "correct9.txt",
                            "correct10.txt"]

    for i in range(len(test_dfa_files)):
        print(f"Testing DFA {test_dfa_files[i]} on strings from {test_string_files[i]}")
        try:
            # Create DFA
            dfa = pa1.DFA(test_dfa_files[i])

            # Open string file.
            string_file = open(test_string_files[i])

            # Simulate DFA on test strings
            results = []
            for str in string_file:
                results.append(dfa.simulate(str.strip()))

            # Get correct results
            correct_results = read_results_file(correct_output_files[i])

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