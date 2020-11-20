from typing import Tuple
import random


class Minesweeper:
    def __init__(self, size: int = 10):
        self.board = [[Tile(-1, False, False) for _ in range(size)]
                      for _ in range(size)]
        self.size = size

    def initialize_board(self, starting_position: Tuple[int, int], bombs: int = 10):
        '''
        Initialize board after click on starting position.
        '''

        for _ in range(bombs):
            r, c = starting_position
            while(starting_position == (r, c)):
                r, c = random.randint(
                    0, self.size - 1), random.randint(0, self.size - 1)
            print((r, c))
            self.board[r][c].is_bomb = True

        self.reveal(starting_position)

    def is_tile_valid(self, coor: Tuple[int, int]) -> bool:
        '''
        Check whether tile is valid (not out of bounds). 
        '''

        return ((coor[0] >= 0) and (coor[0] < self.size)) and ((coor[1] >= 0) and (coor[1] < self.size))

    def reveal(self, current_position: Tuple[int, int]):
        '''
        Does BFS traversal to reveal tile status.
        '''

        offset = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                  (0, 1), (1, -1), (1, 0), (1, 1)]
        queue = []
        visited = [[False for _ in range(self.size)]
                   for _ in range(self.size)]

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
        Toggle mark status
        '''

        r, c = clicked_position
        self.board[r][c].is_marked = not self.board[r][c].is_marked

    def print_board(self):
        for row in self.board:
            for tile in row:
                print(f'{tile.status}{"B" if tile.is_bomb else ""}\t', end='')
            print()

    def count_bomb_around(self, current_position: Tuple[int, int]) -> int:
        offset = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                  (0, 1), (1, -1), (1, 0), (1, 1)]
        count = 0
        r, c = current_position
        for dr, dc in offset:
            if(self.is_tile_valid((r+dr, c+dc)) and self.board[r+dr][c+dc].is_bomb):
                count += 1

        return count


class Tile:
    def __init__(self, status: int, is_bomb: bool, is_marked: bool):
        # Unknown : -1
        # No Bombs : 0
        # Bombs : [1..8]
        self.status = status
        self.is_bomb = is_bomb
        self.is_marked = is_marked
