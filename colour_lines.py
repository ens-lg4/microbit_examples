from microbit import *
import neopixel
from random import randint

screen = neopixel.NeoPixel(pin0, 64)    # physical 8*8
board_size  = 8                         # logical (don't have to match)


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
    def trace_bidirection(dx, dy):
        def trace_unidirection(dx, dy):
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
        return bidirection_coords if len(bidirection_coords)+1 >= 5 else []

    return (trace_bidirection(1, 0)  +
            trace_bidirection(0, 1)  +
            trace_bidirection(1, 1)  +
            trace_bidirection(-1, 1) +
            [(x,y)] )


all_levels_matrix = [[0]*board_size for i in range(board_size)]

def there_is_path(A, B):
    for x in range(8):
        for y in range(8):
            all_levels_matrix[x][y] = 0

    level = all_levels_matrix[A[0]][A[1]] = 1

    while True:
        new_edge_started = False
        for cx in range(8):
            for cy in range(8):
                if all_levels_matrix[cx][cy]==level:
                    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:   # all possible moves from C
                        nx, ny = cx+dx, cy+dy
                        if 0<=nx<board_size and 0<=ny<board_size:                # still within the board?
                            if (nx,ny)==B:
                                return True
                            elif board[nx][ny] == 0 and all_levels_matrix[nx][ny] == 0:  # new accessible?
                                all_levels_matrix[nx][ny] = level+1
                                new_edge_started = True
        if new_edge_started:
            level += 1
        else:
            return False


def add_new_balls(n):
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
under_cursor = board[cursor_x][cursor_y]
plot(cursor_x, cursor_y, highlight[under_cursor])
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
                if there_is_path((selected_x, selected_y), (cursor_x, cursor_y)):
                    board[cursor_x][cursor_y] = selected_c
                    board[selected_x][selected_y] = 0

                    winning_coords = trace_winning_coords(cursor_x, cursor_y, selected_c)
                    if len(winning_coords)>1:   # clean up the winning balls
                        for wx, wy in winning_coords:
                            board[wx][wy] = 0
                            plot(wx, wy, colours[0])
                    else:
                        add_new_balls(3)
                else:
                    display.scroll('No way')
            selected_c = board[selected_x][selected_y]  # unselect and revert to neutral shade
            plot(selected_x, selected_y, colours[selected_c])
            selected_c = 0
        elif under_cursor!=0:   # select a new ball
            selected_x, selected_y, selected_c = cursor_x, cursor_y, under_cursor
        else:
            cursor_moved = False
        sleep(200)
    else:
        cursor_moved = False

    if cursor_moved:
        if selected_c and cursor_x==selected_x and cursor_y==selected_y:
            plot(cursor_x, cursor_y, selected[under_cursor])
        else:
            plot(cursor_x, cursor_y, colours[under_cursor])
        cursor_x, cursor_y = new_x, new_y
        under_cursor = board[cursor_x][cursor_y]
        plot(cursor_x, cursor_y, highlight[under_cursor])
        sleep(200)