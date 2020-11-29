import random
from typing import Tuple
from Minesweeper import Minesweeper


class TestcaseGenerator:
    def __init__(self, size: Tuple[int, int], bombs: Tuple[int, int]) -> None:
        self.min_size, self.max_size = size
        self.min_bombs, self.max_bombs = bombs

    def generate(self):
        size = random.randint(self.min_size, self.max_size)
        bombs = random.randint(self.min_bombs, self.max_bombs)

        print(size, bombs)

        ms = Minesweeper([], size, bombs)
        ms.print_board()
        ms.randomize_bomb()
        ms.print_board()
        while(not ms.is_solveable()):
            ms.reset_board()
            ms.randomize_bomb()

        with open(f'./test/test-{random.randint(0,32767)}', 'w+') as f:
            f.write(f'{size}\n')
            f.write(f'{bombs}\n')
            for i in range(ms.size):
                for j in range(ms.size):
                    if(ms.board[i][j].is_bomb):
                        f.write(f'{i} {j}\n')
