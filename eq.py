from itertools import combinations
import subprocess
import argparse


class QueenBoard:
    def __init__(self, size, values):
        self.size = size
        board = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                measure = 'Q' if int(values[i*self.size+j]) > 0 else '_'
                row.append(measure)
            board.append(row)
        self.board = board
        self.spins = self.spin()
        self.mirrors = self.mirror()

    def turn_half_pi(self, board_original):
        board = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                row.append(board_original[j][contrast_index(self.size, i)])
            board.append(row)
        return board

    def spin(self):
        spins = []
        half_pi = self.turn_half_pi(self.board)
        spins.append(half_pi)
        one_pi = self.turn_half_pi(half_pi)
        spins.append(one_pi)
        one_half_pi = self.turn_half_pi(one_pi)
        spins.append(one_half_pi)
        return spins

    def mirror_lr(self, board_original):
        board = []
        for i in range(self.size):
            row = []
            for j in reversed(board_original[i]):
                row.append(j)
            board.append(row)
        return board

    def mirror_ud(self, board_original):
        board = list(reversed(board_original))
        return board

    def mirror_slash(self, board_original):
        board = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                row.append(board_original[j][i])
            board.append(row)
        return board

    def mirror_backslash(self, board_original):
        lr_mirror = self.mirror_lr(board_original)
        lr_slash = self.mirror_slash(lr_mirror)
        board = self.mirror_lr(lr_slash)
        return board

    def mirror(self):
        mirrors = []
        mirrors.append(self.mirror_lr(self.board))
        mirrors.append(self.mirror_ud(self.board))
        mirrors.append(self.mirror_slash(self.board))
        mirrors.append(self.mirror_backslash(self.board))
        return mirrors


def contrast_index(size, i):
    return size - i - 1


# 各マスに変数を割り当てる
def assign_var(size):
    squares = []
    cnf_var = 1
    for i in range(size):
        row = []
        for j in range(size):
            row.append(cnf_var + j)
        cnf_var += size
        squares.append(row)
    return squares


# 各行に一つはクイーンが存在する
def exist_queen_each_row(size, cnf_vars):
    cnf_line = []
    for i in range(size):
        cnf_line.append(' '.join(map(str, cnf_vars[i])) + ' 0')
    return cnf_line


# 各列に一つはクイーンが存在する
def exist_queen_each_column(size, cnf_vars):
    cnf_line = []
    for j in range(size):
        a_cnf_line = ''
        for i in range(size):
            a_cnf_line += str(cnf_vars[i][j]) + ' '
        a_cnf_line += '0'
        cnf_line.append(a_cnf_line)
    return cnf_line


# 同じ行に二つ以上のクイーンは存在しない
def no_multiple_queen_in_row(size, cnf_vars):
    cnf_line = []
    for i in range(size):
        for j in range(size):
            for j2 in range(j+1, size):
                cnf_line.append("-" + str(cnf_vars[i][j]) +
                               " -" + str(cnf_vars[i][j2]) +
                               " 0")
    return cnf_line


# 同じ列に二つ以上のクイーンは存在しない
def no_multiple_queen_in_column(size, cnf_vars):
    cnf_line = []
    for j in range(size):
        for i in range(size):
            for i2 in range(i+1, size):
                cnf_line.append("-" + str(cnf_vars[i][j]) +
                               " -" + str(cnf_vars[i2][j]) +
                               " 0")
    return cnf_line


def get_backslashline_cnf_vars(size, cnf_vars, reference_point):
    (row, column) = reference_point
    slashline_cnf_vars = [cnf_vars[row][column]]

    while (row + 1 < size) and (column + 1 < size):
        (row, column)=(row+1, column+1)
        slashline_cnf_vars.append(cnf_vars[row][column])
    (row, column) = reference_point
    while (row - 1 >= 0) and (column - 1 >= 0):
        (row, column)=(row-1, column-1)
        slashline_cnf_vars.append(cnf_vars[row][column])    

    return slashline_cnf_vars


def get_slashline_cnf_vars(size, cnf_vars, reference_point):
    (row, column) = reference_point
    backslashline_cnf_vars = [cnf_vars[row][column]]

    while (row + 1 < size) and (column - 1 >= 0):
        (row, column)=(row+1, column-1)
        backslashline_cnf_vars.append(cnf_vars[row][column])
    (row, column) = reference_point
    while (row - 1 >= 0) and (column + 1 < size):
        (row, column)=(row-1, column+1)
        backslashline_cnf_vars.append(cnf_vars[row][column])    

    return backslashline_cnf_vars


