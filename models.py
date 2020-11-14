from utils import get_column_from_nine_by_nine, BLOCK_NUMBER_OFFSET, BLOCK_KEY_VALUE, get_block,\
    positive_update_sudoku, transpose_3_by_3, negative_update_sudoku


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
        for block_number in range(1, 10):
            current_block = get_block(sudoku, block_number)
            # [print(rr) for rr in current_block]
            for row in current_block:
                if str(self.digit) in row:
                    # print(f'found {self.digit} in {block}')
                    self.set_block_to_false(block_number)

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
                positive_update_sudoku(sudoku, i, row_positions[0], str(self.digit), SpatialState.state_space)
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
                positive_update_sudoku(sudoku, column_positions[0], i, str(self.digit), SpatialState.state_space)
            # if 2 == len(column_positions):
            #     if BLOCK_KEY_VALUE[(column_positions[0], i)][0] == BLOCK_KEY_VALUE[(column_positions[1], i)][0]:
            #         print(f'Digit {self.digit}.'
            #               f'Check block adjacent to block: {BLOCK_KEY_VALUE[(column_positions[0], i)][0]}')

    def is_unique_in_block(self, sudoku):
        for block_number in range(1, 10):
            current_block = get_block(self.bool_position, block_number)
            number_count = 0
            for row in current_block:
                number_count += len([j for j, val in enumerate(row) if val])

            if 1 == number_count:
                # print(f'Digit {self.digit} is UNIQUE in block {block_number}. Update row, col and bool_pos')
                i, j = self._get_index_from_block(current_block, block_number)
                positive_update_sudoku(sudoku, i, j, self.digit, SpatialState.state_space)

    def _get_index_from_block(self, block, block_number):
        (row_offset, column_offset) = BLOCK_NUMBER_OFFSET[block_number]

        for i in range(3):
            index = [j for j, val in enumerate(block[i]) if val]
            if index:
                break

        return row_offset + i, column_offset + index[0]

    def check_adjacent_horizontal_blocks(self, sudoku):
        def get_horizontal_block_list(i):
            block_list = list()
            for jj in range(3):
                current_block = get_block(sudoku, i+jj)
                if not self._block_has_digit(current_block):
                    block_list.append((i+jj, get_block(self.bool_position, i+jj)))

            return block_list

        for i in range(1, 10, 3):
            triple_blocks = get_horizontal_block_list(i)

            if 1 == len(triple_blocks):
                # print('Digit', self.digit, 'covered by uniqueness checks.')
                pass
            elif 2 == len(triple_blocks):
                simple_set = {0, 1}
                for block_number in range(2):
                    if 1 == sum(self._horizontal_position_in_block(triple_blocks[block_number][1])):
                        simple_set.remove(block_number)
                        single_true = block_number

                if 1 == len(simple_set):
                    block_to_modify = triple_blocks[simple_set.pop()][0]
                    row_to_modify = [j for j, val in enumerate(self._horizontal_position_in_block(triple_blocks[single_true][1])) if val]  # noqa
                    assert 1 == len(row_to_modify)
                    row_to_modify = row_to_modify[0]

                    print(f'Digit {self.digit} set "False" for row {row_to_modify} in block {block_to_modify}.')
                    (row_offset, col_offset) = BLOCK_NUMBER_OFFSET[block_to_modify]
                    for cc in range(3):
                        self.negative_update(sudoku, row_offset + row_to_modify, col_offset + cc, self.digit)
            elif 3 == len(triple_blocks):
                tmb_list = list()
                for t in triple_blocks:
                    tmb_list.append(self._horizontal_position_in_block(t[1]))

                block_set = {0, 1, 2}
                for j in range(3):
                    if 1 == sum(tmb_list[j]):
                        block_set.remove(j)
                        true_row_position = [k for k, val in enumerate(tmb_list[j]) if val]
                        assert 1 == len(true_row_position)
                        true_row_position = true_row_position[0]

                if 2 == len(block_set):
                    print(f'Digit {self.digit} block {i}. Set False on blocks {block_set} row {true_row_position}')

                    for bb in block_set:
                        (row_offset, col_offset) = BLOCK_NUMBER_OFFSET[bb+i]
                        for cc in range(3):
                            self.negative_update(sudoku, true_row_position+row_offset, cc+col_offset, self.digit)
            else:
                assert not triple_blocks

    def _horizontal_position_in_block(self, block):
        return [bool(sum(block[0])), bool(sum(block[1])), bool(sum(block[2]))]

    def check_adjacent_vertical_blocks(self, sudoku):
        def get_vertical_block_list(i):
            block_list = list()
            for jj in (0, 3, 6):
                current_block = get_block(sudoku, i + jj)
                try:
                    (row_pos, column_pos) = self._position_in_block(current_block)
                except TypeError:  # digit not present
                    transposed_bool_block = transpose_3_by_3(get_block(self.bool_position, i + jj))
                    block_list.append((i + jj, current_block, transposed_bool_block))

            return block_list

        for i in range(1, 4):
            triple_blocks = get_vertical_block_list(i)

            if 1 == len(triple_blocks):
                # print('Digit:', self.digit, 'Already covered in uniqueness checks')
                pass
            elif 2 == len(triple_blocks):
                simple_set = {0, 1}
                for block_number in range(2):
                    if 1 == sum(self._horizontal_position_in_block(triple_blocks[block_number][2])):
                        simple_set.remove(block_number)
                        single_true = block_number

                if 1 == len(simple_set):
                    block_to_modify = triple_blocks[simple_set.pop()][0]
                    col_to_modify = [j for j, val in enumerate(self._horizontal_position_in_block(triple_blocks[single_true][2])) if val]  # noqa
                    assert 1 == len(col_to_modify)
                    col_to_modify = col_to_modify[0]

                    print(f'Digit {self.digit} set "False" on column {col_to_modify} in block {block_to_modify}.')
                    (row_offset, col_offset) = BLOCK_NUMBER_OFFSET[block_to_modify]
                    for rr in range(3):
                        self.negative_update(sudoku, row_offset + rr, col_offset + col_to_modify, self.digit)
            elif 3 == len(triple_blocks):
                lmr_list = list()
                for t in triple_blocks:
                    lmr_list.append(self._horizontal_position_in_block(t[2]))

                col_set = {0, 1, 2}
                for j in range(3):
                    if 1 == sum(lmr_list[j]):
                        col_set.remove(j)
                        true_position = [j for j, val in enumerate(lmr_list[j]) if val]
                        assert 1 == len(true_position)
                        true_position = true_position[0]
                        block_to_modify = triple_blocks[true_position][0]

                if 2 == len(col_set):
                    print(f'Digit {self.digit}. Block number {block_to_modify} set columns {col_set} to False')
                    (row_offset, col_offset) = BLOCK_NUMBER_OFFSET[block_to_modify]
                    for current_col in col_set:
                        for rr in range(3):
                            self.negative_update(sudoku, row_offset+rr, current_col+col_offset, self.digit)
            else:
                assert not triple_blocks

    def negative_update(self, sudoku, row, column, value):
        self.bool_position[row][column] = False
        negative_update_sudoku(sudoku, row, column, value, SpatialState.state_space)

    def _block_has_digit(self, block):
        temp_ = False

        for row in block:
            temp_ = temp_ or str(self.digit) in row

        return temp_

    def _position_in_block(self, block):
        for i in range(3):
            for j in range(3):
                if str(self.digit) == block[i][j]:
                    return i, j

        return None

    def check_spatial_awareness(self, sudoku):
        self.update_spaw_row(sudoku)
        self.update_spaw_col(sudoku)
        self.update_spaw_block(sudoku)
        self.check_empty(sudoku)

        self.is_unique_in_row(sudoku)
        self.is_unique_in_column(sudoku)
        self.is_unique_in_block(sudoku)
        self.check_adjacent_horizontal_blocks(sudoku)
        self.check_adjacent_vertical_blocks(sudoku)


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
