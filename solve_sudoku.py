#!/usr/bin/python3
import copy
from utils import get_sudoku_from_csv, BLOCK_KEY_VALUE, PLOT_DIGIT_SPACES, BLOCK_NUMBER_OFFSET


def get_state_space(sudoku):
    state_space = list()

    for row in range(9):
        temp_row = list()
        for col in range(9):
            if s[row][col]:
                temp_row.append(IntersectionalState(s[row][col]))
            else:
                temp_row.append(IntersectionalState())
        state_space.append(temp_row)

    update_state_space(sudoku, state_space)
    state_space_to_sudoku(state_space, sudoku)

    return state_space


def update_sudoku(sudoku, row, column, value):
    sudoku[row][column] = value
    print(f'==== ({row},{column}): {value}')


def _get_column(nine_by_nine, col_number):
    column = list()
    for i in range(9):
        column.append(nine_by_nine[i][col_number])

    return column


def _get_block(sudoku, block_number):
    block = list()
    row_offset, col_offset = BLOCK_NUMBER_OFFSET[block_number]

    for i in range(3):
        current_row = []
        for j in range(3):
            current_row.append(sudoku[i + row_offset][j + col_offset])
        block.append(current_row)

    return block


def state_space_to_sudoku(state_space, sudoku):
    for row in range(9):
        for col in range(9):
            if 1 == len(state_space[row][col].get_intersection()):
                update_sudoku(sudoku, row, col, str(state_space[row][col].get_intersection().pop()))


def update_state_space(sudoku, state_space):
    for row in range(9):
        for col in range(9):
            if not state_space[row][col].solved:
                # print(state_space[row][col])
                state_space[row][col].check_rows(sudoku, row)
                state_space[row][col].check_columns(sudoku, col)
                state_space[row][col].check_block(sudoku, row, col)
                # print(state_space[row][col])


def get_spatial_awareness(sudoku):
    sp_awareness = list()
    for i in range(1, 10):
        sp_awareness.append(SpatialAware(i))

    # for item in sp_awareness:
    #     print('====')
    #     [print(row) for row in item.bool_position]

    for i in range(9):
        sp_awareness[i].check_spatial_awareness(sudoku)

    return sp_awareness


class SpatialAware:
    def __init__(self, digit):
        self.digit = digit
        self.bool_position = [[True for i in range(9)] for j in range(9)]

    def __str__(self):
        temp_str = str(self.digit) + '\n'
        for row in self.bool_position:
            temp_row = ''
            for item in row:
                if item:
                    temp_row += ' X'
                else:
                    temp_row += ' .'
            temp_str += temp_row + '\n'
        return temp_str

    def update_spaw_row(self, sudoku):
        for row in range(9):
            if str(self.digit) in sudoku[row]:
                # print(f'set row {row} to False for digit {self.digit}')
                self.bool_position[row] = [False]*9

    def update_spaw_col(self, sudoku):
        for col in range(9):
            current_column = _get_column(sudoku, col)
            if str(self.digit) in current_column:
                # print(f'set column {col} to False for digit {self.digit}')
                for row in range(9):
                    self.bool_position[row][col] = False

    def update_spaw_block(self, sudoku):
        for block in range(1, 10):
            current_block = _get_block(sudoku, block)
            # [print(rr) for rr in current_block]
            for row in current_block:
                if str(self.digit) in row:
                    # print(f'found {self.digit} in {block}')
                    self.set_block_to_false(block)

    def set_block_to_false(self, block_number):
        row_offset, col_offset = BLOCK_NUMBER_OFFSET[block_number]
        for i in range(3):
            for j in range(3):
                self.bool_position[i + row_offset][j + col_offset] = False

    def check_empty(self, sudoku):
        for row in range(9):
            for col in range(9):
                if sudoku[row][col]:
                    self.bool_position[row][col] = False

    def is_unique_in_row(self, sudoku):
        i = 0
        for row in self.bool_position:
            row_positions = [j for j, val in enumerate(row) if val]
            if 1 == len(row_positions):
                # print(f'Digit {self.digit} is unique in row number {i}. Update sudoku!')
                update_sudoku(sudoku, i, row_positions[0], str(self.digit))
            elif 2 == len(row_positions):
                if BLOCK_KEY_VALUE[(i, row_positions[0])][0] == BLOCK_KEY_VALUE[(i, row_positions[1])][0]:
                    # print(f'Row {i}, digit {self.digit} on {row_positions}')
                    print(f'Digit {self.digit}.'
                          f'Check block adjacent to block: {BLOCK_KEY_VALUE[(i, row_positions[0])][0]}')
            i += 1

    def is_unique_in_column(self, sudoku):
        for i in range(9):
            current_column = _get_column(self.bool_position, i)
            column_positions = [j for j, val in enumerate(current_column) if val]
            if 1 == len(column_positions):
                update_sudoku(sudoku, column_positions[0], i, str(self.digit))
            if 2 == len(column_positions):
                if BLOCK_KEY_VALUE[(column_positions[0], i)][0] == BLOCK_KEY_VALUE[(column_positions[1], i)][0]:
                    print(f'Digit {self.digit}.'
                          f'Check block adjacent to block: {BLOCK_KEY_VALUE[(column_positions[0], i)][0]}')

    def is_unique_in_block(self, sudoku):
        pass

    def check_spatial_awareness(self, sudoku):
        self.update_spaw_row(sudoku)
        self.update_spaw_col(sudoku)
        self.update_spaw_block(sudoku)
        self.check_empty(sudoku)

        self.is_unique_in_row(sudoku)
        self.is_unique_in_column(sudoku)
        self.is_unique_in_block(sudoku)