# /方向の線上に二つ以上のクイーンは存在しない
def no_multiple_queen_in_slash(size, cnf_vars):
    cnf_line = []
    for i in range(size):
        for k in combinations(get_slashline_cnf_vars(size, cnf_vars, (0, i)), 2):
            cnf_line.append("-" + str(k[0]) + " -" + str(k[1]) + " 0")
    for j in range(1, size):
        for l in combinations(get_slashline_cnf_vars(size, cnf_vars, (j, size-1)), 2):
            cnf_line.append("-" + str(l[0]) + " -" + str(l[1]) + " 0")
    return cnf_line


# \方向の線上に二つ以上のクイーンは存在しない
def no_multiple_queen_in_backslash(size, cnf_vars):
    cnf_line = []
    for j in combinations(get_backslashline_cnf_vars(size, cnf_vars, (0, 0)), 2):
        cnf_line.append("-" + str(j[0]) + " -" + str(j[1]) + " 0")
    for i in range(1, size):
        for k in combinations(get_backslashline_cnf_vars(size, cnf_vars, (0, i)), 2):
            cnf_line.append("-" + str(k[0]) + " -" + str(k[1]) + " 0")
        for l in combinations(get_backslashline_cnf_vars(size, cnf_vars, (i, 0)), 2):
            cnf_line.append("-" + str(l[0]) + " -" + str(l[1]) + " 0")
    return cnf_line


def create_eightqueen_rule_cnf(size, cnf_vars):
    return exist_queen_each_row(size, cnf_vars) + exist_queen_each_column(size, cnf_vars) +\
           no_multiple_queen_in_row(size, cnf_vars) + no_multiple_queen_in_column(size, cnf_vars) +\
           no_multiple_queen_in_slash(size, cnf_vars) + no_multiple_queen_in_backslash(size, cnf_vars)


def sat_to_board(size, result):
    row = 0
    for i in range(size):
        for j in range(size):
            measure = 'Q' if int(result[i*size+j]) > 0 else '_'
            print(measure, end=' ')
        print()
    print("=="*size)


def print_board(board):
    for row in board:
        for q in row:
            print(q, end=' ')
        print()


def compare_board(new_board, boards):
    if len(boards) == 0:
        return True
    for i in boards:
        if new_board.board == i.board:
            return False
        if new_board.board in i.spins:
            return False
        if new_board.board in i.mirrors:
            return False
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("size", type=int, help="the number of queens")
    parser.add_argument("-a", "--answers", required=False, choices=['one', 'all'], default='all', help="find only one answer or all answers")
    parser.add_argument("-nd", "--no_display", required=False, action='store_true', help="do not display answers (only when find all answers)")

    args = parser.parse_args()

    mode_arg = args.answers
    if mode_arg == 'one':
        only_one = True
    elif mode_arg == 'all':
        only_one = False
    else:
        print('MODE MUST BE \'one\' OR \'all\'')
        exit()

    size = args.size
    if size <= 0:
        print('N MUST BE GREATER THAN 0.')
        exit()

    print(size, "-QUEEN", sep='')
    cnf_vars = assign_var(size)

    show_board = (not args.no_display) or only_one
    if show_board:
        print("=="*size)

    eightqeen_rule = create_eightqueen_rule_cnf(size, cnf_vars)
    cnf_line = eightqeen_rule
    counter = 0
    solver_called_times = 0
    result_boards = []
    while True:
        input_cnf = ["p cnf " + str(size**2) + " " + str(len(cnf_line))] + cnf_line

        with open('eightqueen.cnf', 'w') as f:
            f.write('\n'.join(input_cnf) + '\n')

        subprocess.run(["./minisat", "-verb=0", "eightqueen.cnf", "output.txt"],
                       stdout=subprocess.DEVNULL)
        solver_called_times += 1

        with open('output.txt', 'r') as f:
            outputlines = f.readlines()
            if len(outputlines) >= 2:
                (status, result) = (outputlines[0], outputlines[1].split())
            else:
                status = outputlines[0]
                break

        result_qb = QueenBoard(size, result)
        if only_one:
            if show_board:
                sat_to_board(size, result)
            break
        if compare_board(result_qb, result_boards):
            result_boards.insert(0, result_qb)
            if show_board:
                sat_to_board(size, result)
            counter += 1

        queens = list(filter(lambda x: x > 0, map(lambda x: int(x), result)))
        cnf_line.append(' '.join(list(map(lambda x: '-'+str(x), queens)) + ['0']))
    if only_one is False:
        print("ANSWERS:", counter)
        print("SAT Solver was called", solver_called_times, "times.")
