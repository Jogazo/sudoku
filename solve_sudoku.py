#!/usr/bin/python3
import copy

from models import SpatialState, IntersectionalState
from utils import get_sudoku_from_csv, positive_update_sudoku, show_sudoku_as_state_space


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


def state_space_to_sudoku(state_space, sudoku):
    for row in range(9):
        for col in range(9):
            if 1 == len(state_space[row][col].get_intersection()):
                positive_update_sudoku(sudoku, row, col,
                                       str(state_space[row][col].get_intersection().pop()), state_space)


def update_state_space(sudoku, state_space):
    for row in range(9):
        for col in range(9):
            if not state_space[row][col].solved:
                state_space[row][col].check_rows(sudoku, row)
                state_space[row][col].check_columns(sudoku, col)
                state_space[row][col].check_block(sudoku, row, col)


def get_spatial_awareness(sudoku, state_space):
    sp_awareness = list()
    for i in range(1, 10):
        sp_awareness.append(SpatialState(i, state_space))

    for i in range(9):
        sp_awareness[i].check_spatial_awareness(sudoku)

    return sp_awareness


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
    s = get_sudoku_from_csv('sudoku_48_genius.csv')

    sp = get_state_space(s)
    sa_digit_list = get_spatial_awareness(s, sp)

    for it in range(7):
        orig_sudoku = copy.deepcopy(s)
        print(f'iteration {it}')

        for jj in range(9):
            sa_digit_list[jj].check_spatial_awareness(s)

        update_state_space(s, sp)
        state_space_to_sudoku(sp, s)

        if orig_sudoku == s:
            print(f'quit after iteration: {it}')
            break

    show_sudoku_as_state_space(s, sp)
    show_sudoku(s)
