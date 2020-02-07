# microbit_examples

This repository contains examples of [MicroPython games for BBC micro:bit](https://microbit-micropython.readthedocs.io/en/latest/tutorials/hello.html) using [Kitronik's :GAME ZIP64](https://www.kitronik.co.uk/pdf/5626-game-zip-64-microbit-datasheet.pdf) console, which extends the [bare micro:bit](https://en.wikipedia.org/wiki/Micro_Bit) with:
1. a 8x8 matrix of coloured NeoPixels (pin0)
2. 6 extra buttons (pin8, pin12, pin13, pin14, pin15, pin16)
3. a vibrator for haptic feedback (pin1)
4. a piezo buzzer (pin2)
5. on-board batteries for autonomy

# Connect 4

A two-player version of classic [Connect 4](https://en.wikipedia.org/wiki/Connect_Four) game.

Here we show how to use NeoPixel screen as a 2D matrix, how to scan keys, how to use the vibrator.
