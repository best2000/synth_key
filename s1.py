from scipy.io.wavfile import write
import numpy as np
from pynput import keyboard
import matplotlib.pyplot as plt

from pyo import *
s = Server().boot()
s.amp = 0.1

samplerate = 44100


def get_piano_notes():
    '''
    Returns a dict object for all the piano
    note's frequencies
    '''
    # White keys are in Uppercase and black keys (sharps) are in lowercase
    octave = ['C', 'c', 'D', 'd', 'E', 'F', 'f', 'G', 'g', 'A', 'a', 'B', 'CC', 'cc', 'DD', 'dc', 'EE', 'FF', 'ff', 'GG', 'gg', 'AA', 'aa', 'BB']
    base_freq = 261.63  # Frequency of Note C4

    note_freqs = {octave[i]: base_freq * pow(2, (i / 12)) for i in range(len(octave))}
    note_freqs[''] = 0.0
    return note_freqs


def get_wave(freq, duration=0.1):
    amplitude = 4096
    t = np.linspace(0, duration, int(44100 * duration))
    wave = amplitude * np.sin(2 * np.pi * freq * t)
    print(type(wave))

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


def main():
    # Notes of "twinkle twinkle little star"
    music_notes = 'C-C-E-E-G-G-E'
    data = get_song_data(music_notes)
    data = data * (16300 / np.max(data))
    s = Server().boot()
    bs = data.size
    print(data.size)
    t = DataTable(size=data.size)
    osc = TableRead(t, freq=t.getRate(), loop=True, mul=0.1).out()
    arr = np.asarray(t.getBuffer())
    arr[:] = data
    print(arr)

    s.gui(locals())
    #write('nu_ma_lee.wav', samplerate, data.astype(np.int16))

    # Playing chords
    chords = 'GDE-DfA-EGB-CDG'
    data = get_chord_data(chords)
    data = data * (16300 / np.max(data))
    data = np.resize(data, (len(data) * 5,))
    '''s = Server().boot()
    s.amp = 0.001
    bs = data.size
    t = DataTable(size=bs)
    osc = TableRead(t, freq=t.getRate(), loop=True, mul=0.1).out()
    arr = np.asarray(t.getBuffer())
    arr[:] = data
    s.gui(locals())'''
    #write('exp-C-Major.wav', samplerate, data.astype(np.int16))

if __name__ == '__main__':
    main()