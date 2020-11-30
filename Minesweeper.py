from typing import List, Tuple
from enum import Enum
import random
import clips
import os


class Minesweeper:
    def __init__(self, locations: List[Tuple[int, int]], size: int = 10, bombs: int = 10):
        self.board = [[Tile(-1, False, False) for _ in range(size)]
                      for _ in range(size)]
        self.size = size
        self.bombs = bombs
        self.known_bombs = []
        self.status = MinesweeperStatus.PLAYING

        # Initialize
        for r, c in locations:
            self.board[r][c].is_bomb = True

    def randomize_bomb(self):
        '''
        Initialize board with random bombs.
        '''
        for _ in range(self.bombs):
            while True:
                (r, c) = (random.randint(0, self.size-1),
                          random.randint(0, self.size-1))
                if(not self.board[r][c].is_bomb):
                    self.board[r][c].is_bomb = True
                    break

    def is_solveable(self):
        '''
        Check whether the initial configuration is solveable
        '''
        if(self.board[0][0].is_bomb):
            return False

        return True

    def reset_board(self):
        '''
        Reset board number, bomb, and mark status.
        '''
        self.board = [[Tile(-1, False, False) for _ in range(self.size)]
                      for _ in range(self.size)]

    def initialize_board(self):
        '''
        Initialize board after click on starting position.
        '''
        self.reveal((0, 0))

    def is_win(self):
        '''
        Check the winning condition after every iteration of inference
        '''
        for i in range(self.size):
            for j in range(self.size):
                if (self.board[i][j].status == -1 and not self.board[i][j].is_bomb):
                    return
        self.status = MinesweeperStatus.WIN

    def is_tile_valid(self, coor: Tuple[int, int]) -> bool:
        '''
        Check whether tile is valid (not out of bounds).
        '''

        return ((coor[0] >= 0) and (coor[0] < self.size)) and ((coor[1] >= 0) and (coor[1] < self.size))

    def reveal(self, current_position: Tuple[int, int]):
        '''
        Does BFS traversal to reveal tile status.
        '''

        r, c = current_position

        if(self.board[r][c].status != -1):
            return

        # Check if position (r, c) is bomb...
        if(self.board[r][c].is_bomb):
            self.status = MinesweeperStatus.LOSE
            return

        offset = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                  (0, 1), (1, -1), (1, 0), (1, 1)]

        visited = [[self.board[i][j].status != -1 for j in range(self.size)]
                   for i in range(self.size)]
        visited[r][c] = True
        queue = []
        queue.append(current_position)

        while(len(queue) != 0):
            # Pop from queue
            current: Tuple[int, int] = queue.pop(0)
            r, c = current

            # Get current tile's bomb count
            bomb_count = self.count_bomb_around((r, c))
            self.board[r][c].status = bomb_count

            # If no bombs, do BFS
            if(bomb_count == 0):
                for dr, dc in offset:
                    # If tile is valid and not visited...
                    if(self.is_tile_valid((r+dr, c+dc)) and not visited[r+dr][c+dc]):
                        queue.append((r+dr, c+dc))
                        visited[r+dr][c+dc] = True

    def toggle_marked(self, clicked_position: Tuple[int, int]):
        '''
        Toggle mark status.
        '''

        r, c = clicked_position
        self.board[r][c].is_marked = not self.board[r][c].is_marked

    def print_board(self):
        '''
        Outputs board in a console
        '''
        for row in self.board:
            for tile in row:
                print(f'{tile.status}{"B" if tile.is_bomb else ""}\t', end='')
            print()

    def count_bomb_around(self, current_position: Tuple[int, int]) -> int:
        '''
        Count bomb around the position to generate number.
        '''
        offset = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                  (0, 1), (1, -1), (1, 0), (1, 1)]
        count = 0
        r, c = current_position
        for dr, dc in offset:
            if(self.is_tile_valid((r+dr, c+dc)) and self.board[r+dr][c+dc].is_bomb):
                count += 1

        return count

    def unknown_tiles_around(self, current_position: Tuple[int, int]) -> int:
        '''
        Count unknown tiles (not revealed yet) around the position.
        '''

        offset = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                  (0, 1), (1, -1), (1, 0), (1, 1)]
        r, c = current_position
        count = 0
        for dr, dc in offset:
            if (self.is_tile_valid((r+dr, c+dc)) and (self.board[r+dr][c+dc].status == -1 or (r+dr, c+dc) in self.known_bombs)):
                count += 1

        return count

    def inference(self) -> None:
        '''
        Run inference using CLIPS as the guide.
        '''

        numbers: List[Tuple[int, int, int]] = []
        unknowns: List[Tuple[int, int, int]] = []
        for i, row in enumerate(self.board):
            for j, tile in enumerate(row):
                if (tile.status != -1):
                    numbers.append((i, j, tile.status))
                    unknowns.append(
                        (i, j, self.unknown_tiles_around((i, j))))

        env = clips.Environment()
        directory = os.listdir('./minesweeper_inference')

        for i, filename in enumerate(directory):

            # If templates already defined...
            if(i == 3):
                number = env.find_template('number')
                for r, c, n in numbers:
                    new_fact = number.new_fact()
                    new_fact['r'] = r
                    new_fact['c'] = c
                    new_fact['n'] = n
                    new_fact.assertit()

                unknown = env.find_template('unknown')
                for r, c, n in unknowns:
                    new_fact = unknown.new_fact()
                    new_fact['r'] = r
                    new_fact['c'] = c
                    new_fact['n'] = n
                    new_fact.assertit()

                bomb = env.find_template('bomb')
                for r, c in self.known_bombs:
                    new_fact = bomb.new_fact()
                    new_fact['r'] = r
                    new_fact['c'] = c
                    new_fact.assertit()

                env.build(
                    f'(defglobal\n  ?*rsize* = {self.size}\n  ?*csize* = {self.size}\n)\n')

            # Read rules/templates/functions from file
            with open(f'./minesweeper_inference/{filename}', 'r+') as clp:
                env.build(clp.read())

        env.run()

        # Execute action
        for f in env.facts():

            # If a bomb fact is detected...
            if('bomb (' in f.__repr__()):
                print(f)

                bomb_fact = ' '.join(f.__repr__().split()[2:])
                bomb_fact = bomb_fact[1:-1].split()
                r, c = bomb_fact[2][:-1], bomb_fact[4][:-1]
                r, c = int(r), int(c)
                if((r, c) not in self.known_bombs):
                    self.known_bombs.append((r, c))
                self.board[r][c].is_marked = True

            # If a safe fact is detected
            if('safe' in f.__repr__()):
                print(f)
                safe_fact = ' '.join(f.__repr__().split()[2:])
                _, r, c = safe_fact[1:-1].split()
                r, c = int(r), int(c)
                self.reveal((r, c))

        # Change status if lose/win
        self.is_win()


class Tile:
    def __init__(self, status: int, is_bomb: bool, is_marked: bool):
        # Unknown : -1
        # No Bombs : 0
        # Bombs : [1..8]
        self.status = status
        self.is_bomb = is_bomb
        self.is_marked = is_marked


class MinesweeperStatus(Enum):
    PLAYING = 1
    LOSE = 2
    WIN = 3
