import sys
from re import split as spl

if len(sys.argv) == 1:  # 1st case: only python file name passed as argument in CLI
    print('Error: Config file must be given')
    quit()
elif len(sys.argv) == 2:  # 2nd case: config file name passed as argument in CLI
    print('Checking validity of config file...')
else:  # 3rd case: too many arguments passed in CLI
    print('Error: Too many arguments')
    quit()

sigma = []
states = []
transitions = []
F = []
S = ''

with open(sys.argv[1]) as f:
    lines = f.readlines()

    if not lines:  # config file empty
        print('Error: Config file cannot be empty')
        quit()

    index = 0  # using variable index to go through each line
    while index < len(lines):
        if not (lines[index].strip()):  # if line is empty, return error
            print('Format error: Lines cannot be empty')
            quit()

        elif lines[index][0] != '#':  # if current line is not commented, begin search
            if 'Sigma:' == lines[index].strip():  # beginning of 'Sigma' section
                index += 1
                while index < len(lines) and 'End' != lines[index].strip():
                    if lines[index][0] != '#':
                        # if either beginning of other sections or empty line is encountered, throw error message
                        if lines[index].strip() in {'', 'States:', 'Transitions:'}:
                            print('Format error: Section "Sigma" must end with "End" line')
                            quit()
                        elif not (
                        lines[index].strip().isalnum()):  # only alphanumerical characters allowed for declaring letters
                            print('Format error: Section "Sigma" can only contain alphanumerical values')
                            quit()
                        sigma.append(lines[index].strip())

                    index += 1
                index += 1

            elif 'States:' == lines[index].strip():  # beginning of 'States' section
                index += 1
                while index < len(lines) and 'End' != lines[index].strip():
                    if lines[index][0] != '#':
                        if lines[index].strip() in {'', 'Sigma:', 'Transitions:'}:
                            print('Format error: Section "States" must end with "End" line')
                            quit()

                        # state name is stored for validation, regardless of identifiers (S or F)
                        state = lines[index].strip().rstrip(" ,FS").strip()
                        if not (state.strip().isalnum()):
                            print('Format error: Section "States" can only contain alphanumerical values')
                            quit()

                        states.append(state)

                        # if F identifier (by itself or along with S identifier) is found in current line, the state is stored
                        if ',F' in lines[index] or ',FS' in lines[index] or ',SF' in lines[index] or ', F' in lines[
                            index] or ', FS' in lines[index] or ', SF' in lines[index]:
                            F.append(state)

                        # if S identifier (by itself or along with F identifier) is found in current line, we check
                        # if initial state has already been set. either an error is thrown or the state is stored
                        if ',S' in lines[index] or ',FS' in lines[index] or ',SF' in lines[index] or ', S' in lines[
                            index] or ', FS' in lines[index] or ', SF' in lines[index]:
                            if S != '':
                                print('Condition error: There can only be one initial state')
                                quit()
                            else:
                                S = state

                    index += 1
                index += 1

            elif 'Transitions:' == lines[index].strip():  # beginning of 'Transitions' section
                index += 1
                while index < len(lines) and 'End' != lines[index].strip():
                    if lines[index][0] != '#':
                        if lines[index].strip() in {'', 'Sigma:', 'States:'}:
                            print('Format error: Section "Transitions" must end with "End" line')
                            quit()

                        # we split the line and store the values in a tuple for additional validation.
                        # if either more than 3 elements are encountered or non-alphanumerical characters
                        # are found, an error is thrown.
                        currentTransition = tuple([x for x in spl('[,\s+]+', lines[index]) if x])
                        if len(currentTransition) != 3:
                            print('Format error: Section "Transitions" must contain 3 values for each line')
                            quit()
                        for transition in currentTransition:
                            if not (transition.strip().isalnum()):
                                print('Format error: Section "Transitions" can only contain alphanumerical values')
                                quit()

                        transitions.append(currentTransition)

                    index += 1
                index += 1

            else:
                print('Format error: Config file can only contain "Sigma:", "States:" and "Transitions:" sections')
                quit()

        else:
            index += 1


# Function that returns the index of a given element in a list
def index(element, List = states):
    for i in range(len(List)):
        if element == List[i]:
            return i


# T-list that stores each 3-tuple in transitions (state1, letter, state2) where T[state1_index][state2_index]=letter
# initially, each value within it is null
T = [["null" for i in range(len(states))] for i in range(len(states))]

for transition in transitions:
    # verifies that all elements inside each tuple are valid members within states and sigma
    if transition[0] not in states:
        print(f'\'{transition[0]}\' not a valid state')
        quit()
    if transition[1] not in sigma:
        print(f'\'{transition[1]}\' not a valid letter')
        quit()
    if transition[2] not in states:
        print(f'\'{transition[2]}\' not a valid state')
        quit()

    state1, letter, state2 = index(transition[0]), transition[1], index(transition[2])
    if letter in T[state1]:         # testing for determinism; we check if current letter is already an element of T[state1]
        print("Condition error: DFA must have unique transition letters for each state")
        quit()
    else:                           # registers the current tuple
        T[state1][state2] = letter

print("Analyzed DFA is valid!")