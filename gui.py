import PySimpleGUI as gui
from PySimpleGUI.PySimpleGUI import WINDOW_CLOSED


layout = [
    [gui.Text('Title')],
    *[[gui.Button(f'{i},{j}', key=f'tile_{i}_{j}')
       for j in range(10)] for i in range(10)],
    [gui.Text('Title')]
]

window = gui.Window('Minesweeper', layout)

while True:
    event, values = window.read()
    if(event == WINDOW_CLOSED):
        break
    print(event)

window.close()
