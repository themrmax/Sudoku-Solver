assignments = []

verbose_debug = 0
DEBUG_LEAST = 1
DEBUG_TWINS = 2
DEBUG_DIAGONAL = 4

rows = 'ABCDEFGHI'
cols = '123456789'
blank_dot = '.'
all_digits = '123456789'
ncols = len(cols)

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s + t for s in A for t in B]

boxes = cross(rows, cols)
nboxes = len(boxes)

row_units = [cross(r, cols) for r in rows]
# row_units[0] = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9']
column_units = [cross(rows, c) for c in cols]
# column_units[0] = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1']
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
# top left square is square_units[0] = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']

diagL = [i + j for i, j in list(zip(rows, cols))]
diagR = [i + j for i, j in list(zip(rows, reversed(cols)))]

unitlist = [diagL] + [diagR] + row_units + column_units + square_units
# unitlist = diagL + diagR + row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)


def display_datamodel():
    print('This is the Sudoku Project with {} boxes and {} columns'.format(nboxes, ncols))
    print(len(row_units), ' row units:')
    for ru in row_units:
        print(ru)
    print(len(column_units), ' col units: <just tilt your head 90 degrees counterclockwise i.e. to the left>')
    for cu in column_units:
        print(cu)
    print(len(square_units), ' square units:')
    for su in square_units:
        print(su)
    print('Number of rows = {} columns = {}  mini squares={}'
                 .format(len(row_units), len(column_units), len(square_units)))
    for ul in unitlist:
        print(ul)
    print('Units Hash List: ', len(units), ' - dict of boxes is associated with rows, cols or square units')
    for uk in units:
        print(uk, ':', units.get(uk))
    print('Peers Hash List: ', len(peers), ' peers - dict of units affected by any box except itself')
    for pk in peers:
        print(pk, ':', peers[pk])

    return

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    s_board = {}
    if len(grid) != nboxes:
        print('Wrong length of values and mismatched dimensions ', len(grid), ' vs ', nboxes)
    else:
        s_board = dict(zip(boxes, grid))
    for k, v in s_board.items():
        if v == blank_dot:
            # s_board[k] = all_digits
            s_board = assign_value(s_board, k, all_digits)
    return s_board

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    # from IPython.core.debugger import Tracer; Tracer()()
    # dynamically adjust display width used according to box with the longest value i.e.  blank has '123456789'
    if values is None:
        return
    bpu = 3  # boxes per dim of square unit
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * bpu)] * bpu)
    ordA = ord('A')
    # trick: use concatenated chars for rows and cols as box 2-D index
    # the +1 in width allows us to use null string than needing a space in formatting
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if (int(c) % bpu == 0) else '') for c in cols))
        if (ord(r) - ordA + 1) % bpu == 0:
            print(line)
    return


def tupleinList(L, val1, val2):
    if L:
        return (i for i, v in enumerate(L) if (v[1] == val1 and v[2] == val2) or (v[1] == val2 and v[2] ==val1))
    else:
        return 0

def findunit(k1, k2):
    return (u for u in units[k1] if k2 in u)


