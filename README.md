# Connect 4 AI Agent

A simple Connect 4 AI Agent implemented using Negamax with a simple heuristic and a couple of optimizations. Main agent code found [here](agent.py).

## Optimizations

- Alpha Beta pruning
- Transposition table with an LRU cache
- Basic move ordering
- Iterative deepening with timeout

## Contest

### Rules

- 1 second time limit for decision
- Size of code <= 1 MB

### Score calculation

Your agent will play against each other agent in two matches: one where your agent goes first, and one where it goes second.

Each match is worth 1 point. If your agent wins a match, it earns 1 point. If your agent draws, it earns 0.5 points.

Your agent total score will be the sum of the scores across all of its matches played.

### Agent results

| As Player | Win | Lose | Draw |
| --------- | --- | ---- | ---- |
| 1         | 337 | 46   | 41   |
| 2         | 281 | 113  | 30   |

### Overall statistics

| Statistic             | Value     |
| --------------------- | --------- |
| Total num agents      | 425       |
| Mean score            | 424       |
| Standard deviation    | 175.36    |
| Lowest score          | 2.00      |
| Highest score         | 840.00    |
| Score at 10%          | 178.50    |
| Score at 25%          | 309.50    |
| Score at 50%          | 459.50    |
| Score at 75%          | 548.50    |
| Score at 90%          | 627.10    |
| Your score            | 653.50    |

## Setup

### Install Git and Python

Follow the instructions [here](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) to install Git on your computer. Also follow this [guide](https://realpython.com/installing-python/) to install Python if you haven't already.

### Clone repository

Open a command line window and run these commands to clone this entire repository and install the additional dependencies required.

```
git clone https://github.com/SociallyIneptWeeb/Connect4AIAgent
cd Connect4AIAgent
pip install -r requirements.txt
```

## Usage with CLI

To run the Agent in a command line window, run the following command.

```
python simulator.py
```

## Usage with Pygame

To run the agent with a GUI, run the following command.

```
python pygame_simulator.py
```

## Implementation

### Goal of this agent

- Clean and understandable code
- No overcomplicated algorithm
- Beat at least 90% of other AI agents

### Negamax algorithm

As Connect 4 is a zero-sum two player turn based game, negamax variant of the minimax algorithm was chosen.

### Heuristic

Connect 4 is a solved game where it is possible to always select the best move and always win as the first player if given enough time.
However, with the code size (impossible to store every possible state and move) and time limit restrictions (impossible to search through all possible moves), a heuristic is needed to evaluate which player is winning at any given state for the AI to make a decision to the best of its ability.

Iterate over all possible windows of 4 on the current board, i.e. Horizontal, vertical and both diagonals.
If the window has pieces which only belong to a single player, this is a possible winning position for that player.
Accumulate a score for all windows, with a higher reward for windows that are more fully occupied (closer to winning).
Placing in the center column is also given an additional score due to how most winning positions usually require the center column.
These rewards are based off of this [article](https://www.kaggle.com/code/jamesmcguigan/connectx-mcts-bitboard-bitsquares-heuristic#Bitsquares-Heuristic).

A score for a window is then calculated as number_of_pieces to the power of `1.75`.
While this might not be a perfect evaluation of the board state, it is good enough while being less CPU intensive, allowing the agent to search deeper depths.
The rewards for each possible score for a window `[1 ^ 1.75, 2 ^ 1.75, 3 ^ 1.75]` is computed only once upon initialization to further save cost.

### Alpha beta pruning

A common yet significant optimization for the negamax algorithm is alpha beta pruning, eliminating the need to search large portions of a game tree by remembering the lower and upper bounds of the score for a particular move.
More info can be found in this [article](https://www.chessprogramming.org/Alpha-Beta).

### Transposition table

This table stores, for a board state, the best move, the evaluation score and whether the score is an upper/lower bound or an exact score.
This is implemented via the Least Recently Used (LRU) cache whose capacity is limited as storing too many states can negatively impact the lookup time.
This table also serves to reduce the number of states in the game tree that need to be searched.
The key for a board state is obtained by simply converting the numpy array representation to bytes.
More info on transposition tables can be found in this [article](https://www.chessprogramming.org/Transposition_Table).

### Basic move ordering

When iterating over every possible column to start our search, instead of simply iterating from left to right, we search from the middle column and move outwards.
Given a 0-indexed array of columns, the order would look like `[3, 2, 4, 1, 5, 0, 6]`.
This is because the middle columns are very often the best moves to make with higher evaluation scores.
This results in our alpha beta pruning optimization actually pruning a lot more branches than compared to a left to right move order approach.

### Iterative deepening with timeout

As the agent is forced to make a random move if it exceeds the time limit, it is imperative that our agent does NOT leave its chances of winning up to fate.
As the game state progresses, the number of legal moves that the agent can make varies, resulting in a variable time taken to search to particular depth.
At the start of the game, the agent can usually search up to a depth of 6 moves ahead. However, closer to the endgame, this depth can actually increase to over 20 moves ahead depending on the board state.

Thus, iterative deepening was used to maximize the depth of the negamax algorithm, allowing the agent to start searching to a depth of 6 (safe minimum), and if time permits, search another move deeper.
Once the time limit is reached, if the current depth has not been fully explored, simply use the best move found in the previous depth.

### Future improvements

- Represent the game state as bits instead of a numpy array for faster performance
- Mini playbook of best moves for early game
- Instead of resetting transposition table after every depth, use the best move stored in table to begin search at next depth
