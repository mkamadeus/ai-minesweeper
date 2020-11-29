import random
import PySimpleGUI as gui
from PySimpleGUI.PySimpleGUI import WINDOW_CLOSED
from Minesweeper import Minesweeper, MinesweeperStatus
import time
import os

size = int(input())
bombs = int(input())
locations = [list(map(int, input().split(' '))) for _ in range(bombs)]

# test_case = os.listdir('./test')
# with open(f'./test/{test_case[random.randint(0, len(test_case))]}', 'r') as f:
#     info = list(map(lambda s: s.strip(), f.readlines()))
#     size = int(info[0])
#     bombs = int(info[1])
#     locations = []
#     for i, d in enumerate(info[2:]):
#         tmp = d.split()
#         locations.append((int(tmp[0]), int(tmp[1])))
# print(locations)


minesweeper = Minesweeper(locations=locations, size=size, bombs=bombs)
is_initialized = False

gui.theme('DarkAmber')

layout = [
    [gui.Text('Minesweeper', font=('Roboto', 24), justification='center')],
    *[[gui.Button(key=f'tile_{i}_{j}', size=(2, 2), pad=(0, 0), font=('Roboto', 12))
       for j in range(minesweeper.size)] for i in range(minesweeper.size)],
    [gui.Button('lesgo')]
]


window = gui.Window('Minesweeper', layout)

while True:
    event, values = window.read()
    if(event == WINDOW_CLOSED):
        break

    if(event is not None):
        # r, c = list(map(lambda v: int(v), event.split('_')[1:]))

        # print(r, c, minesweeper.board[r][c].is_bomb)

        if(not is_initialized):
            minesweeper.initialize_board()
            is_initialized = True
        else:
            minesweeper.inference()

        for i in range(minesweeper.size):
            for j in range(minesweeper.size):
                status = ''
                if((i, j) in minesweeper.known_bombs):
                    status = 'M'

                if(minesweeper.board[i][j].status != -1):
                    window[f'tile_{i}_{j}'].update(
                        button_color=('white', 'black'), disabled=True)

                    if(minesweeper.board[i][j].is_bomb):
                        status = 'B'
                    else:
                        status = str(minesweeper.board[i][j].status)

                window[f'tile_{i}_{j}'].update(status)

        if(minesweeper.status == MinesweeperStatus.LOSE):
            gui.popup('Cupu kon cok')
            break
        elif(minesweeper.status == MinesweeperStatus.WIN):
            gui.popup('Kon jago euy')
            break

        # time.sleep(1)
        minesweeper.print_board()

window.close()
