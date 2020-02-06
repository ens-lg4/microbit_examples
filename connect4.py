#   MicroPython 2-player version of "Connect 4" game
#   for Keytronik's :GAME ZIP64 console (BBC micro:bit)
#

from microbit import *
import neopixel

## Constants:
#
screen          = neopixel.NeoPixel(pin0, 64)
empty           = (0, 0, 0)     # black
neutral_edge    = (0, 10, 0)    # green
draw_edge       = (10, 0, 10)   # purple
connected       = 4
width           = 7
bottom          = 7
top             = 2
player_colour   = [empty, (20, 0, 0), (0, 0, 20)]
player_name     = ["Nobody", "Red", "Blue"]

## Globals:
#
board           = []

def plot(x, y, colour):
    'Maps 2D coordinates to a 1D vector'

    screen[x+(y*8)] = colour
    screen.show()


def paint_edge(colour):
    'Draws the board edge (Connect-4 is normally played on 7x6 board)'

    for i in range(width):
        plot(i,0,   colour)
        plot(width,i+1, colour)


def has_won(x, y, player):
    'Checks that the current player has won by the last move'

    def check_bidirection(dx, dy):
        'Combine two opposite (uni)directions into one line passing through (x,y)'

        def count_unidirection(dx, dy):
            'Count how many steps the line extends from (x,y) in the given direction (dx,dy), constrained by the board edges'

            dist = 0
            nx = x + dx*(dist+1)
            ny = y + dy*(dist+1)
            while 0<=nx<width and top<=ny<=bottom and board[nx][ny]==player:
                dist += 1
                nx = x + dx*(dist+1)
                ny = y + dy*(dist+1)
            return dist

        return count_unidirection(dx, dy) + 1 + count_unidirection(-dx, -dy) >= connected

    return (check_bidirection(1, 0) or
            check_bidirection(0, 1) or
            check_bidirection(1, 1) or
            check_bidirection(-1, 1) )


def board_is_full():
    'Full to the brim - only check the top edge is full'

    for i in range(width):
        if board[i][top] == 0:
            return False
    return True


def shake(duration_ms=100):
    'Haptic feedback'

    pin1.write_digital(1)
    sleep(duration_ms)
    pin1.write_digital(0)


def wait_for_any_key(delay_ms=50):
    'Scan all available keys'

    while True:
        for pin in (pin8, pin12, pin13, pin14, pin15, pin16):
            if pin.read_digital()==0:
                return
        sleep(delay_ms)


def play_one_game():
    'Built around an infinite keyboard scan loop which is interrupted on win or draw'

    global board    # we need to change the global one

    board           = [[0]*8 for i in range(8)]     # empty the board
    screen.clear()
    paint_edge( neutral_edge )
    display.scroll("C4")
    current_player  = 1
    current_x       = int(width/2)
    current_y       = top-1

    while True:
        current_colour = player_colour[current_player]

        plot(current_x, current_y, current_colour)

        if pin12.read_digital() == 0:               # was the "Left" button pressed?
            plot(current_x, current_y, empty)
            current_x = (current_x-1) % width
            sleep(300)
        elif pin13.read_digital() == 0:             # was the "Right" button pressed?
            plot(current_x, current_y, empty)
            current_x = (current_x+1) % width
            sleep(300)
        elif pin14.read_digital() == 0:             # was the "Down" button pressed?
            for new_y in range(top, bottom+1):      # animation of a falling ball
                if board[current_x][new_y] == 0:
                    plot(current_x, current_y, player_colour[0])
                    current_y = new_y
                    plot(current_x, current_y, current_colour)
                else:
                    break

            if current_y>=top:                      # otherwise this column is full, do not drop the ball here
                board[current_x][current_y] = current_player    # record the move on the board

                if has_won(current_x, current_y, current_player):
                    paint_edge(current_colour)
                    display.scroll(player_name[current_player] + ' wins' )
                    break

                if board_is_full():                 # if nobody has won, but the board is full - it's a draw
                    paint_edge(draw_edge)
                    display.scroll('Draw')
                    break

                current_player  = 3 - current_player         # swap players
                current_x       = int(width/2)
                current_y       = top-1
                sleep(1000)


while True:
    play_one_game()
    sleep(500)
    shake()
    display.scroll('Again?')
    wait_for_any_key()