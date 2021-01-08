# Name: test_pa3.py
# Author: Dr. Glick
# Date: July 1, 2020
# Description: Tests pa3 for comp 370, fall 2020

import pa3

def read_results_file(filename):
    file = open(filename)
    return [True if result == "true" else False for result in file.read().split()]

if __name__ == "__main__":
    num_test_files = 20
    for i in range(1, num_test_files + 1):
        regex_filename = f"regex{i}.txt"
        str_filename = f"str{i}.txt"
        correct_results_filename = f"correct{i}.txt"

        print(f"Testing regex {regex_filename} on strings from {str_filename}")
        try:
            # Create RegEx
            try:
                regex = pa3.RegEx(regex_filename)

                # Open results file, and make sure it is not invalid
                f = open(correct_results_filename)
                first_line = f.readline()
                f.close()
                if first_line == "Invalid expression":
                    print("  Incorrect results")
                    print("  Regular expression is invalid")
                else:
                    # Open string file.
                    string_file = open(str_filename)

                    # Test each string for membership in language of regex
                    results = []
                    for str in string_file:
                        results.append(regex.simulate(str.strip()))

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
            except pa3.InvalidExpression:
                correct_results = open(correct_results_filename).readline().strip()
                if correct_results == "Invalid expression":
                    print("  Correct results")
                else:
                    print("  Incorrect results")
                    print("  Regular expression is valid")
        except OSError as err:
            print(f"Could not open file: {err}")
        except Exception as err:
            print(f"Error simulating dfa: {err}")