import copy
import time
from collections import OrderedDict

import numpy as np

from game_utils import get_valid_col_id, step, is_win


class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        self.cache[key] = value
        self.cache.move_to_end(key)
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


class AIAgent(object):
    """
    A class representing an agent that plays Connect Four.
    """

    def __init__(self, player_id=1):
        """Initializes the agent with the specified player ID.

        Parameters:
        -----------
        player_id : int
            The ID of the player assigned to this agent (1 or 2).
        """
        self.agent_id = player_id
        self.opponent_id = 3 - player_id
        self.min_depth = 6
        self.max_depth = 42
        self.num_rows = 6
        self.num_cols = 7
        self.timeout = 0.95
        self.transposition = LRUCache(4096)
        self.rewards = [0, 1, 2 ** 1.75, 3 ** 1.75, 4 ** 1.75]
        self.move_order = [3, 2, 4, 1, 5, 0, 6]
        self.start_time = None

    def unstep(self, state, col):
        for row in range(self.num_rows):
            if state[row][col] != 0:
                state[row][col] = 0
                break

    def evaluate_window(self, window):
        num_empty = window.count(0)
        num_agent = window.count(self.agent_id)
        num_opponent = 4 - num_agent - num_empty

        if num_empty == 4 - num_agent:
            return self.rewards[num_agent]
        if num_empty == 4 - num_opponent:
            return -self.rewards[num_opponent]

        return 0

    def evaluate(self, state, player_id):
        score = 0
        center_col = [int(i) for i in list(state[:, self.num_cols // 2])]
        center_count = center_col.count(self.agent_id)
        score += center_count * 6

        # rows
        for r in range(self.num_rows):
            row = [int(i) for i in list(state[r, :])]
            for c in range(self.num_cols - 3):
                window = row[c:c + 4]
                score += self.evaluate_window(window)

        # columns
        for c in range(self.num_cols):
            col = [int(i) for i in list(state[:, c])]
            for r in range(self.num_rows - 3):
                window = col[r:r + 4]
                score += self.evaluate_window(window)

        # / diagonal
        for r in range(3, self.num_rows):
            for c in range(self.num_cols - 3):
                window = [state[r - i][c + i] for i in range(4)]
                score += self.evaluate_window(window)

        # \ diagonal
        for r in range(3, self.num_rows):
            for c in range(3, self.num_cols):
                window = [state[r - i][c - i] for i in range(4)]
                score += self.evaluate_window(window)

        return score if self.agent_id == player_id else -score

    def negamax(self, state, alpha, beta, depth_left, player_id):
        old_alpha = alpha
        board_key = state.tobytes()
        if board_key in self.transposition.cache:
            entry = self.transposition.get(board_key)
            if entry['LB']:
                alpha = max(alpha, entry['v'])
            elif entry['UB']:
                beta = min(beta, entry['v'])
            else:
                return entry['move'], entry['v']
            if alpha >= beta:
                return entry['move'], entry['v']

        best_score = -np.inf
        best_move = None

        if is_win(state):
            return best_move, -np.inf

        moves = get_valid_col_id(state)
        valid_moves = [move for move in self.move_order if move in moves]
        if len(valid_moves) == 0:
            return best_move, 0
        best_move = valid_moves[0]

        if depth_left == 0 or len(valid_moves) == 1:
            return best_move, self.evaluate(state, player_id)

        for col in valid_moves:
            step(state, col, player_id)
            _, new_v = self.negamax(state, -beta, -alpha, depth_left - 1, 3 - player_id)
            new_v = -new_v
            if new_v > best_score:
                best_score, best_move = new_v, col
            self.unstep(state, col)
            alpha = max(alpha, new_v)
            if time.perf_counter() - self.start_time >= self.timeout or alpha >= beta:
                break

        entry = {'move': best_move, 'v': best_score, 'UB': False, 'LB': False}
        if best_score <= old_alpha:
            entry['UB'] = True
        elif best_score >= beta:
            entry['LB'] = True

        self.transposition.put(board_key, entry)

        return best_move, best_score

    def negamax_deepening(self, state):
        valid_moves = get_valid_col_id(state)
        best_move, best_score = valid_moves[0], -np.inf
        for depth in range(self.min_depth, self.max_depth + 1):
            self.transposition = LRUCache(4096)
            move, score = self.negamax(state, -np.inf, np.inf, depth, self.agent_id)
            if time.perf_counter() - self.start_time >= self.timeout:
                break

            if score != -np.inf:
                best_move, best_score = move, score

            print(f'{depth} ({move}={score:.1f})', end=' ', flush=True)

            if abs(score) == np.inf:
                break

        print(f' = {best_move} ({best_score:.2f})', flush=True)
        return best_move

    def make_move(self, state):
        self.start_time = time.perf_counter()
        state = copy.deepcopy(state)
        move = self.negamax_deepening(state)
        print(f'AIAgent took {time.perf_counter() - self.start_time:.2f}s')
        return move
