from microbit import *
import neopixel
from random import randint

screen = neopixel.NeoPixel(pin0, 64)
board_size  = 8


def plot(x, y, colour):
    screen[x+(y*board_size)] = colour
    screen.show()


colours     = [(0, 0, 0), (10, 0, 0), (0, 10, 0), (0, 0, 10), (7, 7, 0)]
highlight   = [(10, 10, 10), (40, 0, 0), (0, 40, 0), (0, 0, 40), (20, 20, 0)]
selected    = [(0, 0, 0), (2, 0, 0), (0, 2, 0), (0, 0, 2), (2, 2, 0)]
board       = [[0]*board_size for i in range(board_size)]
n_balls     = 0
score       = 0

def remove_winning_coords(x, y, c):
    global board

    def trace_bidirection(bdx, bdy):

        def trace_unidirection(dx, dy):
            dist = 0
            nx = x + dx*(dist+1)
            ny = y + dy*(dist+1)
            while 0<=nx<board_size and 0<=ny<board_size and board[nx][ny]==c:
                dist += 1
                nx = x + dx*(dist+1)
                ny = y + dy*(dist+1)
            return dist

        one_way_dist        = trace_unidirection(bdx, bdy)
        opposite_way_dist   = trace_unidirection(-bdx, -bdy)

        if one_way_dist + opposite_way_dist + 1 >= 5:
            for dist in range(-opposite_way_dist, one_way_dist+1):
                if dist!=0:
                    winning_coords.append( (x + bdx*dist, y + bdy*dist) )

    global n_balls
    global score

    winning_coords = [ (x, y) ]
    trace_bidirection(1, 0)
    trace_bidirection(0, 1)
    trace_bidirection(1, 1)
    trace_bidirection(-1, 1)
    if len(winning_coords)>1:
        for w in winning_coords:
            board[w[0]][w[1]] = 0
            plot(w[0], w[1], colours[0])
            n_balls -= 1
            score += 1
        display.scroll(score)
        return True
    else:
        return False

all_levels_matrix = [[0]*board_size for i in range(board_size)]

def there_is_path(A, B):
    global all_levels_matrix

    for x in range(8):
        for y in range(8):
            all_levels_matrix[x][y] = 0

    level = all_levels_matrix[A[0]][A[1]] = 1

    while True:
        new_edge_started = False
        for cx in range(8):
            for cy in range(8):
                if all_levels_matrix[cx][cy]==level:
                    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        nx = cx+dx
                        ny = cy+dy
                        if 0<=nx<board_size and 0<=ny<board_size:
                            if nx==B[0] and ny==B[1]:
                                return True
                            elif board[nx][ny] == 0 and all_levels_matrix[nx][ny] == 0:
                                all_levels_matrix[nx][ny] = level+1
                                new_edge_started = True
        if new_edge_started:
            level += 1
        else:
            return False


def add_new_balls(n):
    global n_balls
    global board

    for _ in range(n):
        c = randint(1, len(colours)-1)
        x = randint(0, board_size-1)
        y = randint(0, board_size-1)
        while n_balls<board_size*board_size and board[x][y] != 0:
            x = randint(0, board_size-1)
            y = randint(0, board_size-1)

        if n_balls<board_size*board_size:
            board[x][y] = c
            plot(x, y, colours[c])
            n_balls += 1
            remove_winning_coords(x, y, c)


add_new_balls(5)
cursor_x = 3
cursor_y = 3
under_cursor = board[cursor_x][cursor_y]
plot(cursor_x, cursor_y, highlight[under_cursor])
selected_c = 0
game_on = True

while game_on:
    new_x = cursor_x
    new_y = cursor_y
    cursor_moved = True

    if pin8.read_digital() == 0:
        new_y = (cursor_y-1) % board_size
    elif pin14.read_digital() == 0:
        new_y = (cursor_y+1) % board_size
    elif pin12.read_digital() == 0:
        new_x = (cursor_x-1) % board_size
    elif pin13.read_digital() == 0:
        new_x = (cursor_x+1) % board_size
    elif pin16.read_digital() == 0:
        under_cursor = board[cursor_x][cursor_y]
        if selected_c:
            if under_cursor==0:
                if there_is_path((selected_x, selected_y), (cursor_x, cursor_y)):
                    board[cursor_x][cursor_y] = selected_c
                    board[selected_x][selected_y] = 0

                    if not remove_winning_coords(cursor_x, cursor_y, selected_c):
                        add_new_balls(3)
                        if n_balls==board_size*board_size:
                            display.scroll('Game over. Score: ')
                            display.scroll(score)
                            game_on = False
                else:
                    display.scroll('No way')
            selected_c = board[selected_x][selected_y]
            plot(selected_x, selected_y, colours[selected_c])
            selected_c = 0
        elif under_cursor!=0:
            selected_x = cursor_x
            selected_y = cursor_y
            selected_c = under_cursor
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
        cursor_x = new_x
        cursor_y = new_y
        under_cursor = board[cursor_x][cursor_y]
        plot(cursor_x, cursor_y, highlight[under_cursor])
        sleep(200)

