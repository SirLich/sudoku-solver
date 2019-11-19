# Sudoku Solver

This Sudoku solver was written for Intro to Evolutionary Computation 2019.

You can run like `python3 sudoku_solver.py` or `./sudoku_solver.py`, if you mark it executable first.

The script will automatically solve three puzzles, marked `easy` `medium` and `hard`. Additional puzzles can be created using this tool: https://qqwing.com/generate.html (use the compact format).

The solver uses A*-search using a very depth-first-ish heuristic to brute force solutions.
