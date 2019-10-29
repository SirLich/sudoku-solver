# sudoku_solver

## convert_to_board
```python
convert_to_board(s)
```

Converts a properly formated string into the board format.

Boards can be generated from https://qqwing.com/generate.html,
using the "compact" format.

:param s: string
:return: board

## get_illegal_row_set
```python
get_illegal_row_set(b, r)
```

Returns the set of numbers currently set along a given row.

This is used to test the legality of board-states.
:param b: board
:param r: int (0 to 8)

## get_illegal_column_set
```python
get_illegal_column_set(b, c)
```

Returns the set of numbers currently set along a given column.

This is used to test the legality of board-states.
:param b: board
:param c: int (0 to 8)

## get_illegal_zone_set
```python
get_illegal_zone_set(b, x, y)
```

Returns the set of numbers currently set within a zone.

This is used to test the legality of board-states.
:param b: board
:param x: int (0 to 3)
:param y: int (0 to 3)

## contains_duplicates
```python
contains_duplicates(s)
```

Returns boolean value based on whether an array contains duplicates.

:param s: any array
:return: boolean

## is_valid_board
```python
is_valid_board(b)
```

Returns boolean value based on whether a board is valid.

:param b: board
:return: boolean

## find_smallest_space
```python
find_smallest_space(b)
```

Finds the location on the board with the smallest number of possibilities.

:param b: board
:return: location tuple, such as (4,6)

## num_smallest_space
```python
num_smallest_space(b)
```

Returns the value of the space with the smallest number of possibilities.

:param b: board
:return: location tuple, such as (4,6)

## make_children
```python
make_children(b)
```

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

## is_solved
```python
is_solved(b)
```

Returns boolean value based on whether a board is solved.

:param b: board
:return: boolean

## rate_board
```python
rate_board(b)
```

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

## solve
```python
solve(board, max_iterations, iter_print)
```

Solves a sudoku board using a depth-first-ish heuristic-search.

:param board: board
:param max_iterations: int, maximum iterations
:param iter_print: int, how often the printer should run.
:return: solved board, or partially solved board (fallback if max-iterations are reached)
