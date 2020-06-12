from microbit import *
import music

# Note that for Zip64 we need to use pin2 as the output.
#
# Also, for any game-like applications setting wait=False would start the music
# on the background, asynchronously giving us the control back immediately.

tunes = [
        music.BADDY, music.BA_DING, music.BIRTHDAY, music.BLUES, music.CHASE,
        music.DADADADUM, music.ENTERTAINER, music.FUNERAL, music.FUNK,
        music.JUMP_DOWN, music.JUMP_UP, music.NYAN, music.ODE, music.POWER_DOWN,
        music.POWER_UP, music.PRELUDE, music.PUNCHLINE, music.PYTHON,
        music.RINGTONE, music.WAWAWAWAA, music.WEDDING,
]

current_tune_index = 0
number_of_tunes = len(tunes)

def play_current_tune():
    display.scroll(current_tune_index)
    music.play(tunes[current_tune_index], pin=pin2, wait=False)

play_current_tune() # for faster testing


while True:
    if pin16.read_digital() == 0:       # press "Fire(down)" to stop playing the current tune
        music.stop(pin2)
        sleep(200)n
    elif pin15.read_digital() == 0:     # press "Fire(up)" to (re)start playing the current tune
        play_current_tune()
        sleep(200)
    elif pin12.read_digital() == 0:     # press "Left" to go to the previous tune (circularized list)
        current_tune_index = (current_tune_index-1) % number_of_tunes
        play_current_tune()
        sleep(200)
    elif pin13.read_digital() == 0:     # press "Right" to go to the next tune (circularized list)
        current_tune_index = (current_tune_index+1) % number_of_tunes
        play_current_tune()
        sleep(200)