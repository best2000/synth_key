from pynput import keyboard
from pyo import *
import multiprocessing

def key_process(keychar, is_pressed, s):
    print("im here!")

    w = Sine(freq=500, mul=1).out()
    s.start()
    def on_release(key):
        is_pressed[keychar] = False
        print('release ' + keychar)
        s.stop()
        return False

    with keyboard.Listener(on_release=on_release) as listener:
        listener.join()


if __name__ == '__main__':
    #setup main variables
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

    #setup shared resource
    manager = multiprocessing.Manager()
    wave = manager.dict()
    is_pressed = manager.dict()
    is_pressed['a'] = False
    is_pressed['w'] = False
    is_pressed['s'] = False
    is_pressed['e'] = False
    is_pressed['d'] = False
    is_pressed['f'] = False
    is_pressed['t'] = False
    is_pressed['g'] = False
    is_pressed['y'] = False
    is_pressed['h'] = False
    is_pressed['u'] = False
    is_pressed['j'] = False
    is_pressed['k'] = False
    is_pressed['o'] = False
    is_pressed['l'] = False
    is_pressed['p'] = False
    is_pressed[';'] = False
    is_pressed["'"] = False
    is_pressed['z'] = False
    is_pressed['x'] = False
    is_pressed['c'] = False
    is_pressed['v'] = False
    is_pressed["b"] = False
    is_pressed['0'] = False
    is_pressed['1'] = False
    is_pressed['2'] = False
    is_pressed["3"] = False
    is_pressed['4'] = False
    is_pressed['5'] = False
    is_pressed['6'] = False
    is_pressed['7'] = False
    is_pressed["8"] = False
    is_pressed["9"] = False
    #wave = manager.dict()
    #wave['z'] = Sine(freq=base_freq, mul=1)
    #wave['x'] = SuperSaw(base_freq, bal=0, mul=1)
    #wave['c'] = SuperSaw(base_freq, bal=1, mul=1)
    #wave['v'] = RCOsc(freq=base_freq, sharp=0, mul=1)
    #wave['b'] = RCOsc(freq=base_freq, sharp=1, mul=1)

    #default setup
    base_freq = 261.6
    s = Server().boot()
    w = Sine(freq=base_freq, mul=1).out()

    def effect(keychar):
        if keychar == 'z':  #sin
            w = Sine(freq=base_freq, mul=1).out()
        elif keychar == 'x':    #Roland JP-8000 Supersaw emulator
            w = SuperSaw(base_freq, bal=0, mul=1).out()
        elif keychar == 'c':    #Roland JP-8000  with sideband mixing
            w = SuperSaw(base_freq, bal=1, mul=1).out()
        elif keychar == 'v':    #triangle
            w = RCOsc(freq=base_freq, sharp=0, mul=1).out()
        elif keychar == 'b':    #almost square
            w = RCOsc(freq=base_freq, sharp=1, mul=1).out()

    def get_piano_notes(keychar):
        try:
            i = sound_keys.index(keychar)
        except:
            i = 0
        note_freqs = base_freq * pow(2, (i / 12))
        return note_freqs

    def on_press(key):
        keychar = key.char
        if is_pressed[keychar] == False:
            is_pressed[keychar] = True
            if keychar in sound_keys:
                note_freq = get_piano_notes(keychar)
                print(note_freq)
                w.setFreq(note_freq)
                #assign to process
                multiprocessing.Process(target=key_process, args=[keychar, is_pressed]).start()
            elif keychar in octave_case:
                base_freq = octave_case[keychar]
                print(base_freq)
            elif keychar in effect_keys:
                effect(keychar)

    # Collect events until released
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()