import csv


def get_sudoku_from_csv(file_name):
    sudoku = list()
    with open(file_name, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)

        for r in csv_reader:
            sudoku.append(r)

    return sudoku


def positive_update_sudoku(sudoku, row, column, value, state_space):
    value = str(value)
    state_space[row][column].set_solved()
    sudoku[row][column] = value
    print(f'==== ({row},{column}): {value}')


def negative_update_sudoku(sudoku, row, column, value, state_space):
    try:
        state_space[row][column].row_state.remove(int(value))
    except KeyError:  # element no longer in set
        pass

    try:
        state_space[row][column].col_state.remove(int(value))
    except KeyError:  # element no longer in set
        pass

    try:
        state_space[row][column].block_state.remove(int(value))
    except KeyError:  # element no longer in set
        pass

    print(f'==== ({row},{column}): CANNOT HAVE {value}')


def show_sudoku_as_state_space(sudoku, state_space):
    print('-' * 90)
    for row in range(9):
        to_show = ''
        for col in range(9):
            if sudoku[row][col]:
                to_show += f'{PLOT_DIGIT_SPACES[sudoku[row][col]]}|'
            else:
                as_9char_string = print_set_as_9char_string(state_space[row][col].get_intersection())
                to_show += f'{as_9char_string}|'

        print(to_show)
        if 2 == row % 3:
            print('-'*90)


def get_block(nine_by_nine, block_number):
    block = list()
    row_offset, col_offset = BLOCK_NUMBER_OFFSET[block_number]

    for i in range(3):
        current_row = []
        for j in range(3):
            current_row.append(nine_by_nine[i + row_offset][j + col_offset])
        block.append(current_row)

    return block


def transpose_3_by_3(three_by_three):
    transposed = list()

    for i in range(3):
        transposed.append([three_by_three[0][i], three_by_three[1][i], three_by_three[2][i]])

    return transposed


def get_column_from_nine_by_nine(nine_by_nine, col_number):
    column = list()
    for i in range(9):
        column.append(nine_by_nine[i][col_number])

    return column


def print_set_as_9char_string(set_in):
    to_print = ''
    for i in range(1, 10):
        if i in set_in:
            to_print += str(i)
        else:
            to_print += ' '

    return to_print


BLOCK_NUMBER_OFFSET = {
    1: (0, 0),
    2: (0, 3),
    3: (0, 6),
    4: (3, 0),
    5: (3, 3),
    6: (3, 6),
    7: (6, 0),
    8: (6, 3),
    9: (6, 6),
}


BLOCK_KEY_VALUE = {
    (0, 0): (1, 0, 0),
    (0, 1): (1, 0, 0),
    (0, 2): (1, 0, 0),
    (0, 3): (2, 0, 3),
    (0, 4): (2, 0, 3),
    (0, 5): (2, 0, 3),
    (0, 6): (3, 0, 6),
    (0, 7): (3, 0, 6),
    (0, 8): (3, 0, 6),
    (1, 0): (1, 0, 0),
    (1, 1): (1, 0, 0),
    (1, 2): (1, 0, 0),
    (1, 3): (2, 0, 3),
    (1, 4): (2, 0, 3),
    (1, 5): (2, 0, 3),
    (1, 6): (3, 0, 6),
    (1, 7): (3, 0, 6),
    (1, 8): (3, 0, 6),
    (2, 0): (1, 0, 0),
    (2, 1): (1, 0, 0),
    (2, 2): (1, 0, 0),
    (2, 3): (2, 0, 3),
    (2, 4): (2, 0, 3),
    (2, 5): (2, 0, 3),
    (2, 6): (3, 0, 6),
    (2, 7): (3, 0, 6),
    (2, 8): (3, 0, 6),
    #
    (3, 0): (4, 3, 0),
    (3, 1): (4, 3, 0),
    (3, 2): (4, 3, 0),
    (3, 3): (5, 3, 3),
    (3, 4): (5, 3, 3),
    (3, 5): (5, 3, 3),
    (3, 6): (6, 3, 6),
    (3, 7): (6, 3, 6),
    (3, 8): (6, 3, 6),
    (4, 0): (4, 3, 0),
    (4, 1): (4, 3, 0),
    (4, 2): (4, 3, 0),
    (4, 3): (5, 3, 3),
    (4, 4): (5, 3, 3),
    (4, 5): (5, 3, 3),
    (4, 6): (6, 3, 6),
    (4, 7): (6, 3, 6),
    (4, 8): (6, 3, 6),
    (5, 0): (4, 3, 0),
    (5, 1): (4, 3, 0),
    (5, 2): (4, 3, 0),
    (5, 3): (5, 3, 3),
    (5, 4): (5, 3, 3),
    (5, 5): (5, 3, 3),
    (5, 6): (6, 3, 6),
    (5, 7): (6, 3, 6),
    (5, 8): (6, 3, 6),
    #
    (6, 0): (7, 6, 0),
    (6, 1): (7, 6, 0),
    (6, 2): (7, 6, 0),
    (6, 3): (8, 6, 3),
    (6, 4): (8, 6, 3),
    (6, 5): (8, 6, 3),
    (6, 6): (9, 6, 6),
    (6, 7): (9, 6, 6),
    (6, 8): (9, 6, 6),
    (7, 0): (7, 6, 0),
    (7, 1): (7, 6, 0),
    (7, 2): (7, 6, 0),
    (7, 3): (8, 6, 3),
    (7, 4): (8, 6, 3),
    (7, 5): (8, 6, 3),
    (7, 6): (9, 6, 6),
    (7, 7): (9, 6, 6),
    (7, 8): (9, 6, 6),
    (8, 0): (7, 6, 0),
    (8, 1): (7, 6, 0),
    (8, 2): (7, 6, 0),
    (8, 3): (8, 6, 3),
    (8, 4): (8, 6, 3),
    (8, 5): (8, 6, 3),
    (8, 6): (9, 6, 6),
    (8, 7): (9, 6, 6),
    (8, 8): (9, 6, 6),
}

PLOT_DIGIT_SPACES = {
    '1': '1        ',
    '2': ' 2       ',
    '3': '  3      ',
    '4': '   4     ',
    '5': '    5    ',
    '6': '     6   ',
    '7': '      7  ',
    '8': '       8 ',
    '9': '        9',
}
