from pynput import keyboard
from pyo import *

base_freq = 261.6

s = Server().boot()
sine = Sine(freq=base_freq, mul=1).out()

octave = ['a', 'w', 's', 'e', 'd', 'f', 't', 'g', 'y', 'h', 'u', 'j', 'k', 'o', 'l', 'p', ';', "'"]
is_pressed = False

def get_piano_notes(keychar):
    global base_freq, octave
    try:
        i = octave.index(keychar)
    except:
        i = 0
    note_freqs = base_freq * pow(2, (i / 12))
    return note_freqs

def on_press(key):
    global is_pressed, base_freq, octave, sine
    if not is_pressed:
        is_pressed = True
        if key == keyboard.Key.esc:
            # Stop listener
            return False
        else:
            keychar = key.char
            case = {
                "0": 16.35,
                "1": 32.7,
                "2": 65.41,
                "3": 130.81,
                "4": 261.63,
                "5": 523.25,
                "6": 1046.50,
                "7": 2093,
                "8": 4186.01,
                "9": 8372.019
            }
            if keychar in case:
                base_freq = case[keychar]
                print(base_freq)
            elif keychar in octave:
                note_freq = get_piano_notes(keychar)
                print(note_freq)
                sine.setFreq(note_freq)
                s.start()


def on_release(key):
    global is_pressed
    is_pressed = False
    s.stop()
    if key == keyboard.Key.esc:
        return False

# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()