import PySimpleGUI as gui
from PySimpleGUI.PySimpleGUI import WINDOW_CLOSED
from Minesweeper import Minesweeper, MinesweeperStatus
import time

minesweeper = Minesweeper(size=4)
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
            minesweeper.initialize_board((0, 0))
            is_initialized = True
        else:
            minesweeper.inference()

        for i in range(minesweeper.size):
            for j in range(minesweeper.size):
                status = ''
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
