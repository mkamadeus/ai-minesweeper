import PySimpleGUI as gui
from PySimpleGUI.PySimpleGUI import WINDOW_CLOSED
from Minesweeper import Minesweeper, MinesweeperStatus

size = int(input())
bombs = int(input())
locations = [list(map(int, input().split(', '))) for _ in range(bombs)]

minesweeper = Minesweeper(locations=locations, size=size, bombs=bombs)
is_initialized = False

gui.theme('DarkAmber')

layout = [
    [gui.Text('Minesweeper', font=('Roboto', 24), justification='center')],
    *[[gui.Button(key=f'tile_{i}_{j}', size=(2, 2), pad=(0, 0), font=('Roboto', 12))
       for j in range(minesweeper.size)] for i in range(minesweeper.size)],
    [gui.Button('Run!')]
]


window = gui.Window('Minesweeper', layout)

while True:
    event, values = window.read()
    if(event == WINDOW_CLOSED):
        break

    if(event is not None):
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
            gui.popup('AI kalah! Silahkan coba lagi!', title='AI kalah!')
            break
        elif(minesweeper.status == MinesweeperStatus.WIN):
            gui.popup('AI menang! Skynet sudah ada di depan mata Anda!', title='AI menang!')
            break

        # time.sleep(1)
        minesweeper.print_board()

window.close()
