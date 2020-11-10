from pynput import keyboard
from pyo import *
import numpy as np

s = Server().boot()

bs = 44100

t = DataTable(size=44100)
osc = TableRead(t, freq=t.getRate(), loop=True, mul=0.1).out()

arr = np.asarray(t.getBuffer())

samplerate = 44100

base_freq = 261.6

def get_piano_notes():
    octave = ['a', 'w', 's', 'e', 'd', 'f', 't', 'g', 'y', 'h', 'u', 'j','k','o','l','p',';','[']
    global base_freq

    note_freqs = {octave[i]: base_freq * pow(2, (i / 12)) for i in range(len(octave))}
    note_freqs[''] = 0.0

    return note_freqs


def get_wave(freq, duration=1):
    amplitude = 4096
    t = np.linspace(0, duration, int(samplerate * duration))
    wave = amplitude * np.sin(2 * np.pi * freq * t)

    return wave


def get_song_data(music_notes):
    note_freqs = get_piano_notes()
    song = [get_wave(note_freqs[note]) for note in music_notes.split('-')]
    song = np.concatenate(song)
    return song.astype(np.int16)


def get_chord_data(chords):
    chords = chords.split('-')
    note_freqs = get_piano_notes()

    chord_data = []
    for chord in chords:
        data = sum([get_wave(note_freqs[note]) for note in list(chord)])
        chord_data.append(data)

    chord_data = np.concatenate(chord_data, axis=0)
    return chord_data.astype(np.int16)


def main(keychar):
    music_notes = keychar
    data = get_song_data(music_notes)
    data = data * (16300 / np.max(data))

    return data


def process():
    data = main(keychar)
    #arr[:] = data
    s = Server().boot()
    s.start()
    sine = Sine(freq=[400,500], mul=.2).out()

s.setCallback(process)
is_pressed = False


def on_press(key):
    oc = ""
    try:
        global keychar, base_freq
        keychar = key.char
        if keychar == "0":
            base_freq = 16.35
            oc = keychar
        elif keychar == "1":
            base_freq = 32.7
            oc = keychar
        elif keychar == "2":
            base_freq = 65.41
            oc = keychar
        elif keychar == "3":
            base_freq = 130.81
            oc = keychar
        elif keychar == "4":
            base_freq = 261.63
            oc = keychar
        elif keychar == "5":
            base_freq = 523.25
            oc = keychar
        elif keychar == "6":
            base_freq = 1046.50
            oc = keychar
        elif keychar == "7":
            base_freq = 2093
            oc = keychar
        elif keychar == "8":
            base_freq = 4186.01
            oc = keychar
        elif keychar == "9":
            base_freq = 8372.019
            oc = keychar

        global is_pressed
        if not is_pressed:
            is_pressed = True
            print(keychar+" "+oc, end="\r")
            s.start()
    except:
        pass


def on_release(key):
    global is_pressed
    is_pressed = False
    s.stop()
    if key == keyboard.Key.esc:
        return False


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
