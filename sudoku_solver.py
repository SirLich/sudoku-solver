#!/usr/bin/python3

from queue import PriorityQueue
import copy
import pprint

#Credits:
# Generate puzzles: https://qqwing.com/generate.html, use "compact" format.

#Some sample puzzles to solve:
p1 = '''..1...7.8
        ...5.....
        .6...35..
        .3.7..68.
        5.78..14.
        .2.......
        7.3..1...
        ........6
        ....28.3.'''

p2 = '''2...8.1.5
        ......93.
        531.....2
        ..95..8..
        42..3....
        75..98...
        ..2....9.
        8.....5..
        .4.....27'''

p3 = '''...3..51.
        ........8
        ..2.8..3.
        .915..26.
        ....6....
        6...71.5.
        ..61...2.
        8.9..6...
        3...5.6..'''


def convert_to_board(s):
    """
    Converts a properly formated string into the board format.

    Boards can be generated from https://qqwing.com/generate.html,
    using the "compact" format.

    :param s: string
    :return: board
    """
    board = []
    for line in s.split("\n"):
        row = []
        for c in line.strip():
            if(c == '.'):
                space = [1,2,3,4,5,6,7,8,9]
            else:
                space = [int(c)]
            row.append(space)
        board.append(row)
    return board

def get_illegal_row_set(b, r):
    """
    Returns the set of numbers currently set along a given row.

    This is used to test the legality of board-states.
    :param b: board
    :param r: int (0 to 8)
    """
    illegal = []
    for space in b[r]:
        if len(space) == 1:
            illegal.append(space[0])
    return illegal

def get_illegal_column_set(b, c):
    """
    Returns the set of numbers currently set along a given column.

    This is used to test the legality of board-states.
    :param b: board
    :param c: int (0 to 8)
    """
    illegal = []
    for row in b:
        if(len(row[c]) == 1):
            illegal.append(row[c][0])
    return illegal

def get_illegal_zone_set(b, x, y):
    """
    Returns the set of numbers currently set within a zone.

    This is used to test the legality of board-states.
    :param b: board
    :param x: int (0 to 3)
    :param y: int (0 to 3)
    """
    illegal = []
    for i in range(y*3, y*3 + 3):
        for j in range(x*3, x*3 + 3):
            if(len(b[i][j]) == 1):
                illegal.append(b[i][j][0])
    return illegal


def contains_duplicates(s):
    """
    Returns boolean value based on whether an array contains duplicates.

    :param s: any array
    :return: boolean
    """
    return len(set(s)) != len(s)

def is_valid_board(b):
    """
    Returns boolean value based on whether a board is valid.

    :param b: board
    :return: boolean
    """
    for i in range(9):
        if(contains_duplicates(get_illegal_row_set(b, i))):
            return False

    for i in range(9):
        if(contains_duplicates(get_illegal_column_set(b, i))):
            return False

    for i in range(3):
        for j in range(3):
            if(contains_duplicates(get_illegal_zone_set(b, i, j))):
                return False
    return True

def find_smallest_space(b):
    """
    Finds the location on the board with the smallest number of possibilities.

    :param b: board
    :return: location tuple, such as (4,6)
    """
    smallest = 10
    loc = [0, 0]
    for i in range(9):
        for j in range(9):
            if(len(b[i][j]) <= smallest and len(b[i][j]) != 1):
                smallest = len(b[i][j])
                loc = [i, j]
    return loc

def num_smallest_space(b):
    """
    Returns the value of the space with the smallest number of possibilities.

    :param b: board
    :return: location tuple, such as (4,6)
    """
    loc = find_smallest_space(b)
    return str(len(b[loc[0]][loc[1]]))

def make_children(b):
    """
    Creates children of a board by creating duplicates of the board with a
    small change.

    In this case, the small change is finding the location with the smallest
    non-one possibilities (such as space (0,3) with possibilities [1,3,5]) and
    setting that space to each possibility.

    So in this case, space (0, 3) would be set to:
    Child one: [1]
    Child two: [3]
    Child three: [5]

    :param b: board
    :return: array of boards
    """
    children = []
    loc = find_smallest_space(b)
    for mark in b[loc[0]][loc[1]]:
        child = copy.deepcopy(b)
        child[loc[0]][loc[1]] = [mark]
        children.append(child)
    return children

def is_solved(b):
    """
    Returns boolean value based on whether a board is solved.

    :param b: board
    :return: boolean
    """
    if(not is_valid_board(b)):
        return False

    for row in b:
        for space in row:
            if(len(space) != 1):
                return False
    return True

def rate_board(b):
    """
    Heuristic function for rating a boards viability.

    The heuristic works by weighting two different measures:
    board-completion:
        This is calculated as the number of spaces which only have
        one possibility.

    smallest-possibility:
        This is calculated as whichever space has the smallest non-one numbers
        of possibility.

    The heuristic first weights for board-competion, and the "tie-breaker" is
    by finding the board with the least complexity. In other words, whichever
    board will spawn the least-number of chilren when calling make_children.

    :param b: board
    :return: int rating
    """
    filled = 0
    for row in b:
        for space in row:
            if(len(space) == 1):
                filled += 1

    return - (filled * 100 + int(num_smallest_space(b)))


def solve(board, max_iterations, iter_print):
    """
    Solves a sudoku board using a depth-first-ish heuristic-search.

    :param board: board
    :param max_iterations: int, maximum iterations
    :param iter_print: int, how often the printer should run.
    :return: solved board, or partially solved board (fallback if max-iterations are reached)
    """
    #Seed the boards with the starting board
    boards = PriorityQueue()
    boards.put((rate_board(board), board, 0))

    #Iterate over the boards, pulling from the highest rated
    iterations = 0

    while not boards.empty():
        t = boards.get()
        b = t[1]

        #Print some statistics each iter_print
        if(iterations%iter_print == 0):
            print("iteration: " + str(iterations))
            print(str(rate_board(b)) + " rating")
            print("")

        iterations += 1

        #End early, if we overmax
        if(iterations > max_iterations):
            print("MAX ITERATIONS REACHED:")
            return b

        #End early if we found a board!
        if(is_solved(b)):
            print("SOLVED:")
            return b

        #Only make new children if the board is valid
        if(is_valid_board):
            children = make_children(copy.deepcopy(b))
            for child in children:
                if(is_valid_board(child)):
                    boards.put((rate_board(child), child, iterations))

#Global to call the solver :)
pp = pprint.PrettyPrinter(indent=4)

print("SOLVING p1")
pp.pprint(solve(convert_to_board(p1), 50000, 500))

print("SOLVING p2")
pp.pprint(solve(convert_to_board(p2), 50000, 500))

print("SOLVING p3")
pp.pprint(solve(convert_to_board(p3), 50000, 500))




























#bottom
