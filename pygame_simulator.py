import pygame
import math
from simulator import GameController, HumanAgent
from agent import AIAgent

BLACK = (0,0,0)
GREY =  (200,200,200)
WHITE = (255,255,255)

PLAYER_1 = (239,124,0)
PLAYER_2 = (0,61,124)

SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 5)


class GameControllerPygame(GameController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        pygame.init()

        self.n_rows, self.n_cols = self.board.size()

        self.width = self.n_cols * SQUARESIZE
        self.height = (self.n_rows+1) * SQUARESIZE
        self.size = (self.width, self.height)
        
        self.font = pygame.font.SysFont("monospace", 70)
        
        # state value to (Color, text)
        self.gamepiece_lookup = {
            0: (BLACK, None),
            1: (PLAYER_1, "1"),
            2: (PLAYER_2, "2"),
        }
        
        for a in self.agents_lookup.values():
            if isinstance(a, HumanPygameAgent):
                a.register_pygame(self)
        self.screen = pygame.display.set_mode(self.size)

    def draw_board(self):
        curr_state = self.board.get_state()
        for c in range(self.n_cols):
            for r in range(self.n_rows):
                pygame.draw.rect(self.screen, GREY, (c*SQUARESIZE, self.height-int(r*SQUARESIZE+SQUARESIZE), SQUARESIZE, SQUARESIZE))
                circle_coord = (int(c*SQUARESIZE+SQUARESIZE/2), self.height-int(r*SQUARESIZE+SQUARESIZE/2))
                self.draw_game_piece(curr_state[self.n_rows-r-1][c], circle_coord)
        pygame.display.update()
        
    def draw_game_piece(self, player_id, circle_coord):
        player_color, player_text = self.gamepiece_lookup[player_id]
        pygame.draw.circle(self.screen, player_color, circle_coord, RADIUS)
        
        if player_text:
            pyg_text = self.font.render(player_text, True, WHITE)
            self.screen.blit(pyg_text, pyg_text.get_rect(center = circle_coord))
        
    def draw_moving_game_piece(self, player_id, circle_coord):
        pygame.draw.rect(self.screen, BLACK, (0,0, self.width, SQUARESIZE))
        self.draw_game_piece(player_id, circle_coord)
        pygame.display.update()
        
    def show_message(self, text):
        pygame.draw.rect(self.screen, BLACK, (0,0, self.width, SQUARESIZE))
        label = self.font.render(text, True, WHITE)
        self.screen.blit(label, label.get_rect(center=(self.width/2, SQUARESIZE/2)))
        pygame.display.update()
        pygame.time.wait(1000)


# -1 is only implemented for human agents
class HumanPygameAgent(HumanAgent):
    def __init__(self, player_id):
        super().__init__(player_id)
        self.pygame_controller = None
    def register_pygame(self, pygame_controller):
        self.pygame_controller = pygame_controller
    def make_move(self, state):
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                return -1

            if event.type == pygame.MOUSEMOTION:
                circle_coord = (event.pos[0], int(SQUARESIZE/2))
                self.pygame_controller.draw_moving_game_piece(self.player_id, circle_coord)
                continue
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))
                return col
            
        return None


if __name__ == "__main__":
    from connect_four import ConnectFour
    board = ConnectFour()
    game = GameControllerPygame(board=board, agents=[HumanPygameAgent(1), AIAgent(2)])
    winner_id = game.run()
    print(f"Winner: {winner_id}")
