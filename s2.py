from pynput import keyboard
from pyo import *

#default setup
base_freq = 261.6
s = Server().boot()
w = Sine(freq=base_freq, mul=1).out()

sound_keys = ['a', 'w', 's', 'e', 'd', 'f', 't', 'g', 'y', 'h', 'u', 'j', 'k', 'o', 'l', 'p', ';', "'"]
octave_case = {"0": 16.35,
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
effect_keys = ["z", "x", "c", "v", 'b', 'n', 'm', ',', '.', '/']
is_pressed = False

def effect(keychar):
    global w
    if keychar == 'z':  #sin

    elif keychar == 'x':    #supersaw
        w = SuperSaw(base_freq, bal=0, mul=1).out()
    elif keychar == 'c':    #triangle
        w = RCOsc(freq=base_freq, sharp=0, mul=1).out()
    elif keychar == '/':    #almost square
        w = Sine(freq=base_freq, mul=1).out()

def get_piano_notes(keychar):
    global base_freq, sound_keys
    try:
        i = sound_keys.index(keychar)
    except:
        i = 0
    note_freqs = base_freq * pow(2, (i / 12))
    return note_freqs

def on_press(key):
    global is_pressed, base_freq, sound_keys, w, octave_case, effect_keys
    if not is_pressed:
        is_pressed = True
        if key == keyboard.Key.esc:
            return False    # Stop listener
        else:   #check keychar
            keychar = key.char
            if keychar in sound_keys:
                note_freq = get_piano_notes(keychar)
                print(note_freq)
                w.setFreq(note_freq)
                s.start()
            elif keychar in octave_case:
                base_freq = octave_case[keychar]
                print(base_freq)
            elif keychar in effect_keys:
                effect(keychar)



def on_release(key):
    global is_pressed
    is_pressed = False
    s.stop()
    if key == keyboard.Key.esc:
        return False

# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()