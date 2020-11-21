import PySimpleGUI as gui
from PySimpleGUI.PySimpleGUI import WINDOW_CLOSED
from Minesweeper import Minesweeper, MinesweeperStatus

minesweeper = Minesweeper(size=8, bombs=5)
is_initialized = False

layout = [
    [gui.Text('Minesweeper')],
    *[[gui.Button(key=f'tile_{i}_{j}')
       for j in range(minesweeper.size)] for i in range(minesweeper.size)],
]


window = gui.Window('Minesweeper', layout)

while True:
    event, values = window.read()
    if(event == WINDOW_CLOSED):
        break

    if(event is not None and 'tile' in event):
        r, c = list(map(lambda v: int(v), event.split('_')[1:]))

        print(r, c, minesweeper.board[r][c].is_bomb)

        if(not is_initialized):
            minesweeper.initialize_board((r, c))
            is_initialized = True
        else:
            minesweeper.reveal((r, c))

        if(minesweeper.status == MinesweeperStatus.LOSE):
            gui.popup('Cupu kon cok')
            break

        for i in range(minesweeper.size):
            for j in range(minesweeper.size):
                status = ''
                if(minesweeper.board[i][j].status != -1):
                    if(minesweeper.board[i][j].is_bomb):
                        status = 'B'
                    else:
                        status = str(minesweeper.board[i][j].status)
                window[f'tile_{i}_{j}'].update(status)

        minesweeper.print_board()

window.close()
