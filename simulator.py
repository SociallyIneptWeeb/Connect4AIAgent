from connect_four import ConnectFour
from agent import AIAgent


class GameController(object):
    def __init__(self, board, agents):
        self.board = board
        self.agents_lookup = {i + 1: a for i, a in enumerate(agents)}
    def show_message(self, text):
        print(text)
        
    def draw_board(self):
        print(self.board.get_state())

    def run(self):
        self.draw_board()
        
        # Start with P1
        player_id = 1
        turn = 0
        winner_id = None  # To store the winner ID
        is_quit = False
        
        while (not is_quit) and (not self.board.is_end()):
            player_id = turn % 2 + 1
            agent = self.agents_lookup[player_id]
            try:
                action = agent.make_move(self.board.get_state())

                if action!=None:
                    
                    if action == -1:
                        is_quit = True
                        continue
                        
                    self.board.step((action, player_id))
                    self.draw_board()
                    
                    if self.board.is_win():
                        self.show_message(f"Player {player_id} wins!")
                        winner_id = player_id
                    
                    turn += 1
                    
            except ValueError as e:
                import traceback
                print(traceback.format_exc())
                self.show_message("Invalid Action!")
            except Exception as e:
                import traceback
                print(traceback.format_exc())
                self.show_message("Fatal Error!")
        
        print("Actions:", self.board.get_ledger_actions())
        return winner_id


class Agent(object):
    """
    A class representing an agent that plays Connect Four.
    """
    def __init__(self, player_id):
        """Initializes the agent with the specified player ID.

        Parameters:
        -----------
        player_id : int
            The ID of the player assigned to this agent (1 or 2).
        """
        self.player_id = player_id
    def make_move(self, state):
        """
        Determines and returns the next move for the agent based on the current game state.

        Parameters:
        -----------
        state : np.ndarray
            A 2D numpy array representing the current, read-only state of the game board. 
            The board contains:
            - 0 for an empty cell,
            - 1 for Player 1's piece,
            - 2 for Player 2's piece.

        Returns:
        --------
        int
            The valid action, ie. a valid column index (col_id) where this agent chooses to drop its piece.
        """
        return 0


# -1 is only implemented for human agents
class HumanAgent(Agent):
    def __init__(self, player_id):
        super().__init__(player_id)

    def make_move(self, state):
        col_id = input(f"[Player {self.player_id}] (-1 to quit) Drop Piece to: ")
        return int(col_id)


if __name__ == "__main__":
    board = ConnectFour()
    # Create and run the game controller without a UI
    game = GameController(board=board, agents=[HumanAgent(1), AIAgent(2)])
    winner_id = game.run()
    print(f"Winner: {winner_id}")
