# microbit_examples

This repository contains examples of [MicroPython](https://microbit-micropython.readthedocs.io/en/latest/tutorials/hello.html)
code for [BBC micro:bit](https://en.wikipedia.org/wiki/Micro_Bit) development board
plugged into [Kitronik's :GAME ZIP64](https://www.kitronik.co.uk/pdf/5626-game-zip-64-microbit-datasheet.pdf) console,
which adds:
1. an 8x8 matrix of coloured NeoPixels (pin0)
2. 6 extra buttons (pin8, pin12, pin13, pin14, pin15, pin16)
3. a vibrator for haptic feedback (pin1)
4. a piezo buzzer (pin2)
5. on-board batteries for autonomy

# [Connect 4](connect4.py)

A two-player version of classic [Connect 4](https://en.wikipedia.org/wiki/Connect_Four) game.

Here we show how to use NeoPixel screen as a 2D matrix, how to scan keys, how to use the vibrator.

# [Colour lines](colour_lines.py)

A minimalistic implementation of [Colour lines](http://www.vtorov.com/lines/) game.

Here we show how to create a highlighting cursor, how to detect reachability between two points in a maze
using very little heap memory available.

An easier-to-understand (but more heap-memory greedy) [maze reachability algorithm for non-Micro Python](mazement.py) .

# [2048](2048_mb.py)

An implementation of the game of [2048](https://play2048.co) .

There is a natural way to map a grid of 4x4 tiles onto the matrix of 8x8 pixels
by using 2x2 pixel tiles, which gives us an additional way to colour-code them by using patterns
in addition to "solid" colours.

