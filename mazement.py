#!/usr/bin/env python3

# A simple algorithm to find a path between A and B in a 4-connected maze.
#
# Designed for the game of "Colour lines"

from random import randint

empty   = ' '
wall    = 'O'
path    = '.'

def init_board(width, height, obstacles):

    board = [[empty]*height for x in range(width)]

    def place_randomly_on_board(symbol):
        x = randint(0, width-1)
        y = randint(0, height-1)
        while board[x][y] != empty:
            x = randint(0, width-1)
            y = randint(0, height-1)
        board[x][y] = symbol
        return x,y

    for _ in range(obstacles):
        place_randomly_on_board(wall)

    A = place_randomly_on_board('A')
    B = place_randomly_on_board('B')

    return board, A, B


def show_board(board):
    width   = len(board)
    height  = len(board[0])

    for y in range(len(board[0])):
        for x in range(len(board)):
            print('{} '.format(board[x][y]), end='')
        print()


def find_path(board, A, B):
    width   = len(board)
    height  = len(board[0])

    all_accessible_set  = { A }
    current_edge_set    = { A }
    prev                = dict()

    while True:
        new_edge_set = set()
        for C in current_edge_set:
            cx, cy = C
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:   # all possible moves from C
                N = nx, ny = cx+dx, cy+dy
                if 0<=nx<width and 0<=ny<height:                # still within the board?
                    if N==B:
                        prev[ N ] = C
                        P = prev[N]
                        while P!=A:
                            px, py = P
                            board[px][py]=path                  # show the path on the board
                            P = prev[P]
                        return True
                    elif board[nx][ny] == empty and N not in all_accessible_set:  # new accessible?
                        prev[ N ] = C
                        all_accessible_set.add( N )
                        new_edge_set.add( N )

        if new_edge_set:
            current_edge_set = new_edge_set
        else:
            return False


maze, A, B = init_board(40, 20, 320)

found_path = find_path(maze, A, B)

show_board(maze)    # will contain the path if found

if not found_path:
    print("\nUnreachable")
