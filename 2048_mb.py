from microbit import *
import neopixel
from random import randint

goal = 2048
goal_reached = False


colours = {
    'black':    ( 0,  0,  0),
    'red':      (10,  0,  0),
    'yellow':   ( 7,  7,  0),
    'green':    ( 0, 10,  0),
    'cyan':     ( 0,  7,  2),
    'blue':     ( 0,  0, 10),
    'purple':   ( 7,  0,  7),
    'white':    ( 7,  7,  7),
}

patterns = {
    0:      ('black',   'black'),
    2:      ('red',     'red'),
    4:      ('yellow',  'yellow'),
    8:      ('green',   'green'),
    16:     ('blue',    'blue'),
    32:     ('purple',  'purple'),
    64:     ('red',     'white'),
    128:    ('yellow',  'white'),
    256:    ('green',   'white'),
    512:    ('blue',    'white'),
    1024:   ('purple',  'white'),
    2048:   ('white',  'white'),
}

board = [ [0, 0, 0, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0] ]
size = len(board)   # high level board abstraction (pieces)

board_size  = 8     # low level board abstraction (pixels)
screen = neopixel.NeoPixel(pin0, board_size*board_size)


def low_level_plot(x, y, colour_name):
    screen[x+(y*board_size)] = colours[colour_name]
    screen.show()


def draw_square(x, y, first_colour, second_colour):
    low_level_plot(2*x,   2*y,   first_colour)
    low_level_plot(2*x+1, 2*y+1, first_colour)
    low_level_plot(2*x+1, 2*y,   second_colour)
    low_level_plot(2*x,   2*y+1, second_colour)


def show_board():
    for y in range(size):
        for x in range(size):
            power_of_two = board[y][x]
            first_colour, second_colour = patterns[power_of_two]
            draw_square(x,y, first_colour, second_colour)


def place_new_number_randomly():
    x = randint(0, size-1)
    y = randint(0, size-1)
    while board[y][x]>0:
        x = randint(0, size-1)
        y = randint(0, size-1)

    nbr = 2**randint(1,2)
    board[y][x] = nbr


def can_move():
    for y in range(size):
        for x in range(size):
            if board[y][x]==0:
                return True
            if y+1<size and board[y][x]==board[y+1][x]:
                return True
            if x+1<size and board[y][x]==board[y][x+1]:
                return True
    return False


def squash_list(original_list):

    def squash(compact):
        global goal_reached

        for head in range(len(compact)-1):
            if head+1<len(compact) and compact[head]==compact[head+1]:
                compact.pop(head)
                compact[head] *= 2
                if compact[head] == goal:
                    goal_reached = True
        return compact

    orig_length = len(original_list)
    modified_list = squash( [num for num in original_list if num>0] )
    modified_list += [0]*(orig_length-len(modified_list))
    return modified_list


def squash_up():
    any_changes = False
    for x in range(size):
        original_list = []
        for y in range(size):
            original_list.append( board[y][x] )
        modified_list = squash_list(original_list)
        if original_list != modified_list:
            any_changes = True
        for y in range(size):
            board[y][x] = modified_list.pop(0)
    return any_changes

def squash_down():
    any_changes = False
    for x in range(size):
        original_list = []
        for y in reversed(range(size)):
            original_list.append( board[y][x] )
        modified_list = squash_list(original_list)
        if original_list != modified_list:
            any_changes = True
        for y in reversed(range(size)):
            board[y][x] = modified_list.pop(0)
    return any_changes

def squash_left():
    any_changes = False
    for y in range(size):
        original_list = []
        for x in range(size):
            original_list.append( board[y][x] )
        modified_list = squash_list(original_list)
        if original_list != modified_list:
            any_changes = True
        for x in range(size):
            board[y][x] = modified_list.pop(0)
    return any_changes

def squash_right():
    any_changes = False
    for y in range(size):
        original_list = []
        for x in reversed(range(size)):
            original_list.append( board[y][x] )
        modified_list = squash_list(original_list)
        if original_list != modified_list:
            any_changes = True
        for x in reversed(range(size)):
            board[y][x] = modified_list.pop(0)
    return any_changes


def game():
    global goal_reached

    place_new_number_randomly()
    place_new_number_randomly()
    show_board()

    while (not goal_reached) and can_move():
        any_changes = False
        while not any_changes:
            if pin8.read_digital() == 0:
                any_changes = squash_up()
            elif pin14.read_digital() == 0:
                any_changes = squash_down()
            elif pin12.read_digital() == 0:
                any_changes = squash_left()
            elif pin13.read_digital() == 0:
                any_changes = squash_right()
        place_new_number_randomly()
        show_board()
        sleep(500)

    if goal_reached:
        display.scroll('You win')
    else:
        display.scroll('Board full')

game()