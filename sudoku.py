import copy

class Variable():
    """ create new variable with coordinates """
    def __init__(self, y, x):
        self.x = x
        self.y = y

    """ define hashing of variable to use it as key in dicts and store them in sets"""
    def __hash__(self):
        return hash((self.x, self.y))

    """ define a way to determine whether to variables are equal"""
    def __eq__(self, other):
        return (
                (self.x == other.x) and
                (self.y == other.y)
                )

    """ define string representation of class """
    def __str__(self):
        return f"({self.y}, {self.x})"


    def __repr__(self):
        return f"Variable({self.y}, {self.x})"


class Sudoku():
    """ define structure of a crossword """
    def __init__(self, structure_file):

        with open(structure_file) as f:
            contents = f.read().splitlines()
            self.height = len(contents)
            self.width = self.height

            #You may add a check that provided structure is correct

            self.structure = []
            for y in range(self.height):
                row = []
                for x in range(self.width):
                    if contents[y][x].isdigit():
                        row.append(contents[y][x])
                    else:
                        row.append(False)
                self.structure.append(row)

        # determine variables set
        self.variables = set()
        for y in range(self.height):
            for x in range(self.width):
                self.variables.add(Variable(y, x))

        # determine initial assignment
        self.initial_assignment = dict()
        for variable in self.variables:
            if self.structure[variable.y][variable.x]:
                self.initial_assignment[variable] = int(self.structure[variable.y][variable.x])

    #return set of all variables that are constraining current variable (hirizontal and vertical row)
    def neighbors(self, var):
        neighbors = set()
        for variable in self.variables:
            if var == variable:
                continue
            elif (var.x == variable.x) ^ (var.y == variable.y):
                neighbors.add(variable)
            elif (var.x // 3 == variable.x // 3) and (var.y // 3 == variable.y // 3):
                neighbors.add(variable)

        return neighbors

class SudokuSolver():

    counter = 0

    def __init__(self, sudoku):
        self.sudoku = sudoku

        #initialize domains for all variables
        values = set(i for i in range(1,10))
        self.domains = {var : values.copy() for var in self.sudoku.variables}

    #return 2D array representing current assignment
    def grid(self, assignment):
        # create empty grid with None for every cell
        grid = [
            [None for _ in range(self.sudoku.width)]
            for _ in range(self.sudoku.height)
        ]

        for var, value in assignment.items():
            grid[var.y][var.x] = value

        return grid

    # print current assignment to the terminal
    def print(self, assignment):
        grid = self.grid(assignment)
        for y in range(self.sudoku.height):
            for x in range(self.sudoku.width):
                print(grid[y][x] or "#", end="")
            print()

    def solve(self):
    # Enforce node and arc consistency, and then solve the CSP.
        self.ac3(self.sudoku.initial_assignment)
        return self.backtrack(self.sudoku.initial_assignment)

    # check that assignment is consistent: no same numbers in horizontal and vertical rows
    def consistent(self, assignment):

        for variable in assignment:
            neighbors = self.sudoku.neighbors(variable)
            for neighbor in neighbors:
                if neighbor in assignment:
                    if assignment[variable] == assignment[neighbor]:
                        return False
        return True

    # return unassigned variable
    def select_unassigned_var(self, assignment):
        values_in_domain = 10

        for var in self.sudoku.variables:
            if var not in assignment:
                if len(self.domains[var]) < values_in_domain:
                    unassigned_var = var
                    values_in_domain = len(self.domains[var])
                

        return unassigned_var

    # check whether the assignment is complete
    def assignment_complete(self, assignment):
        if not assignment:
            return False

        if len(assignment) != len(self.sudoku.variables):
            return False

        for key in assignment:
            if assignment[key] == None:
                return False

        return True

    # some heuristic to remove values from domain that are not in line with current assignment
    def ac3(self, assignment, var = None):

        # if algorithm initialized for the first time with only initial data
        if not var:
            for variable_x in self.sudoku.variables:
                if variable_x in assignment:
                    continue
                for variable_y in self.sudoku.neighbors(variable_x):
                    if variable_y not in assignment:
                        continue
                    for value in self.domains[variable_x].copy():
                        if value == assignment[variable_y]:
                            self.domains[variable_x].remove(value)
        return True


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        if self.assignment_complete(assignment):
            return assignment

        #try new variable
        var = self.select_unassigned_var(assignment)

        for value in self.domains[var]:
            self.counter += 1

            new_assignment = assignment.copy()
            new_assignment[var] = value
            tmp_domain = copy.deepcopy(self.domains)
            self.ac3(new_assignment)

            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result is not None:
                    return result
            self.domains = copy.deepcopy(tmp_domain)
        return None

"""
sudoku = Sudoku("structure0.txt")
solver = SudokuSolver(sudoku)
solver.print(solver.sudoku.initial_assignment)
print()
assignment = solver.solve()

if assignment is None:
    print("No solution")
else:
    solver.print(assignment)

print(solver.counter)
"""








