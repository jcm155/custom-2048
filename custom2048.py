import random
import math

class GameBoard:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = []
        self.score = 0
        for i in range(height):
            newRow = []
            for j in range(width):
                newRow.append(Cell(j, i))
            self.board.append(newRow)
        self.parameters = {
            "starting_tiles": 4, # how many tiles should it start with?
            "chance_to_spawn_lowest": 1, # what are the odds of a better tile spawning?
            "sprite_sheet_file": "2048.png", # where are the images coming from?
            "sprite_sheet_rows": 4, # how many rows does the sprite sheet have?
            "sprite_sheet_cols": 4, # how many columns does the sprite sheet have?
            "sprite_sheet_width": 400, # how wide in pixels is the sprite sheet?
            "sprite_sheet_height": 400, # how tall in pixels is the sprite sheet?
            "win_condition": 11 # which tile should you go for?
        }
        self.turn_stack = []
        self.win_state = 0

    def __str__(self):
        returnStr = ""
        for row in self.board:
            for j, cell in enumerate(row):
                returnStr += str(cell.value)
                if j < self.width-1:
                    returnStr += ", "
            returnStr += "\n"
        return returnStr

    def get_sprite(self, value):
        cell_width = self.parameters["sprite_sheet_width"]/self.parameters["sprite_sheet_cols"]
        cell_height = self.parameters["sprite_sheet_height"]/self.parameters["sprite_sheet_rows"]
        cell_x = value % self.parameters["sprite_sheet_cols"]
        cell_y = math.floor(value/self.parameters["sprite_sheet_cols"])
        if cell_x >= self.parameters["sprite_sheet_cols"]:
            cell_x = self.parameters["sprite_sheet_cols"]-1
        if cell_y >= self.parameters["sprite_sheet_rows"]:
            cell_y = self.parameters["sprite_sheet_rows"]-1
        return (cell_x * cell_width, cell_y * cell_height, cell_width, cell_height)
    
    def game_is_over(self):
        if not self.is_full():
            return False
        for row in self.board:
            target_row = []
            for cell in row:
                target_row.append(cell.value)
            if self.get_first_pair(target_row) != -1:
                return False
        for i in range(self.width):
            target_col = []
            for j in range(self.height):
                target_col.append(self.board[j][i].value)
            if self.get_first_pair(target_col) != -1:
                return False
        return True

    def game_is_won(self):
        if self.win_state == 2:
            return False
        if self.win_state == 1:
            return True
        for row in self.board:
            for cell in row:
                if cell.value == self.parameters["win_condition"]:
                    self.win_state = 1
                    return True
        return False

    def continue_after_win(self):
        if self.win_state == 1:
            self.win_state = 2

    def is_full(self):
        for row in self.board:
            for cell in row:
                if cell.is_empty():
                    return False
        return True

    def spawn_new(self):
        if self.is_full():
            return False
        cell = self.board[random.randint(0, self.height-1)][random.randint(0, self.width-1)]
        while not cell.is_empty():
            cell = self.board[random.randint(0, self.height-1)][random.randint(0, self.width-1)]
        newVal = 1
        while random.random() >= self.parameters["chance_to_spawn_lowest"] and newVal < 15:
            newVal += 1
        cell.set_value(newVal)

    def set_initial_state(self):
        for i in range(self.parameters["starting_tiles"]):
            self.spawn_new()

    def set_parameter(self, name, val):
        if name not in self.parameters and name not in ["height", "width"]:
            return
        if name == "starting_tiles" and (not isinstance(val, int) or val < 1):
            return
        if name == "chance_to_spawn_lowest" and (not isinstance(val, float) or val < 0.01 or val > 1):
            return
        if name == "sprite_sheet_file" and not isinstance(val, str):
            return
        if name == "sprite_sheet_rows" and (not isinstance(val, int) or val < 1):
            return
        if name == "sprite_sheet_cols" and (not isinstance(val, int) or val < 1):
            return
        if name == "sprite_sheet_width" and not isinstance(val, int) and not isinstance(val, float):
            return
        if name == "sprite_sheet_height" and not isinstance(val, int) and not isinstance(val, float):
            return
        if name == "win_condition" and (not isinstance(val, int) or val < 1):
            return
        if (name == "height" or name == "width") and (not isinstance(val, int) or val < 1):
            return
        if name == "chance_to_spawn_lowest":
            val = round(val, 2)
        if name == "height":
            self.height = val
        elif name == "width":
            self.width = val
        else:
            self.parameters[name] = val

    def shift(self, direction):
        self.backup()
        backup_board = []
        for row in self.board:
            nr = []
            for cell in row:
                nr.append(cell.value)
            backup_board.append(nr)
        if direction.lower() == "left":
            for i, row in enumerate(self.board):
                target_row = []
                for cell in row:
                    target_row.append(cell.value)
                new_row = self.shift_list(target_row, False)
                for j, num in enumerate(new_row):
                    self.board[i][j].set_value(num)
            if not self.board_changed(backup_board):
                self.undo()
            return self.board_changed(backup_board)
        elif direction.lower() == "right":
            for i, row in enumerate(self.board):
                target_row = []
                for cell in row:
                    target_row.append(cell.value)
                new_row = self.shift_list(target_row, True)
                for j, num in enumerate(new_row):
                    self.board[i][j].set_value(num)
            if not self.board_changed(backup_board):
                self.undo()
            return self.board_changed(backup_board)
        elif direction.lower() == "up":
            for i in range(self.width):
                target_col = []
                for j in range(self.height):
                    target_col.append(self.board[j][i].value)
                new_col = self.shift_list(target_col, False)
                for j, num in enumerate(new_col):
                    self.board[j][i].set_value(num)
            if not self.board_changed(backup_board):
                self.undo()
            return self.board_changed(backup_board)
        elif direction.lower() == "down":
            for i in range(self.width):
                target_col = []
                for j in range(self.height):
                    target_col.append(self.board[j][i].value)
                new_col = self.shift_list(target_col, True)
                for j, num in enumerate(new_col):
                    self.board[j][i].set_value(num)
            if not self.board_changed(backup_board):
                self.undo()
            return self.board_changed(backup_board)
        else:
            print("\""+direction+"\" is not a recognized direction.")
            return False

    def shift_list(self, old_list, right_align):
        filled_cells = []
        for cell in old_list:
            if cell != 0:
                filled_cells.append(cell)
        if right_align:
            filled_cells.reverse()
        new_list = []
        pair_index = self.get_first_pair(filled_cells)
        while pair_index != -1:
            cells_to_delete = pair_index+2
            for i in range(pair_index):
                new_list.append(filled_cells[i])
            new_list.append(filled_cells[pair_index]+1)
            self.score += math.pow(2, filled_cells[pair_index]+1)
            for i in range(cells_to_delete):
                filled_cells.pop(0)
            pair_index = self.get_first_pair(filled_cells)
        for cell in filled_cells:
            new_list.append(cell)
        if right_align:
            new_list.reverse()
        while len(new_list) < len(old_list):
            if right_align:
                new_list = [0] + new_list
            else:
                new_list += [0]
        return new_list

    def get_first_pair(self, test_list):
        for i in range(len(test_list)-1):
            if test_list[i] == test_list[i+1]:
                return i
        return -1

    def board_changed(self, backup):
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if cell.value != backup[i][j]:
                    return True
        return False

    def reset(self):
        self.board = []
        for i in range(self.height):
            newRow = []
            for j in range(self.width):
                newRow.append(Cell(j, i))
            self.board.append(newRow)
        self.set_initial_state()
        self.score = 0
        self.win_state = 0
        self.turn_stack = []

    def backup(self):
        backup = []
        for row in self.board:
            nr = []
            for cell in row:
                nr.append(cell.value)
            backup.append(nr)
        self.turn_stack.append(GameState(backup, self.score))

    def undo(self):
        if len(self.turn_stack) == 0:
            return
        new_state = self.turn_stack.pop()
        for i, row in enumerate(new_state.board):
            for j, cell in enumerate(row):
                self.board[i][j].set_value(cell)
        self.score = new_state.score

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.value = 0

    def is_empty(self):
        return self.value == 0

    def set_value(self, val):
        self.value = val

class GameState:
    def __init__(self, board, score):
        self.board = board
        self.score = score