def naked_twins(grid):
    """Eliminate values using the naked twins strategy.
    Args:  grid(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns: the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of twins then verify if naked -meaning they both belong in the same unit
    # Eliminate the naked twins as possibilities for their peers
    # possible generalization naked siblings for > 2 ?

    # this bloody code looks like a C program not Pythonic :-(  fix prettier later

    numdigits = 2
    naked_list = []
    for t in grid:
        gval = grid[t]
        if (len(gval) == numdigits) :# treat as potential naked twin
            for p in peers[t]:
                if (gval == grid[p]):           # found a twin value in same peer
                    unit = findunit(t, p)       # store in list the unit to which naked pair belongs to
                    naked_twin = (gval, t, p, unit)    # create a list of tuples
                    naked_list.append(naked_twin)
                    # else: optimize later so as not to add commutative tuple?

    if naked_list != []:
        for naked_twin in naked_list:
            digitpair = naked_twin[0]
            for unit in enumerate(naked_twin[3]):
                for u in unit[1]:               # rewrite for a better way to do this!!!! ;-(
                    if len(grid[u]) >= numdigits and sorted(grid[u]) != sorted(digitpair):  # do not touch twins!
                        for rd in digitpair:    # rd is just 2 digits but this is for later generalization
                            if rd in grid[u]:
                                new_value = grid[u].replace(rd, '')
                                grid = assign_value(grid, u, new_value)
    return grid


def eliminate(values):
    """
    Eliminate values from peers of each box with a single value.
    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.
    Input Args:  values: Sudoku in dictionary form. 
    Returns:     Resulting Sudoku in dictionary form after eliminating values.
    """
    solved_values = [box for box in values if len(values[box]) == 1]
    for box in solved_values:
        bv = values[box]
        peerlist = peers[box]  # list of peers in RC notation
        for p in peerlist:
            for digit_taken in bv:  # check each digit in bv vs candidate values of peer
                newval = values[p].replace(digit_taken, '')
                values = assign_value(values, p, newval)
    return values


def only_choice(s_grid):
    """Finalize all values that are the only choice for a unit.
    Go through all the units, check unitlist (peer plus itself so you can set digit)
    and whenever there is a unit with a value
        that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choies.
    """
    for unit in unitlist:
        # check all 3 adjacent units: rows, cols, square
        for digit in all_digits:
            # make list of possible boxes for digit (pbfd)
            # Academic:why is optimized failing? i.e. skip box that has solution already?
            #       (if digit in s_grid[box] and (len(s_grid[box])>1))
            pbfd = [box for box in unit if digit in s_grid[box] ]
            if len(pbfd) == 1:  # only choice - possible box for digit
                ##  s_grid[pbfd[0]] = digit
                s_grid = assign_value(s_grid, pbfd[0], digit)
    return s_grid


def reduce_puzzle(values):
    # note auto-grader has a bug when submitted code has certain print functions, maybe it is running Python 2.x
    stalled = False
    reduction_count = 0

    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
#        if solved_values_before >= nboxes:
#             return values

        reduction_count += 1
        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        if verbose_debug > 0:
            print('--- Sudoku Grid after elimination strategy ', reduction_count)
            display(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        if verbose_debug > 0:
            print('--- Sudoku Grid after only choice strategy', reduction_count)
            display(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = (solved_values_before == solved_values_after)

        # Sanity check, return False if there is a box with zero available values:
        badlist = [box for box in values.keys() if len(values[box]) == 0]
        if len(badlist) > 0:
            if verbose_debug > 0:
                print('Exception (likely DUPLICATE BOX ENTRY) - Bad Solution!', badlist)
            return False
        # allow partially solved puzzle and return value grid
    return values


def search(values):
    """
    Using depth-first search and propagation, create a search tree and solve the sudoku
    """
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)  # note reduce puzzle may return partially solved values
    if values is False:  # if dictionary returned is empty grid means this instance of values is no solution
        return False
    if all(len(values[i]) == 1 for i in values):
        if verbose_debug > 0:
            print('This is final solution')
        return values  # DONE, exit all the way from DFS
    # Choose one of the unfilled squares with the fewest possibilities
    min_digits, fewest_branch = min((len(values[u]), u) for u in values if len(values[u]) > 1)
    # Now use recursion to solve each possible sudokus, and if one returns a value, return that answer!
    for candidate in values[fewest_branch]:
        # instantiate sub tree
        dup_values = values.copy()
        ## dup_values[fewest_branch] = candidate
        dup_values = assign_value(dup_values, fewest_branch, candidate)

        if verbose_debug > 0:
            print('Branching with ', fewest_branch, ' using candidate value=', candidate)
            display(dup_values)

        subtree_values = search(dup_values)
        if subtree_values:  # some grid solution found, pop back to caller owning tree
            return subtree_values  # exit all the way
    # WARNING: do not automatically return values after for loop - it might have to be an empty grid


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    s_grid = grid_values(grid)

    ### --- debugging code ---
    if (verbose_debug & DEBUG_DIAGONAL) == DEBUG_DIAGONAL:
        print('Sudoku Grid - START')
        display(s_grid)
    ### --- end of debugging ---

    s_grid = search(s_grid)

    ### --- debugging code ---
    if (verbose_debug & DEBUG_DIAGONAL) == DEBUG_DIAGONAL:
        print('Sudoku Grid - PUZZLE END STATE')
        display(s_grid)
    ### --- end of debugging ---

    return s_grid


if __name__ == '__main__':

    ### --------------------------------- start verbose debug ----------------------------------------
    if (verbose_debug > DEBUG_DIAGONAL):
        display_datamodel()

    if ((verbose_debug & DEBUG_TWINS )== DEBUG_TWINS):
        before_naked_twins_1 = {'I6': '4', 'H9': '3', 'I2': '6', 'E8': '1', 'H3': '5', 'H7': '8', 'I7': '1', 'I4': '8',
                            'H5': '6', 'F9': '7', 'G7': '6', 'G6': '3', 'G5': '2', 'E1': '8', 'G3': '1', 'G2': '8',
                            'G1': '7', 'I1': '23', 'C8': '5', 'I3': '23', 'E5': '347', 'I5': '5', 'C9': '1', 'G9': '5',
                            'G8': '4', 'A1': '1', 'A3': '4', 'A2': '237', 'A5': '9', 'A4': '2357', 'A7': '27',
                            'A6': '257', 'C3': '8', 'C2': '237', 'C1': '23', 'E6': '579', 'C7': '9', 'C6': '6',
                            'C5': '37', 'C4': '4', 'I9': '9', 'D8': '8', 'I8': '7', 'E4': '6', 'D9': '6', 'H8': '2',
                            'F6': '125', 'A9': '8', 'G4': '9', 'A8': '6', 'E7': '345', 'E3': '379', 'F1': '6',
                            'F2': '4', 'F3': '23', 'F4': '1235', 'F5': '8', 'E2': '37', 'F7': '35', 'F8': '9',
                            'D2': '1', 'H1': '4', 'H6': '17', 'H2': '9', 'H4': '17', 'D3': '2379', 'B4': '27',
                            'B5': '1', 'B6': '8', 'B7': '27', 'E9': '2', 'B1': '9', 'B2': '5', 'B3': '6', 'D6': '279',
                            'D7': '34', 'D4': '237', 'D5': '347', 'B8': '3', 'B9': '4', 'D1': '5'}

        print('Naked Twins Sample 1 - before')
        display(before_naked_twins_1)
        naked_twins(before_naked_twins_1)
        print('Naked Twins Sample 1 - after')
        display(before_naked_twins_1)

        ans1 =  {'G7': '6', 'G6': '3', 'G5': '2', 'G4': '9', 'G3': '1', 'G2': '8', 'G1': '7', 'G9': '5', 'G8': '4', 'C9': '1',
         'C8': '5', 'C3': '8', 'C2': '237', 'C1': '23', 'C7': '9', 'C6': '6', 'C5': '37', 'A4': '2357', 'A9': '8',
         'A8': '6', 'F1': '6', 'F2': '4', 'F3': '23', 'F4': '1235', 'F5': '8', 'F6': '125', 'F7': '35', 'F8': '9',
         'F9': '7', 'B4': '27', 'B5': '1', 'B6': '8', 'B7': '27', 'E9': '2', 'B1': '9', 'B2': '5', 'B3': '6', 'C4': '4',
         'B8': '3', 'B9': '4', 'I9': '9', 'I8': '7', 'I1': '23', 'I3': '23', 'I2': '6', 'I5': '5', 'I4': '8', 'I7': '1',
         'I6': '4', 'A1': '1', 'A3': '4', 'A2': '237', 'A5': '9', 'E8': '1', 'A7': '27', 'A6': '257', 'E5': '347',
         'E4': '6', 'E7': '345', 'E6': '579', 'E1': '8', 'E3': '79', 'E2': '37', 'H8': '2', 'H9': '3', 'H2': '9',
         'H3': '5', 'H1': '4', 'H6': '17', 'H7': '8', 'H4': '17', 'H5': '6', 'D8': '8', 'D9': '6', 'D6': '279',
         'D7': '34', 'D4': '237', 'D5': '347', 'D2': '1', 'D3': '79', 'D1': '5'}

        ans2 = {'I6': '4', 'H9': '3', 'I2': '6', 'E8': '1', 'H3': '5', 'H7': '8', 'I7': '1', 'I4': '8', 'H5': '6', 'F9': '7',
         'G7': '6', 'G6': '3', 'G5': '2', 'E1': '8', 'G3': '1', 'G2': '8', 'G1': '7', 'I1': '23', 'C8': '5', 'I3': '23',
         'E5': '347', 'I5': '5', 'C9': '1', 'G9': '5', 'G8': '4', 'A1': '1', 'A3': '4', 'A2': '237', 'A5': '9',
         'A4': '2357', 'A7': '27', 'A6': '257', 'C3': '8', 'C2': '237', 'C1': '23', 'E6': '579', 'C7': '9', 'C6': '6',
         'C5': '37', 'C4': '4', 'I9': '9', 'D8': '8', 'I8': '7', 'E4': '6', 'D9': '6', 'H8': '2', 'F6': '125',
         'A9': '8', 'G4': '9', 'A8': '6', 'E7': '345', 'E3': '79', 'F1': '6', 'F2': '4', 'F3': '23', 'F4': '1235',
         'F5': '8', 'E2': '3', 'F7': '35', 'F8': '9', 'D2': '1', 'H1': '4', 'H6': '17', 'H2': '9', 'H4': '17',
         'D3': '79', 'B4': '27', 'B5': '1', 'B6': '8', 'B7': '27', 'E9': '2', 'B1': '9', 'B2': '5', 'B3': '6',
         'D6': '279', 'D7': '34', 'D4': '237', 'D5': '347', 'B8': '3', 'B9': '4', 'D1': '5'}

        print('-- expected answer --')
        display(ans1)
        print('-- expected answer --')
        display(ans2)


        before_naked_u = {"G7": "2345678", "G6": "1236789", "G5": "23456789", "G4": "345678",
         "G3": "1234569", "G2": "12345678", "G1": "23456789", "G9": "24578",
         "G8": "345678", "C9": "124578", "C8": "3456789", "C3": "1234569",
         "C2": "1234568", "C1": "2345689", "C7": "2345678", "C6": "236789",
         "C5": "23456789", "C4": "345678", "E5": "678", "E4": "2", "F1": "1",
         "F2": "24", "F3": "24", "F4": "9", "F5": "37", "F6": "37", "F7": "58",
         "F8": "58", "F9": "6", "B4": "345678", "B5": "23456789", "B6":
             "236789", "B7": "2345678", "B1": "2345689", "B2": "1234568", "B3":
             "1234569", "B8": "3456789", "B9": "124578", "I9": "9", "I8": "345678",
         "I1": "2345678", "I3": "23456", "I2": "2345678", "I5": "2345678",
         "I4": "345678", "I7": "1", "I6": "23678", "A1": "2345689", "A3": "7",
         "A2": "234568", "E9": "3", "A4": "34568", "A7": "234568", "A6":
             "23689", "A9": "2458", "A8": "345689", "E7": "9", "E6": "4", "E1":
             "567", "E3": "56", "E2": "567", "E8": "1", "A5": "1", "H8": "345678",
         "H9": "24578", "H2": "12345678", "H3": "1234569", "H1": "23456789",
         "H6": "1236789", "H7": "2345678", "H4": "345678", "H5": "23456789",
         "D8": "2", "D9": "47", "D6": "5", "D7": "47", "D4": "1", "D5": "36",
         "D2": "9", "D3": "8", "D1": "36"}

        print('Naked Twins Sample from Udacity -- before')
        display(before_naked_u)
        naked_twins(before_naked_u)
        print('Naked Twins from Udacity - after')
        display(before_naked_u)

        puzzle_01 = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
        puzzle_02 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'

    ###-------------------------------- end verbose debug ---------------------------------------

    # ====================   OFFICIAL ASSIGNMENT ======================
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    if (verbose_debug & DEBUG_DIAGONAL) == DEBUG_DIAGONAL:
        print('================================')
        print('Cross Validation / Test of Diagonal Sudoku')
        diag_sudoku_grid0 = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
        display(solve(diag_sudoku_grid0))

    ### - optional - Collapsible scaffolding code. Tests other sudokus from the web - future:read a text file input
    multiple_puzzles = False

    if (multiple_puzzles is True):
        puzzleList = [
            '4.......3..9.........1...7.....1.8.....5.9.....1.2.....3...5.........7..7.......8',  # D1.00
            '......3.......12..71..9......36...................56......4..67..95.......8......',  # D1.01
            '....3...1..6..........9...5.......6..1.7.8.2..8.......3...1..........7..9...2....',  # D1.02
            '...47..........8.........5.9..2.1...4.......6...3.6..1.7.........4..........89...',  # D1.03
            '...4.....37.5............89....9......2...7......3....43............2.45.....6...',  # D1.04
            '..7........5.4...........18...3.6....1.....7....8.2...62...........9.6........4..',  # D1.05
            '....29.......7......3...8..........735.....161..........6...4......6.......83....',  # D1.06
            '7.......8.....14...4........7..1.......4.3.......6..2........3...35.....5.......4',  # D1.07
            '5.......7......2.....3...1...8.4.......7.8.......2.9...8...5.....1......6.......9',  # D1.08
            '..682...........69..7.......2..........9.4..........8.......5..58...........521..'  # D1.09
        ]
        print('Run other sudoku diagonal problems')
        for puzzle in puzzleList:
            print('================================ Next Puzzle ')
            print('START:')
            display(grid_values(puzzle))
            print('SOLUTION:')
            display(solve(puzzle))
        print('========== THE END ============')


    ###

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
