import numpy as np
import copy

COLUMN_COUNT = 7
ROW_COUNT = 6

def is_valid_col_id(state, col_id):
    """
    Checks if placing a piece in the specified column is a valid move.

    Parameters:
    -----------
    state : np.ndarray
        A 2D numpy array representing the current state of the game board.
    col_id : int
        The column index to check for validity.

    Returns:
    --------
    bool
        True if the column is valid (i.e., the top cell of the column is empty), otherwise False.
    """
    return state[0][col_id] == 0

def get_valid_col_id(state):
    """
    Returns a list of valid column indices where a move can be made.

    Parameters:
    -----------
    state : np.ndarray
        A 2D numpy array representing the current state of the game board.

    Returns:
    --------
    np.ndarray
        An array of column indices (col_id) where the top cell is empty and a move can be made.
    """
    return np.where(state[0]==0)[0]

def initialize():
    """
    Initializes a new Connect Four game board with 6 rows and 7 columns.

    Returns:
    --------
    np.ndarray
        A 2D numpy array of shape (6, 7) filled with zeros, representing an empty Connect Four board.
        - 0 represents an empty cell.
    """
    return np.zeros((ROW_COUNT, COLUMN_COUNT), dtype=int)

def step(state, col_id, player_id, in_place=True):
    """
    Simulates placing a piece on the game board at the specified column for the given player, updating the board state.

    Parameters:
    -----------
    state : np.ndarray
        The current game board, represented as a 2D numpy array.
        - 0 represents an empty cell,
        - 1 represents Player 1's piece,
        - 2 represents Player 2's piece.

    col_id : int
        The column index where the player wants to drop their piece. Must be between 0 and COLUMN_COUNT - 1.

    player_id : int
        The ID of the player making the move (1 for Player 1, 2 for Player 2). Must be either 1 or 2.

    in_place : bool, optional (default=True)
        If True, modifies the original `state` in-place.
        If False, creates a deep copy of `state` and modifies the copy.

    Returns:
    --------
    np.ndarray
        The updated game board after the player's piece is placed in the specified column.

    Raises:
    -------
    ValueError:
        - If `player_id` is not 1 or 2.
        - If `col_id` is out of bounds (not between 0 and COLUMN_COUNT - 1).
        - If the specified column is already full (no available empty cell).
    """
    if in_place:
        temp_board = state
    else:
        temp_board = copy.deepcopy(state)

    if player_id not in {1, 2}:
        raise ValueError("Invalid player_id: must be either 1 (Player 1) or 2 (Player 2).")
    
    if not (0 <= col_id < COLUMN_COUNT):
        raise ValueError(f"Invalid column ID: {col_id}. It must be between 0 and {COLUMN_COUNT - 1}.")
    
    row_id = None
    # Start from the last row and find the first location to enter the player_id
    for r in reversed(range(ROW_COUNT)):
        if temp_board[r][col_id] == 0:
            row_id = r
            break

    if row_id == None:
        raise ValueError(f"Invalid action: column {col_id} is already full.")

    temp_board[row_id][col_id] = player_id

    return temp_board

def is_win(state):
    """
    Checks if there is a winning condition on the game board.

    Parameters:
    -----------
    state : np.ndarray
        A 2D numpy array representing the current state of the game board.

    Returns:
    --------
    bool
        True if a player has won by aligning four consecutive pieces vertically, horizontally, or diagonally, otherwise False.
    """
    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT):
            if state[row][col] == 0:
                continue
            if col + 3 < COLUMN_COUNT and state[row][col] == state[row][col + 1] == state[row][col + 2] == state[row][col + 3]:
                return True
            if row + 3 < ROW_COUNT and state[row][col] == state[row + 1][col] == state[row + 2][col] == state[row + 3][col]:
                return True
            if row + 3 < ROW_COUNT and col + 3 < COLUMN_COUNT and state[row][col] == state[row + 1][col + 1] == state[row + 2][col + 2] == state[row + 3][col + 3]:
                return True
            if row + 3 < ROW_COUNT and col - 3 >= 0 and state[row][col] == state[row + 1][col - 1] == state[row + 2][col - 2] == state[row + 3][col - 3]:
                return True
    return False

def is_end(state):
    """
    Checks if the game has ended either by a player winning or by the board being full (resulting in a draw).

    Parameters:
    -----------
    state : np.ndarray
        A 2D numpy array representing the current state of the game board.

    Returns:
    --------
    bool
        True if the game has ended (either due to a win or a full board resulting in a draw), otherwise False.
    """
    return len(get_valid_col_id(state)) == 0 or is_win(state)