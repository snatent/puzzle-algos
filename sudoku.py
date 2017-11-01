import math

# Simple Sudoku Solver - Artificial Intelligence Assignment Fall 2016
# Uses Belief Propagation

def print_matrix(matrix):
    for row in matrix:
        str = ''
        for item in row:
            str += '{} '.format(item)
        print(str)

def get_row(matrix, index):
    return matrix[index]

def get_col(matrix, index):
    ret = []
    for row in matrix:
        ret += [row[index]]
    return ret

def get_square(matrix, x_index, y_index):
    row_start = 3 * math.floor(x_index/3)
    col_start = 3 * math.floor(y_index/3)
    ret = [i[col_start:col_start + 3] for i in matrix[row_start:row_start + 3]]
    return ret

def get_square_numbers(square):
    nums = []
    for row in square:
        for item in row:
            nums += [item]
    return set(nums)


def count_empty_spaces(matrix):
    count = 0
    for row in matrix:
        for item in row:
            if item is 0: 
                count +=1
    return count



def check_space(matrix, belief_matrix, x_index, y_index):
    """This function checks a single space on the board to see what is and is not
    within the realm of possibility"""
    row = get_row(matrix, x_index)  # Getting messages from row factor
    col = get_col(matrix, y_index)  # Getting messages from column factor
    square = get_square_numbers(get_square(matrix, x_index, y_index))  # Getting messages from square factor

    features = [row, col, square]
    possibilities = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for feature in features:
        for item in feature:
            if item in possibilities:
                possibilities.remove(item)
    belief_matrix[x_index][y_index] = possibilities # Sending message from variable



def solve_sudoku(matrix, belief_matrix):
    count = count_empty_spaces(matrix)
    while(count > 0):
        for x in range(0,9):
            for y in range(0,9):
                if matrix[x][y] is 0:
                    check_space(matrix, belief_matrix, x, y)
                    if len(belief_matrix[x][y]) is 1:
                        matrix[x][y] = belief_matrix[x][y][0]
                        count -= 1
    print_matrix(matrix)




# TESTS

# matrix = [ 
#    [0,0,3,0,2,0,6,0,0],
#    [9,0,0,3,0,5,0,0,1],
#    [0,0,1,8,0,6,4,0,0],
#    [0,0,8,1,0,2,9,0,0],
#    [7,0,0,0,0,0,0,0,8],
#    [0,0,6,7,0,8,2,0,0],
#    [0,0,2,6,0,9,5,0,0],
#    [8,0,0,2,0,3,0,0,9],
#    [0,0,5,0,1,0,3,0,0]
#    ]

# belief_matrix = [[{1, 2, 3, 4, 5, 6, 7, 8, 9} for x in range(0, 9)] for x in range(0,9)]

# solve_sudoku(matrix, belief_matrix)