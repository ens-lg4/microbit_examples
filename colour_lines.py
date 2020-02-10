from microbit import *
import neopixel
from random import randint

screen = neopixel.NeoPixel(pin0, 64)    # physical 8*8
board_size  = 8                         # logical (don't have to match)
connected   = 5


# Enable NeoPixels to use x & y values
def plot(x, y, colour):
    screen[x+(y*8)] = colour            # physical 8
    screen.show()


black = (0, 0, 0)
colours     = [black, (10, 0, 0), (0, 10, 0), (0, 0, 10), (7, 7, 0)]
highlight   = [(10, 10, 10), (40, 0, 0), (0, 40, 0), (0, 0, 40), (20, 20, 0)]
selected    = [black, (2, 0, 0), (0, 2, 0), (0, 0, 2), (2, 2, 0)]
board       = [[0]*board_size for i in range(board_size)]
n_balls     = 0


def trace_winning_coords(x, y, c):
    'Return the list of all completed line coordinates that the current c has matched with'

    def trace_bidirection(dx, dy):
        'Combine two opposite (uni)directions into one line passing through (x,y)'

        def trace_unidirection(dx, dy):
            'Trace the longest line that extends from (x,y) in the given direction (dx,dy), constrained by the board edges'

            dist = 0
            coords = []
            nx = x + dx*(dist+1)
            ny = y + dy*(dist+1)
            while 0<=nx<board_size and 0<=ny<board_size and board[nx][ny]==c:
                dist += 1
                coords += [(nx, ny)]
                nx = x + dx*(dist+1)
                ny = y + dy*(dist+1)
            return coords

        bidirection_coords = trace_unidirection(dx, dy) + trace_unidirection(-dx, -dy)
        return bidirection_coords if len(bidirection_coords) >= (connected-1) else []

    return (trace_bidirection(1, 0)  +
            trace_bidirection(0, 1)  +
            trace_bidirection(1, 1)  +
            trace_bidirection(-1, 1) +
            [(x,y)] )


def add_new_balls(n):   # ToDo: check that newly added balls have automatically completed some lines
    global n_balls

    for _ in range(n):
        c = randint(1, len(colours)-1)
        x = randint(0, board_size-1)
        y = randint(0, board_size-1)
        while n_balls<board_size*board_size and board[x][y] != 0:
            x = randint(0, board_size-1)
            y = randint(0, board_size-1)

        if n_balls<board_size*board_size:
            board[x][y] = c
            plot(x, y, colours[board[x][y]])
            n_balls += 1


add_new_balls(5)
cursor_x = 3
cursor_y = 3
plot(cursor_x, cursor_y, highlight[board[cursor_x][cursor_y]])
selected_c = 0

while True:
    new_x, new_y, cursor_moved = cursor_x, cursor_y, True

    # Up
    if pin8.read_digital() == 0:
        new_y = (cursor_y-1) % 8
    # Down
    elif pin14.read_digital() == 0:
        new_y = (cursor_y+1) % 8
    # Left
    elif pin12.read_digital() == 0:
        new_x = (cursor_x-1) % 8
    # Left
    elif pin13.read_digital() == 0:
        new_x = (cursor_x+1) % 8
    elif pin16.read_digital() == 0: # obligatory change of state
        under_cursor = board[cursor_x][cursor_y]
        if selected_c:
            if under_cursor==0:
                board[cursor_x][cursor_y] = selected_c
                board[selected_x][selected_y] = 0
                plot(cursor_x, cursor_y, highlight[selected_c])

                winning_coords = trace_winning_coords(cursor_x, cursor_y, selected_c)
                if len(winning_coords)>1:
                    # remove the balls at winning coords
                    for wx, wy in winning_coords:
                        board[wx][wy] = 0
                        plot(wx, wy, colours[0])
                else:
                    add_new_balls(3)
            else:   # just unselect and revert to neutral shade
                pass
            selected_c = board[selected_x][selected_y]
            plot(selected_x, selected_y, colours[selected_c])
            selected_c = 0
        elif under_cursor!=0:   # select a new ball
            selected_x, selected_y, selected_c = cursor_x, cursor_y, under_cursor
            plot(selected_x, selected_y, selected[selected_c])

        cursor_moved = False
        sleep(200)
    else:
        cursor_moved = False

    if cursor_moved:
        if selected_c and cursor_x==selected_x and cursor_y==selected_y:
            plot(cursor_x, cursor_y, selected[board[cursor_x][cursor_y]])
        else:
            plot(cursor_x, cursor_y, colours[board[cursor_x][cursor_y]])
        cursor_x, cursor_y = new_x, new_y
        plot(cursor_x, cursor_y, highlight[board[cursor_x][cursor_y]])
        sleep(200)