from copy import deepcopy
import sys

# Artificial Intelligence Assignment Fall 2016
# Solves Rush Hour using Iterative Deepening Depth-First Search
sys.setrecursionlimit(1000)

def sanitize_input(rush_input):
    new_input = []
    for car in rush_input:
        car = list(car)
        car[2] = ord(car[2]) - 65
        car[3] = int(car[3]) - 1
        new_input += [car]
    return new_input

def format_output(rush_output):
    new_output = []
    for car in rush_output:
        row = chr(car[2] + 65)
        col = car[3] + 1
        new_output += ["{}{}{}{}".format(car[0], car[1], row, col)]
    return new_output

def size(node):
    """returns the size of the car"""
    car_type = node[0]
    if car_type is 'B':
        return 3
    else:
        return 2

# Getters
def get_type(node):
    return node[0]

def get_dir(node):
    return node[1]

def col(node):
    return node[3]

def row(node):
    return node[2]

def print_matrix(matrix):
    for row in matrix:
        print_str = ''
        for col in row:
            print_str += "{} ".format(col)
        print(print_str)            


def build_matrix(input):
    # initialize 6x6 matrix
    matrix = [[0 for x in range(0,6)] for x in range(0,6)]

    for car in input:
        pos = [row(car), col(car)]
        # print("BUILD MATRIX POS ",pos)
        for i in range(0, size(car)):
            matrix[pos[0]][pos[1]] = get_type(car)
            if (get_dir(car)) is 'H':
                pos[1] += 1
            else:
                pos[0] += 1
    return matrix

def print_matrix(matrix):
    for row in matrix:
        print_str = ''
        for col in row:
            print_str += "{} ".format(col)
        print(print_str)

def is_soln(inp):
    if ['I', 'H', 2, 4] in inp:
        return True
    return False


def move_car_H(car, cars, pos):
    spot = cars.index(car)
    new_cars = deepcopy(cars)
    new_cars[spot][3] = col(car) + pos
    return new_cars

def move_car_V(car, cars, pos):
    spot = cars.index(car)
    new_cars = deepcopy(cars)
    new_cars[spot][2] = row(car) + pos
    return new_cars



def expand(inp):
    # print("Visited Nodes {} \n".format(visited_nodes))
    matrix = build_matrix(inp)
    frontier = []
    if is_soln(inp):
        return True
    for car in inp:
        car_row = row(car)
        car_col = col(car)
        if get_dir(car) is 'V':
            # can move up?
            if car_row > 0 and matrix[car_row - 1][car_col] is 0:
                item = move_car_V(car, inp, -1)
                frontier += [item]
            # can move down?
            if car_row + size(car) < 6 and matrix[car_row + size(car)][car_col] is 0:
                item = move_car_V(car, inp, 1)
                frontier += [item]

        else:
            # can move left?
            if car_col > 0 and matrix[car_row][car_col - 1] is 0:
                item = move_car_H(car, inp, -1)
                frontier += [item]

            # can move right?
            if car_col + size(car) < 6 and matrix[car_row][car_col + size(car)] is 0:
                item = move_car_H(car, inp, 1)
                frontier += [item]
    return frontier


def dfs(inp, limit, level, print_nodes = False):
    global visited_nodes
    visited_nodes += 1

    print("Visited Nodes: ",visited_nodes)
    if print_nodes:
       print("Level {}".format(level))
       print("Node: {}".format(format_output(inp)))
    if is_soln(inp):
        return [inp]
    if limit > 0:
        frontier = expand(inp)
        for item in frontier:
            soln = dfs(item, limit - 1, level + 1, print_nodes)
            if soln:
                # print(inp)
                return [inp] + soln
    return False


def iterative_deepening(inp):
    limit = 1
    soln = False

    while not soln:
        soln = dfs(inp, limit, 0)
        limit += 1
    count = 0
    for item in soln:
        print("Move {}".format(count))
        print("State: ", format_output(item))
        print_matrix(build_matrix(item))
        print('\n')
        count += 1
    print("Ran with depth {} and visited {} nodes".format(limit, visited_nodes))

# TESTS
# rush_in = ['IHC3', 'CVA3', 'BHB4', 'CVC5', 'CVE5']
# rush_in2 = ['IHC4', 'CVA4', 'BVA6', 'CVD4', 'CHE5']
# inp = sanitize_input(rush_in)
# inp2 = sanitize_input(rush_in2)


# visited_nodes = 0
# iterative_deepening(inp2)
# dfs(inp, 3, 0)