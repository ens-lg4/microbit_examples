#!/usr/bin/env python3

# A simple algorithm to find a path between A and B in a 4-connected maze.
#
# Designed for the game of "Colour lines"

from random import randint

empty_symbol    = ' '
wall_symbol     = 'O'
path_symbol     = '.'

def init_board(width, height, obstacles):

    board = [[empty_symbol]*height for x in range(width)]

    def place_randomly_on_board(symbol):
        x = randint(0, width-1)
        y = randint(0, height-1)
        while board[x][y] != empty_symbol:
            x = randint(0, width-1)
            y = randint(0, height-1)
        board[x][y] = symbol
        return x,y

    for _ in range(obstacles):
        place_randomly_on_board(wall_symbol)

    A = place_randomly_on_board('A')
    B = place_randomly_on_board('B')

    return board, A, B


def show_board(board):
    width   = len(board)
    height  = len(board[0])

    for y in range(len(board[0])):
        for x in range(len(board)):
            print('{}'.format(board[x][y]), end='')
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
                        path_list = []
                        while P!=A:
                            path_list.insert(0, P)
                            P = prev[P]
                        return (True, path_list)
                    elif board[nx][ny] == empty_symbol and N not in all_accessible_set:  # new accessible?
                        prev[ N ] = C
                        all_accessible_set.add( N )
                        new_edge_set.add( N )

        if new_edge_set:
            current_edge_set = new_edge_set
        else:
            return (False, [])


maze, A, B = init_board(40, 20, 250)

found_path, path_list = find_path(maze, A, B)

for px, py in path_list:
    maze[px][py] = path_symbol

show_board(maze)    # will contain the path if found

if not found_path:
    print("\nUnreachable")
