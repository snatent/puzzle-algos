from copy import deepcopy
import sys


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
    target_car = []
    for car in inp:
        if car[0] is 'I':
            target_car = car
            break
    if target_car[2] is 2 and target_car[3] is 4:
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



def expand(inp, visited_nodes):
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
                if item not in visited_nodes:
                    frontier += [item]
            # can move down?
            if car_row + size(car) < 6 and matrix[car_row + size(car)][car_col] is 0:
                item = move_car_V(car, inp, 1)
                if item not in visited_nodes:
                    frontier += [item]

        else:
            # can move left?
            if car_col > 0 and matrix[car_row][car_col - 1] is 0:
                item = move_car_H(car, inp, -1)
                if item not in visited_nodes:
                    frontier += [item]

            # can move right?
            if car_col + size(car) < 6 and matrix[car_row][car_col + size(car)] is 0:
                item = move_car_H(car, inp, 1)
                if item not in visited_nodes:
                    frontier += [item]
    return frontier



def get_cost(frontier):
    ret = []
    for state in frontier: 
        heuristic = 0
        row = build_matrix(state)[2]
        car = []
        for item in state:
            if item[0] is 'I':
                car = item
                break
        pos = car[3]
        for item in row[pos + 2:]:
            heuristic += 1
            if item is not 0:
                heuristic += 1
        ret += [(state, heuristic)]
    def getHeur(item):
        return item[1]

    # now we should sort them
    return sorted(ret, key=getHeur)


def dfs(inp, limit):
    if is_soln(inp):
        # print(inp)
        return [inp]
    if limit > 0:
        # print("Tesing this node with limit {}: ".format(limit))
        # print_matrix(build_matrix(inp))
        frontier = expand(inp)
        for item in frontier:
            soln = dfs(item, limit - 1)
            if soln:
                # print(inp)
                return [inp] + soln
    return False

def iterative_deepening(inp):
    limit = 1
    soln = False
    while not soln:
        soln = dfs(inp, limit)
        limit += 1
    print("Solved with limit {}".format(limit))
    count = 0
    for item in soln:
        print("Move {}".format(count))
        print_matrix(build_matrix(item))
        print('\n')
        count += 1


def astar(inp, travelled, visited_nodes):
    #print("On Level {}".format(travelled))
    #print_matrix(build_matrix(inp))
    visited_nodes += [inp]
    if is_soln(inp):
        print("Visited Nodes: {} Depth: {}".format(len(visited_nodes), travelled + 1))
        return [inp]
    cost_frontier = get_cost(expand(inp, visited_nodes))
    '''for item in cost_frontier:
        print("COST: {}".format(item[1]))

        print_matrix(build_matrix(item[0]))'''
    # get minimum cost
    for item in cost_frontier:
        soln = astar(item[0], travelled + 1, visited_nodes)
        if soln:
            return [inp] + soln

    return False



rush_in = ['IHC3', 'CVA3', 'BHB4', 'CVC5', 'CVE5']
inp = sanitize_input(rush_in)

rush_in2 = ['IHC4', 'CVA4', 'BVA6', 'CVD4', 'CHE5']
inp2 = sanitize_input(rush_in2)

rush_in3 = ['IHC4', 'BVC6', 'BHD1', 'CVD5', 'CVE3', 'BHF4']
inp3 = sanitize_input(rush_in3)

rush_in4 = ['IHC1', 'BHA2', 'CHA5', 'CHB5', 'CVC3', 'CVC6', 'BHE1', 'CVE6']
inp4 = sanitize_input(rush_in4)


# iterative_deepening(inp)
def test_input(inp, print_nodes = False):
    soln = astar(inp, 0, [])
    count = 0
    if print_nodes and soln:
        for item in soln:
            print("Move {}".format(count))
            print_matrix(build_matrix(item))
            print('\n')
            count += 1


test_input(inp)
test_input(inp2)
test_input(inp3)
test_input(inp4)