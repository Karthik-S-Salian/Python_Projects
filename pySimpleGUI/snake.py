from random import randint

import PySimpleGUI as sg

# game constants
FIELD_SIZE = 400
CELL_NUM = 15
CELL_SIZE = FIELD_SIZE / CELL_NUM
DIRECTIONS = {'left': (-1, 0), 'right': (1, 0), 'up': (0, 1), 'down': (0, -1)}
snake_body = [(4, 4), (3, 4), (2, 4)]
direction = DIRECTIONS['up']


def span_apple():
    apple_pos = (randint(0, CELL_NUM - 1), randint(0, CELL_NUM - 1))
    while apple_pos in snake_body:
        apple_pos = (randint(0, CELL_NUM - 1), randint(0, CELL_NUM - 1))
    return apple_pos


def convert_pos_to_pixel(cell):
    tl = cell[0] * CELL_SIZE, cell[1] * CELL_SIZE
    br = tl[0] + CELL_SIZE, tl[1] + CELL_SIZE
    return tl, br


field = sg.Graph(
    canvas_size=(FIELD_SIZE, FIELD_SIZE),
    graph_bottom_left=(0, 0),
    graph_top_right=(FIELD_SIZE, FIELD_SIZE),
    background_color='black')

layout = [[field]]

window = sg.Window('Snake', layout, return_keyboard_events=True)

apple_pos = span_apple()
while True:
    event, values = window.read(timeout=500)
    print(event)

    if event == sg.WIN_CLOSED: break
    if event == 'Left:37': direction = DIRECTIONS['left']
    if event == 'Up:38': direction = DIRECTIONS['up']
    if event == 'Right:39': direction = DIRECTIONS['right']
    if event == 'Down:40': direction = DIRECTIONS['down']

    new_head = (snake_body[0][0] + direction[0], snake_body[0][1] + direction[1])
    if new_head[0] < 0 or new_head[0] >= CELL_NUM \
            or new_head[1] < 0 or new_head[1] >= CELL_NUM \
            or new_head in snake_body[:-1]:
        break

    snake_body.insert(0, new_head)
    if new_head == apple_pos:
        apple_pos = span_apple()
    else:
        snake_body.pop()

    field.DrawRectangle((0, 0), (FIELD_SIZE, FIELD_SIZE), 'black')
    field.DrawRectangle(*convert_pos_to_pixel(apple_pos), 'red')
    field.DrawRectangle(*convert_pos_to_pixel(snake_body[0]), 'yellow')

    for part in snake_body[1:]:
        tl, br = convert_pos_to_pixel(part)
        field.DrawRectangle(tl, br, 'green')

window.close()
