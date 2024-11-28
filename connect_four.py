

import numpy as np
import game_utils

class ConnectFour(object):
    def __init__(self):
        self.state = game_utils.initialize()
        self.ledger = []
    
    def __str__(self):
        return str(self.state)
    
    def is_win(self):
        return game_utils.is_win(self.state)
    
    def is_end(self):
        return game_utils.is_end(self.state)
    
    def step(self, action):
        col_id, player_id = action
    
        observation = game_utils.step(self.state, col_id, player_id, in_place=True)
        has_won = self.is_win()
        no_more_actions = len(self.get_valid_col_id()) == 0
        terminated = has_won or no_more_actions
        
        if has_won:
            # Win
            reward = 1
        elif no_more_actions:
            # Draw
            reward = 0.5
        else:
            # Lose
            reward = 0

        row_id = np.where(self.state[:,col_id] == player_id)[0][0]
        self.ledger.append((row_id, col_id, player_id))

        return observation, reward, terminated
    def get_state(self):
        read_only_state = self.state.view()
        read_only_state.flags.writeable = False
        return read_only_state

    def size(self):
        return self.state.shape
    
    def get_valid_col_id(self):
        return game_utils.get_valid_col_id(self.state)
    
    def is_valid_col_id(self, col_id):
        return game_utils.is_valid_col_id(self.state, col_id)
    
    def get_cell(self, row_id, col_id):
        return self.state[row_id][col_id]
    
    def get_ledger_actions(self):
        return [ c for _,c,_ in self.ledger]