class IntersectionalState:
    def __init__(self, value=None):
        self.row_state = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        self.col_state = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        self.block_state = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        self.solved = bool(value)

    def get_intersection(self):
        return self.row_state & self.col_state & self.block_state

    def __str__(self):
        if self.solved:
            return ''
        else:
            return str(self.get_intersection())

    def check_rows(self, s, row):
        for i in range(9):
            if s[row][i]:
                try:
                    # print(f'remove {s[row][i]} from self.row_state set')
                    self.row_state.remove(int(s[row][i]))
                except KeyError:
                    pass

    def check_columns(self, s, col):
        for i in range(9):
            if s[i][col]:
                try:
                    # print(f'remove {s[i][col]} from self.col_state set')
                    self.col_state.remove(int(s[i][col]))
                except KeyError:
                    pass

    def check_block(self, s, row, col):
        (block_number, row_offset, col_offset) = BLOCK_KEY_VALUE[(row, col)]

        for rr in range(3):
            for cc in range(3):
                cvalue = s[rr + row_offset][cc + col_offset]
                if cvalue:
                    try:
                        # print(f'remove {cvalue} from self.block_state')
                        self.block_state.remove(int(cvalue))
                    except KeyError:
                        pass


def print_set_as_9char_string(set_in):
    to_print = ''
    for i in range(1, 10):
        if i in set_in:
            to_print += str(i)
        else:
            to_print += ' '

    return to_print


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


def show_sudoku(sudoku):
    print('-' * 12)
    for row in range(9):
        to_show = ''
        for col in range(9):
            if sudoku[row][col]:
                to_show += f'{sudoku[row][col]}'
            else:
                to_show += ' '

            if 2 == col % 3:
                to_show += '|'

        print(to_show)
        if 2 == row % 3:
            print('-'*12)


if __name__ == '__main__':
    s = get_sudoku_from_csv('sudoku04.csv')

    sa_digit_list = get_spatial_awareness(s)
    sp = get_state_space(s)

    for it in range(7):
        orig_sudoku = copy.deepcopy(s)
        print(f'iteration {it}')

        for jj in range(9):
            sa_digit_list[jj].check_spatial_awareness(s)

        update_state_space(s, sp)
        state_space_to_sudoku(sp, s)

        if orig_sudoku == s:
            break

    show_sudoku_as_state_space(s, sp)

    # for i in range(9):
    #     print(sa_digit_list[i])
    show_sudoku(s)
