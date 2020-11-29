from ClipsInstance import ClipsInstance
from typing import List, Tuple
from enum import Enum
import random
import copy
import clips


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
        for i in range(self.bombs):
            while True:
                (r, c) = (random.randint(0, self.size-1),
                          random.randint(0, self.size-1))
                if(not self.board[r][c].is_bomb):
                    self.board[r][c].is_bomb = True
                    break

    def is_solveable(self):
        # Check if (0,0) has bomb, if yes, invalidated
        if(self.board[0][0].is_bomb):
            return False

        return True
        # ms = copy.deepcopy(self)

        # while True:
        #     # print(12)
        #     currently_solveable = False
        #     for i in range(ms.size):
        #         for j in range(ms.size):
        #             if(ms.board[i][j].status != -1 and ms.unknown_tiles_around((i, j)) == ms.board[i][j].status):
        #                 currently_solveable = True
        #                 offset = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
        #                           (0, 1), (1, -1), (1, 0), (1, 1)]
        #                 for dr, dc in offset:
        #                     if(ms.board[i+dr][j+dc].status == -1):
        #                         ms.board[i+dr][j+dc].is_marked = True

        #     for i in range(ms.size):
        #         for j in range(ms.size):
        #             if(ms.board[i][j].status != -1):
        #                 currently_solveable = True
        #                 offset = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
        #                           (0, 1), (1, -1), (1, 0), (1, 1)]
        #                 for dr, dc in offset:
        #                     if(ms.board[i+dr][j+dc].status != -1 and ms.board[][]):
        #                         ms.board[i+dr][j+dc].is_marked = True

        #                 break
        #         if(currently_solveable):
        #             break

        #     ms.print_board()
        #     print('-----')

        #     if(ms.is_win()):
        #         return True

        #     if(not currently_solveable):
        #         return False

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

        # # self.randomize_bomb()
        # self.board[2][2].is_bomb = True

        self.reveal((0, 0))

    def is_win(self):
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
        Toggle mark status
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
            if (self.is_tile_valid((r+dr, c+dc)) and self.board[r+dr][c+dc].status == -1):
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
        env.build('''
(deftemplate number
(slot r)
(slot c)
(slot n)
)
        ''')
        env.build('''
(deftemplate unknown
(slot r)
(slot c)
(slot n)
)
        ''')

        number = env.find_template('number')
        for r, c, n in numbers:
            new_fact = number.new_fact()
            new_fact['r'] = r
            new_fact['c'] = c
            new_fact['n'] = n
            new_fact.assertit()

        for r, c in self.known_bombs:
            env.assert_string(f"(bombs {r} {c})")

        unknown = env.find_template('unknown')
        for r, c, n in unknowns:
            new_fact = unknown.new_fact()
            new_fact['r'] = r
            new_fact['c'] = c
            new_fact['n'] = n
            new_fact.assertit()

        env.build(
            f'(defglobal\n  ?*rsize* = {self.size}\n  ?*csize* = {self.size}\n)\n')

        env.build('''
(deffunction isvalid(?r ?c)
(return (and(>= ?r 0) (>= ?c 0) (< ?r ?*rsize*) (< ?c ?*csize*)))
)
        ''')

        env.build('''
(deffunction isaround(?r ?c ?br ?bc)
(return (and (and (>= ?br (- ?r 1)) (<= ?br (+ ?r 1))) (and (>= ?bc (- ?c 1)) (<= ?bc (+ ?c 1)))))
)
        ''')

        env.build('''
(defrule markbomb
(number (r ?r) (c ?c) (n ?num))
(unknown (r ?r) (c ?c) (n ?num))
(test (> ?num 0))
=>
(loop-for-count (?i (- ?r 1) (+ ?r 1)) do
(loop-for-count (?j (- ?c 1) (+ ?c 1)) do
    (if (and
    (isvalid ?i ?j)
    (not (and (eq ?i ?r) (eq ?j ?c)))
    ) then
    (assert (bomb ?i ?j))
    )
)
)
)
        ''')

        env.build('''
(defrule unmarkbomb
?f <- (bomb ?r ?c)
(number (r ?r) (c ?c) (n ?))
=>
(retract ?f)
)
        ''')

        env.build('''
(defrule marksafe
(number (r ?r) (c ?c) (n ?))
(bomb ?br ?bc)
=>
(if (isaround ?br ?bc ?r ?c) then
(loop-for-count (?i (- ?r 1) (+ ?r 1)) do
    (loop-for-count (?j (- ?c 1) (+ ?c 1)) do
    (if (and
        (isvalid ?i ?j)
        (not (and (eq ?i ?r) (eq ?j ?c)))
    ) then
        (assert (safe ?i ?j))
    )
    )
)
)
)
        ''')

        env.build('''
(defrule umarksafe
?f <- (safe ?r ?c)
(or
(bomb ?r ?c)
(number (r ?r) (c ?c) (n ?))
)
=>
(retract ?f)
)
        ''')
        # for t in env.templates():
        #     print(t)
        # for t in env.templates():
        #     print(t)

        # data += f'(deffacts initial-fact\n{numbers_string}\n{unknown_string}\n)\n'
        # data += f'(defglobal\n  ?*rsize* = {self.size}\n  ?*csize* = {self.size}\n)\n'

        # print(data)

        env.run()

        # Execute action
        for f in env.facts():
            print(f)
            if('bomb' in f.__repr__()):
                bomb_fact = ' '.join(f.__repr__().split()[2:])
                _, r, c = bomb_fact[1:-1].split()
                r, c = int(r), int(c)
                self.known_bombs.append((r, c))
                self.board[r][c].is_marked = True
                # pass

            if('safe' in f.__repr__()):
                safe_fact = ' '.join(f.__repr__().split()[2:])
                _, r, c = safe_fact[1:-1].split()
                r, c = int(r), int(c)
                self.reveal((r, c))
                # print(data)

                # def initialize_state_clips(starting_position: Tuple[int, int]):
                #     self.initialize_board(starting_position)

                #     with open('./clips/minesweeper.clp', 'a') as file:

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
