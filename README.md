# Sudoku-Solver

## Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

answers by (manny) Emmanuel.P.Ablaza@gmail.com

# Question 1 (Naked Twins)

Q: How do we use constraint propagation to solve the naked twins problem?  

A: * (note: if a definition of constraint propagation is needed, see below). 

For the naked twins problem, constraint propagation helps by limiting for us values to choose from in related squares (i.e. squares belonging in the same unit as the twins).

If there are 2 unsolved squares (let us call them "naked twins") "
such that these squares have the same 2 possible values
(no other value will be valid for these twins because of other constraints),such twins will help us narrow down the overall solution.

We can eliminate these 2 values that work for the twins from
the set of possible values of other unsolved squares in the same units to which these twin squares belong to.

(note: recall that a unit is a row or a column or a square 3x3 in size, or a diagonal if the original square is along the longest
left leaning or right leaning diagonal) 

Perhaps we should explain first: What is constraint propagation?
The constraint propagation is a method of satisfying a certain number of constraints on a given system, equation or problem, where there might be some initial "freedom" or choices of what
allowable values can be input into system, or variables of the equation can have.

Now given a set of allowable inputs, the other related/dependent variables will be taking on other allowed values (can be computed from the original constraint). This process continues recursively until there are no more changes in the system or in the equation.

So for example, a couple of the algorithms we know could help us implement constraint propagation for Sudoku are:
(1) If a square has only one candidate value, then eliminate that value from the square's peers. 
(2) If a unit has only choice remaining place for a value, then put the value there. These above in turn simplifies, or reduces the Sudoku puzzle.
*

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  

A: *For the diagonal sudoku problem, essentially the new constraint states "no number value may appear more than once in the longest diagonal from top left to bottom right and top right to bottom left".

This is a very similar way of stating the original constraints
that no any two squares in the same unit (row, column or 3x3 square) may have the same value.

Think of the squares in the longest left leaning and right leaning diagonals of the grid as having as additional unit the diagonal to which it belongs, respectively.  Notice E5 will be in both diagonal units.

Then just use the same general sudoku constraint propagation as before. Solving additional diagonal constraints simply meant adding the diagonals into units, so that the unitlist and peers will include the squares that are in these diagonals. When the constraint propagation is done, it is considering the diagonals as well in evaluating validity of values assignment. All other squares outside of the diagonals follow original constraints.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

