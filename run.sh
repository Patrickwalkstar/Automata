echo "Please input the option: DFA, NFA, RELA"
echo "RELA stands for Regular Expression Lexical Analysis"
read option

if [ $option = "DFA" ]; then
    echo "The option selected was DFA"
    echo "Running the DFA test"
    cd Deterministic_Finite_Automaton_Simulator/Program_Files
    python test_pa1.py
    cd ../..
elif [ $option = "NFA" ]; then
    echo "The option selected was NFA"
    echo "Running the NFA test"
    cd Nondeterministic_Finite_Automaton_Simulator/Program_Files
    python test_pa2.py
    cd ../..
elif [ $option = "RELA" ]; then
    echo "The option selected was RELA, or Regular Expression Lexical Analysis"
    echo "Running the RELA test"
    cd Regular_Expression_Simulator_and_Lexical_Analysis/Program_Files
    python test_pa3.py
    cd ../..
else
    echo "Invalid Input"
fi