import time
import random
import PySimpleGUI as gui
from PySimpleGUI.PySimpleGUI import WINDOW_CLOSED
from Minesweeper import Minesweeper, MinesweeperStatus

# Get all arguments input from test case
size = int(input())
bombs = int(input())
locations = [list(map(int, input().split(', '))) for _ in range(bombs)]

# Create new minesweeper object
minesweeper = Minesweeper(locations=locations, size=size, bombs=bombs)
is_initialized = False
is_manual = False

# Initialize all GUI components
gui.theme('DarkAmber')

layout = [
    [gui.Text('Minesweeper', font=('Roboto', 24), justification='center')],
    *[[gui.Button(key=f'tile_{i}_{j}', size=(2, 2), pad=(0, 0), font=('Roboto', 12))
       for j in range(minesweeper.size)] for i in range(minesweeper.size)],
    [gui.Button('Step', disabled=False, key="-step-"), gui.Button(
        'Manual Toggle', key="-manual-"), gui.Button('Simulate', key='-simulate-')]
]

# Generate window application
window = gui.Window('Minesweeper', layout)

# Lose and Win Random Messages
lose_message = [
    'Yah kalah :(',
    'Anda/AI kalah, silakan coba lagi.',
    'あなたが失う!',
    'Anda cupu. Mati ajalah coy'
]

win_message = [
    'Yey menang :)',
    'UwU menang dong :>',
    'あなたが勝つ!',
    'Anda jago juga!'
]


def update_gui():
    """
    Procedure for updating GUI
    """
    for i in range(minesweeper.size):
        for j in range(minesweeper.size):
            status = ''
            if((i, j) in minesweeper.known_bombs):
                status = 'M'
                window[f'tile_{i}_{j}'].update(
                    button_color=("#000000", "#faa228"))

            if(minesweeper.board[i][j].status != -1):
                if(minesweeper.board[i][j].status == 0):
                    window[f'tile_{i}_{j}'].update(
                        button_color=('#555555', 'gray'))
                else:
                    window[f'tile_{i}_{j}'].update(
                        button_color=('#ffd000', '#333333'))

                if(minesweeper.board[i][j].is_bomb):
                    status = 'B'
                else:
                    status = str(minesweeper.board[i][j].status)

            window[f'tile_{i}_{j}'].update(status)


# While event running
while True:
    event, values = window.read()

    # Get event close app
    if (event == WINDOW_CLOSED):
        break

    if(event == '-simulate-'):
        while minesweeper.status == MinesweeperStatus.PLAYING:
            if(not is_initialized):
                minesweeper.initialize_board()
                is_initialized = True
                window['-step-'].update(disabled=is_manual,
                                        button_color=('white', 'gray'))
                window['-manual-'].update(disabled=is_manual,
                                          button_color=('white', 'gray'))
                window['-simulate-'].update(disabled=is_manual,
                                            button_color=('white', 'gray'))
            else:
                minesweeper.inference()
            update_gui()
            window.refresh()
            time.sleep(0.5)

    # If manual toggled...
    if (event == '-manual-'):
        is_manual = True
        window['-step-'].update(disabled=is_manual,
                                button_color=('white', 'gray'))

    if (is_manual and 'tile' in event):
        if(not is_initialized):
            minesweeper.initialize_board()
            is_initialized = True
        else:
            r, c = list(map(int, event.split('_')[1:]))
            minesweeper.reveal((r, c))

    # If manual is not toggled and
    if (event == '-step-' and not is_manual):
        if(not is_initialized):
            minesweeper.initialize_board()
            is_initialized = True
        else:
            minesweeper.inference()

    update_gui()

    # If the minesweeper state is Terminal State
    if (minesweeper.status == MinesweeperStatus.LOSE):
        gui.popup(lose_message[random.randint(
            0, len(lose_message) - 1)], title='You lose!')
        break
    elif (minesweeper.status == MinesweeperStatus.WIN):
        gui.popup(win_message[random.randint(0, len(win_message) - 1)],
                  title='You win!')
        break

window.close()
