from microbit import *
import music

## This is my cover of Dr.Mario "Fever" theme by Hirokazu Tanaka of Nintendo ( https://en.wikipedia.org/wiki/Dr._Mario )
#
# The version I used to transcribe:  https://www.youtube.com/watch?v=L-d1pPzACR0
# A great piano cover: https://www.youtube.com/watch?v=0crCBwfB1XA

dr_mario_tune = [
##  Intro is not to be included in the main loop, but there is no API means for this :(
#
#    'g2:2', 'g', 'bb', 'b', 'c3', 'b2', 'bb', 'a',
#    'g2:2', 'g', 'bb', 'b', 'c3', 'b2', 'bb', 'a',

    'a#4:2', 'b', 'a#', 'b', 'a', 'g', 'g', 'a', 'a#', 'b', 'a', 'g', 'g', 'r:6',
    'a#4:2', 'b', 'a#', 'b', 'a', 'g', 'g', 'a', 'b2:1', 'b', 'b', 'r', 'c3', 'c', 'c', 'r', 'c#', 'c#', 'c#', 'r', 'd', 'd', 'd', 'r',
    'a#4:2', 'b', 'a#', 'b', 'a', 'g', 'g', 'a', 'a#', 'b', 'a', 'g', 'g', 'r', 'r', 'r',
    'a#4:2', 'b', 'a#', 'b', 'a', 'g', 'g', 'a', 'e7:1', 'd5', 'e7', 'g5', 'e7:1', 'd5', 'b6', 'd7', 'e7:1', 'd5', 'e7', 'g5', 'e7:1', 'd5', 'b6', 'd7',

    'eb5:2', 'e', 'eb', 'e', 'd', 'c', 'c', 'a4', 'eb5', 'e', 'd', 'c', 'c', 'r:6',
    'eb5:2', 'e', 'eb', 'e', 'd', 'c', 'c', 'a4', 'f#', 'a', 'b', 'd5', 'c', 'r', 'b4', 'r',
    'eb5:2', 'e', 'd', 'c', 'c', 'r', 'f3', 'r',
    'eb5:2', 'e', 'd', 'c', 'c', 'r', 'f#3', 'r',
    'eb5:2', 'e', 'eb', 'e', 'd', 'c', 'c', 'a4', 'c5', 'r', 'd', 'r', 'c', 'r', 'c3', 'r',

    'e3:8', 'd:4', 'g:4', 'c:16',
    'a:8', 'g:4', 'c4:4', 'f3:16',
    'e3:8', 'd:4', 'g:4', 'c:16',
    'a:8', 'g:4', 'b:4', 'c4:16',

    'eb5:2', 'e', 'd', 'c', 'c', 'r', 'f3', 'r',
    'eb5:2', 'e', 'd', 'c', 'c', 'r', 'f#3', 'r',
    'eb5:2', 'e', 'eb', 'e', 'd', 'c', 'c', 'a4', 'c5', 'r', 'd', 'r', 'c', 'r', 'c3', 'r',

    'g2:2', 'g', 'bb', 'b', 'c3', 'c', 'c#', 'd',
    'g2:2', 'g', 'bb', 'b', 'c3', 'c', 'c#', 'd',
    'g2:2', 'g', 'bb', 'b', 'c3', 'c', 'c#', 'd',
    'bb', 'a', 'g#', 'g', 'f#', 'f', 'e', 'eb',

    'g2:2', 'g', 'bb', 'b', 'c3', 'c', 'c#', 'd',
    'g2:2', 'g', 'bb', 'b', 'c3', 'c', 'c#', 'd',
    'g2:2', 'g', 'bb', 'b', 'c3', 'c', 'c#', 'd',
    'bb:2', 'a', 'g#', 'g', 'f#', 'f', 'e', 'eb',
    'd:2', 'db', 'r:12',
    'd:2', 'db', 'r:12',
    'd:2', 'db', 'r:12',
    'a:2', 'r:14'
]


music.set_tempo(ticks=4, bpm=150)
music.play(dr_mario_tune, pin=pin2, wait=False, loop=True)  # start playing immediately, the user can stop it manually


while True:
    if pin16.read_digital() == 0:
        music.stop(pin2)
        sleep(200)
    elif pin15.read_digital() == 0:
        music.play(dr_mario_tune, pin=pin2, wait=False, loop=True)
        sleep(200)