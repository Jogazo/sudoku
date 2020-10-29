from utils import get_column_from_nine_by_nine, BLOCK_NUMBER_OFFSET, BLOCK_KEY_VALUE, get_block, update_sudoku


class SpatialState:
    def __init__(self, digit, sp):
        SpatialState.state_space = sp
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
            current_column = get_column_from_nine_by_nine(sudoku, col)
            if str(self.digit) in current_column:
                # print(f'set column {col} to False for digit {self.digit}')
                for row in range(9):
                    self.bool_position[row][col] = False

    def update_spaw_block(self, sudoku):
        for block in range(1, 10):
            current_block = get_block(sudoku, block)
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
                update_sudoku(sudoku, i, row_positions[0], str(self.digit), SpatialState.state_space)
            # elif 2 == len(row_positions):
            #     if BLOCK_KEY_VALUE[(i, row_positions[0])][0] == BLOCK_KEY_VALUE[(i, row_positions[1])][0]:
            #         # print(f'Row {i}, digit {self.digit} on {row_positions}')
            #         print(f'Digit {self.digit}.'
            #               f'Check block adjacent to block: {BLOCK_KEY_VALUE[(i, row_positions[0])][0]}')
            i += 1

    def is_unique_in_column(self, sudoku):
        for i in range(9):
            current_column = get_column_from_nine_by_nine(self.bool_position, i)
            column_positions = [j for j, val in enumerate(current_column) if val]
            if 1 == len(column_positions):
                update_sudoku(sudoku, column_positions[0], i, str(self.digit), SpatialState.state_space)
            # if 2 == len(column_positions):
            #     if BLOCK_KEY_VALUE[(column_positions[0], i)][0] == BLOCK_KEY_VALUE[(column_positions[1], i)][0]:
            #         print(f'Digit {self.digit}.'
            #               f'Check block adjacent to block: {BLOCK_KEY_VALUE[(column_positions[0], i)][0]}')

    def check_adjacent_horizontal_blocks(self, sudoku):
        for i in range(1, 10, 3):
            top_middle_bottom = list()
            for jj in range(3):
                current_block = get_block(sudoku, i+jj)
                current_bool_block = get_block(self.bool_position, i+jj)
                if self._block_has_digit(current_block):
                    # print(f'Block {i+jj} BREAK!!!')
                    break
                else:
                    top_middle_bottom.append(self._horizontal_position_in_block(current_bool_block))
            if 3 == len(top_middle_bottom):
                print(f'Digit {self.digit}, adjacent horizontal block number {i}')
                [print(elt) for elt in top_middle_bottom]

    def _horizontal_position_in_block(self, block):
        # print('TOP', block[0], sum(block[0]))
        # print('MIDDLE', block[1], sum(block[1]))
        # print('BOTTOM', block[2], sum(block[2]))
        return (bool(sum(block[0])), bool(sum(block[1])), bool(sum(block[2])))

    def _block_has_digit(self, block):
        temp_ = False

        for row in block:
            temp_ = temp_ or str(self.digit) in row

        return temp_

    def check_spatial_awareness(self, sudoku):
        self.update_spaw_row(sudoku)
        self.update_spaw_col(sudoku)
        self.update_spaw_block(sudoku)
        self.check_empty(sudoku)

        self.is_unique_in_row(sudoku)
        self.is_unique_in_column(sudoku)
        self.check_adjacent_horizontal_blocks(sudoku)


class IntersectionalState:
    def __init__(self, value=None):
        self.row_state = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        self.col_state = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        self.block_state = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        self.solved = bool(value)

    def get_intersection(self):
        return self.row_state & self.col_state & self.block_state

    def set_solved(self):
        self.row_state = self.col_state = self.block_state = set()
        self.solved = True

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
